# Chief Architect Response: Phase 2 Implementation Spec Review

**Document ID:** chief_architect_phase2_response
**Version:** 1.0
**Date:** 2026-01-12
**Author:** Chief Architect (Claude Opus 4.5)
**Status:** Final

**References:**
- `Phase2-Implementation-Spec.md` v1.0
- `Phase2-Implementation-Spec-Review-Consolidation.md` v1.0
- `V3.0-Implementation-Roadmap.md` v1.4

---

## Executive Summary

The LLM Review Board has provided comprehensive feedback on the Phase 2 Implementation Spec. After careful analysis and codebase verification, I **accept the overall "Conditional Accept" verdict** and acknowledge that the spec requires updates before implementation can proceed safely.

**Summary of Dispositions:**
| Category | Accept | Modify | Reject | Total |
|----------|--------|--------|--------|-------|
| Critical | 4 | 0 | 0 | 4 |
| Major | 5 | 0 | 0 | 5 |
| Minor | 5 | 0 | 0 | 5 |
| **Total** | **14** | **0** | **0** | **14** |

All issues raised by the reviewers are valid and will be incorporated into spec v1.1.

---

## Part 1: Response to Critical Issues

### C1: Type Duplication Risk

**Review Finding:** Spec creates new `CurationLevel` enum in `core/types.py` when one already exists in `core/curation.py`.

**Disposition:** ACCEPT

**Verification Performed:**
```python
# Verified in ontos/core/curation.py lines 18-22:
class CurationLevel(IntEnum):
    """Document curation levels."""
    SCAFFOLD = 0  # Auto-generated placeholder
    STUB = 1      # User provides goal only
    FULL = 2      # Complete Ontos document
```

**Root Cause Analysis:**
The original spec was drafted based on Roadmap assumptions without full codebase verification. The existing `CurationLevel` in `core/curation.py` is functionally identical to what was proposed.

**Resolution for v1.1:**
1. **REMOVE** `CurationLevel` definition from `core/types.py` spec
2. **ADD** re-export in `core/types.py`: `from ontos.core.curation import CurationLevel`
3. **DOCUMENT** consolidation strategy: `core/types.py` should consolidate existing types via re-export, not duplicate them

**Additional Discovery:**
`DocumentType` and `DocumentStatus` as proposed enums do NOT exist in the current codebase. `core/ontology.py` uses `TypeDefinition` frozen dataclass with string values. The spec's proposal to create these enums is valid NEW work, not duplication.

---

### C2: Missing `commands/map.py`

**Review Finding:** Roadmap Section 4.1 requires `commands/map.py` containing `generate_context_map()` orchestration, but spec omits this.

**Disposition:** ACCEPT

**Verification from Roadmap v1.4, Section 4.1:**
> "Phase 2 deliverables include... `commands/map.py` - Context map generation"

**Root Cause Analysis:**
The spec focused on extracting pure logic modules (`core/graph.py`, `core/validation.py`, etc.) but failed to include the orchestration command that ties them together.

**Resolution for v1.1:**
Add new module specification:

```
### 4.9 `ontos/commands/map.py` - NEW

**Purpose:** Orchestrate context map generation using extracted core modules.

**Source:** `ontos/_scripts/ontos_generate_context_map.py` orchestration logic (lines 925-1126)

**Public API:**
- `generate_context_map(ctx: SessionContext, output: OutputHandler) -> str`
- `GenerateMapOptions` dataclass for configuration

**Responsibilities:**
- Call `core/validation.ValidationOrchestrator`
- Call `core/graph.build_graph()` and `core/graph.detect_cycles()`
- Call `core/tokens.estimate_tokens()`
- Format and output the context map markdown

**Size Target:** ~200 lines (orchestration + formatting only)
```

---

### C3: Missing `commands/log.py`

**Review Finding:** Roadmap Section 4.1 requires `commands/log.py` containing `end_session()` orchestration, but spec omits this.

**Disposition:** ACCEPT

**Verification from Roadmap v1.4, Section 4.1:**
> "Phase 2 deliverables include... `commands/log.py` - Session log creation"

**Root Cause Analysis:**
Same as C2 - orchestration commands were overlooked while focusing on core module extraction.

**Resolution for v1.1:**
Add new module specification:

```
### 4.10 `ontos/commands/log.py` - NEW

**Purpose:** Orchestrate session log creation using extracted core/io modules.

**Source:** `ontos/_scripts/ontos_end_session.py` orchestration logic (lines 1608-1904)

**Public API:**
- `end_session(ctx: SessionContext, output: OutputHandler) -> Path`
- `EndSessionOptions` dataclass for configuration

**Responsibilities:**
- Call `io/git.get_current_branch()`, `io/git.get_commits_since_push()`
- Call `core/suggestions.suggest_impacts()`
- Call `io/files` for log file creation
- Handle interactive prompts via OutputHandler

**Size Target:** ~250 lines (orchestration + user interaction)
```

---

### C4: God Scripts Not Reduced to <300 Lines

**Review Finding:** Roadmap requires God Scripts reduced to <300 lines each, but spec's extraction plan doesn't achieve this.

**Disposition:** ACCEPT

**Current State:**
- `ontos_end_session.py`: 1,905 lines
- `ontos_generate_context_map.py`: 1,296 lines

**Analysis:**
The original spec extracts ~500-800 lines per script into modules, leaving:
- `ontos_end_session.py`: ~1,100-1,400 lines (still 4-5x over target)
- `ontos_generate_context_map.py`: ~500-800 lines (still 2-3x over target)

**Resolution for v1.1:**
1. **ADD** explicit line count targets per extraction
2. **ADD** `commands/map.py` and `commands/log.py` to absorb remaining orchestration
3. **REVISE** extraction scope to move MORE code into modules:
   - Move ALL template constants to `core/types.py`
   - Move ALL validation to `core/validation.py`
   - Move ALL git operations to `io/git.py`
   - Move ALL suggestion logic to `core/suggestions.py`
4. **ADD** exit criteria: "God Scripts contain ONLY CLI argument parsing and deprecation notices"

**Updated Target Structure:**
| Script | Current | After Phase 2 | Remaining Content |
|--------|---------|---------------|-------------------|
| `ontos_end_session.py` | 1,905 | <200 | argparse + deprecation + call `commands/log.py` |
| `ontos_generate_context_map.py` | 1,296 | <200 | argparse + deprecation + call `commands/map.py` |

---

## Part 2: Response to Major Issues

### M1: Missing REFACTOR Tasks for God Scripts

**Review Finding:** Spec shows what to extract but lacks explicit tasks for updating God Script imports and removing extracted code.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add explicit refactor tasks to Section 5.1 Task Sequence:

**Day 5 (expanded):**
| Task | Description | Verification |
|------|-------------|--------------|
| 5.1 | Update `ontos_generate_context_map.py` imports | Imports compile |
| 5.2 | Remove extracted functions from script | Script < 200 lines |
| 5.3 | Replace inline code with module calls | Golden Master passes |
| 5.4 | Update `ontos_end_session.py` imports | Imports compile |
| 5.5 | Remove extracted functions from script | Script < 200 lines |
| 5.6 | Replace inline code with module calls | Golden Master passes |

---

### M2: PyYAML Dependency in Core Layer

**Review Finding:** Architecture requires `core/` to be stdlib-only, but `core/frontmatter.py` already imports `yaml`.

**Disposition:** ACCEPT

**Verification Performed:**
```python
# Confirmed in ontos/core/frontmatter.py line 9:
import yaml
```

This is a PRE-EXISTING architecture violation that Phase 2 must address.

**Resolution for v1.1:**
1. **ADD** new module: `io/yaml.py` - PyYAML wrapper for YAML parsing
2. **ADD** migration task: Move YAML operations from `core/frontmatter.py` to `io/yaml.py`
3. **MODIFY** `core/frontmatter.py` to accept parsed dict (pure data transformation)

**New Module Specification:**
```python
# ontos/io/yaml.py
"""YAML parsing operations - isolates PyYAML dependency from core."""
import yaml

def parse_yaml(content: str) -> dict:
    """Parse YAML content. Raises YAMLError on invalid input."""
    return yaml.safe_load(content) or {}

def dump_yaml(data: dict) -> str:
    """Serialize dict to YAML string."""
    return yaml.dump(data, default_flow_style=False)
```

**Migration Pattern:**
```python
# Before (core/frontmatter.py):
import yaml
def parse_frontmatter(content):
    fm_dict = yaml.safe_load(fm_text)
    ...

# After (core/frontmatter.py):
# No yaml import!
def parse_frontmatter(content: str, yaml_parser=None):
    """Parse frontmatter. yaml_parser injected by caller (usually io layer)."""
    if yaml_parser is None:
        from ontos.io.yaml import parse_yaml
        yaml_parser = parse_yaml
    fm_dict = yaml_parser(fm_text)
    ...
```

---

### M3: Circular Import Prevention Strategy

**Review Finding:** Spec acknowledges high likelihood of circular imports but provides no concrete prevention strategy beyond "careful ordering."

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add Section 5.3: Circular Import Prevention

**Strategy:**
1. **types.py MUST have zero internal imports** - verified in spec, confirmed
2. **Import order within modules:**
   ```python
   # Correct order for any ontos module:
   from __future__ import annotations  # FIRST - enables forward refs
   # stdlib imports
   # third-party imports
   # ontos.core.types imports (always safe)
   # other ontos imports (if needed)
   ```
3. **Add CI test:**
   ```python
   # tests/test_circular_imports.py
   def test_no_circular_imports():
       """Verify all modules can be imported independently."""
       import importlib
       modules = [
           "ontos.core.types",
           "ontos.core.tokens",
           "ontos.core.graph",
           "ontos.core.suggestions",
           "ontos.core.validation",
           "ontos.io.git",
           "ontos.io.files",
           "ontos.io.toml",
           "ontos.io.yaml",
       ]
       for mod in modules:
           importlib.import_module(mod)  # Should not raise ImportError
   ```
4. **Add CI check to test suite:**
   ```bash
   # In CI pipeline:
   python -c "import ontos; import ontos.core; import ontos.io; import ontos.commands"
   ```

---

### M4: Type Normalization Boundary

**Review Finding:** When does `type: "kernel"` (string) become `DocumentType.KERNEL` (enum)? Boundary unclear.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add Section 3.3: Type Normalization Boundary

**Design Decision:**
- **io layer** handles raw strings from files
- **core layer** works with normalized types (enums)
- **Conversion happens at io/core boundary** in `io/files.py`

**Implementation:**
```python
# ontos/io/files.py
from ontos.core.types import DocumentType, DocumentStatus, DocumentData

def load_document(path: Path, yaml_parser) -> DocumentData:
    """Load and normalize a document file."""
    content = path.read_text()
    fm = parse_frontmatter(content, yaml_parser)

    # Normalize strings to enums HERE
    doc_type = DocumentType(fm.get("type", "atom"))
    doc_status = DocumentStatus(fm.get("status", "draft"))

    return DocumentData(
        id=fm["id"],
        type=doc_type,        # Enum, not string
        status=doc_status,    # Enum, not string
        filepath=path,
        frontmatter=fm,
        content=content,
        depends_on=fm.get("depends_on", []),
        impacts=fm.get("impacts", []),
    )
```

**Validation:** Enum conversion happens ONCE, in `io/files.py`. All `core/` modules receive pre-normalized `DocumentData`.

---

### M5: `load_common_concepts` Ownership Unclear

**Review Finding:** Both God Scripts use `load_common_concepts()` but spec doesn't specify which module owns it.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Assign to `core/suggestions.py` since it's used for concept validation during impact suggestion.

**Update `core/suggestions.py` spec:**
```python
def load_common_concepts(context_map_path: Path) -> Set[str]:
    """Load common concepts from context map.

    Parses the ## Common Concepts section of the context map.

    Args:
        context_map_path: Path to Ontos_Context_Map.md

    Returns:
        Set of known concept strings
    """
    ...
```

---

## Part 3: Response to Minor Issues

### m1: `tomli` Fallback for Python 3.9-3.10

**Review Finding:** Spec mentions `tomli` fallback but doesn't add it to dependencies.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add to Section 4.8 (`io/toml.py`):

```python
# Python 3.11+ has tomllib in stdlib
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:
        raise ImportError(
            "tomli required for Python < 3.11. Install with: pip install tomli"
        )
```

Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
python39 = ["tomli>=2.0.0"]

# Or conditional dependency:
dependencies = [
    "tomli>=2.0.0; python_version < '3.11'"
]
```

---

### m2: Watch Mode Deferred Without Tracking

**Review Finding:** Spec defers watch mode to v3.1 without adding tracking issue.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add to Section 1.2 (Out of Scope):
> Watch mode (`--watch` flag) - Deferred to v3.1. **Tracking:** Create GitHub issue "Watch mode for context map generation" with label `v3.1-backlog`.

---

### m3: Missing `scan_docs` Extraction Detail

**Review Finding:** Table says `scan_docs` goes to `io/files.py (partial)` but doesn't explain what's partial.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Clarify in Section 2.2:

| Function | Lines | Extraction Target | Notes |
|----------|-------|-------------------|-------|
| `scan_docs` | 201-273 | `io/files.py` -> `scan_documents()` | File discovery logic only. Document parsing remains in calling code. |

The "partial" refers to:
- **Extracted:** Directory walking, glob matching, skip pattern filtering
- **Remains:** YAML frontmatter parsing (happens after scan)

---

### m4: `validate_describes_field` Referenced but Not Specified

**Review Finding:** Function listed in shared dependencies but no extraction target given.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add to `core/validation.py` since it's a validation function:

```python
def validate_describes_field(
    doc: DocumentData,
    valid_targets: Set[str]
) -> Optional[ValidationError]:
    """Validate describes field references valid targets.

    Args:
        doc: Document with optional describes field
        valid_targets: Set of valid target doc_ids

    Returns:
        ValidationError if invalid, None if valid
    """
    describes = doc.frontmatter.get("describes")
    if describes and describes not in valid_targets:
        return ValidationError(
            error_type=ValidationErrorType.SCHEMA,
            doc_id=doc.id,
            filepath=str(doc.filepath),
            message=f"describes '{describes}' not found",
            fix_suggestion=f"Update describes to valid target or remove",
            severity="warning"
        )
    return None
```

---

### m5: Test File Locations Not Specified

**Review Finding:** Spec says "Tests Required" but doesn't specify where test files should live.

**Disposition:** ACCEPT

**Resolution for v1.1:**
Add Section 6.3: Test File Structure

```
tests/
├── core/
│   ├── test_types.py        # Tests for core/types.py
│   ├── test_tokens.py       # Tests for core/tokens.py
│   ├── test_graph.py        # Tests for core/graph.py
│   ├── test_suggestions.py  # Tests for core/suggestions.py
│   └── test_validation.py   # Tests for core/validation.py
├── io/
│   ├── test_git.py          # Tests for io/git.py
│   ├── test_files.py        # Tests for io/files.py
│   ├── test_toml.py         # Tests for io/toml.py
│   └── test_yaml.py         # Tests for io/yaml.py
├── commands/
│   ├── test_map.py          # Tests for commands/map.py
│   └── test_log.py          # Tests for commands/log.py
└── test_circular_imports.py # CI: circular import prevention
```

---

## Part 4: Critical Risk Areas

### 4.1 Circular Imports

**Risk Level:** HIGH

**Mitigation Strategy:**
1. `core/types.py` has ZERO internal imports (verified)
2. Explicit import order documented in Section 5.3
3. CI test `test_circular_imports.py` blocks PRs with cycles
4. Forward reference annotations via `from __future__ import annotations`

**Verification Command:**
```bash
python -c "import ontos.core; import ontos.io; import ontos.commands"
```

---

### 4.2 Extraction Boundaries

**Risk Level:** MEDIUM

**Mitigation Strategy:**
1. Each extraction follows pattern: Copy -> Import -> Comment -> Test -> Delete
2. Golden Master runs after EACH extraction, not at end
3. Explicit line count targets (God Scripts < 200 lines each)
4. Clear ownership table for every shared function

---

### 4.3 Architecture Enforcement

**Risk Level:** MEDIUM

**Mitigation Strategy:**
1. **PRE-EXISTING VIOLATION FIXED:** `core/frontmatter.py` PyYAML import moved to `io/yaml.py`
2. **CI Check:** Add import linter that fails if `core/` imports from `io/` or `subprocess`
3. **Code Review Checklist:** Architecture constraints in PR template

**Architecture Constraints (Enforced):**
| Layer | May Import From | Must Not Import From |
|-------|-----------------|---------------------|
| `core/` | stdlib, `core/types` | `io/`, `commands/`, subprocess |
| `io/` | stdlib, `core/types`, third-party | `commands/` |
| `commands/` | All layers | - |

---

### 4.4 Test Coverage

**Risk Level:** LOW (existing coverage is good)

**Mitigation Strategy:**
1. Golden Master tests (16 fixtures) catch behavioral regression
2. Unit tests required for each new module before merge
3. Minimum coverage threshold: 80% for new code
4. CI runs full test suite on every PR

---

## Part 5: Updated Deliverables

### 5.1 Phase 2 Deliverables (Revised)

| Module | Status | Lines (Est.) |
|--------|--------|--------------|
| `core/types.py` | NEW | ~120 |
| `core/tokens.py` | NEW | ~30 |
| `core/graph.py` | NEW | ~150 |
| `core/suggestions.py` | NEW | ~100 |
| `core/validation.py` | NEW | ~200 |
| `io/git.py` | NEW | ~100 |
| `io/files.py` | NEW | ~80 |
| `io/toml.py` | NEW | ~50 |
| `io/yaml.py` | NEW (added) | ~30 |
| `commands/map.py` | NEW (added) | ~200 |
| `commands/log.py` | NEW (added) | ~250 |
| 7 minor commands | MIGRATED | ~2,400 |
| `ontos_end_session.py` | REFACTORED | <200 |
| `ontos_generate_context_map.py` | REFACTORED | <200 |

**Total New Code:** ~1,310 lines in new modules
**Total Migrated:** ~2,400 lines from minor scripts
**Net God Script Reduction:** ~2,800 lines removed

### 5.2 Updated Exit Criteria

Phase 2 is complete when:
- [ ] All 11 new modules created (8 original + `io/yaml.py` + `commands/map.py` + `commands/log.py`)
- [ ] God Scripts < 200 lines each (argparse + deprecation only)
- [ ] 7 minor commands migrated to `commands/`
- [ ] Pre-existing PyYAML violation fixed (`core/frontmatter.py`)
- [ ] Golden Master tests pass (16/16)
- [ ] All unit tests pass (303+ existing + new module tests)
- [ ] No circular imports (CI test passes)
- [ ] Architecture constraints enforced (no `core/` -> `io/` imports)
- [ ] Tag `v3.0.0-beta` created

---

## Part 6: Conclusion

The LLM Review Board has identified legitimate gaps in the Phase 2 Implementation Spec. All 14 issues are accepted without modification.

**Key Changes for v1.1:**
1. **Critical:** Add `commands/map.py` and `commands/log.py` per Roadmap requirements
2. **Critical:** Consolidate types via re-export, not duplication
3. **Critical:** Reduce God Scripts to <200 lines each (not 500-800)
4. **Major:** Add `io/yaml.py` to fix pre-existing architecture violation
5. **Major:** Add explicit circular import prevention strategy with CI test
6. **Major:** Document type normalization boundary at io/core interface

The updated spec v1.1 will be produced incorporating all accepted changes.

---

**Sign-off:**

_Chief Architect_
_2026-01-12_

---

*End of Chief Architect Response v1.0*
