---
id: v3_1_0_track_a_ca_rulings_d3a
type: decision
status: complete
depends_on: [v3_1_0_track_a_pr_review_chief_architect]
concepts: [chief-architect-decision, review-board-rulings, track-a, phase-d]
---

# Phase D.3a-Decision: Chief Architect Rulings

**Project:** Ontos v3.1.0
**Phase:** D.3a-Decision (CA Rulings on Consolidation)
**PR:** #54 — Track A
**Author:** Chief Architect (Claude Opus 4.5)
**Date:** 2026-01-21

---

## Ruling 1: B-1 — `FrontmatterParseError` Implementation

**Issue:** Spec §3.5 requires `FrontmatterParseError` dataclass with filepath, line, column, message fields. Not implemented.

**Ruling: DEFER TO v3.2**

**Rationale:**

1. **Current error handling works.** Users receive error messages for malformed frontmatter today. The spec item is about *structured* error reporting (a dataclass), not whether errors are caught and reported.

2. **This is polish, not core functionality.** Track A's value proposition is Obsidian compatibility and token efficiency — `--obsidian`, `--compact`, `--filter`, `DocumentCache`. Those are all implemented correctly.

3. **Structured errors deserve proper design.** A v3.2 implementation can consider:
   - Integration with `--json` output mode
   - Consistency with other error types across the codebase
   - Whether to include suggested fixes in the error structure

4. **Shipping velocity matters.** Track A is ready. Blocking a complete feature PR for a non-user-facing dataclass definition is not justified.

**Required actions:**

- [x] Add to Appendix A (Deferred Items): `FrontmatterParseError` structured type
- [x] Release notes note: "Structured parse error types deferred to v3.2"

**Spec update (add to Appendix A):**
```markdown
### CODE-06: FrontmatterParseError Structured Type

**Original spec:** §3.5
**Deferral reason:** Current error handling functional; structured type enables JSON output integration
**Target:** v3.2
**Dependencies:** None
```

---

## Ruling 2: M-1 — Obsidian Leniency Scope

**Issue:** `read_file_lenient()` (BOM stripping, leading whitespace handling) is applied to ALL file reads, not just when `--obsidian` flag is set.

**Ruling: KEEP UNCONDITIONAL (Option B)**

**Rationale:**

1. **BOM/whitespace issues are not Obsidian-specific.** UTF-8 BOM can appear in files created by any Windows editor. Leading whitespace can result from copy-paste, template expansion, or IDE auto-formatting. These are general file hygiene issues, not Obsidian quirks.

2. **No known downside to leniency.** Stripping a BOM or leading whitespace before `---` has no negative effect on well-formed files. The operation is idempotent and invisible to users with clean files.

3. **Better user experience.** A user with a BOM-corrupted file shouldn't need to know about `--obsidian` to get reasonable behavior. The tool should Just Work™.

4. **Simpler code.** Conditional leniency adds code paths and testing burden. Unconditional leniency is one path, always applied.

5. **Spec intent vs. spec letter.** The spec said "when `--obsidian` is active" because we were thinking about Obsidian users. But the leniency benefits everyone. The spec should describe what we *want*, not constrain us to a suboptimal design.

**Required actions:**

- [x] Update spec §3.5 to reflect actual behavior
- [x] No code changes needed — current implementation is correct

**Spec update (§3.5):**

Replace:
> When `--obsidian` flag is active, apply minimal leniency to frontmatter parsing

With:
> Apply minimal leniency to frontmatter parsing in all modes. Specifically:
> 1. Strip UTF-8 BOM (0xEF 0xBB 0xBF) if present
> 2. Allow leading whitespace/newlines before `---` delimiter
>
> This improves compatibility with files from various editors without requiring special flags.

---

## Summary

| Item | Ruling | Action Required |
|------|--------|-----------------|
| B-1: FrontmatterParseError | **Defer to v3.2** | Add CODE-06 to Appendix A |
| M-1: Leniency scope | **Keep unconditional** | Update spec §3.5 wording |

---

## Guidance for Antigravity (D.4a)

**No code changes required for these rulings.**

1. **B-1:** The missing `FrontmatterParseError` dataclass is deferred. Do not implement it in Track A.

2. **M-1:** The current unconditional leniency is correct. Do not gate behind `--obsidian`.

**If there are other blocking issues from D.3a consolidation**, those should proceed to D.4a for fix instructions.

---

## Dissent Record

**Codex's M-1 concern acknowledged but overruled.** The literal spec reading supports gating, but the user-centric design principle favors unconditional leniency. Spec will be updated to match implementation, not vice versa.

---

*Phase D.3a-Decision — Chief Architect Rulings*
*Claude Opus 4.5 — 2026-01-21*
