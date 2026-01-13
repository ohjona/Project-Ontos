# Ontos v3.0.1: Implementation Prompt for Antigravity

**Author:** Chief Architect (Claude Opus 4.5)
**Date:** 2026-01-13
**Spec Version:** 1.1
**Target:** Antigravity (Developer)

---

## Current State Verification

Before writing this prompt, I verified:

| Check | Result |
|-------|--------|
| On main branch | `phase4-full-cli` (PR #44 merged to main expected) |
| v3.0.0 tagged | Verify with `git tag` |
| Tests pass | Run `pytest tests/ -v` |
| Current version | pyproject.toml: 3.0.0a1, __init__.py: 3.0.0b1 (MISMATCH - to fix) |
| Golden baselines | `tests/golden/baselines/` (shows FutureWarning for ontos_lib) |

---

## Overview

Phase 5 is a patch release focused on polish, documentation, and technical debt cleanup.

**Target Version:** v3.0.1
**Total Tasks:** 9 (7 Must + 2 Should)
**Estimated Complexity:** Medium (due to P5-2 full migration)

---

## Pre-Implementation Checklist

```bash
git checkout main
git pull origin main
git checkout -b phase5-polish

# Verify current state
pytest tests/ -v
pytest tests/golden/ -v
ontos --version
```

---

## Architecture Constraints

| Layer | Cannot Import From |
|-------|-------------------|
| `ontos/core/` | `ontos/io/`, `ontos/ui/` |
| `ontos/ui/` | `ontos/io/` |
| `ontos/commands/` | (can import all) |

**Verify before committing:**
```bash
grep -rn "from ontos.io" ontos/core/ | grep -v "^#" | grep -v '"""'
# Should return nothing (docstrings are OK)
```

---

## Task Sequence

### Task 5.0: Version Sync (PREREQUISITE)

**Issue:** Version mismatch between pyproject.toml (3.0.0a1) and __init__.py (3.0.0b1)

**Files to Modify:**
- `pyproject.toml` line 7
- `ontos/__init__.py` line 10

**Changes:**
```python
# pyproject.toml line 7
version = "3.0.1"

# ontos/__init__.py line 10
__version__ = "3.0.1"
```

**Verification:**
```bash
python -c "import ontos; print(ontos.__version__)"  # Should print 3.0.1
grep 'version = ' pyproject.toml  # Should show 3.0.1
```

**Commit:**
```bash
git add pyproject.toml ontos/__init__.py
git commit -m "chore: sync version to 3.0.1 for Phase 5 release"
```

---

### Task 5.1: Update Docstrings in core/ (P5-1)

**Issue:** Docstrings show `from ontos.io` examples, which misleads about architecture

**Status:** Functions already use DI. Only docstrings need updating.

**Files to Modify:**
1. `ontos/core/config.py` - lines 9, 177, 227
2. `ontos/core/staleness.py` - lines 16, 58, 334
3. `ontos/core/frontmatter.py` - lines 13, 32

**Pattern - BEFORE:**
```python
"""
For production use with git:
    from ontos.io.git import get_git_config
    source = get_source(git_username_provider=lambda: get_git_config("user.name"))
"""
```

**Pattern - AFTER:**
```python
"""
For production use:
    source = get_source(git_username_provider=my_git_provider)

The caller (commands layer) provides the IO callback.
"""
```

**Specific Changes:**

1. **`ontos/core/config.py`**
   - Line 9: Remove example import, describe DI pattern
   - Line 177: Update docstring to not show io import
   - Line 227: Update docstring to not show io import

2. **`ontos/core/staleness.py`**
   - Line 16: Update module docstring
   - Line 58: Update function docstring
   - Line 334: Update function docstring

3. **`ontos/core/frontmatter.py`**
   - Line 13: Update module docstring
   - Line 32: Update function docstring

**Verification:**
```bash
# Docstrings should NOT show io imports
grep -n "from ontos.io" ontos/core/*.py
# Should only return lines that are inside docstrings (verify manually)

pytest tests/core/ -v
```

**Commit:**
```bash
git add ontos/core/config.py ontos/core/staleness.py ontos/core/frontmatter.py
git commit -m "docs(core): update docstrings to show DI pattern, not io imports

Clarifies architecture: core/ functions receive IO callbacks from callers.
Closes P5-1."
```

---

### Task 5.2: Full Migration from ontos_lib (P5-2)

**Issue:** Remove deprecated `ontos_lib.py` shim, but 15+ files still import from it

**Strategy:** Migrate all imports, then delete

#### Step 2.1: Migrate `ontos_init.py`

**File:** `ontos_init.py`
**Lines:** 237, 270, 298

**BEFORE:**
```python
from ontos_lib import resolve_config
```

**AFTER:**
```python
from ontos.core.paths import resolve_config
```

#### Step 2.2: Migrate `ontos/_scripts/` files

**Files to update:**
| File | Import Line | Change to |
|------|-------------|-----------|
| `ontos_maintain.py` | 11, 204 | `from ontos.core.proposals import find_draft_proposals`<br>`from ontos.core.paths import get_proposals_dir, get_decision_history_path, resolve_config` |
| `ontos_pre_commit_check.py` | 16 | `from ontos.core.* import ...` (map each import) |
| `ontos_pre_push_check.py` | 25 | `from ontos.core.paths import resolve_config` |
| `ontos_verify.py` | 22 | Map all imports to ontos.core equivalents |
| `ontos_query.py` | 12 | Map all imports to ontos.core equivalents |
| `ontos_consolidate.py` | 14 | `from ontos.core.frontmatter import parse_frontmatter`<br>`from ontos.core.paths import find_last_session_date` |

**Import Mapping Reference:**
```python
# OLD → NEW
from ontos_lib import parse_frontmatter → from ontos.core.frontmatter import parse_frontmatter
from ontos_lib import resolve_config → from ontos.core.paths import resolve_config
from ontos_lib import find_draft_proposals → from ontos.core.proposals import find_draft_proposals
from ontos_lib import get_proposals_dir → from ontos.core.paths import get_proposals_dir
from ontos_lib import get_decision_history_path → from ontos.core.paths import get_decision_history_path
from ontos_lib import find_last_session_date → from ontos.core.paths import find_last_session_date
from ontos_lib import SessionContext → from ontos.core.context import SessionContext
from ontos_lib import validate_describes_field → from ontos.core.staleness import validate_describes_field
from ontos_lib import check_staleness → from ontos.core.staleness import check_staleness
from ontos_lib import generate_decision_history → from ontos.core.history import generate_decision_history
from ontos_lib import BLOCKED_BRANCH_NAMES → from ontos.core.config import BLOCKED_BRANCH_NAMES
from ontos_lib import get_source → from ontos.core.config import get_source
from ontos_lib import get_logs_dir → from ontos.core.paths import get_logs_dir
from ontos_lib import get_log_count → from ontos.core.paths import get_log_count
from ontos_lib import get_logs_older_than → from ontos.core.paths import get_logs_older_than
from ontos_lib import get_archive_dir → from ontos.core.paths import get_archive_dir
from ontos_lib import load_decision_history_entries → from ontos.core.proposals import load_decision_history_entries
from ontos_lib import get_git_last_modified → from ontos.core.config import get_git_last_modified
```

#### Step 2.3: Migrate `.ontos/scripts/` files (installed hooks)

Same mapping as above for:
- `.ontos/scripts/ontos_generate_context_map.py`
- `.ontos/scripts/ontos_end_session.py`
- `.ontos/scripts/ontos_maintain.py`
- `.ontos/scripts/ontos_query.py`
- `.ontos/scripts/ontos_verify.py`
- `.ontos/scripts/ontos_pre_commit_check.py`
- `.ontos/scripts/ontos_pre_push_check.py`
- `.ontos/scripts/ontos_consolidate.py`

#### Step 2.4: Update Tests

**Files:**
- `tests/test_session_context.py` - lines 110-150 (shim tests)
- `tests/test_config.py` - lines 38-72
- `tests/test_immutable_history.py` - line 21
- `tests/test_describes.py` - line 21
- `tests/test_validation.py` - line 27
- `tests/test_pre_commit_check.py` - lines 163-190

**For shim tests:** Either delete them (shim is being removed) or convert to test new import paths.

#### Step 2.5: Update Golden Master Baselines

**Files:**
- `tests/golden/baselines/small/map_stderr.txt`
- `tests/golden/baselines/small/log_stderr.txt`
- `tests/golden/baselines/medium/map_stderr.txt`
- `tests/golden/baselines/medium/log_stderr.txt`

These currently show `FutureWarning: from ontos_lib import`. After migration, this warning should disappear. **Regenerate baselines after migration.**

```bash
# After all migrations complete:
cd tests/golden
python compare_golden_master.py --update
```

#### Step 2.6: Delete Legacy Files

**Pre-deletion verification (B1 Mitigation):**
```bash
grep -r 'from ontos_lib\|import ontos_lib' . --include='*.py' | grep -v 'archive/' | grep -v '.bak'
# Must return 0 matches
```

**Delete:**
```bash
rm .ontos/scripts/ontos_lib.py
rm ontos/_scripts/ontos_lib.py  # if exists
rm install.py
```

**Verification:**
```bash
pytest tests/ -v
pytest tests/golden/ -v
# All should pass without FutureWarning about ontos_lib
```

**Commits (atomic):**
```bash
git add ontos_init.py ontos/_scripts/*.py
git commit -m "refactor: migrate ontos_init and _scripts from ontos_lib to ontos.core"

git add .ontos/scripts/*.py
git commit -m "refactor: migrate .ontos/scripts from ontos_lib to ontos.core"

git add tests/*.py tests/golden/baselines/
git commit -m "test: update tests and baselines for ontos_lib removal"

git rm .ontos/scripts/ontos_lib.py install.py
git commit -m "chore: remove deprecated ontos_lib.py and install.py

BREAKING for anyone using ontos_lib directly (deprecated since v2.9.2).
Closes P5-2."
```

---

### Task 5.3: Lenient Hook Detection (P5-3)

**Issue:** `ontos doctor` warns "Non-Ontos hooks" even for Ontos-managed hooks that lack the marker

**File:** `ontos/commands/doctor.py`
**Lines:** 140-156

**Current Code:**
```python
# Check if hooks are Ontos-managed
ontos_marker = "# ontos-managed-hook"
non_ontos = []

for hook_path in [pre_push, pre_commit]:
    if hook_path.exists():
        content = hook_path.read_text()
        if ontos_marker not in content:
            non_ontos.append(hook_path.name)
```

**New Code:**
```python
def _is_ontos_hook_lenient(hook_path: Path) -> bool:
    """Check if hook is Ontos-managed (heuristic for reporting only).

    Uses lenient matching for doctor reporting. The strict marker check
    remains in init.py for overwrite decisions.
    """
    try:
        content = hook_path.read_text()
        return (
            "# ontos-managed-hook" in content or
            "ontos hook" in content or
            "python3 -m ontos" in content
        )
    except Exception:
        return False  # Binary or unreadable - treat as non-Ontos

# Check if hooks are Ontos-managed (lenient for reporting)
non_ontos = []

for hook_path in [pre_push, pre_commit]:
    if hook_path.exists():
        if not _is_ontos_hook_lenient(hook_path):
            non_ontos.append(hook_path.name)
```

**Add helper function at line ~79 (before `check_git_hooks`):**
```python
def _is_ontos_hook_lenient(hook_path: Path) -> bool:
    """Check if hook is Ontos-managed (heuristic for reporting only)."""
    try:
        content = hook_path.read_text()
        return (
            "# ontos-managed-hook" in content or
            "ontos hook" in content or
            "python3 -m ontos" in content
        )
    except Exception:
        return False
```

**New Tests (B2 Mitigation):**

Create/update `tests/commands/test_doctor_hooks.py`:
```python
"""Tests for lenient hook detection in doctor command."""
import pytest
from pathlib import Path
from unittest.mock import patch
from ontos.commands.doctor import _is_ontos_hook_lenient

class TestLenientHookDetection:
    """Test cases for is_ontos_hook_lenient function."""

    def test_detects_marker(self, tmp_path):
        """Hook with marker should be detected."""
        hook = tmp_path / "pre-push"
        hook.write_text("#!/bin/bash\n# ontos-managed-hook\nontos hook pre-push")
        assert _is_ontos_hook_lenient(hook) is True

    def test_detects_ontos_hook_substring(self, tmp_path):
        """Hook with 'ontos hook' should be detected."""
        hook = tmp_path / "pre-push"
        hook.write_text("#!/bin/bash\nontos hook pre-push")
        assert _is_ontos_hook_lenient(hook) is True

    def test_detects_python_m_ontos(self, tmp_path):
        """Hook with 'python3 -m ontos' should be detected."""
        hook = tmp_path / "pre-commit"
        hook.write_text("#!/bin/bash\npython3 -m ontos hook pre-commit")
        assert _is_ontos_hook_lenient(hook) is True

    def test_foreign_hook_husky(self, tmp_path):
        """Husky hook should NOT be detected as Ontos."""
        hook = tmp_path / "pre-commit"
        hook.write_text('#!/bin/sh\n. "$(dirname "$0")/_/husky.sh"\nnpx lint-staged')
        assert _is_ontos_hook_lenient(hook) is False

    def test_foreign_hook_precommit(self, tmp_path):
        """pre-commit framework hook should NOT be detected as Ontos."""
        hook = tmp_path / "pre-commit"
        hook.write_text('#!/usr/bin/env bash\nexec pre-commit "$@"')
        assert _is_ontos_hook_lenient(hook) is False

    def test_empty_hook(self, tmp_path):
        """Empty hook should NOT be detected as Ontos."""
        hook = tmp_path / "pre-push"
        hook.write_text("")
        assert _is_ontos_hook_lenient(hook) is False

    def test_binary_hook_graceful(self, tmp_path):
        """Binary hook should be handled gracefully (no crash)."""
        hook = tmp_path / "pre-push"
        hook.write_bytes(b'\x00\x01\x02\x03')  # Binary content
        # Should not crash, should return False
        assert _is_ontos_hook_lenient(hook) is False

    def test_unreadable_hook(self, tmp_path):
        """Unreadable hook should be handled gracefully."""
        hook = tmp_path / "pre-push"
        hook.write_text("content")
        hook.chmod(0o000)  # Remove read permission
        try:
            assert _is_ontos_hook_lenient(hook) is False
        finally:
            hook.chmod(0o644)  # Restore for cleanup
```

**Verification:**
```bash
pytest tests/commands/test_doctor_hooks.py -v
pytest tests/commands/test_doctor_phase4.py -v
ontos doctor  # Should not warn about Ontos hooks
```

**Commit:**
```bash
git add ontos/commands/doctor.py tests/commands/test_doctor_hooks.py
git commit -m "fix(doctor): use lenient heuristics for hook detection

- Add _is_ontos_hook_lenient() for reporting (doctor only)
- init.py still uses strict marker check for overwrites
- Add negative test cases for foreign hooks

Closes P5-3."
```

---

### Task 5.4: Add Frontmatter to Context Map (P5-4)

**Issue:** Context map lacks YAML frontmatter, so Ontos can't "read itself"

**Note:** This requires updating the map generation code, not just the current file.

**File to investigate:** Find where context map is generated (likely `ontos/commands/map.py` or similar)

**Golden Master Requirement (B3 Mitigation):**
After implementing, regenerate golden baselines:
```bash
cd tests/golden
python compare_golden_master.py --update
```

**Frontmatter to add:**
```yaml
---
id: ontos_context_map
type: reference
status: generated
generated_by: ontos map
generated_at: <timestamp>
---
```

**Commit:**
```bash
git add ontos/commands/map.py tests/golden/baselines/
git commit -m "feat(map): add frontmatter to generated context map

Context map now includes YAML frontmatter for Ontos self-reference.
Golden baselines updated.

Closes P5-4."
```

---

### Task 5.5: Update README.md (P5-5)

**File:** `README.md`

**Updates needed:**
1. Change install instructions from `curl install.py` to `pip install ontos`
2. Update version references to v3.0.1
3. Add PyPI badge
4. Update CLI examples for v3.0 commands

**Commit:**
```bash
git add README.md
git commit -m "docs: update README for v3.0.1 release

- Installation via pip install ontos
- Updated CLI examples
- Added PyPI badge"
```

---

### Task 5.6: Create Migration Guide (P5-6)

**File:** `docs/reference/Migration_v2_to_v3.md`

**Content outline:**
1. What changed in v3.0
2. Installation changes (pip vs install.py)
3. CLI changes (new unified CLI)
4. Import changes (ontos_lib deprecated)
5. Configuration changes (.ontos.toml)

**Commit:**
```bash
git add docs/reference/Migration_v2_to_v3.md
git commit -m "docs: add migration guide from v2.x to v3.0"
```

---

### Task 5.7: Update Ontos_Manual.md (P5-7)

**File:** `docs/reference/Ontos_Manual.md`

**Updates:**
1. Update header from "v2.9" to "v3.0"
2. Expand Section 10 (Unified CLI) with full command reference
3. Update installation section for pip
4. Remove references to deprecated ontos_lib

**Commit:**
```bash
git add docs/reference/Ontos_Manual.md
git commit -m "docs: update manual for v3.0.1"
```

---

### Task 5.8: Release Verification (P5-8)

**Pre-release checks:**

```bash
# 1. Version matches
ontos --version  # Should show 3.0.1
grep 'version = ' pyproject.toml  # Should show 3.0.1
python -c "import ontos; print(ontos.__version__)"  # Should show 3.0.1

# 2. URLs in pyproject.toml are valid
curl -I https://github.com/ohjona/Project-Ontos  # Should return 200

# 3. Full test suite
pytest tests/ -v --tb=short
pytest tests/golden/ -v

# 4. All commands work
ontos --help
ontos init --help
ontos map --help
ontos doctor
ontos log --help

# 5. Build works
pip install build
python -m build
```

**PyPI publication steps:**
```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Verify test install
pip install --index-url https://test.pypi.org/simple/ ontos

# Production PyPI
twine upload dist/*
```

---

### Task 5.9: Performance Verification (P5-9)

**Target:** `ontos map` completes in <500ms for typical repo

```bash
# Time the map command
time ontos map --quiet

# Should be under 500ms for repos with <100 documents
```

---

## Final Verification

After ALL tasks complete:

```bash
# 1. Full test suite
pytest tests/ -v --tb=short

# 2. Golden Master
pytest tests/golden/ -v

# 3. All commands work
ontos --version  # 3.0.1
ontos --help
ontos init --help
ontos map --help
ontos doctor
ontos log --help

# 4. Architecture check
grep -rn "from ontos.io" ontos/core/ | grep -v '"""'  # Empty except docstrings
grep -rn "from ontos_lib" . --include='*.py' | grep -v 'archive/'  # Empty

# 5. No FutureWarning
python -c "import ontos"  # No deprecation warning
```

---

## PR Preparation

### PR Title
```
fix: Phase 5 — Polish & Fixes (v3.0.1)
```

### PR Description Template
```markdown
## Summary

Phase 5 patch release: technical debt cleanup, UX improvements, documentation updates.

**Spec:** Phase5-Implementation-Spec.md v1.1

## Changes

### Technical Debt
- P5-1: Updated docstrings to show DI pattern (arch violation was already fixed)
- P5-2: Full migration from ontos_lib to ontos.core, removed deprecated shim

### UX Improvements
- P5-3: Lenient hook detection in doctor command
- P5-4: Added frontmatter to context map

### Documentation
- P5-5: Updated README for v3.0.1
- P5-6: Added migration guide (v2 to v3)
- P5-7: Updated Ontos Manual

### Release
- Version synced to 3.0.1
- Verified performance targets

## Testing

- [ ] All unit tests pass
- [ ] Golden Master passes
- [ ] Manual testing complete
- [ ] No regressions
- [ ] Architecture constraints verified

## Checklist

- [ ] Follows spec v1.1
- [ ] One commit per logical change
- [ ] Backward compatible (except ontos_lib removal, deprecated since v2.9.2)
```

---

## Commit History (Expected)

| # | Commit Message |
|---|----------------|
| 1 | `chore: sync version to 3.0.1` |
| 2 | `docs(core): update docstrings to show DI pattern` |
| 3 | `refactor: migrate ontos_init and _scripts from ontos_lib` |
| 4 | `refactor: migrate .ontos/scripts from ontos_lib` |
| 5 | `test: update tests and baselines for ontos_lib removal` |
| 6 | `chore: remove deprecated ontos_lib.py and install.py` |
| 7 | `fix(doctor): use lenient heuristics for hook detection` |
| 8 | `feat(map): add frontmatter to generated context map` |
| 9 | `docs: update README for v3.0.1` |
| 10 | `docs: add migration guide from v2.x to v3.0` |
| 11 | `docs: update manual for v3.0.1` |

---

## Common Mistakes to Avoid

1. **Forgetting to migrate a file** — Run grep scan before deleting ontos_lib
2. **Breaking golden baselines** — Regenerate after any output format change
3. **Architecture violations in docstrings** — These still matter for documentation
4. **Bundling migrations in one commit** — Keep atomic (scripts vs tests vs delete)
5. **Version mismatch** — Sync pyproject.toml and __init__.py before any other changes

---

## If You Get Stuck

1. **Import not found:** Check the mapping table in Task 5.2
2. **Test fails after migration:** Ensure you updated all import statements in that file
3. **Golden Master fails:** Regenerate baselines with `--update` flag
4. **Unclear scope:** Check spec v1.1 — if not in spec, don't do it

---

**Implementation prompt signed by:**
- **Role:** Chief Architect
- **Model:** Claude Opus 4.5
- **Date:** 2026-01-13
- **Phase:** 5 — Polish & Fixes
