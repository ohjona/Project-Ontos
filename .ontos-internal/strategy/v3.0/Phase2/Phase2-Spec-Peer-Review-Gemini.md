# Phase 2 Implementation Spec: Peer Review

**Spec Version:** 1.0
**Reviewer:** Gemini (Peer Reviewer)
**Date:** 2026-01-12

---

## 1. Spec Completeness

### 1.1 Required Sections Check

| Section | Present? | Complete? | Notes |
|---------|----------|-----------|-------|
| Overview & Scope | Yes | Yes | Clear distinction between extraction and migration. |
| Entry/Exit Criteria | Yes | Yes | Golden Master requirement is prominent. |
| Current State Analysis | Yes | Yes | **Excellent** verification of line numbers and symbols. |
| Target State | Yes | Yes | Clear architecture diagram. |
| File Specifications | Yes | Yes | Detailed Python code for new modules. |
| Migration Tasks | Yes | **Partial** | Missing explicit steps for *Refactoring* existing core modules. |
| Test Specifications | Yes | Yes | Test requirements per module. |
| Verification Protocol | Yes | Yes | Good focus on incremental verification. |
| Risks & Mitigations | Yes | Yes | Circular imports correctly identified as top risk. |

### 1.2 Missing Elements

| Missing Element | Impact | Recommendation |
|-----------------|--------|----------------|
| **Refactoring Steps** | **High** | The Roadmap (Sec 4.10) requires refactoring `staleness.py`, `history.py`, etc., to remove I/O. The Phase 2 Spec lists them as "Existing" but does not allocate tasks/days to perform this refactoring. If not done, `commands/log.py` will inadvertently cause I/O in the core layer via `staleness.py`. **Add explicit tasks for this.** |
| `load_common_concepts` Migration | Medium | `suggestions.py` uses `validate_concepts` which needs a concept list. Currently `ontos_lib` loads this from file. Spec doesn't specify where `load_common_concepts` moves (likely `io/files.py` + `core/frontmatter.py`). |

### 1.3 Codebase Analysis Verification

**Did the Chief Architect actually explore the codebase?**

- [x] Current structure documented with actual paths
- [x] God Script contents analyzed with real line numbers
    - `ontos_end_session.py`: `TEMPLATES` verified at lines 780+
    - `ontos_generate_context_map.py`: `estimate_tokens` verified at lines 71-102
- [x] Dependencies mapped from actual imports
- [x] Gap analysis comparing Roadmap vs reality

**Evidence of codebase exploration:** **Strong**. The line numbers and function names match the actual files perfectly.

---

## 2. Module Specifications Quality

### 2.1 Core Modules

#### `core/graph.py`

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Purpose clear | Yes | Dependency graph logic. |
| Source location specified | Yes | Lines 428-560 verified. |
| Public API defined | Yes | `DependencyGraph`, `build_graph`, etc. |
| Code provided/outlined | Yes | **Recursive DFS Warning**: The spec uses recursive DFS (`def dfs`). Python's recursion limit (1000) is usually fine for docs, but iterative DFS is safer for graph algorithms. |

**Implementability:** **Ready**.

---

#### `core/validation.py`

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Purpose clear | Yes | Unified Orchestrator. |
| Architecture compliance | Yes | Collects errors instead of exiting. |

**Implementability:** **Ready**.

---

#### `core/types.py`

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Purpose clear | Yes | Central type definitions. |
| Dependencies listed | Yes | None (Crucial for avoiding circular imports). |

**Implementability:** **Ready**.

---

#### `core/suggestions.py`

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Purpose clear | Yes | Logic extracted from `ontos_end_session.py`. |
| Pure logic? | Yes | `load_document_index` takes string content, not file path. Good! |

**Implementability:** **Ready**.

---

### 2.2 I/O Modules

#### `io/git.py`

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Purpose clear | Yes | Isolates subprocess calls. |
| Completeness | Yes | Covers branches, diffs, logs, mtime. |

**Architecture compliance:** **Yes**. Properly separates I/O.

---

#### `io/files.py`

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Purpose clear | Yes | File system operations. |
| `find_project_root` | Yes | Correctly implements the "walk up" logic required by v3. |

**Implementability:** **Ready**.

---

### 2.3 Module Specifications Summary

| Module | Spec Quality | Implementable? | Top Issue |
|--------|--------------|----------------|-----------|
| core/graph.py | Good | Yes | Recursive DFS (minor) |
| core/validation.py | Good | Yes | None |
| core/types.py | Good | Yes | None |
| core/suggestions.py | Good | Yes | None |
| io/git.py | Good | Yes | None |
| io/files.py | Good | Yes | None |
| io/toml.py | Good | Yes | None |

---

## 3. Extraction Plan Analysis

### 3.1 Task Sequencing

**Are tasks ordered correctly by dependency?**

| Task | Dependencies | Order Correct? | Notes |
|------|--------------|----------------|-------|
| types.py | None | Yes | First foundation. |
| tokens.py | None | Yes | Independent. |
| io/git.py | None | Yes | Independent foundation. |
| core/graph.py | types.py | Yes | |
| core/validation.py | types.py, graph.py | Yes | |
| God Script refactoring | All modules | Yes | Final step. |

**Dependency ordering verdict:** **Correct**.

### 3.2 Extraction Strategy

**Is the extraction strategy safe?**

- **Copy-before-delete:** Specified in Section 8.1.
- **Golden Master:** Specified after each module extraction.
- **Rollback:** Explicitly mentioned.

**Verdict:** **Safe**.

### 3.3 Timeline Realism

- **Concern:** The schedule (Section 5.1) packs "God Script Integration" into Day 5, but this step implicitly includes the "Refactoring" of existing modules (`staleness.py`, etc.) which is missing from the table.
- **Recommendation:** Add a dedicated "Refactoring Day" (Day 4 or 5) to purify existing core modules before integrating them into the new commands.

---

## 4. Test Coverage

### 4.1 Unit Tests

| Module | Tests Specified? | Adequate? |
|--------|------------------|-----------|
| core/graph.py | Yes | Yes (Cycle detection, orphans) |
| core/validation.py | Yes | Yes |
| io/git.py | Yes | Yes |
| io/files.py | Yes | Yes |

### 4.2 Integration Tests

- **Golden Master** is the MVP here. The spec rightly relies on it heavily (Section 6).
- **Missing:** Explicit test for `ontos init` (though that's Phase 3, `io/files.py` needs to support it).

**Test coverage verdict:** **Adequate**.

---

## 5. Documentation Quality

### 5.1 Clarity

- **Code Examples:** Excellent. The provided Python code snippets are nearly production-ready.
- **Architecture:** Clear distinction between `core/` (pure) and `io/` (impure).

---

## 6. Positive Observations

1.  **Codebase Reality:** The spec is grounded in reality. The line numbers for `ontos_end_session.py` (e.g., impact suggestion at 1193) are accurate.
2.  **Pure Core Pattern:** The design of `core/suggestions.py` (accepting `context_map_content` string instead of reading a file) is a perfect example of the Functional Core architecture.
3.  **Golden Master Focus:** Relying on Golden Master for the refactoring phase is the only sane way to handle a rewrite of this magnitude.

---

## 7. Summary

### 7.1 Overall Assessment

| Area | Verdict |
|------|---------|
| Completeness | **Gaps exist** (Missing refactor plan) |
| Module Specs | **Ready** |
| Extraction Plan | **Sound** |
| Test Coverage | **Adequate** |
| Documentation | **Clear** |

### 7.2 Issues by Severity

| Severity | Count | Issue |
|----------|-------|-------|
| **Major** | 1 | Missing explicit tasks for refactoring existing core modules (`staleness.py`, `history.py`) to remove I/O. |
| Minor | 1 | Recursive DFS in `graph.py` (could be iterative). |
| Minor | 1 | `load_common_concepts` migration location unclear. |

### 7.3 Recommendation

**Verdict:** **Approve with changes**

**Required Changes:**
1.  **Add "Refactor Existing Modules" to Section 5.1 (Migration Tasks).** Specifically, `staleness.py`, `history.py`, and `proposals.py` currently contain `subprocess` calls or direct file I/O. These MUST be purified (logic separated from I/O) before `commands/log.py` uses them, or the v3 architecture is violated.
2.  **Explicitly handle `common_concepts` loading.** Define where `load_common_concepts` lives (likely `io/files.py` reading + `core/frontmatter.py` parsing).

**Summary:** The specification for *new* modules is excellent. The plan for decomposing the God Scripts is sound. The only oversight is the cleanup of *existing* modules that the God Scripts depend on. Address this, and the spec is solid.

---

*End of Peer Review*
