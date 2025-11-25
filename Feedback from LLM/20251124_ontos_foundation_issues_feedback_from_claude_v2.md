# Ontos Iteration 2 - Revision Request

**Context:** Foundation issues from Iteration 1 have been addressed. This document outlines the next set of improvements to solidify the protocol and align with the core design philosophy.

---

## Core Design Philosophy (Apply to All Changes)

Ontos follows a **"LLM-Powered Generation + Deterministic Validation"** model:

| Responsibility | Owner | Examples |
|----------------|-------|----------|
| Creative work | LLM | Tagging documents, inferring dependencies, writing summaries, choosing types |
| Validation work | Scripts | Catching cycles, broken links, orphans, architectural violations |

**Rationale:** LLMs will continue to evolve and improve at inference tasks. Scripts provide a deterministic safety net that catches mistakes regardless of which LLM was used.

All changes below should reinforce this split.

---

## Issue 1: Deprecate Old Manual

### Problem

`20251123_Project Ontos The Manual MVP Playbook.md` still exists and contains outdated information:
- Old bracket notation for YAML options
- Old activation phrases ("We are finishing this session")
- Manual LLM prompts instead of script-based automation

This contradicts the new Manual (v0.3) and could confuse agents that discover it.

### Required Fix

Add YAML frontmatter to mark it as deprecated:

```yaml
---
id: manual_mvp_playbook_deprecated
type: strategy
status: deprecated
owner: null
depends_on: []
---
```

Add a note at the top of the document body:

```markdown
> ⚠️ **DEPRECATED**: This document is superseded by [The Manual v0.3](20251124_Project%20Ontos%20The%20Manual.md). Retained for historical reference only.
```

---

## Issue 2: Regenerate CONTEXT_MAP.md

### Problem

The current `CONTEXT_MAP.md` still shows the old parsing output:

```
Status: ['draft | active | deprecated']
```

This indicates the map was generated before the template fix was applied.

### Required Fix

Run:

```bash
python3 scripts/generate_context_map.py
```

Verify the output shows:

```
Status: draft
```

Commit the updated `CONTEXT_MAP.md`.

---

## Issue 3: Add Crisp Type Definitions to the Manual

### Problem

The four document types (kernel, strategy, product, atom) are referenced throughout the codebase but never formally defined. LLMs performing tagging or maintenance need clear definitions to make correct decisions.

### Required Fix

Add a new section to `20251124_Project Ontos The Manual.md` after Phase 0, titled **"Document Type Taxonomy"**.

The definitions must be:
1. **Concise** - One sentence each, max
2. **Distinguishable** - Clear boundaries between types
3. **LLM-optimized** - Written so an LLM can confidently classify documents

**Suggested content:**

```markdown
## Document Type Taxonomy

Ontos uses four hierarchical document types. When tagging documents, select the type that best matches the document's *purpose*, not its format.

| Type | Rank | Definition | Signal Words |
|------|------|------------|--------------|
| `kernel` | 0 | Immutable foundational principles that rarely change. | mission, values, philosophy, principles, "why we exist" |
| `strategy` | 1 | High-level decisions about goals, audiences, and approaches. | goals, roadmap, monetization, target market, competitive positioning |
| `product` | 2 | User-facing features, journeys, and requirements. | user flow, feature spec, requirements, user story, journey |
| `atom` | 3 | Technical implementation details and specifications. | API, schema, config, implementation, technical spec, code |

### Dependency Rule

Dependencies flow **down** the hierarchy. Higher-ranked documents can depend on lower-ranked documents.

- ✅ `atom` → `product` → `strategy` → `kernel` (valid chain)
- ❌ `kernel` → `atom` (architectural violation)

### Classification Heuristic

When uncertain, ask: *"If this document changes, what else breaks?"*

- If everything breaks → `kernel`
- If business direction changes → `strategy`
- If user experience changes → `product`
- If only implementation changes → `atom`
```

---

## Issue 4: Update Migration Script Prompt

### Problem

The prompt in `migrate_frontmatter.py` (lines 9-18) contains brief type definitions that may drift from the canonical definitions in the Manual.

### Required Fix

Update the prompt to reference the taxonomy and include the full definitions. Replace the current rules section with:

```python
prompt = """You are the Ontos Librarian. Analyze each document and generate YAML frontmatter metadata.

## Type Taxonomy (Select ONE per document)

| Type | Definition | Signal Words |
|------|------------|--------------|
| kernel | Immutable foundational principles that rarely change | mission, values, philosophy, principles |
| strategy | High-level decisions about goals, audiences, approaches | goals, roadmap, monetization, target market |
| product | User-facing features, journeys, requirements | user flow, feature spec, requirements, user story |
| atom | Technical implementation details and specifications | API, schema, config, implementation, technical spec |

## Classification Heuristic
When uncertain: "If this document changes, what else breaks?"
- Everything breaks → kernel
- Business direction changes → strategy  
- User experience changes → product
- Only implementation changes → atom

## Output Format
Output ONLY valid JSON. No markdown code blocks. No explanation.

{
  "filepath": {
    "id": "unique_snake_case_slug",
    "type": "kernel|strategy|product|atom",
    "status": "active",
    "depends_on": ["other_doc_ids_if_known"]
  }
}

## Files to Process:
"""
```

---

## Issue 5: Add `--strict` Flag for CI/CD

### Problem

`generate_context_map.py` always exits with code 0, even when issues (cycles, broken links, violations) are found. This means CI/CD pipelines cannot enforce graph integrity.

### Required Fix

Add a `--strict` flag that exits with code 1 when issues are detected.

**Changes to `scripts/generate_context_map.py`:**

1. Add argument:
```python
parser.add_argument('--strict', action='store_true', 
    help='Exit with error code 1 if any issues are found')
```

2. Modify the end of `generate_context_map()`:
```python
# After writing the file
print(f"Successfully generated {OUTPUT_FILE}")

# Add summary
print(f"\n📊 Summary: {len(files_data)} documents scanned, {len(issues)} issues found.")

# Return issues count for strict mode
return len(issues)
```

3. Modify `__main__`:
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Ontos Context Map')
    parser.add_argument('--dir', type=str, default=DEFAULT_DOCS_DIR, 
        help='Directory to scan (default: docs)')
    parser.add_argument('--strict', action='store_true', 
        help='Exit with error code 1 if issues found')
    args = parser.parse_args()
    
    issue_count = generate_context_map(args.dir)
    
    if args.strict and issue_count > 0:
        print(f"\n❌ Strict mode: {issue_count} issues detected. Exiting with error.")
        sys.exit(1)
```

4. Update CI example in `DEPLOYMENT.md`:
```yaml
- name: Verify Ontos Graph
  run: python3 scripts/generate_context_map.py --strict
```

---

## Issue 6: Automate Migration Script with LLM API

### Problem

The current `migrate_frontmatter.py` workflow requires manual steps:
1. Script generates prompt file
2. Human copies prompt into LLM chat
3. Human copies response back
4. Human saves as JSON file
5. Script applies changes

This friction is unnecessary. The script should call an LLM API directly.

### Required Fix

Rewrite `migrate_frontmatter.py` to call an LLM API (e.g., Anthropic, OpenAI, or Google) directly.

**Design requirements:**

1. **Configuration via environment variable:**
   ```bash
   export ONTOS_LLM_API_KEY="your-api-key"
   export ONTOS_LLM_PROVIDER="anthropic"  # or "openai", "google"
   ```

2. **Single command execution:**
   ```bash
   python3 scripts/migrate_frontmatter.py --auto
   ```

3. **Transparency:** Print exactly what the LLM decided for each file:
   ```
   📄 docs/auth/login.md
      ID: feature_login
      Type: product
      Depends: [auth_architecture]
   
   📄 docs/api/endpoints.md
      ID: api_endpoints
      Type: atom
      Depends: [feature_login]
   
   ✅ Tagged 2 files. Run `python3 scripts/generate_context_map.py` to verify.
   ```

4. **Dry-run by default:** Require `--apply` flag to actually write changes:
   ```bash
   python3 scripts/migrate_frontmatter.py --auto          # Preview only
   python3 scripts/migrate_frontmatter.py --auto --apply  # Actually write
   ```

5. **Preserve manual workflow:** Keep the existing prompt-file workflow as a fallback for users without API access:
   ```bash
   python3 scripts/migrate_frontmatter.py              # Manual (current behavior)
   python3 scripts/migrate_frontmatter.py --auto       # Automated with LLM API
   ```

6. **Error handling:** If API call fails, fall back to manual workflow with clear message:
   ```
   ❌ LLM API call failed: Invalid API key
   💡 Falling back to manual mode. Prompt saved to migration_prompt.txt
   ```

**Suggested libraries:**
- `anthropic` for Claude API
- `openai` for OpenAI API
- `google-generativeai` for Gemini API

Add to a `requirements.txt`:
```
pyyaml
anthropic>=0.18.0
openai>=1.0.0
google-generativeai>=0.3.0
```

---

## Deliverables Summary

| # | File | Action |
|---|------|--------|
| 1 | `20251123_Project Ontos The Manual MVP Playbook.md` | Add deprecation frontmatter + notice |
| 2 | `CONTEXT_MAP.md` | Regenerate to verify template fix |
| 3 | `20251124_Project Ontos The Manual.md` | Add "Document Type Taxonomy" section |
| 4 | `scripts/migrate_frontmatter.py` | Update prompt with full taxonomy |
| 5 | `scripts/generate_context_map.py` | Add `--strict` flag |
| 6 | `scripts/migrate_frontmatter.py` | Add `--auto` flag with LLM API integration |
| 7 | `DEPLOYMENT.md` | Update CI example with `--strict` |
| 8 | `requirements.txt` | Create with dependencies |

---

## Verification Checklist

After changes are made:

- [ ] Run `python3 scripts/generate_context_map.py` - should show `Status: draft` for template
- [ ] Run `python3 scripts/generate_context_map.py --strict` on a repo with a cycle - should exit 1
- [ ] Old manual shows as `deprecated` in the context map
- [ ] `migrate_frontmatter.py --auto` calls LLM and prints decisions clearly
- [ ] `migrate_frontmatter.py --auto --apply` actually writes frontmatter
- [ ] Manual workflow still works without API key
