# Ontos v3.0 Implementation Spec: Phase 2 — Core Decomposition

**Version:** 1.2
**Date:** 2026-01-12
**Author:** Chief Architect (Claude Opus 4.5)
**Status:** Approved — Ready for Implementation

**References:**
- `V3.0-Implementation-Roadmap.md` v1.4, Section 4
- `V3.0-Technical-Architecture.md` v1.4
- `Phase1-Implementation-Spec.md` v1.1 (predecessor)
- `Chief_Architect_Phase2_Response.md` v1.0 (review response)
- `Chief_Architect_Round2_Critical_Analysis.md` v1.0 (verification analysis)

**Revision History:**
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-12 | Initial spec with verified codebase analysis |
| 1.1 | 2026-01-12 | Incorporated all 14 review findings (4 critical, 5 major, 5 minor) |
| 1.2 | 2026-01-12 | Added subprocess violations in `staleness.py`/`config.py`; added CI architecture enforcement |

---

## 1. Overview

### 1.1 Purpose

Phase 2 decomposes the two "God Scripts" (`ontos_end_session.py` at 1,905 lines and `ontos_generate_context_map.py` at 1,296 lines) into modular components following the layered architecture established in Phase 1. This is the highest-risk phase of v3.0.

### 1.2 Scope

| In Scope | Out of Scope |
|----------|--------------|
| Extract `core/` modules from God Scripts | CLI refactoring (Phase 4) |
| Create `io/` modules for I/O separation | Full `.ontos.toml` config system (Phase 3) |
| Create `commands/map.py` and `commands/log.py` | New features |
| Migrate 7 minor commands to `commands/` | MCP layer |
| Fix pre-existing PyYAML architecture violation | `commands/init.py` (Phase 3) |
| Fix pre-existing subprocess architecture violations (`staleness.py`, `config.py`) | Watch mode (`--watch` flag) — Deferred to v3.1. **Tracking:** Create GitHub issue "Watch mode for context map generation" with label `v3.1-backlog` |
| Update imports in bundled scripts | |
| Maintain Golden Master parity | |

### 1.3 Entry Criteria

Before starting Phase 2:
- [x] Phase 1 merged and verified (PR #40)
- [x] Golden Master tests passing (16/16)
- [x] Branch `Phase2_V3.0_beta` created from `main`

### 1.4 Exit Criteria

Phase 2 is complete when:
- [ ] All 11 new modules created (`core/graph.py`, `core/validation.py`, `core/types.py`, `core/suggestions.py`, `core/tokens.py`, `io/git.py`, `io/files.py`, `io/toml.py`, `io/yaml.py`, `commands/map.py`, `commands/log.py`)
- [ ] God Scripts < 200 lines each (argparse + deprecation only)
- [ ] 7 minor commands migrated to `commands/`
- [ ] Pre-existing PyYAML violation fixed (`core/frontmatter.py`)
- [ ] Pre-existing subprocess violations fixed (`core/staleness.py`, `core/config.py`)
- [ ] Golden Master tests pass (16/16)
- [ ] All unit tests pass (303+ existing + new module tests)
- [ ] No circular imports (CI test passes)
- [ ] Architecture constraints enforced (no `core/` -> `io/` imports, no subprocess in `core/`)
- [ ] Tag `v3.0.0-beta` created

### 1.5 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Circular imports | High | High | `types.py` first (no deps), CI test, explicit import order |
| Behavior regression | Medium | Critical | Golden Master after each extraction |
| Hidden dependencies | Medium | Medium | Thorough dependency mapping |
| God Script breaks | Medium | High | Incremental extraction with rollback |
| Type duplication | Medium | Medium | Re-export existing types, don't duplicate |

---

## 2. Current State Analysis (Verified)

### 2.1 Post-Phase 1 Package Structure

```
ontos/
├── __init__.py              (57 lines - main exports)
├── __main__.py              (entry point)
├── cli.py                   (CLI interface, delegates to scripts)
├── core/                    (11 modules, 2,754 lines)
│   ├── __init__.py          (86 lines - re-exports)
│   ├── config.py            (83 lines) — CONTAINS subprocess (violation)
│   ├── context.py           (271 lines)
│   ├── curation.py          (489 lines) — CONTAINS CurationLevel IntEnum
│   ├── frontmatter.py       (122 lines) — CONTAINS PyYAML import (violation)
│   ├── history.py           (263 lines)
│   ├── ontology.py          (192 lines)
│   ├── paths.py             (345 lines)
│   ├── proposals.py         (134 lines)
│   ├── schema.py            (421 lines)
│   └── staleness.py         (353 lines) — CONTAINS subprocess (violation)
├── ui/
│   └── output.py            (OutputHandler)
├── commands/                (placeholder - 1 line __init__.py)
├── io/                      (placeholder - 1 line __init__.py)
├── mcp/                     (placeholder - 1 line __init__.py)
├── _scripts/                (26 bundled scripts, 9,563 lines)
├── _templates/              (bundled templates)
└── _hooks/                  (bundled git hooks)
```

### 2.2 God Script Analysis

#### `ontos/_scripts/ontos_end_session.py` — 1,905 lines

**Imports (Lines 1-39):**
- stdlib: `os`, `re`, `datetime`, `subprocess`, `argparse`, `sys`, `pathlib.Path`, `typing.Optional`
- internal: `ontos.core.context.SessionContext`, `ontos.ui.output.OutputHandler`
- config: `ontos_config` (version, paths), `ontos_lib` (21 functions)

**NO CLASSES** — Entirely function-based

**Major Sections:**
| Section | Lines | Functions | Extraction Target | Notes |
|---------|-------|-----------|-------------------|-------|
| Proposal Graduation | 46-296 | `detect_implemented_proposal`, `graduate_proposal`, `add_graduation_to_ledger`, `prompt_graduation` | `commands/log.py` | Orchestration logic |
| Session Appending | 304-773 | `get_current_branch`, `slugify`, `find_existing_log_for_today`, `validate_branch_in_log`, `append_to_log`, `get_commits_since_push`, `find_enhance_target`, `find_active_log_for_branch`, `auto_archive`, `create_auto_log` | `io/git.py`, `io/files.py`, `commands/log.py` | Split: git ops to io, orchestration to commands |
| Templates | 779-812 | Constants: `TEMPLATES`, `SECTION_TEMPLATES` | `core/types.py` | Constants only |
| Validation | 849-932 | `validate_topic_slug`, `generate_auto_slug` | `commands/log.py` | Orchestration |
| Git Operations | 935-1001 | `get_session_git_log`, `find_changelog` | `io/git.py`, `io/files.py` | Pure I/O |
| Changelog | 1004-1190 | `create_changelog`, `prompt_changelog_entry`, `add_changelog_entry` | `commands/log.py` | Orchestration |
| Impact Suggestion | 1193-1400 | `load_document_index`, `suggest_impacts`, `prompt_for_impacts`, `validate_concepts` | `core/suggestions.py` | Pure logic |
| Log Creation | 1403-1540 | `create_log_file`, `_create_archive_marker` | `commands/log.py` | Orchestration |
| Staleness Check | 1548-1605 | `check_stale_docs_warning` | `commands/log.py` | Uses existing `core/staleness` |
| Main | 1608-1904 | `main`, `emit_deprecation_notice` | Keep | Entry point only |

#### `ontos/_scripts/ontos_generate_context_map.py` — 1,296 lines

**Imports (Lines 1-66):**
- stdlib: `os`, `sys`, `time`, `re`, `datetime`, `argparse`, `pathlib.Path`, `typing.Optional`, `yaml`
- internal: `ontos.core.context.SessionContext`, `ontos.ui.output.OutputHandler`, `ontos.core.curation`
- config: `ontos_config`, `ontos_lib` (21 functions), `ontos_config_defaults`

**One Inner Class:** `ChangeHandler` (lines 1146-1157) for watch mode

**Major Sections:**
| Section | Lines | Functions | Extraction Target | Notes |
|---------|-------|-----------|-------------------|-------|
| Token Estimation | 71-102 | `estimate_tokens`, `format_token_count` | `core/tokens.py` | Pure logic |
| Data Quality | 106-198 | `lint_data_quality` | `commands/map.py` | Uses other validators |
| Document Scanning | 201-273 | `scan_docs` | `io/files.py` -> `scan_documents()` | File discovery only; YAML parsing remains in caller |
| Tree Generation | 276-327 | `generate_tree` | `commands/map.py` | Orchestration |
| Timeline | 330-383 | `generate_timeline` | `commands/map.py` | Pure transformation |
| Provenance | 386-424 | `generate_provenance_header` | `commands/map.py` | Orchestration |
| Dependency Validation | 428-560 | `validate_dependencies` | `core/graph.py` | Pure logic |
| Log Schema Validation | 564-619 | `validate_log_schema` | `core/validation.py` | Pure logic |
| Impacts Validation | 622-692 | `validate_impacts` | `core/validation.py` | Pure logic |
| Status Validation | 695-799 | `validate_v26_status` | `core/validation.py` | Pure logic |
| Describes Validation | 802-848 | `validate_v27_describes` | `core/validation.py` | Pure logic |
| Staleness Audit | 851-915 | `generate_staleness_audit` | `commands/map.py` | Uses `core/staleness` |
| Status Indicator | 918-922 | `get_status_indicator` | `commands/map.py` | Simple utility |
| Main Generation | 925-1126 | `generate_context_map` | `commands/map.py` | Orchestration |
| Watch Mode | 1129-1179 | `watch_mode`, `ChangeHandler` | Defer to v3.1 | Out of scope |
| Consolidation Check | 1182-1216 | `check_consolidation_status` | `commands/map.py` | Orchestration |
| Main | 1219-1283 | `main`, `emit_deprecation_notice` | Keep | Entry point only |

### 2.3 Dependency Analysis

**God Script → Core Module Dependencies:**
| Script | Imports From | Symbols Used |
|--------|--------------|--------------|
| `ontos_end_session.py` | `ontos.core.context` | `SessionContext` |
| `ontos_end_session.py` | `ontos.ui.output` | `OutputHandler` |
| `ontos_generate_context_map.py` | `ontos.core.context` | `SessionContext` |
| `ontos_generate_context_map.py` | `ontos.core.curation` | `CurationLevel`, `detect_curation_level`, `level_marker` |
| `ontos_generate_context_map.py` | `ontos.ui.output` | `OutputHandler` |

**Shared `ontos_lib` Functions (both scripts use):**
- `parse_frontmatter`, `normalize_depends_on`, `normalize_type`
- `check_staleness`, `validate_describes_field`, `detect_describes_cycles`
- `load_common_concepts`, `get_proposals_dir`, `load_decision_history_entries`
- `resolve_config`, `get_source`, `get_git_last_modified`

**Function Ownership Assignment:**
| Function | Owner Module |
|----------|--------------|
| `load_common_concepts` | `core/suggestions.py` |
| `validate_describes_field` | `core/validation.py` |

### 2.4 Gap Analysis: Roadmap vs Reality

| Roadmap Assumed | Actual State | Impact |
|-----------------|--------------|--------|
| Scripts at `.ontos/scripts/` | Scripts at `ontos/_scripts/` | Update all path references |
| Line numbers from v2.9.x | Line numbers verified current | Some drift but accurate |
| `ontos/io/` needs creation | Placeholder exists with 1-line `__init__.py` | Just add modules |
| `ontos/commands/` needs creation | Placeholder exists | Just add modules |
| `core/graph.py` from lines 428-560 | Verified: `validate_dependencies()` at 428-560 | Match |
| `core/tokens.py` from lines 71-104 | Verified: `estimate_tokens()` at 71-85, `format_token_count()` at 88-102 | Match |
| `CurationLevel` needs creation | Already exists in `core/curation.py` lines 18-22 | Re-export, don't duplicate |
| `core/` is stdlib-only | `core/frontmatter.py` imports PyYAML | Must fix in Phase 2 |
| `core/` has no subprocess | `core/staleness.py` and `core/config.py` use subprocess | Must fix in Phase 2 |

---

## 3. Target State

### 3.1 Target Package Structure

```
ontos/
├── __init__.py              # Unchanged
├── __main__.py              # Unchanged
├── cli.py                   # Unchanged (Phase 4 will refactor)
├── core/
│   ├── __init__.py          # MODIFIED — add new exports
│   ├── config.py            # Existing
│   ├── context.py           # Existing
│   ├── curation.py          # Existing (contains CurationLevel)
│   ├── frontmatter.py       # MODIFIED — remove PyYAML import
│   ├── graph.py             # NEW — dependency graph, cycle detection
│   ├── history.py           # Existing
│   ├── ontology.py          # Existing
│   ├── paths.py             # Existing
│   ├── proposals.py         # Existing
│   ├── schema.py            # Existing
│   ├── staleness.py         # Existing
│   ├── suggestions.py       # NEW — impact/concept suggestions
│   ├── tokens.py            # NEW — token estimation
│   ├── types.py             # NEW — shared enums, dataclasses, re-exports
│   └── validation.py        # NEW — ValidationOrchestrator
├── io/
│   ├── __init__.py          # NEW — io exports
│   ├── files.py             # NEW — file operations
│   ├── git.py               # NEW — git subprocess operations
│   ├── toml.py              # NEW — TOML parsing (for Phase 3)
│   └── yaml.py              # NEW — PyYAML wrapper
├── ui/
│   └── output.py            # Existing
├── commands/
│   ├── __init__.py          # MODIFIED — add command exports
│   ├── consolidate.py       # NEW — from ontos_consolidate.py
│   ├── log.py               # NEW — session log orchestration
│   ├── map.py               # NEW — context map orchestration
│   ├── migrate.py           # NEW — from ontos_migrate_schema.py
│   ├── promote.py           # NEW — from ontos_promote.py
│   ├── query.py             # NEW — from ontos_query.py
│   ├── scaffold.py          # NEW — from ontos_scaffold.py
│   ├── stub.py              # NEW — from ontos_stub.py
│   └── verify.py            # NEW — from ontos_verify.py
├── mcp/
│   └── __init__.py          # Placeholder (unchanged)
└── _scripts/
    ├── ontos.py             # MODIFIED — uses new modules
    ├── ontos_end_session.py # MODIFIED — < 200 lines, calls commands/log.py
    ├── ontos_generate_context_map.py  # MODIFIED — < 200 lines, calls commands/map.py
    └── ... (other scripts)
```

### 3.2 Module Responsibilities

| Module | Responsibility | Public API |
|--------|----------------|------------|
| `core/graph.py` | Dependency graph, cycle detection, orphan detection | `DependencyGraph`, `build_graph()`, `detect_cycles()`, `detect_orphans()` |
| `core/validation.py` | Validation orchestration, error collection | `ValidationOrchestrator`, `ValidationError`, `ValidationResult`, `validate_describes_field()` |
| `core/types.py` | Shared enums, dataclasses, constants, re-exports | `DocumentType`, `DocumentStatus`, `ValidationErrorType`, `TEMPLATES`, `CurationLevel` (re-export) |
| `core/suggestions.py` | Impact/concept suggestion algorithms | `suggest_impacts()`, `validate_concepts()`, `load_document_index()`, `load_common_concepts()` |
| `core/tokens.py` | Token estimation for LLM context | `estimate_tokens()`, `format_token_count()` |
| `io/git.py` | Git subprocess operations | `get_current_branch()`, `get_commits_since_push()`, `get_file_mtime()` |
| `io/files.py` | File I/O operations | `find_project_root()`, `scan_documents()`, `read_document()`, `load_document()` |
| `io/toml.py` | TOML config loading | `load_config()`, `write_config()`, `merge_configs()` |
| `io/yaml.py` | PyYAML wrapper | `parse_yaml()`, `dump_yaml()` |
| `commands/map.py` | Context map orchestration | `generate_context_map()`, `GenerateMapOptions` |
| `commands/log.py` | Session log orchestration | `end_session()`, `EndSessionOptions` |

### 3.3 Type Normalization Boundary

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

## 4. File Specifications

### 4.1 `ontos/core/types.py` — NEW

**Purpose:** Central type definitions, enums, constants. Must have NO dependencies on other new modules. Re-exports existing types for consolidation.

**Source:** Constants extracted from both God Scripts + new type definitions.

```python
"""
Shared type definitions for Ontos core modules.

This module has NO dependencies on other ontos modules (except re-exports)
to prevent circular imports. Import this first when building other core modules.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# =============================================================================
# RE-EXPORTS (consolidate existing types here)
# =============================================================================

# Re-export CurationLevel from its canonical location
from ontos.core.curation import CurationLevel

# =============================================================================
# ENUMS (new)
# =============================================================================

class DocumentType(Enum):
    """Document types in the Ontos ontology."""
    KERNEL = "kernel"
    STRATEGY = "strategy"
    PRODUCT = "product"
    ATOM = "atom"
    LOG = "log"

class DocumentStatus(Enum):
    """Document lifecycle status."""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REJECTED = "rejected"
    COMPLETE = "complete"

class ValidationErrorType(Enum):
    """Categories of validation errors."""
    BROKEN_LINK = "broken_link"
    CYCLE = "cycle"
    ORPHAN = "orphan"
    ARCHITECTURE = "architecture"
    SCHEMA = "schema"
    STATUS = "status"
    STALENESS = "staleness"
    CURATION = "curation"
    IMPACTS = "impacts"

# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class DocumentData:
    """Parsed document with frontmatter and content."""
    id: str
    type: DocumentType
    status: DocumentStatus
    filepath: Path
    frontmatter: Dict[str, Any]
    content: str
    depends_on: List[str] = field(default_factory=list)
    impacts: List[str] = field(default_factory=list)

@dataclass
class ValidationError:
    """A single validation error or warning."""
    error_type: ValidationErrorType
    doc_id: str
    filepath: str
    message: str
    fix_suggestion: str
    severity: str  # 'error', 'warning', 'info'

@dataclass
class ValidationResult:
    """Result of running all validations."""
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 1 if self.errors else 0

# =============================================================================
# CONSTANTS (from ontos_end_session.py lines 779-846)
# =============================================================================

VALID_SLUG_PATTERN = r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$"
MAX_SLUG_LENGTH = 50

CHANGELOG_CATEGORIES = [
    "Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"
]

DEFAULT_CHANGELOG = "CHANGELOG.md"

# Event type templates for session logs
TEMPLATES = {
    "chore": "## Summary\n\n## Changes Made\n\n## Testing",
    "fix": "## Summary\n\n## Root Cause\n\n## Fix Applied\n\n## Testing",
    "feature": "## Summary\n\n## Implementation\n\n## Testing\n\n## Documentation",
    "refactor": "## Summary\n\n## Changes\n\n## Rationale\n\n## Testing",
    "exploration": "## Objective\n\n## Findings\n\n## Conclusions\n\n## Next Steps",
    "decision": "## Context\n\n## Decision\n\n## Rationale\n\n## Consequences",
}

SECTION_TEMPLATES = {
    "Summary": "<!-- Brief description of what was done -->",
    "Changes Made": "<!-- List of changes -->",
    "Testing": "<!-- How this was tested -->",
    "Root Cause": "<!-- What caused the issue -->",
    "Fix Applied": "<!-- How the fix works -->",
}
```

**Dependencies:** `core/curation.py` (for re-export only)

**Tests Required:**
- [ ] `test_document_type_values` — Enum values match expected
- [ ] `test_validation_result_exit_code` — 0 when no errors, 1 when errors
- [ ] `test_templates_keys` — All event types have templates
- [ ] `test_curation_level_reexport` — CurationLevel accessible from types

---

### 4.2 `ontos/core/tokens.py` — NEW

**Purpose:** Token estimation for context maps.

**Source:** `ontos/_scripts/ontos_generate_context_map.py` lines 71-102

```python
"""
Token estimation utilities for context map generation.

Extracted from ontos_generate_context_map.py during Phase 2 decomposition.
"""

def estimate_tokens(content: str) -> int:
    """Estimate token count using character-based heuristic.

    Uses ~4 characters per token (standard GPT approximation).

    Args:
        content: Text content to estimate

    Returns:
        Estimated token count
    """
    if not content:
        return 0
    return len(content) // 4


def format_token_count(tokens: int) -> str:
    """Format token count for display with thousand separators.

    Args:
        tokens: Token count to format

    Returns:
        Formatted string like "~2,500 tokens" or "~12k tokens"
    """
    if tokens < 1000:
        return f"~{tokens} tokens"
    elif tokens < 10000:
        return f"~{tokens:,} tokens"
    else:
        k = tokens // 1000
        return f"~{k}k tokens"
```

**Dependencies:** None (stdlib only)

**Tests Required:**
- [ ] `test_estimate_tokens_empty` — Empty string returns 0
- [ ] `test_estimate_tokens_short` — Short text estimates correctly
- [ ] `test_format_token_count_small` — Under 1000 formats without comma
- [ ] `test_format_token_count_medium` — 1000-9999 formats with comma
- [ ] `test_format_token_count_large` — 10000+ formats with k suffix

---

### 4.3 `ontos/core/graph.py` — NEW

**Purpose:** Dependency graph building, cycle detection, orphan detection.

**Source:** `ontos/_scripts/ontos_generate_context_map.py` lines 428-560

```python
"""
Dependency graph building and validation.

Extracted from ontos_generate_context_map.py during Phase 2 decomposition.
Implements O(V+E) DFS for cycle detection (NOT O(N²) path.index() pattern).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple

from ontos.core.types import DocumentData, ValidationError, ValidationErrorType


@dataclass
class GraphNode:
    """A node in the dependency graph."""
    doc_id: str
    doc_type: str
    filepath: str
    depends_on: List[str] = field(default_factory=list)


@dataclass
class DependencyGraph:
    """Represents document dependency relationships."""
    nodes: Dict[str, GraphNode] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)  # id -> depends_on
    reverse_edges: Dict[str, List[str]] = field(default_factory=dict)  # id -> depended_by

    def add_node(self, doc_id: str, doc_type: str, filepath: str, depends_on: List[str]) -> None:
        """Add a document node to the graph."""
        self.nodes[doc_id] = GraphNode(doc_id, doc_type, filepath, depends_on)
        self.edges[doc_id] = depends_on
        for dep in depends_on:
            if dep not in self.reverse_edges:
                self.reverse_edges[dep] = []
            self.reverse_edges[dep].append(doc_id)


def build_graph(docs: Dict[str, DocumentData]) -> Tuple[DependencyGraph, List[ValidationError]]:
    """Build dependency graph from document dictionary.

    Args:
        docs: Dictionary mapping doc_id to DocumentData

    Returns:
        Tuple of (DependencyGraph, list of broken link errors)
    """
    graph = DependencyGraph()
    errors = []
    existing_ids = set(docs.keys())

    for doc_id, doc in docs.items():
        depends_on = doc.depends_on if hasattr(doc, 'depends_on') else []
        graph.add_node(doc_id, doc.type.value, str(doc.filepath), depends_on)

        # Check for broken links
        for dep_id in depends_on:
            if dep_id not in existing_ids:
                errors.append(ValidationError(
                    error_type=ValidationErrorType.BROKEN_LINK,
                    doc_id=doc_id,
                    filepath=str(doc.filepath),
                    message=f"Broken dependency: '{dep_id}' does not exist",
                    fix_suggestion=f"Remove '{dep_id}' from depends_on or create the missing document",
                    severity="error"
                ))

    return graph, errors


def detect_cycles(graph: DependencyGraph) -> List[List[str]]:
    """Detect circular dependencies using DFS.

    Uses O(V+E) algorithm with visited and in_stack sets.

    Args:
        graph: DependencyGraph to analyze

    Returns:
        List of cycles (each cycle is a list of doc_ids)
    """
    visited: Set[str] = set()
    in_stack: Set[str] = set()
    cycles: List[List[str]] = []

    def dfs(node: str, path: List[str]) -> None:
        if node in in_stack:
            # Found cycle - extract it from path
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return

        if node in visited:
            return

        visited.add(node)
        in_stack.add(node)
        path.append(node)

        for neighbor in graph.edges.get(node, []):
            if neighbor in graph.nodes:  # Only follow valid edges
                dfs(neighbor, path)

        path.pop()
        in_stack.remove(node)

    for node in graph.nodes:
        if node not in visited:
            dfs(node, [])

    return cycles


def detect_orphans(graph: DependencyGraph, allowed_orphan_types: Set[str]) -> List[str]:
    """Find documents with no incoming edges (not depended on by anyone).

    Args:
        graph: DependencyGraph to analyze
        allowed_orphan_types: Document types that are allowed to be orphans

    Returns:
        List of orphan doc_ids
    """
    orphans = []
    for doc_id, node in graph.nodes.items():
        if node.doc_type in allowed_orphan_types:
            continue
        if doc_id not in graph.reverse_edges or not graph.reverse_edges[doc_id]:
            orphans.append(doc_id)
    return orphans


def calculate_depths(graph: DependencyGraph) -> Dict[str, int]:
    """Calculate dependency depth for each node.

    Depth is the longest path to a leaf node (document with no dependencies).

    Args:
        graph: DependencyGraph to analyze

    Returns:
        Dictionary mapping doc_id to depth
    """
    depths: Dict[str, int] = {}
    computing: Set[str] = set()  # Prevent infinite recursion on cycles

    def get_depth(node: str) -> int:
        if node in depths:
            return depths[node]
        if node in computing:
            return 0  # Cycle detected, treat as leaf
        if node not in graph.nodes:
            return 0

        computing.add(node)
        deps = graph.edges.get(node, [])
        if not deps:
            depth = 0
        else:
            depth = 1 + max(get_depth(d) for d in deps if d in graph.nodes)
        computing.remove(node)
        depths[node] = depth
        return depth

    for node in graph.nodes:
        get_depth(node)

    return depths
```

**Dependencies:** `core/types.py`

**Tests Required:**
- [ ] `test_build_graph_empty` — Empty docs returns empty graph
- [ ] `test_build_graph_with_deps` — Dependencies correctly recorded
- [ ] `test_build_graph_broken_link` — Missing deps generate errors
- [ ] `test_detect_cycles_none` — No cycles returns empty list
- [ ] `test_detect_cycles_simple` — A→B→A detected
- [ ] `test_detect_cycles_complex` — Multi-node cycle detected
- [ ] `test_detect_orphans` — Unreferenced docs found
- [ ] `test_calculate_depths` — Depth calculation correct

---

### 4.4 `ontos/core/suggestions.py` — NEW

**Purpose:** Impact and concept suggestion algorithms.

**Source:** `ontos/_scripts/ontos_end_session.py` lines 1193-1400

```python
"""
Impact and concept suggestion algorithms for session logs.

Extracted from ontos_end_session.py during Phase 2 decomposition.
"""

from __future__ import annotations
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def load_document_index(context_map_content: str) -> Dict[str, str]:
    """Parse context map to build filepath -> doc_id mapping.

    Args:
        context_map_content: Content of Ontos_Context_Map.md

    Returns:
        Dictionary mapping filepath to doc_id
    """
    index: Dict[str, str] = {}

    # Parse table rows from context map
    # Format: | path/to/file.md | doc_id | type | status |
    for line in context_map_content.split('\n'):
        if '|' not in line or line.strip().startswith('|--'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            filepath = parts[1]
            doc_id = parts[2]
            if filepath and doc_id and not filepath.startswith('Path'):
                index[filepath] = doc_id

    return index


def load_common_concepts(context_map_content: str) -> Set[str]:
    """Load common concepts from context map.

    Parses the ## Common Concepts section of the context map.

    Args:
        context_map_content: Content of Ontos_Context_Map.md

    Returns:
        Set of known concept strings
    """
    concepts: Set[str] = set()
    in_concepts_section = False

    for line in context_map_content.split('\n'):
        if line.startswith('## Common Concepts'):
            in_concepts_section = True
            continue
        if in_concepts_section:
            if line.startswith('## '):
                break  # Next section
            # Parse concept entries (typically comma-separated or bullet points)
            if line.strip().startswith('-'):
                concept = line.strip().lstrip('-').strip()
                if concept:
                    concepts.add(concept)
            elif ',' in line:
                for concept in line.split(','):
                    concept = concept.strip()
                    if concept:
                        concepts.add(concept)

    return concepts


def suggest_impacts(
    changed_files: List[str],
    document_index: Dict[str, str],
    commit_messages: List[str]
) -> List[str]:
    """Suggest document IDs that may be impacted by changes.

    Analyzes changed files and commit messages to identify related documents.

    Args:
        changed_files: List of file paths that changed
        document_index: Mapping of filepath to doc_id
        commit_messages: List of commit messages

    Returns:
        List of suggested doc_ids
    """
    suggestions: Set[str] = set()

    # Direct matches: changed file is a documented file
    for filepath in changed_files:
        if filepath in document_index:
            suggestions.add(document_index[filepath])

    # Indirect matches: filename appears in doc_id
    for filepath in changed_files:
        basename = os.path.basename(filepath)
        name_without_ext = os.path.splitext(basename)[0]

        for doc_id in document_index.values():
            # Check if file name appears in doc_id
            if name_without_ext.lower() in doc_id.lower():
                suggestions.add(doc_id)

    # Commit message analysis: extract potential doc references
    doc_id_pattern = re.compile(r'\b([a-z][a-z0-9_]+(?:_[a-z0-9]+)*)\b')
    all_doc_ids = set(document_index.values())

    for message in commit_messages:
        matches = doc_id_pattern.findall(message.lower())
        for match in matches:
            if match in all_doc_ids:
                suggestions.add(match)

    return sorted(suggestions)


def validate_concepts(
    concepts: List[str],
    known_concepts: Set[str]
) -> Tuple[List[str], List[str]]:
    """Validate concepts against known vocabulary.

    Args:
        concepts: List of concepts to validate
        known_concepts: Set of valid concept strings

    Returns:
        Tuple of (valid_concepts, unknown_concepts)
    """
    valid = []
    unknown = []

    for concept in concepts:
        if concept in known_concepts:
            valid.append(concept)
        else:
            unknown.append(concept)

    return valid, unknown
```

**Dependencies:** stdlib only

**Tests Required:**
- [ ] `test_load_document_index` — Parses context map table correctly
- [ ] `test_load_common_concepts` — Parses concepts section correctly
- [ ] `test_suggest_impacts_direct` — Direct file matches found
- [ ] `test_suggest_impacts_indirect` — Filename substring matches found
- [ ] `test_validate_concepts_all_valid` — All known concepts pass
- [ ] `test_validate_concepts_unknown` — Unknown concepts flagged

---

### 4.5 `ontos/core/validation.py` — NEW

**Purpose:** Unified validation orchestration with error collection.

**Source:** `ontos/_scripts/ontos_generate_context_map.py` lines 564-848

```python
"""
Validation orchestration for context map generation.

Extracts validation logic from ontos_generate_context_map.py and provides
a unified interface that collects all errors before returning (no hard exits).
"""

from __future__ import annotations
from typing import Dict, List, Set, Tuple, Optional, Any

from ontos.core.types import (
    DocumentData,
    ValidationError,
    ValidationResult,
    ValidationErrorType,
)
from ontos.core.graph import (
    build_graph,
    detect_cycles,
    detect_orphans,
    calculate_depths,
)


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


class ValidationOrchestrator:
    """Orchestrates all validation checks and collects errors."""

    def __init__(
        self,
        docs: Dict[str, DocumentData],
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize with documents and optional config.

        Args:
            docs: Dictionary mapping doc_id to DocumentData
            config: Optional configuration dict
        """
        self.docs = docs
        self.config = config or {}
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def validate_all(self) -> ValidationResult:
        """Run all validations and return collected results.

        Returns:
            ValidationResult with all errors and warnings
        """
        self.validate_graph()
        self.validate_log_schema()
        self.validate_impacts()
        self.validate_describes()

        return ValidationResult(
            errors=self.errors,
            warnings=self.warnings
        )

    def validate_graph(self) -> None:
        """Validate dependency graph: broken links, cycles, orphans, depth."""
        graph, broken_link_errors = build_graph(self.docs)
        self.errors.extend(broken_link_errors)

        # Detect cycles
        cycles = detect_cycles(graph)
        for cycle in cycles:
            cycle_str = " -> ".join(cycle)
            self.errors.append(ValidationError(
                error_type=ValidationErrorType.CYCLE,
                doc_id=cycle[0],
                filepath=str(self.docs[cycle[0]].filepath) if cycle[0] in self.docs else "",
                message=f"Circular dependency: {cycle_str}",
                fix_suggestion="Break the cycle by removing one dependency",
                severity="error"
            ))

        # Detect orphans
        allowed_orphans = set(self.config.get("allowed_orphan_types", ["atom", "log"]))
        orphans = detect_orphans(graph, allowed_orphans)
        for orphan_id in orphans:
            if orphan_id in self.docs:
                self.warnings.append(ValidationError(
                    error_type=ValidationErrorType.ORPHAN,
                    doc_id=orphan_id,
                    filepath=str(self.docs[orphan_id].filepath),
                    message=f"Document has no incoming dependencies",
                    fix_suggestion="Add this document to another document's depends_on",
                    severity="warning"
                ))

        # Check depth
        max_depth = self.config.get("max_dependency_depth", 5)
        depths = calculate_depths(graph)
        for doc_id, depth in depths.items():
            if depth > max_depth:
                self.warnings.append(ValidationError(
                    error_type=ValidationErrorType.ARCHITECTURE,
                    doc_id=doc_id,
                    filepath=str(self.docs[doc_id].filepath) if doc_id in self.docs else "",
                    message=f"Dependency depth {depth} exceeds max {max_depth}",
                    fix_suggestion="Consider flattening the dependency chain",
                    severity="warning"
                ))

    def validate_log_schema(self) -> None:
        """Validate log documents have required v2.0 fields."""
        required_fields = {"branch", "event_type", "source"}

        for doc_id, doc in self.docs.items():
            if doc.type.value != "log":
                continue

            missing = required_fields - set(doc.frontmatter.keys())
            if missing:
                self.warnings.append(ValidationError(
                    error_type=ValidationErrorType.SCHEMA,
                    doc_id=doc_id,
                    filepath=str(doc.filepath),
                    message=f"Log missing fields: {', '.join(sorted(missing))}",
                    fix_suggestion="Add missing fields to frontmatter",
                    severity="warning"
                ))

    def validate_impacts(self) -> None:
        """Validate impacts[] references exist."""
        valid_ids = set(self.docs.keys())

        for doc_id, doc in self.docs.items():
            for impact in doc.impacts:
                if impact not in valid_ids:
                    self.warnings.append(ValidationError(
                        error_type=ValidationErrorType.IMPACTS,
                        doc_id=doc_id,
                        filepath=str(doc.filepath),
                        message=f"Impact reference '{impact}' not found",
                        fix_suggestion=f"Remove '{impact}' or create the document",
                        severity="warning"
                    ))

    def validate_describes(self) -> None:
        """Validate describes field references."""
        valid_ids = set(self.docs.keys())

        for doc_id, doc in self.docs.items():
            error = validate_describes_field(doc, valid_ids)
            if error:
                self.warnings.append(error)
```

**Dependencies:** `core/types.py`, `core/graph.py`

**Tests Required:**
- [ ] `test_orchestrator_empty_docs` — No errors for empty docs
- [ ] `test_orchestrator_collects_all` — All error types collected
- [ ] `test_validate_graph_broken_links` — Broken links detected
- [ ] `test_validate_graph_cycles` — Cycles detected
- [ ] `test_validate_log_schema_missing` — Missing fields flagged
- [ ] `test_validate_impacts_invalid` — Invalid refs flagged
- [ ] `test_validate_describes_field` — Invalid describes flagged

---

### 4.6 `ontos/io/git.py` — NEW

**Purpose:** All git subprocess operations.

**Source:** Various functions from both God Scripts

```python
"""
Git subprocess operations.

All git interactions should go through this module to maintain
the core/io separation required by the architecture.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


def get_current_branch() -> Optional[str]:
    """Get the current git branch name.

    Returns:
        Branch name or None if not in a git repo
    """
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def get_commits_since_push(fallback_count: int = 5) -> List[str]:
    """Get commit messages for unpushed commits.

    Args:
        fallback_count: Number of commits to return if no upstream

    Returns:
        List of commit messages
    """
    try:
        # Try to get commits since last push
        result = subprocess.run(
            ["git", "log", "@{u}..HEAD", "--format=%s"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')

        # Fallback: last N commits
        result = subprocess.run(
            ["git", "log", f"-{fallback_count}", "--format=%s"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


def get_changed_files_since_push() -> List[str]:
    """Get list of files changed since last push.

    Returns:
        List of file paths
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "@{u}..HEAD"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')

        # Fallback: files in last commit
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


def get_file_mtime(filepath: Path) -> Optional[datetime]:
    """Get last modification time from git.

    Args:
        filepath: Path to file

    Returns:
        Datetime of last modification or None
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(filepath)],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return datetime.fromisoformat(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass
    return None


def is_git_repo() -> bool:
    """Check if current directory is in a git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_git_root() -> Optional[Path]:
    """Get the root directory of the git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None
```

**Dependencies:** stdlib only

**Tests Required:**
- [ ] `test_get_current_branch` — Returns branch name
- [ ] `test_get_commits_since_push_fallback` — Uses fallback when no upstream
- [ ] `test_get_changed_files` — Returns file list
- [ ] `test_is_git_repo_true` — Detects git repo
- [ ] `test_get_git_root` — Returns correct path

---

### 4.7 `ontos/io/files.py` — NEW

**Purpose:** File system operations for documents.

```python
"""
File system operations for Ontos.

Provides file I/O utilities that core modules should NOT call directly.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from ontos.core.types import DocumentType, DocumentStatus, DocumentData


def find_project_root(start_path: Path = None) -> Path:
    """Find Ontos project root by walking up from start_path.

    Resolution precedence:
    1. Nearest `.ontos.toml` file
    2. Git repository root (`.git/` directory)
    3. Raises FileNotFoundError

    Args:
        start_path: Starting directory (defaults to cwd)

    Returns:
        Path to project root

    Raises:
        FileNotFoundError: If no project root found
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    while current != current.parent:
        # Check for .ontos.toml
        if (current / ".ontos.toml").exists():
            return current
        # Check for .git
        if (current / ".git").exists():
            return current
        current = current.parent

    raise FileNotFoundError(
        f"No Ontos project found. Run 'ontos init' to initialize, "
        f"or ensure you're in a git repository."
    )


def scan_documents(
    dirs: List[Path],
    skip_patterns: List[str] = None
) -> List[Path]:
    """Recursively find markdown files.

    Args:
        dirs: Directories to scan
        skip_patterns: Glob patterns to skip

    Returns:
        List of markdown file paths
    """
    skip_patterns = skip_patterns or []
    results = []

    for dir_path in dirs:
        if not dir_path.exists():
            continue
        for md_file in dir_path.rglob("*.md"):
            # Check skip patterns
            skip = False
            for pattern in skip_patterns:
                if md_file.match(pattern):
                    skip = True
                    break
            if not skip:
                results.append(md_file)

    return sorted(results)


def read_document(path: Path) -> str:
    """Read document content.

    Args:
        path: Path to document

    Returns:
        Document content as string
    """
    return path.read_text(encoding="utf-8")


def load_document(
    path: Path,
    frontmatter_parser: Callable[[str], Tuple[Dict, str]]
) -> DocumentData:
    """Load and normalize a document file.

    This is the type normalization boundary - strings become enums here.

    Args:
        path: Path to document
        frontmatter_parser: Function to parse frontmatter from content

    Returns:
        DocumentData with normalized types
    """
    content = path.read_text(encoding="utf-8")
    fm, body = frontmatter_parser(content)

    # Normalize strings to enums at this boundary
    doc_type = DocumentType(fm.get("type", "atom"))
    doc_status = DocumentStatus(fm.get("status", "draft"))

    return DocumentData(
        id=fm.get("id", path.stem),
        type=doc_type,
        status=doc_status,
        filepath=path,
        frontmatter=fm,
        content=body,
        depends_on=fm.get("depends_on", []),
        impacts=fm.get("impacts", []),
    )


def get_file_mtime(path: Path) -> Optional[datetime]:
    """Get file modification time from filesystem.

    Args:
        path: Path to file

    Returns:
        Datetime or None if file doesn't exist
    """
    try:
        stat = path.stat()
        return datetime.fromtimestamp(stat.st_mtime)
    except OSError:
        return None


def write_text_file(
    path: Path,
    content: str,
    encoding: str = "utf-8"
) -> None:
    """Write text content to file.

    For simple writes. Use SessionContext for transactional multi-file writes.

    Args:
        path: Destination path
        content: Content to write
        encoding: File encoding
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
```

**Dependencies:** `core/types.py` (for DocumentData, enums)

**Tests Required:**
- [ ] `test_find_project_root_toml` — Finds .ontos.toml
- [ ] `test_find_project_root_git` — Falls back to .git
- [ ] `test_find_project_root_not_found` — Raises FileNotFoundError
- [ ] `test_scan_documents` — Finds .md files
- [ ] `test_scan_documents_skip` — Respects skip patterns
- [ ] `test_load_document_normalizes_types` — Strings become enums

---

### 4.8 `ontos/io/toml.py` — NEW

**Purpose:** TOML config loading (prepares for Phase 3).

```python
"""
TOML configuration loading and writing.

Supports Python 3.9+ with tomli fallback for older versions.
"""

from pathlib import Path
from typing import Any, Dict

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


def load_config(path: Path) -> Dict[str, Any]:
    """Load .ontos.toml configuration file.

    Args:
        path: Path to .ontos.toml

    Returns:
        Configuration dictionary (empty if file not found)
    """
    if not path.exists():
        return {}

    with open(path, "rb") as f:
        return tomllib.load(f)


def merge_configs(base: Dict, override: Dict) -> Dict:
    """Deep merge two config dictionaries.

    Override values win. Nested dicts are recursively merged.

    Args:
        base: Base configuration
        override: Override configuration

    Returns:
        Merged configuration
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result


# Default configuration values
DEFAULT_CONFIG = {
    "ontos": {
        "version": "3.0"
    },
    "paths": {
        "docs_dir": "docs",
        "logs_dir": "docs/logs",
        "context_map": "Ontos_Context_Map.md"
    },
    "scanning": {
        "skip_patterns": ["_template.md", "archive/*"]
    },
    "validation": {
        "max_dependency_depth": 5,
        "allowed_orphan_types": ["atom"],
        "strict": False
    },
    "workflow": {
        "enforce_archive_before_push": True,
        "require_source_in_logs": True
    }
}
```

**Dependencies:** `tomli` (Python 3.9-3.10) or `tomllib` (3.11+)

**pyproject.toml update required:**
```toml
dependencies = [
    "tomli>=2.0.0; python_version < '3.11'"
]
```

**Tests Required:**
- [ ] `test_load_config_exists` — Loads valid TOML
- [ ] `test_load_config_missing` — Returns empty dict
- [ ] `test_merge_configs_simple` — Override wins
- [ ] `test_merge_configs_nested` — Deep merge works

---

### 4.9 `ontos/io/yaml.py` — NEW

**Purpose:** PyYAML wrapper to isolate third-party dependency from core.

```python
"""
YAML parsing operations.

Isolates PyYAML dependency from core modules to maintain
the stdlib-only constraint for the core layer.
"""

import yaml


def parse_yaml(content: str) -> dict:
    """Parse YAML content safely.

    Args:
        content: YAML string to parse

    Returns:
        Parsed dictionary (empty dict if content is empty/None)

    Raises:
        yaml.YAMLError: If content is invalid YAML
    """
    return yaml.safe_load(content) or {}


def dump_yaml(data: dict, default_flow_style: bool = False) -> str:
    """Serialize dictionary to YAML string.

    Args:
        data: Dictionary to serialize
        default_flow_style: Use flow style (inline) formatting

    Returns:
        YAML string
    """
    return yaml.dump(data, default_flow_style=default_flow_style)
```

**Dependencies:** `PyYAML`

**Tests Required:**
- [ ] `test_parse_yaml_valid` — Parses valid YAML
- [ ] `test_parse_yaml_empty` — Returns empty dict for empty input
- [ ] `test_parse_yaml_invalid` — Raises YAMLError
- [ ] `test_dump_yaml` — Serializes dict to YAML

---

### 4.10 `ontos/commands/map.py` — NEW

**Purpose:** Orchestrate context map generation using extracted core modules.

**Source:** `ontos/_scripts/ontos_generate_context_map.py` orchestration logic (lines 925-1126)

```python
"""
Context map generation command.

Orchestrates the generation of Ontos_Context_Map.md using
extracted core and io modules.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any

from ontos.core.context import SessionContext
from ontos.core.validation import ValidationOrchestrator
from ontos.core.tokens import estimate_tokens, format_token_count
from ontos.core.types import DocumentData
from ontos.ui.output import OutputHandler


@dataclass
class GenerateMapOptions:
    """Configuration options for context map generation."""
    output_path: Optional[Path] = None
    strict: bool = False
    include_staleness: bool = True
    include_timeline: bool = True
    max_dependency_depth: int = 5


def generate_context_map(
    ctx: SessionContext,
    output: OutputHandler,
    options: GenerateMapOptions = None
) -> str:
    """Generate the context map markdown content.

    Args:
        ctx: Session context with project configuration
        output: Output handler for user feedback
        options: Generation options

    Returns:
        Generated context map content as string
    """
    options = options or GenerateMapOptions()

    # 1. Scan documents
    from ontos.io.files import scan_documents, load_document
    from ontos.io.yaml import parse_yaml
    from ontos.core.frontmatter import parse_frontmatter

    docs_dir = ctx.project_root / ctx.config.get("paths", {}).get("docs_dir", "docs")
    skip_patterns = ctx.config.get("scanning", {}).get("skip_patterns", [])

    doc_paths = scan_documents([docs_dir], skip_patterns)
    output.info(f"Found {len(doc_paths)} documents")

    # 2. Load and parse documents
    docs: Dict[str, DocumentData] = {}
    for path in doc_paths:
        try:
            doc = load_document(path, lambda c: parse_frontmatter(c))
            docs[doc.id] = doc
        except Exception as e:
            output.warning(f"Failed to parse {path}: {e}")

    # 3. Run validation
    validator = ValidationOrchestrator(docs, ctx.config.get("validation", {}))
    result = validator.validate_all()

    for error in result.errors:
        output.error(f"{error.doc_id}: {error.message}")
    for warning in result.warnings:
        output.warning(f"{warning.doc_id}: {warning.message}")

    if options.strict and result.errors:
        raise ValueError(f"Validation failed with {len(result.errors)} errors")

    # 4. Generate content sections
    sections = []

    # Header
    sections.append(_generate_header(ctx, docs))

    # Document table
    sections.append(_generate_document_table(docs))

    # Dependency tree
    sections.append(_generate_dependency_tree(docs))

    # Timeline (if enabled)
    if options.include_timeline:
        sections.append(_generate_timeline(docs))

    # Staleness audit (if enabled)
    if options.include_staleness:
        sections.append(_generate_staleness_audit(docs))

    # Token estimate
    content = "\n\n".join(sections)
    tokens = estimate_tokens(content)
    output.info(f"Context map: {format_token_count(tokens)}")

    return content


def _generate_header(ctx: SessionContext, docs: Dict[str, DocumentData]) -> str:
    """Generate context map header with provenance."""
    # Implementation extracted from ontos_generate_context_map.py
    ...


def _generate_document_table(docs: Dict[str, DocumentData]) -> str:
    """Generate document listing table."""
    # Implementation extracted from ontos_generate_context_map.py
    ...


def _generate_dependency_tree(docs: Dict[str, DocumentData]) -> str:
    """Generate dependency tree visualization."""
    # Implementation extracted from ontos_generate_context_map.py
    ...


def _generate_timeline(docs: Dict[str, DocumentData]) -> str:
    """Generate activity timeline."""
    # Implementation extracted from ontos_generate_context_map.py
    ...


def _generate_staleness_audit(docs: Dict[str, DocumentData]) -> str:
    """Generate staleness audit section."""
    # Implementation extracted from ontos_generate_context_map.py
    ...
```

**Dependencies:** `core/context`, `core/validation`, `core/tokens`, `core/types`, `io/files`, `io/yaml`, `ui/output`

**Size Target:** ~200 lines

**Tests Required:**
- [ ] `test_generate_context_map_empty` — Handles empty docs
- [ ] `test_generate_context_map_with_docs` — Generates valid content
- [ ] `test_generate_context_map_strict_fails` — Fails on errors in strict mode

---

### 4.11 `ontos/commands/log.py` — NEW

**Purpose:** Orchestrate session log creation using extracted core/io modules.

**Source:** `ontos/_scripts/ontos_end_session.py` orchestration logic (lines 1608-1904)

```python
"""
Session log creation command.

Orchestrates the creation of session logs using
extracted core and io modules.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any

from ontos.core.context import SessionContext
from ontos.core.suggestions import suggest_impacts, load_document_index, load_common_concepts, validate_concepts
from ontos.core.types import TEMPLATES
from ontos.ui.output import OutputHandler


@dataclass
class EndSessionOptions:
    """Configuration options for session log creation."""
    event_type: str = "chore"
    topic: Optional[str] = None
    auto_mode: bool = False
    skip_impacts: bool = False
    skip_concepts: bool = False


def end_session(
    ctx: SessionContext,
    output: OutputHandler,
    options: EndSessionOptions = None
) -> Path:
    """Create a session log file.

    Args:
        ctx: Session context with project configuration
        output: Output handler for user feedback
        options: Session options

    Returns:
        Path to created log file
    """
    options = options or EndSessionOptions()

    # 1. Get git information
    from ontos.io.git import get_current_branch, get_commits_since_push, get_changed_files_since_push

    branch = get_current_branch()
    if not branch:
        raise ValueError("Not in a git repository or no branch checked out")

    commits = get_commits_since_push()
    changed_files = get_changed_files_since_push()

    output.info(f"Branch: {branch}")
    output.info(f"Commits since push: {len(commits)}")

    # 2. Load context map for suggestions
    context_map_path = ctx.project_root / ctx.config.get("paths", {}).get("context_map", "Ontos_Context_Map.md")
    if context_map_path.exists():
        context_map_content = context_map_path.read_text()
        doc_index = load_document_index(context_map_content)
        common_concepts = load_common_concepts(context_map_content)
    else:
        doc_index = {}
        common_concepts = set()

    # 3. Suggest impacts
    if not options.skip_impacts:
        suggested_impacts = suggest_impacts(changed_files, doc_index, commits)
        output.info(f"Suggested impacts: {', '.join(suggested_impacts) or 'none'}")
    else:
        suggested_impacts = []

    # 4. Generate log content
    template = TEMPLATES.get(options.event_type, TEMPLATES["chore"])
    log_content = _generate_log_content(
        branch=branch,
        event_type=options.event_type,
        topic=options.topic,
        template=template,
        commits=commits,
        impacts=suggested_impacts,
    )

    # 5. Write log file
    from ontos.io.files import write_text_file
    from datetime import date

    logs_dir = ctx.project_root / ctx.config.get("paths", {}).get("logs_dir", "docs/logs")
    today = date.today().isoformat()
    slug = options.topic or _generate_slug(commits)
    log_path = logs_dir / f"{today}_{slug}.md"

    write_text_file(log_path, log_content)
    output.success(f"Created log: {log_path}")

    return log_path


def _generate_log_content(
    branch: str,
    event_type: str,
    topic: Optional[str],
    template: str,
    commits: List[str],
    impacts: List[str],
) -> str:
    """Generate log file content."""
    # Implementation extracted from ontos_end_session.py
    ...


def _generate_slug(commits: List[str]) -> str:
    """Generate topic slug from commits."""
    # Implementation extracted from ontos_end_session.py
    ...
```

**Dependencies:** `core/context`, `core/suggestions`, `core/types`, `io/git`, `io/files`, `ui/output`

**Size Target:** ~250 lines

**Tests Required:**
- [ ] `test_end_session_creates_log` — Creates log file
- [ ] `test_end_session_suggests_impacts` — Suggests impacts correctly
- [ ] `test_end_session_auto_mode` — Works in auto mode

---

## 5. Migration Tasks

### 5.1 Task Sequence

**Day 1: Foundation (No Dependencies)**

| Task | Module | Dependencies | Test Command |
|------|--------|--------------|--------------|
| 1.1 | `core/types.py` | None (re-export only) | `pytest tests/core/test_types.py` |
| 1.2 | `core/tokens.py` | None | `pytest tests/core/test_tokens.py` |
| 1.3 | `io/__init__.py` | None | Import check |
| 1.4 | `io/yaml.py` | PyYAML | `pytest tests/io/test_yaml.py` |

**Day 2: I/O Layer**

| Task | Module | Dependencies | Test Command |
|------|--------|--------------|--------------|
| 2.1 | `io/git.py` | None | `pytest tests/io/test_git.py` |
| 2.2 | `io/files.py` | `core/types` | `pytest tests/io/test_files.py` |
| 2.3 | `io/toml.py` | tomli | `pytest tests/io/test_toml.py` |

**Day 3: Core Graph**

| Task | Module | Dependencies | Test Command |
|------|--------|--------------|--------------|
| 3.1 | `core/graph.py` | `core/types.py` | `pytest tests/core/test_graph.py` |
| 3.2 | `core/suggestions.py` | None | `pytest tests/core/test_suggestions.py` |

**Day 4: Validation and Architecture Fixes**

| Task | Module | Dependencies | Test Command |
|------|--------|--------------|--------------|
| 4.1 | `core/validation.py` | `types.py`, `graph.py` | `pytest tests/core/test_validation.py` |
| 4.2 | Update `core/__init__.py` | All new modules | Import check |
| 4.3 | Fix `core/frontmatter.py` | Remove PyYAML, use `io/yaml.py` | Unit tests |
| 4.4 | Refactor `core/staleness.py` | Remove subprocess, use `io/git.py` | `pytest tests/core/test_staleness.py` |
| 4.5 | Refactor `core/config.py` | Remove subprocess, use `io/git.py` | `pytest tests/core/test_config.py` |

**Day 5: Command Modules**

| Task | Module | Dependencies | Test Command |
|------|--------|--------------|--------------|
| 5.1 | `commands/map.py` | core/*, io/* | `pytest tests/commands/test_map.py` |
| 5.2 | `commands/log.py` | core/*, io/* | `pytest tests/commands/test_log.py` |
| 5.3 | Update `commands/__init__.py` | New commands | Import check |

**Day 6: God Script Refactoring**

| Task | Description | Verification |
|------|-------------|--------------|
| 6.1 | Update `ontos_generate_context_map.py` imports | Imports compile |
| 6.2 | Remove extracted functions from script | Script < 200 lines |
| 6.3 | Replace inline code with `commands/map.py` calls | Golden Master passes |
| 6.4 | Update `ontos_end_session.py` imports | Imports compile |
| 6.5 | Remove extracted functions from script | Script < 200 lines |
| 6.6 | Replace inline code with `commands/log.py` calls | Golden Master passes |

**Day 7: Minor Command Migration**

| Task | Source Script | Target | Test Command |
|------|--------------|--------|--------------|
| 7.1 | `ontos_verify.py` (315 lines) | `commands/verify.py` | Golden Master |
| 7.2 | `ontos_query.py` (326 lines) | `commands/query.py` | Golden Master |
| 7.3 | `ontos_migrate_schema.py` (337 lines) | `commands/migrate.py` | Golden Master |
| 7.4 | `ontos_consolidate.py` (465 lines) | `commands/consolidate.py` | Golden Master |

**Day 8: Remaining Commands**

| Task | Source Script | Target | Test Command |
|------|--------------|--------|--------------|
| 8.1 | `ontos_promote.py` (453 lines) | `commands/promote.py` | Golden Master |
| 8.2 | `ontos_scaffold.py` (274 lines) | `commands/scaffold.py` | Golden Master |
| 8.3 | `ontos_stub.py` (279 lines) | `commands/stub.py` | Golden Master |

**Day 9: Final Integration**

| Task | Description | Test Command |
|------|-------------|--------------|
| 9.1 | Update `io/__init__.py` exports | Import check |
| 9.2 | Run full Golden Master suite | `python tests/golden/compare_golden_master.py --all` |
| 9.3 | Run all unit tests | `pytest tests/ -v` |
| 9.4 | Run circular import test | `pytest tests/test_circular_imports.py` |

### 5.2 Dependency Graph

```
types.py (re-exports CurationLevel only)
    │
    ├──► tokens.py (no deps)
    │
    ├──► graph.py
    │       │
    │       ▼
    │   validation.py
    │
    └──► suggestions.py (no deps)

yaml.py (PyYAML)
    │
git.py (no deps)
    │
files.py (core/types)
    │
toml.py (tomli)

[All core + io modules]
    │
    ├──► commands/map.py
    │
    └──► commands/log.py

[All modules]
    │
    ▼
God Script refactoring (< 200 lines each)
    │
    ▼
Minor command migration
    │
    ▼
Integration testing
```

### 5.3 Architecture Enforcement

**Strategy:**
1. **`types.py` MUST have zero new internal imports** (only re-exports from existing modules)
2. **Import order within all ontos modules:**
   ```python
   # Correct order for any ontos module:
   from __future__ import annotations  # FIRST - enables forward refs
   # stdlib imports
   # third-party imports
   # ontos.core.types imports (always safe)
   # other ontos imports (if needed)
   ```
3. **CI test to prevent circular import regressions:**
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
           "ontos.commands.map",
           "ontos.commands.log",
       ]
       for mod in modules:
           importlib.import_module(mod)  # Should not raise ImportError
   ```
4. **CI pipeline import check:**
   ```bash
   python -c "import ontos; import ontos.core; import ontos.io; import ontos.commands"
   ```
5. **CI architecture constraint check (no subprocess in core/):**
   ```bash
   # tests/test_architecture.py or CI script
   if grep -r "import subprocess" ontos/core/; then
       echo "ERROR: subprocess import found in core/ — violates architecture"
       exit 1
   fi
   ```
   This check ensures the `core/` layer remains subprocess-free after Phase 2 refactoring.

---

## 6. Verification Protocol

### 6.1 After Each Module Extraction

```bash
# 1. Run module-specific tests
pytest tests/core/test_[module].py -v

# 2. Check for import errors
python -c "from ontos.core.[module] import *"

# 3. Verify no circular imports
python -c "import ontos; import ontos.core; import ontos.io"

# 4. Run Golden Master (if touching God Scripts)
python tests/golden/compare_golden_master.py
```

### 6.2 Final Verification

```bash
# Full test suite
pytest tests/ -v --cov=ontos --cov-report=term-missing

# Golden Master (all fixtures)
python tests/golden/compare_golden_master.py --all

# Import check
python -c "from ontos import *; from ontos.core import *; from ontos.io import *; from ontos.commands import *"

# Circular import test
pytest tests/test_circular_imports.py -v

# CLI still works
python -m ontos._scripts.ontos --version
python -m ontos._scripts.ontos map --help
```

### 6.3 Test File Structure

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
├── golden/                  # Existing Golden Master tests
└── test_circular_imports.py # CI: circular import prevention
```

---

## 7. Acceptance Criteria

- [ ] **11 new modules created** with specified interfaces (5 core + 4 io + 2 commands)
- [ ] **9 minor commands migrated** to `commands/` package (7 original + map + log)
- [ ] **God Scripts < 200 lines each** (argparse + deprecation only)
- [ ] **Pre-existing PyYAML violation fixed** in `core/frontmatter.py`
- [ ] **303+ existing tests pass**
- [ ] **16/16 Golden Master tests pass** (exact behavior match)
- [ ] **No circular imports** (CI test passes)
- [ ] **Architecture enforced**: `core/` modules don't import from `io/` or `commands/`
- [ ] **Type normalization** happens at io/core boundary in `io/files.py`
- [ ] **Tag `v3.0.0-beta`** when complete

---

## 8. Implementation Notes

### 8.1 Extraction Strategy

For each extraction:
1. **Copy** code to new module (don't delete from source yet)
2. **Add imports** in God Script to new module
3. **Comment out** old code in God Script (keep for reference)
4. **Run tests** — verify behavior unchanged
5. **Delete** commented code after Golden Master passes
6. **Verify** God Script < 200 lines after all extractions

### 8.2 Import Conventions

```python
# God Scripts should import from public APIs:
from ontos.core.graph import build_graph, detect_cycles
from ontos.core.validation import ValidationOrchestrator
from ontos.io.git import get_current_branch
from ontos.commands.map import generate_context_map

# NOT internal modules:
# from ontos.core.graph import _internal_helper  # Wrong
```

### 8.3 Architecture Constraints (Enforced)

Per Technical Architecture v1.4:
- `core/` modules MUST NOT import from `io/` (except `core/types` re-exports)
- `core/` modules MUST NOT call subprocess directly
- `core/` modules MUST NOT call `print()`
- `core/` modules MUST NOT import PyYAML directly (use `io/yaml.py`)
- `io/` modules MAY import from `core/types` only
- Commands MAY import from both `core/` and `io/`

**Architecture Constraints Table:**
| Layer | May Import From | Must Not Import From |
|-------|-----------------|---------------------|
| `core/` | stdlib, `core/types` | `io/`, `commands/`, subprocess, PyYAML |
| `io/` | stdlib, `core/types`, third-party | `commands/` |
| `commands/` | All layers | — |

---

## 9. Deliverables Summary

### 9.1 Phase 2 Deliverables (Final)

| Module | Status | Lines (Est.) |
|--------|--------|--------------|
| `core/types.py` | NEW | ~120 |
| `core/tokens.py` | NEW | ~30 |
| `core/graph.py` | NEW | ~150 |
| `core/suggestions.py` | NEW | ~120 |
| `core/validation.py` | NEW | ~220 |
| `io/git.py` | NEW | ~100 |
| `io/files.py` | NEW | ~100 |
| `io/toml.py` | NEW | ~60 |
| `io/yaml.py` | NEW | ~30 |
| `commands/map.py` | NEW | ~200 |
| `commands/log.py` | NEW | ~250 |
| 7 minor commands | MIGRATED | ~2,400 |
| `ontos_end_session.py` | REFACTORED | <200 |
| `ontos_generate_context_map.py` | REFACTORED | <200 |
| `core/frontmatter.py` | MODIFIED | ~100 |

**Total New Code:** ~1,380 lines in new modules
**Total Migrated:** ~2,400 lines from minor scripts
**Net God Script Reduction:** ~2,800 lines removed

---

*End of Phase 2 Implementation Spec v1.1*
