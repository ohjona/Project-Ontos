# Phase 2 Implementation Spec: Adversarial Review (Codex)

**Spec Version:** 1.0  
**Reviewer:** Codex (Adversarial Reviewer)  
**Date:** 2026-01-12  

---

## 1. Circular Import Attack

### 1.1 Dependency Graph Analysis

```
core/types.py (new)  → core/graph.py → core/validation.py
                     → core/suggestions.py
core/curation.py (existing)
core/ontology.py (existing)
core/schema.py (existing)
core/frontmatter.py (existing; uses yaml)
core/__init__.py (re-exports everything)
io/git.py, io/files.py, io/toml.py (new)
```

**Potential cycles identified:**

| Cycle Risk | Modules Involved | How It Happens | Likelihood |
|-----------|------------------|----------------|------------|
| `core/__init__` re-export cycle | `core/__init__` ↔ `core/validation` ↔ `core/graph` ↔ `core/types` ↔ `core/__init__` | Eager imports in `core/__init__` pull all modules; any module importing `core` or `core.*` triggers the full graph | High |
| Type duplication cycle | `core/curation` ↔ `core/types` | `CurationLevel` exists in `core/curation` today, but spec adds a new enum in `core/types`. If either imports the other to “reuse” symbols, you can create circular dependency | Med |
| Ontology/type divergence | `core/ontology` ↔ `core/types` ↔ `core/schema` | Existing ontology likely defines types/status; new `core/types` duplicates those constants; downstream modules may import from both | Med |

### 1.2 Cross-Layer Import Risk

| Risk | Description | Impact |
|------|-------------|--------|
| core imports io | `core/validation` or `core/graph` might need file or git info (mtime, repo root) | Architecture violation |
| io imports core (beyond types) | `io/files` or `io/git` calls validation helpers | Architecture violation and potential circular import |
| Circular via re-exports | `core/__init__` exporting new modules leads to import-time cycles | ImportError at runtime |

### 1.3 God Script Transition Risk

| Risk | Description | Impact |
|------|-------------|--------|
| Import both old and new | God Scripts use old functions but new helpers with same names | Subtle behavior drift, dual logic |
| Partial extraction | Half of a function moved, half left | Hard-to-debug output changes |
| Re-export confusion | Old code still imports from `ontos.core` while new modules are `ontos.core.*` | Import order dependent failures |

### 1.4 Circular Import Verdict

**Circular import risk level:** High  
**Specific risks the spec doesn't address:**
- `core/__init__.py` re-export strategy when new modules depend on each other.
- Type duplication with existing `core/curation` and `core/ontology`.  
**Mitigation recommendations:**
- Freeze `core/__init__.py` to only export stable symbols; avoid `from .graph import *` and similar.
- Move existing enums/types into `core/types.py` and update all callers; no duplicates.
- Add a CI guard: import test that imports `ontos.core` under `PYTHONWARNINGS=error` and fails on ImportError.

---

## 2. Extraction Boundary Attack

### 2.1 Boundary Correctness

#### `core/graph.py` Extraction

| Question | Answer | Concern |
|----------|--------|---------|
| Hidden dependencies? | Yes | `validate_dependencies` likely relies on shared normalization helpers from `ontos_lib` (not in spec). |
| Surrounding code depends on moved symbols? | Yes | The God Script currently uses local validation helpers, not a new `DependencyGraph` class. |
| Local variables/closures? | Uncertain | Need to verify whether existing code relies on closures or module-level constants. |
| Module-level state? | Yes | Graph logic likely uses global config (allowed orphan types, max depth). |

#### `core/validation.py` Extraction

| Question | Answer | Concern |
|----------|--------|---------|
| Hidden dependencies? | Yes | Existing validation uses `normalize_*`, schema checks, and UI formatting. The spec’s version is simplified. |
| Surrounding code depends on symbols moved? | Yes | Current code probably expects per-check exit behavior and formatted output. |
| Local variables/closures? | Uncertain | There are likely shared dicts/constants in the script (schema definitions). |
| Module-level state? | Yes | Configuration values are implicit in the script (e.g., default required fields). |

#### `core/suggestions.py` Extraction

| Question | Answer | Concern |
|----------|--------|---------|
| Hidden dependencies? | Yes | Assumes `context_map` table format stays identical; doc index parsing is fragile. |
| Surrounding code depends on symbols moved? | Yes | Current script may parse impacts differently (case/format). |
| Local variables/closures? | No | Functions are standalone in spec. |
| Module-level state? | No | Uses stdlib only. |

### 2.2 Missing Code

| Missing Extraction | Where It Lives | Why It Should Be Extracted |
|--------------------|----------------|---------------------------|
| Normalization helpers (`normalize_depends_on`, `normalize_type`) | `ontos_lib` | `core/graph` and `core/validation` rely on normalized inputs; leaving in `ontos_lib` keeps hidden dependency. |
| Schema validation constants | God Scripts | `core/validation` spec uses hardcoded required fields but doesn’t include current schema definitions. |
| Frontmatter parsing | `core/frontmatter.py` | Critical for consistent DocumentData types; not addressed in spec. |

### 2.3 Incorrect Placement

| Code | Spec Places In | Should Be In | Why |
|------|----------------|--------------|-----|
| `CurationLevel` | `core/types.py` (new) | Existing `core/curation.py` or move existing enum into `core/types` | Duplication creates diverging enums and circular import risk. |
| `DocumentType`, `DocumentStatus` | `core/types.py` | Existing `core/ontology.py` or move existing definitions | Two competing type systems will break comparisons. |

### 2.4 Boundary Verdict

**Extraction boundaries:** Problems found  
Primary issue: the spec defines a new type system rather than centralizing existing ones.

---

## 3. Test Coverage Attack

### 3.1 Coverage Gaps

| Gap | What's Not Tested | What Could Break | Severity |
|-----|-------------------|------------------|----------|
| Type compatibility | `DocumentData.type` uses Enum but existing code passes strings | AttributeError (`.value`) and GM failures | Critical |
| Schema fidelity | Spec simplifies validation logic | Silent behavior changes | High |
| `core/__init__` re-exports | Cycles and shadowing | ImportError at runtime | High |
| Context map parsing | `load_document_index` table parsing assumptions | False positives/negatives in impacts | Med |

### 3.2 Golden Master Limitations

| Limitation | Description | Risk |
|------------|-------------|------|
| Coverage | GM likely doesn’t exercise all validation branches | Missing regression detection |
| Edge cases | GM fixtures might not include cyclic deps, broken links, or invalid logs | Validation changes slip through |
| Error paths | GM focuses on normal command flow | Non-zero exit behavior may change silently |
| Performance | GM doesn’t measure algorithmic regressions | Hidden O(N²) issues |

### 3.3 Unit Test Adequacy

| Module | Tests Specified | Coverage Target | Adequate for Risk Level? |
|--------|-----------------|-----------------|--------------------------|
| core/graph.py | 7 | Not specified | Marginal |
| core/validation.py | 6 | Not specified | No |
| core/types.py | 3 | Not specified | Marginal |
| core/suggestions.py | 5 | Not specified | Marginal |
| core/tokens.py | 5 | Not specified | Yes |
| io/git.py | 5 | Not specified | No (needs failure/timeout tests) |
| io/files.py | 5 | Not specified | No (needs symlink/encoding tests) |
| io/toml.py | 4 | Not specified | Marginal |

### 3.4 Missing Test Scenarios

| Missing Test | What It Would Catch | Priority |
|--------------|---------------------|----------|
| `DocumentData.type` as string | `.value` AttributeError in `build_graph` | Critical |
| `core/__init__` import | Circular import regression | High |
| Context map parsing header variance | Bad impacts suggestions | High |
| `scan_documents` skip pattern correctness | Over/under inclusion | Med |

### 3.5 Test Coverage Verdict

**Test coverage adequate for Phase 2 risk level:** No  
**Critical gaps:** Type compatibility, validation fidelity, circular import import tests.

---

## 4. Assumption Audit

### 4.1 Dangerous Assumptions

| Assumption | Where | Why It Might Be Wrong | Impact If Wrong |
|-----------|-------|------------------------|----------------|
| God Script functions are self-contained | extraction plan | Many functions rely on `ontos_lib` and shared globals | Broken modules |
| Types can be redefined | `core/types.py` | Existing enums in core already used | Divergence and subtle equality failures |
| `DocumentData.type` is always Enum | `core/graph.py` | Existing code uses strings | Runtime crash |
| `core/__init__` can re-export all | Phase 2 plan | Import order creates cycles | ImportError |
| Validation logic can be simplified | `core/validation.py` | Current logic has nuance | GM failures |

### 4.2 Assumptions Not Validated

| Assumption | How To Validate | Validated In Spec? |
|-----------|-----------------|-------------------|
| Existing type definitions | Search for `DocumentType`, `CurationLevel` usage | No |
| Validation fidelity | Compare extracted logic with GM output | No |
| Import order safety | Add a direct import test | No |

### 4.3 Assumption Risk Verdict

**Most dangerous assumptions:**
1. Types can be duplicated without breaking equality.
2. `DocumentData.type` is always Enum.
3. Core re-exports won’t create circular imports.

---

## 5. Failure Mode Analysis

### 5.1 Extraction Failures

| Failure | How It Happens | Detection | Recovery |
|---------|----------------|-----------|----------|
| Circular import | `core/__init__` imports new modules which import each other | ImportError | Remove re-exports; import lazily |
| Missing symbol | God Script expects local helper not moved | NameError | Restore helper or re-export |
| Behavior change | Validation logic simplified | GM fails or diff | Re-implement existing logic exactly |
| Type mismatch | String vs Enum | AttributeError | Normalize types at ingest |

### 5.2 Architecture Violations

| Violation | How It Happens | Detection | Impact |
|-----------|----------------|-----------|--------|
| core imports io | Validation calls git/file ops | Code review only | Architecture rot |
| io imports core beyond types | io functions use validators | Import test | Layer coupling |

### 5.3 Production Failures

| User Action | Potential Failure | Severity |
|-------------|-------------------|----------|
| `ontos map` | Validation fails due to type mismatch | Critical |
| `ontos log` | Impact suggestions wrong due to parsing | High |
| `pip install ontos` | ImportError from core circularity | Critical |

### 5.4 Failure Mode Verdict

**Failure modes adequately addressed:** No  
**Unmitigated risks:** Type duplication, circular imports, validation fidelity.

---

## 6. Architecture Constraint Attack

### 6.1 Core/IO Separation

| Scenario | How core ends up needing io | Likelihood |
|----------|-----------------------------|------------|
| Validation needs file mtime | to detect staleness | High |
| Graph needs file reads | to build doc list | Med |
| Suggestions need git log | to correlate commit messages | Med |

**Does the spec address this?** Partially. It says io should handle I/O but does not show how data is passed into core without violating core purity.

### 6.2 Stdlib-Only Core

| Potential Violation | Current Usage | Alternative |
|--------------------|---------------|-------------|
| PyYAML in core | `core/frontmatter.py` uses PyYAML (external) | Move parsing to io or replace with stdlib for Phase 2 |

**Does the spec audit core's dependencies?** No. This is a direct conflict with architecture.

### 6.3 Architecture Enforcement

| Enforcement | Spec Includes? | Effectiveness |
|-------------|----------------|---------------|
| Linting rules | No | — |
| Import tests | No | — |
| Code review | Yes | Medium |
| Documentation | Yes | Low |

**Architecture constraint verdict:** At risk

---

## 7. Edge Cases and Security

### 7.1 Edge Cases Not Addressed

| Edge Case | Module | What Could Happen |
|-----------|--------|-------------------|
| `DocumentData.type` is a string | core/graph | AttributeError on `.value` |
| Context map table format changes | core/suggestions | Wrong index → wrong impacts |
| `.git` is a file (worktree) | io/files | `find_project_root` works but later ops assume directory |
| Large repo scan | io/files | `rglob` + skip patterns slow, no limits |
| Non-UTF8 docs | io/files | read failure |

### 7.2 Security Considerations

| Concern | Module | Risk | Mitigation Specified? |
|---------|--------|------|----------------------|
| Path traversal | io/files | Med | No |
| Command injection | io/git | Low | Yes (no shell) |
| Unsafe TOML parsing | io/toml | Low | Partial (tomllib/tomli only) |

### 7.3 Backward Compatibility

| Compatibility Risk | Description | Impact |
|--------------------|-------------|--------|
| Import path changes | Existing imports from `ontos_lib`/old scripts | ImportError |
| Symbol renames | New types replace old enums | NameError or silent mismatch |
| Behavior changes | Simplified validation logic | GM failures |

**Does the spec address backward compatibility?** Partially. It doesn’t define a compatibility layer for old symbols.

---

## 8. Summary

### 8.1 Attack Results

| Attack Vector | Findings | Severity |
|---------------|----------|----------|
| Circular imports | High risk from `core/__init__` and duplicated types | High |
| Extraction boundaries | Missing dependencies and simplified logic | High |
| Test coverage | Missing tests for type compatibility and import order | High |
| Assumptions | Several unsafe assumptions not validated | High |
| Failure modes | Key regressions not mitigated | High |
| Architecture constraints | Zero-dep core already violated | High |
| Edge cases | Type mismatch, parsing variance | Med |

### 8.2 Critical Vulnerabilities

| Vulnerability | Impact | Recommendation |
|---------------|--------|----------------|
| Duplicate type systems (`core/types` vs existing enums) | Silent behavior drift and equality failures | Consolidate existing enums into `core/types`, update all imports |
| `DocumentData.type` assumed Enum | Runtime crash in `build_graph` | Normalize to enum at ingest or guard with `isinstance` |
| `core/__init__` eager re-exports | Circular import failures | Use explicit imports or lazy import pattern |

### 8.3 What the Chief Architect Missed

- Existing type definitions (DocumentType, CurationLevel) already live in core; the spec creates new competing versions.
- `core/frontmatter` still uses PyYAML, violating stdlib-only core constraint.
- Validation logic in spec is simplified relative to current scripts; Golden Master will likely fail.

### 8.4 Recommendation

**Verdict:** Request changes

**Must fix before implementation:**
1. Consolidate and centralize core type definitions; do not duplicate enums.
2. Define a safe type normalization boundary between `io` and `core`.
3. Specify a no-cycle import strategy for `core/__init__.py`.

**Should fix:**
1. Reconcile validation logic with exact existing behavior; no simplification without GM evidence.
2. Add explicit import tests to detect cycles early.

**Accept risk:**
1. `io/files.scan_documents` performance (acceptable for Phase 2 if not tuned).

### 8.5 Survivability Assessment

**Will this spec survive implementation?** With fixes  
**Phase 2 risk level after this spec:** Unchanged  
**Summary:** The decomposition plan is viable, but the type system duplication and import strategy will almost certainly cause runtime failures and Golden Master regressions. The spec needs a tighter compatibility plan and explicit cycle-avoidance before Antigravity starts.

---

*End of Adversarial Review*
