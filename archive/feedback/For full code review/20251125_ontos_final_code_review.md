# Ontos Final Code Review - Polish & Robustness

**Context:** Foundation and simplification work is complete. This document covers the final code audit findings - edge cases, robustness improvements, and minor polish items.

**Priority:** These are not blockers. The project works. These improvements make it production-ready.

---

## Issue 1: String Handling Bug in `depends_on`

### Problem

In `scripts/generate_context_map.py`, the `validate_dependencies` function assumes `depends_on` is always a list (line 87):

```python
if deps:
    for dep in deps:
```

If a user writes:
```yaml
depends_on: auth_flow  # String, not list
```

Instead of:
```yaml
depends_on: [auth_flow]  # Correct list format
```

The code iterates over characters: `'a', 'u', 't', 'h', '_', 'f', 'l', 'o', 'w'` — causing false "broken link" errors.

### Required Fix

In `scripts/generate_context_map.py`, add type checking in `validate_dependencies()`:

```python
for doc_id, data in files_data.items():
    deps = data['depends_on']
    if deps:
        # Handle case where user wrote string instead of list
        if isinstance(deps, str):
            deps = [deps]
        for dep in deps:
```

Also apply the same fix in the type hierarchy validation section (around line 140).

---

## Issue 2: File Encoding Handling

### Problem

All three scripts open files without specifying encoding:

```python
with open(filepath, 'r') as f:
```

Files with non-UTF-8 encoding (common on Windows, or files from legacy systems) will crash with `UnicodeDecodeError`.

### Required Fix

Update all file open calls across all three scripts:

**`scripts/generate_context_map.py`** (line 12):
```python
with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
```

**`scripts/migrate_frontmatter.py`** (line 9):
```python
with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
```

**`scripts/end_session.py`** (line 63):
```python
with open(filepath, 'w', encoding='utf-8') as f:
```

---

## Issue 3: Bare Exception Clause

### Problem

In `scripts/migrate_frontmatter.py`, the `has_frontmatter` function uses a bare `except`:

```python
def has_frontmatter(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.readline().strip() == '---'
    except:
        return False
```

This catches everything including `KeyboardInterrupt` and `SystemExit`, hiding real errors.

### Required Fix

Be specific about expected exceptions:

```python
def has_frontmatter(filepath):
    """Checks if a file already has YAML frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.readline().strip() == '---'
    except (IOError, PermissionError, OSError):
        return False
```

---

## Issue 4: Remove Unused Import

### Problem

`scripts/migrate_frontmatter.py` imports `json` but never uses it (leftover from removed API integration).

### Required Fix

Remove line 2:

```python
import os
import json  # DELETE THIS LINE
import argparse
```

---

## Issue 5: Add Summary Output

### Problem

`scripts/generate_context_map.py` prints "Successfully generated CONTEXT_MAP.md" but doesn't report how many documents were scanned or issues found (unless using `--strict`). Users have to open the file to see results.

### Required Fix

Add a summary line at the end of `generate_context_map()`, before the return:

```python
print(f"Successfully generated {OUTPUT_FILE}")
print(f"📊 Scanned {len(files_data)} documents, found {len(issues)} issues.")

return len(issues)
```

---

## Issue 6: Add `.gitignore`

### Problem

The project has no `.gitignore`. Transient files like `migration_prompt.txt` and Python cache files could be accidentally committed.

### Required Fix

Create `.gitignore` in the project root:

```gitignore
# Ontos transient files
migration_prompt.txt

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Issue 7: Add Taxonomy Reference to Agent Instructions

### Problem

`AGENT_INSTRUCTIONS.md` tells agents about the dependency rule:

> A **Kernel** (0) cannot depend on an **Atom** (3).

But doesn't include the full type taxonomy. An agent doing maintenance might not know what qualifies as each type without reading the Manual separately.

### Required Fix

Add a brief taxonomy reference to `AGENT_INSTRUCTIONS.md`, after the protocol section:

```markdown
## Document Type Reference

| Type | Rank | Use For |
|------|------|---------|
| kernel | 0 | Foundational principles (mission, values) |
| strategy | 1 | Business decisions (goals, roadmap) |
| product | 2 | User-facing specs (features, journeys) |
| atom | 3 | Technical details (API, schemas) |

**Dependency Rule:** Higher ranks depend on lower ranks. `atom` → `product` → `strategy` → `kernel`.

For full definitions, see [The Manual](20251124_Project%20Ontos%20The%20Manual.md).
```

---

## Issue 8: Expand `.cursorrules` Context Selection

### Problem

`.cursorrules` tells Cursor to "Load only relevant context IDs" but doesn't explain how to determine relevance. This leaves behavior undefined.

### Required Fix

Expand `.cursorrules`:

```markdown
# Ontos Protocol for Cursor

You are operating within the Ontos framework.

## Activation
When the user says **"Ontos"** (or "Activate Ontos"):
1.  Check/Run `python3 scripts/generate_context_map.py`.
2.  Read `CONTEXT_MAP.md`.
3.  Identify relevant doc IDs based on the user's request.
4.  Follow `depends_on` links to load parent context.
5.  Read ONLY those specific files.
6.  Confirm: "Loaded: [IDs]".

## Context Selection Guidelines
- Start with IDs directly matching the user's request
- Follow `depends_on` chains upward (atom → product → strategy → kernel)
- Stop when you reach kernel or have sufficient context
- Prefer loading fewer, more relevant docs over many tangential ones

## Maintenance
When creating or modifying docs:
1.  Add/update YAML frontmatter (id, type, status, depends_on).
2.  Run `python3 scripts/generate_context_map.py` to validate.
3.  Fix any reported issues before committing.

## Archival
When the user says **"Archive Ontos"** (or "Ontos archive"):
1.  Run `python3 scripts/end_session.py "slug"`.
2.  Fill in the log with decisions and changes.
3.  Commit.
```

---

## Issue 9: Noisy Orphan Detection (Optional)

### Problem

The template file (`docs/template.md`) always shows as an orphan in the Dependency Audit because nothing depends on it. This is expected behavior for a template but creates noise.

### Optional Fix

In `scripts/generate_context_map.py`, modify orphan detection to skip templates:

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

**Note:** This is optional. Some users may prefer to see all orphans regardless.

---

## Deliverables Summary

| # | File | Action |
|---|------|--------|
| 1 | `scripts/generate_context_map.py` | Fix `depends_on` string handling |
| 2 | `scripts/generate_context_map.py` | Add encoding to file open |
| 3 | `scripts/migrate_frontmatter.py` | Add encoding to file open |
| 4 | `scripts/end_session.py` | Add encoding to file write |
| 5 | `scripts/migrate_frontmatter.py` | Fix bare except clause |
| 6 | `scripts/migrate_frontmatter.py` | Remove unused `json` import |
| 7 | `scripts/generate_context_map.py` | Add summary output |
| 8 | `.gitignore` | Create file |
| 9 | `AGENT_INSTRUCTIONS.md` | Add taxonomy reference |
| 10 | `.cursorrules` | Expand context selection guidance |
| 11 | `scripts/generate_context_map.py` | (Optional) Skip templates in orphan detection |

---

## Verification Checklist

After changes:

- [ ] `python3 scripts/generate_context_map.py` prints scan summary
- [ ] Script handles `depends_on: single_string` without error
- [ ] Scripts don't crash on files with weird encodings
- [ ] `migration_prompt.txt` is in `.gitignore`
- [ ] `AGENT_INSTRUCTIONS.md` includes type taxonomy table
- [ ] `.cursorrules` explains context selection
