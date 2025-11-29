# Project Ontos - Comprehensive Review & Suggestions

**Review Date:** 2025-11-29
**Reviewer:** Claude (Opus 4)
**Repository:** Project-Ontos
**Purpose:** This document contains actionable recommendations for improving Project Ontos. It is formatted for LLM consumption to enable review and implementation.

---

## Project Context

**What is Project Ontos?**

Project Ontos is a lightweight, AI-agent-native protocol that converts documentation folders into structured Knowledge Graphs. It helps AI agents (Cursor, Claude, Gemini, etc.) navigate projects intelligently by providing deterministic context mapping through metadata-enhanced markdown files.

**Core Components:**

| Component | Path | Purpose |
|-----------|------|---------|
| `generate_context_map.py` | `scripts/generate_context_map.py` | Builds knowledge graph, runs 5 integrity checks |
| `migrate_frontmatter.py` | `scripts/migrate_frontmatter.py` | Scans for untagged markdown files |
| `end_session.py` | `scripts/end_session.py` | Creates session log files for archival |
| `CONTEXT_MAP.md` | Root directory | Auto-generated knowledge graph (disposable artifact) |
| `Ontos_Manual.md` | Root directory | Protocol specification (v0.3) |
| `Ontos_Agent_Instructions.md` | Root directory | System prompt for AI agents |

**YAML Frontmatter Schema:**

```yaml
---
id: unique_slug_name          # REQUIRED - stable identifier, never change
type: kernel|strategy|product|atom  # REQUIRED - hierarchical document type
status: draft|active|deprecated     # OPTIONAL - document state
owner: null                   # OPTIONAL - responsible role
depends_on: [id1, id2]        # OPTIONAL - list of dependency IDs
---
```

**Type Hierarchy (Rank 0-3):**
- `kernel` (0): Foundational principles (mission, values)
- `strategy` (1): Business decisions (goals, roadmap)
- `product` (2): User-facing specs (features, journeys)
- `atom` (3): Technical details (API, schemas)

**Dependency Rule:** Dependencies flow DOWN the hierarchy. Higher-ranked documents can depend on lower-ranked documents. Violations are flagged as architectural errors.

---

## Recommendations

### Priority Legend

- 🔴 **HIGH**: Bugs or broken functionality that should be fixed immediately
- 🟡 **MEDIUM**: Improvements that enhance reliability or developer experience
- 🟢 **LOW**: Nice-to-have enhancements for future iterations

---

## 🔴 HIGH PRIORITY (Bugs & Critical Fixes)

### 1. Fix Broken Link in Agent Instructions

**File:** `Ontos_Agent_Instructions.md`
**Line:** 27
**Issue:** Reference to non-existent file

**Current Code:**
```markdown
For full definitions, see [The Manual](20251124_Project%20Ontos%20The%20Manual.md).
```

**Required Fix:**
```markdown
For full definitions, see [The Manual](Ontos_Manual.md).
```

**Implementation Steps:**
1. Open `Ontos_Agent_Instructions.md`
2. Find line 27 containing the broken link
3. Replace the old filename with `Ontos_Manual.md`
4. Save the file

---

### 2. Exclude Log Files from Orphan Detection

**File:** `scripts/generate_context_map.py`
**Lines:** 127-138
**Issue:** Session logs are intentionally standalone but flagged as orphans

**Current Behavior:**
```
- [ORPHAN] **log_20251125_iteration_3_complete** is not depended on by any other document.
```

**Current Code:**
```python
# 3. Orphan Detection
for doc_id in existing_ids:
    if not rev_adj[doc_id]:
        doc_type = files_data[doc_id]['type']
        filename = files_data[doc_id]['filename']

        # Skip expected root types and templates
        if doc_type in ['product', 'strategy', 'kernel']:
            continue
        if 'template' in filename.lower():
            continue

        issues.append(f"- [ORPHAN] **{doc_id}** is not depended on by any other document.")
```

**Required Fix:**
```python
# 3. Orphan Detection
for doc_id in existing_ids:
    if not rev_adj[doc_id]:
        doc_type = files_data[doc_id]['type']
        filename = files_data[doc_id]['filename']
        filepath = files_data[doc_id]['filepath']

        # Skip expected root types and templates
        if doc_type in ['product', 'strategy', 'kernel']:
            continue
        if 'template' in filename.lower():
            continue
        # Skip log files - they are intentionally standalone
        if '/logs/' in filepath or '\\logs\\' in filepath:
            continue

        issues.append(f"- [ORPHAN] **{doc_id}** is not depended on by any other document.")
```

**Implementation Steps:**
1. Open `scripts/generate_context_map.py`
2. Locate the orphan detection section (around line 127)
3. Add `filepath = files_data[doc_id]['filepath']` after line 130
4. Add the logs directory check before the orphan warning
5. Test by running `python3 scripts/generate_context_map.py` - log files should no longer appear as orphans

---

### 3. Add Missing Encoding Parameter

**File:** `scripts/migrate_frontmatter.py`
**Line:** 84
**Issue:** File write missing UTF-8 encoding (inconsistent with other file operations)

**Current Code:**
```python
with open(PROMPT_FILE, 'w') as f:
    f.write(prompt)
```

**Required Fix:**
```python
with open(PROMPT_FILE, 'w', encoding='utf-8') as f:
    f.write(prompt)
```

**Implementation Steps:**
1. Open `scripts/migrate_frontmatter.py`
2. Find line 84 with the `open()` call
3. Add `encoding='utf-8'` parameter
4. Save the file

---

## 🟡 MEDIUM PRIORITY (Reliability & DX Improvements)

### 4. Add `--quiet` Flag to All Scripts

**Issue:** Scripts print to stdout, which may interfere with CI/CD pipelines or scripted usage.

**Files to Modify:**
- `scripts/generate_context_map.py`
- `scripts/migrate_frontmatter.py`
- `scripts/end_session.py`

**Implementation Pattern:**

Add to argument parser:
```python
parser.add_argument('--quiet', '-q', action='store_true',
                    help='Suppress output except errors')
```

Wrap print statements:
```python
if not args.quiet:
    print(f"Scanning {target_dir}...")
```

**For `generate_context_map.py`, add JSON output option:**
```python
parser.add_argument('--json', action='store_true',
                    help='Output results as JSON instead of markdown')
```

---

### 5. Add `--strict` Mode to All Scripts

**Issue:** Only `generate_context_map.py` has strict mode. Other scripts always exit 0.

**Files to Modify:**
- `scripts/migrate_frontmatter.py` - Exit 1 if untagged files found
- `scripts/end_session.py` - Exit 1 if log creation fails

**Implementation for `migrate_frontmatter.py`:**

Add to argument parser:
```python
parser.add_argument('--strict', action='store_true',
                    help='Exit with error code 1 if untagged files found')
```

Add before function return:
```python
if args.strict and untagged:
    sys.exit(1)
```

Don't forget to add `import sys` at the top of the file.

---

### 6. Fix Template ID Appearing in Context Map

**File:** `docs/template.md`
**Issue:** The placeholder ID `unique_slug_name` appears as a real document in the context map.

**Option A - Use underscore prefix convention:**
```yaml
---
id: _template
type: atom
status: draft
---
```

Then update `generate_context_map.py` to skip IDs starting with underscore:
```python
if frontmatter and 'id' in frontmatter:
    doc_id = frontmatter['id']
    # Skip internal/template documents
    if doc_id.startswith('_'):
        continue
    files_data[doc_id] = { ... }
```

**Option B - Exclude template files entirely:**

In `scan_docs()` function:
```python
if file.endswith('.md'):
    # Skip template files
    if file.lower() == 'template.md':
        continue
    filepath = os.path.join(subdir, file)
    ...
```

---

### 7. Add Version Tracking

**Issue:** Manual says v0.3 but no programmatic version exists.

**Create new file:** `scripts/__init__.py`
```python
__version__ = "0.3.0"
```

**Update each script to include version flag:**
```python
from . import __version__

parser.add_argument('--version', '-V', action='version',
                    version=f'%(prog)s {__version__}')
```

**Alternative - Create `VERSION` file in root:**
```
0.3.0
```

---

## 🟢 LOW PRIORITY (Enhancements)

### 8. Add Pre-commit Hook Configuration

**Create new file:** `.pre-commit-config.yaml`

```yaml
# See https://pre-commit.com for more information
repos:
  - repo: local
    hooks:
      - id: ontos-validate
        name: Validate Ontos Context Map
        entry: python3 scripts/generate_context_map.py --strict
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]

      - id: ontos-check-frontmatter
        name: Check for untagged files
        entry: python3 scripts/migrate_frontmatter.py --strict
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
```

**Update README.md** with installation instructions:
```markdown
## Pre-commit Hooks (Optional)

Install pre-commit hooks to validate the graph on every commit:

```bash
pip install pre-commit
pre-commit install
```
```

---

### 9. Add Watch Mode for Development

**File:** `scripts/generate_context_map.py`

**Add watchdog dependency to `requirements.txt`:**
```
pyyaml
watchdog
```

**Add watch functionality:**
```python
def watch_mode(target_dir):
    """Watch for file changes and regenerate map."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Install watchdog for watch mode: pip install watchdog")
        sys.exit(1)

    class ChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith('.md'):
                print(f"\n🔄 Change detected: {event.src_path}")
                generate_context_map(target_dir)

    observer = Observer()
    observer.schedule(ChangeHandler(), target_dir, recursive=True)
    observer.start()
    print(f"👀 Watching {target_dir} for changes... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

**Add argument:**
```python
parser.add_argument('--watch', '-w', action='store_true',
                    help='Watch for file changes and regenerate')
```

---

### 10. Support Multiple Directories

**File:** `scripts/generate_context_map.py`

**Current limitation:** Only scans one directory.

**Update argument parser:**
```python
parser.add_argument('--dir', type=str, action='append', dest='dirs',
                    help='Directory to scan (can be specified multiple times)')
```

**Update main logic:**
```python
dirs = args.dirs if args.dirs else [DEFAULT_DOCS_DIR]
all_files_data = {}
for target_dir in dirs:
    files_data = scan_docs(target_dir)
    all_files_data.update(files_data)
```

**Usage:**
```bash
python3 scripts/generate_context_map.py --dir docs --dir specs --dir guides
```

---

### 11. Add Dry-Run Mode for Migration

**File:** `scripts/migrate_frontmatter.py`

**Add argument:**
```python
parser.add_argument('--dry-run', action='store_true',
                    help='Show what would be done without writing files')
```

**Update main logic:**
```python
if args.dry_run:
    print(f"\n📋 Would generate prompt for {len(untagged)} files")
    print("(Dry run - no files written)")
    return

# Existing file write logic...
```

---

### 12. Add Type Hints to All Scripts

**Example transformation for `generate_context_map.py`:**

```python
from typing import Optional

def parse_frontmatter(filepath: str) -> Optional[dict]:
    """Parses YAML frontmatter from a markdown file."""
    ...

def scan_docs(root_dir: str) -> dict[str, dict]:
    """Scans the docs directory for markdown files and parses their metadata."""
    ...

def validate_dependencies(files_data: dict[str, dict]) -> list[str]:
    """Checks for broken links, cycles, orphans, depth, and type violations."""
    ...

def generate_context_map(target_dir: str) -> int:
    """Main function to generate the CONTEXT_MAP.md file. Returns issue count."""
    ...
```

---

### 13. Extract Constants to Configuration File

**Create new file:** `scripts/config.py`

```python
"""Ontos configuration constants."""

# Directory settings
DEFAULT_DOCS_DIR = 'docs'
LOG_DIR = 'docs/logs'

# Output files
CONTEXT_MAP_FILE = 'CONTEXT_MAP.md'
MIGRATION_PROMPT_FILE = 'migration_prompt.txt'

# Validation thresholds
MAX_DEPENDENCY_DEPTH = 5

# Document type hierarchy (lower number = higher in hierarchy)
TYPE_HIERARCHY = {
    'kernel': 0,
    'strategy': 1,
    'product': 2,
    'atom': 3,
    'unknown': 4
}

# Types that are allowed to be orphans (no dependents)
ALLOWED_ORPHAN_TYPES = ['product', 'strategy', 'kernel']

# Files/patterns to skip during scanning
SKIP_PATTERNS = ['template.md']
```

**Update scripts to import from config:**
```python
from config import DEFAULT_DOCS_DIR, CONTEXT_MAP_FILE, TYPE_HIERARCHY
```

---

### 14. Add Unit Tests

**Create directory structure:**
```
tests/
├── __init__.py
├── conftest.py
├── test_frontmatter_parsing.py
├── test_cycle_detection.py
├── test_orphan_detection.py
├── test_type_hierarchy.py
└── fixtures/
    └── sample_docs/
        ├── valid_kernel.md
        ├── valid_atom.md
        ├── circular_a.md
        ├── circular_b.md
        └── no_frontmatter.md
```

**Example test file:** `tests/test_frontmatter_parsing.py`

```python
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from generate_context_map import parse_frontmatter

class TestFrontmatterParsing:
    def test_valid_frontmatter(self, tmp_path):
        """Test parsing valid YAML frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text("""---
id: test_doc
type: atom
status: active
depends_on: [dep1, dep2]
---
# Content here
""")
        result = parse_frontmatter(str(test_file))
        assert result['id'] == 'test_doc'
        assert result['type'] == 'atom'
        assert result['depends_on'] == ['dep1', 'dep2']

    def test_missing_frontmatter(self, tmp_path):
        """Test file without frontmatter returns None."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Just a heading\nNo frontmatter here.")
        result = parse_frontmatter(str(test_file))
        assert result is None

    def test_string_depends_on(self, tmp_path):
        """Test that string depends_on is handled (edge case)."""
        test_file = tmp_path / "test.md"
        test_file.write_text("""---
id: test_doc
type: atom
depends_on: single_dep
---
""")
        result = parse_frontmatter(str(test_file))
        # The parse function returns raw YAML, validation handles conversion
        assert result['depends_on'] == 'single_dep'
```

**Add to `requirements.txt`:**
```
pyyaml
pytest
pytest-cov
```

**Add test command to README:**
```bash
pytest tests/ -v --cov=scripts
```

---

### 15. Create CHANGELOG.md

**Create new file:** `CHANGELOG.md`

```markdown
# Changelog

All notable changes to Project Ontos will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Exclude log files from orphan detection
- Add `--quiet` flag to all scripts
- Add `--strict` flag to migrate_frontmatter.py

### Fixed
- Broken link in Ontos_Agent_Instructions.md
- Missing UTF-8 encoding in migrate_frontmatter.py

## [0.3.0] - 2025-11-24

### Added
- Strict mode (`--strict` flag) for CI/CD integration
- Maintenance protocol ("Maintain Ontos" command)
- Session archival with `end_session.py`
- Migration script for untagged files

### Fixed
- String handling in `depends_on` field (now accepts string or list)
- UTF-8 encoding with fallback for file reading
- Specific exception handling (removed bare `except:`)

### Changed
- Improved orphan detection to skip templates
- Added document count and issue count to output

## [0.2.0] - 2025-11-23

### Added
- Five integrity checks (broken links, cycles, orphans, depth, architecture)
- Type hierarchy validation
- Cycle detection using DFS

## [0.1.0] - 2025-11-22

### Added
- Initial YAML frontmatter specification
- Basic context map generation
- Document type taxonomy (kernel, strategy, product, atom)
```

---

### 16. Add Troubleshooting Section to Manual

**Append to:** `Ontos_Manual.md`

```markdown
## Troubleshooting

### "My file doesn't appear in the context map"

**Cause:** File is missing YAML frontmatter or the `id` field.

**Solution:**
1. Run `python3 scripts/migrate_frontmatter.py` to identify untagged files
2. Add frontmatter to the file:
   ```yaml
   ---
   id: your_unique_id
   type: atom
   ---
   ```
3. Regenerate the map: `python3 scripts/generate_context_map.py`

### "How do I fix a circular dependency?"

**Example Error:** `[CYCLE] Circular dependency detected: doc_a -> doc_b -> doc_a`

**Solution:**
1. Identify which dependency is incorrect (usually the one that points "up" the hierarchy)
2. Remove the problematic `depends_on` entry from one of the files
3. Consider if documents should be merged or restructured

### "Two files have the same ID"

**Behavior:** Only the last-scanned file will appear in the map.

**Solution:**
1. Search for duplicate IDs: `grep -r "^id:" docs/`
2. Rename one of the IDs to be unique
3. Update any `depends_on` references to the renamed ID

### "Architectural violation error"

**Example Error:** `[ARCHITECTURE] kernel_mission (kernel) depends on higher-layer api_spec (atom)`

**Explanation:** Kernels are foundational and should not depend on implementation details.

**Solution:**
1. Review if the dependency is actually needed
2. If needed, consider changing the document type:
   - Maybe `kernel_mission` should be `strategy`
   - Or `api_spec` should be elevated to `product`
3. Remove the dependency if it's not essential
```

---

## Implementation Checklist

Use this checklist to track progress:

```markdown
### 🔴 High Priority
- [ ] Fix broken link in Ontos_Agent_Instructions.md (line 27)
- [ ] Add log file exclusion to orphan detection in generate_context_map.py
- [ ] Add encoding='utf-8' to migrate_frontmatter.py (line 84)

### 🟡 Medium Priority
- [ ] Add --quiet flag to all scripts
- [ ] Add --strict flag to migrate_frontmatter.py and end_session.py
- [ ] Fix template.md ID (use _template or exclude from scanning)
- [ ] Add version tracking

### 🟢 Low Priority
- [ ] Create .pre-commit-config.yaml
- [ ] Add --watch mode to generate_context_map.py
- [ ] Support multiple directories
- [ ] Add --dry-run to migrate_frontmatter.py
- [ ] Add type hints to all scripts
- [ ] Extract constants to config.py
- [ ] Create tests/ directory with unit tests
- [ ] Create CHANGELOG.md
- [ ] Add troubleshooting section to manual
```

---

## Notes for Implementing Agent

1. **Test after each change:** Run `python3 scripts/generate_context_map.py` after modifications to ensure nothing breaks.

2. **Maintain backwards compatibility:** The `--strict`, `--quiet`, and other flags should be optional additions, not breaking changes.

3. **Follow existing code style:** The codebase uses:
   - 4-space indentation
   - Single quotes for strings (mostly)
   - f-strings for formatting
   - Docstrings for functions

4. **Commit strategy:** Consider grouping related changes:
   - Commit 1: High priority bug fixes
   - Commit 2: Medium priority improvements
   - Commit 3: Low priority enhancements

5. **Update CONTEXT_MAP.md:** After making changes to the docs/ directory, regenerate the context map.

---

*End of Review Document*
