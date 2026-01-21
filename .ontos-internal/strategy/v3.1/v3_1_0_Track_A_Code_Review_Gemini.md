# Phase D.2a: Review Board — Track A Code Review

**Project:** Ontos v3.1.0
**Phase:** D.2a (Code Review)
**Track:** A — Obsidian Compatibility + Token Efficiency
**Branch:** `feat/v3.1.0-track-a`
**PR:** #54
**Date:** 2026-01-21

---

## Your Role

**Review signed by:**
- **Role:** Peer/Strategic Reviewer
- **Model:** Gemini 2.5 Pro
- **Date:** 2026-01-21
- **Review Type:** Code Review (Phase D.2a)
- **PR:** #54

---

## Output Structure

### Part 1: Spec Compliance Review

#### §3.1 Tags and Aliases

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `normalize_tags()` merges concepts + tags | `frontmatter.py` | ✅ | ✅ | |
| Tags deduplicated and sorted | `frontmatter.py` | ✅ | ✅ | |
| Handles string input (not just list) | `frontmatter.py` | ✅ | ✅ | |
| Whitespace stripped | `frontmatter.py` | ✅ | ✅ | |
| `normalize_aliases()` auto-generates | `frontmatter.py` | ✅ | ✅ | |
| Title Case variant from id | `frontmatter.py` | ✅ | ✅ | |
| kebab-case variant from id | `frontmatter.py` | ✅ | ✅ | |

#### §3.2 Obsidian Mode

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `--obsidian` flag registered | `cli.py` | ✅ | ✅ | |
| `MapOptions.obsidian` field | `map.py` | ✅ | ✅ | |
| `_format_doc_link()` function | `map.py` | ✅ | ✅ | |
| `[[filename|id]]` when filename ≠ id | `map.py` | ✅ | ✅ | Verified manually |
| `[[id]]` when filename == id | `map.py` | ✅ | ✅ | Verified manually |
| Uses `doc_path.stem` for filename | `map.py` | ✅ | ✅ | |

#### §3.3 Document Cache

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `DocumentCache` class exists | `cache.py` | ✅ | ✅ | |
| `CacheEntry` dataclass | `cache.py` | ✅ | ✅ | |
| mtime-based invalidation | `cache.py` | ✅ | ✅ | |
| `get()` returns None on miss | `cache.py` | ✅ | ✅ | |
| `get()` returns None on stale | `cache.py` | ✅ | ✅ | |
| `set()` stores with mtime | `cache.py` | ✅ | ✅ | |
| `invalidate()` removes entry | `cache.py` | ✅ | ✅ | |
| `clear()` removes all | `cache.py` | ✅ | ✅ | |
| `stats` property | `cache.py` | ✅ | ✅ | |
| `--no-cache` flag | `cli.py` | ✅ | ✅ | |
| Cache integrated into map command | `map.py` | ✅ | ✅ | |

#### §3.4 Compact Output

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `CompactMode` enum (OFF, BASIC, RICH) | `map.py` | ✅ | ✅ | |
| `--compact` flag accepts basic/rich | `cli.py` | ✅ | ✅ | |
| `_generate_compact_output()` function | `map.py` | ✅ | ✅ | |
| Basic format: `id:type:status` | `map.py` | ✅ | ✅ | |
| Rich format: `id:type:status:"summary"` | `map.py` | ✅ | ✅ | |
| Backslash escaped: `\` → `\\` | `map.py` | ✅ | ✅ | Order is correct |
| Quote escaped: `"` → `\"` | `map.py` | ✅ | ✅ | Order is correct |
| Newline escaped: `\n` → `\\n` | `map.py` | ✅ | ✅ | Order is correct |
| Escaping order correct (backslash first) | `map.py` | ✅ | ✅ | |

#### §3.5 YAML Errors and Leniency

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `FrontmatterParseError` dataclass | `frontmatter.py` | ❌ | ❌ | **MISSING** |
| filepath, line, column, message fields | `frontmatter.py` | ❌ | ❌ | **MISSING** |
| Optional suggestion field | `frontmatter.py` | ❌ | ❌ | **MISSING** |
| `__str__` formats as `file:line:col: message` | `frontmatter.py` | ❌ | ❌ | **MISSING** |
| `read_file_lenient()` function | `obsidian.py` | ✅ | ✅ | |
| Strips UTF-8 BOM (`\xef\xbb\xbf`) | `obsidian.py` | ✅ | ✅ | |
| Handles leading whitespace before `---` | `obsidian.py` | ✅ | ✅ | |
| Schema version error includes upgrade hint | `frontmatter.py` | ❌ | ❌ | **MISSING** |

#### §3.6 Doctor Verbose

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `-v`/`--verbose` flag registered | `cli.py` | ✅ | ✅ | |
| `_get_config_path()` helper | `doctor.py` | ✅ | ✅ | |
| Checks `.ontos.toml` in repo root | `doctor.py` | ✅ | ✅ | |
| `_print_config_paths()` function | `doctor.py` | ✅ | ✅ | |
| Shows repo_root | `doctor.py` | ✅ | ✅ | |
| Shows config_path (or "default") | `doctor.py` | ✅ | ✅ | |
| Shows docs_dir | `doctor.py` | ✅ | ✅ | |
| Shows context_map path | `doctor.py` | ✅ | ✅ | |

#### §3.7 Filter Flag

| Requirement | Code Location | Implemented? | Correctly? | Notes |
|-------------|---------------|--------------|------------|-------|
| `--filter` / `-f` flag registered | `cli.py` | ✅ | ✅ | |
| `FilterExpression` dataclass | `map.py` | ✅ | ✅ | |
| `parse_filter()` function | `map.py` | ✅ | ✅ | |
| Splits on whitespace | `map.py` | ✅ | ✅ | |
| Splits field:value on `:` | `map.py` | ✅ | ✅ | |
| Splits values on `,` | `map.py` | ✅ | ✅ | |
| `matches_filter()` function | `map.py` | ✅ | ✅ | |
| `type` field matching | `map.py` | ✅ | ✅ | |
| `status` field matching | `map.py` | ✅ | ✅ | |
| `concept` field matching | `map.py` | ✅ | ✅ | |
| `id` field with glob (fnmatch) | `map.py` | ✅ | ✅ | |
| Multiple values = OR | `map.py` | ✅ | ✅ | |
| Multiple fields = AND | `map.py` | ✅ | ✅ | |
| Case-insensitive matching | `map.py` | ✅ | ✅ | |

---

### Part 2: Code Quality Review

#### New Files

| File | Lines | Readability | Error Handling | Type Hints | Docstrings | Overall |
|------|-------|-------------|----------------|------------|------------|---------|
| `cache.py` | ~70 | Good | Good | Good | Good | Good |
| `obsidian.py` | ~40 | Good | Good | Good | Good | Good |

#### Modified Files

| File | Change Size | Risk | Quality | Notes |
|------|-------------|------|---------|-------|
| `frontmatter.py` | M | Med | Adequate | Missing error classes; good normalization logic |
| `map.py` | M | Med | Good | Clean integration of new features |
| `doctor.py` | S | Low | Good | Verbose output is helpful |
| `cli.py` | S | Low | Good | Standard argparse updates |

---

### Part 3: Architecture Compliance

| Constraint | Check | Status |
|------------|-------|--------|
| No `core/` → `io/` imports | `grep -rn "from ontos.io" ontos/core/` | ✅ Empty |
| No `core/` → `commands/` imports | `grep -rn "from ontos.commands" ontos/core/` | ✅ Empty |
| `cache.py` in `core/` | File location | ✅ |
| `obsidian.py` in `io/` | File location | ✅ |
| Consistent import style | Match existing patterns | ✅ |

---

### Part 4: Test Coverage Assessment

| Test File | Exists? | Coverage | Quality | Missing Cases |
|-----------|---------|----------|---------|---------------|
| `test_cache.py` | ✅ | Good | Good | |
| `test_frontmatter_tags.py` | ✅ | Good | Good | |
| `test_map_compact.py` | ✅ | Good | Good | |
| `test_map_filter.py` | ✅ | Good | Good | |
| `test_map_obsidian.py` | ❌ | None | N/A | Entire file missing |

---

### Part 5: Edge Case & Failure Mode Analysis

#### normalize_tags / normalize_aliases

| Edge Case | Expected Behavior | Handled? | Test? |
|-----------|-------------------|----------|-------|
| Empty frontmatter `{}` | Return `[]` | ✅ | ✅ |
| `tags: null` | Return `[]` or skip | ✅ | ✅ |
| `tags: ""` (empty string) | Return `[]` | ✅ | ✅ |
| `tags: "single"` (string not list) | Return `["single"]` | ✅ | ✅ |
| `tags: [null, "", "valid"]` | Filter out null/empty | ✅ | ✅ |
| `tags: [" spaced "]` | Strip whitespace | ✅ | ✅ |
| Duplicate between tags and concepts | Deduplicate | ✅ | ✅ |
| `doc_id` is empty/None | Don't crash on alias generation | ✅ | ✅ |

#### Compact Output Escaping

| Edge Case | Input | Expected Output | Handled? | Test? |
|-----------|-------|-----------------|----------|-------|
| Quote in summary | `He said "hello"` | `He said \"hello\"` | ✅ | ✅ |
| Newline in summary | `Line1\nLine2` | `Line1\\nLine2` | ✅ | ✅ |
| Backslash in summary | `path\to\file` | `path\\to\\file` | ✅ | ✅ |
| All three combined | `"a\nb\\c"` | `\"a\\nb\\\\c\"` | ✅ | ✅ |

#### Filter Parsing

| Edge Case | Input | Expected Behavior | Handled? | Test? |
|-----------|-------|-------------------|----------|-------|
| Empty string | `""` | No filters | ✅ | ✅ |
| Whitespace only | `"   "` | No filters | ✅ | ✅ |
| Missing colon | `"type"` | Ignore | ✅ | ✅ |
| Empty value | `"type:"` | Match nothing or error | ✅ | ✅ |
| Unknown field | `"unknown:value"` | Ignore | ✅ | ✅ |
| Trailing comma | `"type:a,b," ` | Ignore empty | ✅ | ✅ |
| Case variations | `"TYPE:Strategy"` | Case-insensitive | ✅ | ✅ |
| Glob characters | `"id:auth_*"` | fnmatch pattern | ✅ | ✅ |

#### Wikilink Formatting (Manual Check)

| Edge Case | Filename | doc_id | Expected | Handled? | Test? |
|-----------|----------|--------|----------|----------|-------|
| Match | `auth_flow.md` | `auth_flow` | `[[auth_flow]]` | ✅ | ❌ (Manual) |
| Mismatch | `auth-flow.md` | `auth_flow` | `[[auth-flow|auth_flow]]` | ✅ | ❌ (Manual) |

---

### Part 6: Issues Found

#### Major (Should fix before merge)

| # | Issue | File | Line(s) | Description | Suggested Fix |
|---|-------|------|---------|-------------|---------------|
| M-1 | Spec Violation: Frontmatter Error Handling | `ontos/core/frontmatter.py` | N/A | The spec requires a `FrontmatterParseError` dataclass and detailed error reporting (file, line, col, message). Current implementation swallows errors or returns None. | Implement `FrontmatterParseError` and update `parse_frontmatter` to raise/return it. |
| M-2 | Missing Tests: Obsidian Mode | `tests/` | N/A | No automated tests for `map --obsidian`. This functionality relies only on manual smoke testing. | Create `tests/commands/test_map_obsidian.py` to verify wikilink generation. |

#### Minor (Consider fixing)

| # | Issue | File | Line(s) | Description | Suggested Fix |
|---|-------|------|---------|-------------|---------------|
| m-1 | Missing Schema Version Hint | `ontos/core/frontmatter.py` | N/A | Spec requires "Schema version error includes upgrade hint". Not found in code. | Add logic to check schema version during parsing and provide hint in error. |

---

### Part 7: Verdict

**Spec Compliance:** Major gaps (Frontmatter Error Handling missing)

**Code Quality:** Good

**Test Coverage:** Adequate (Obsidian tests missing)

**Risk Assessment:** Low

**Recommendation:** Request revision

**Blocking issues:** 2 (M-1, M-2)

**Summary:**
The Track A implementation successfully delivers the core features: Obsidian compatibility, compact output, filtering, and caching. The code quality is generally good, and manual verification confirms the features work as expected. However, the implementation completely misses the required "Better YAML Errors" feature (§3.5), relying instead on silent failure or fallback parsing. Additionally, the Obsidian functionality lacks automated regression tests. These must be addressed before merge.
