# Phase 5 Spec Review: Peer Reviewer

**Reviewer:** Gemini (Peer)
**Model:** Gemini 2.5 Pro
**Date:** 2026-01-13
**Spec Version:** 1.0

---

## 1. Summary

| Aspect | Rating | Notes |
|--------|--------|-------|
| Issue coverage | Complete | Covers docs, tech debt, and release tasks well. |
| Prioritization | Appropriate | Correctly identifies "Must" vs "Should". |
| UX improvements | Good | Fixes meaningful friction (hooks warning). |
| Documentation | Good | Migration guide is crucial and included. |

**Recommendation:** Approve with suggestions

---

## 2. Issue Coverage

### 2.1 Missing Issues?

| Potential Issue | Should Be Included? | Priority |
|-----------------|---------------------|----------|
| Verify `--version` output | Yes | Must |
| Verify clean uninstall | Yes | Should |
| Check documentation links | Yes | Must |

**Reasoning:**
- `ontos --version` must match the PyPI version to confirm successful build/install.
- Broken documentation links in `pyproject.toml` are a common release error.

### 2.2 Issue Research

- **Deprecation Best Practices:** "Soft deprecation" (warnings) is preferred before hard removal. The spec's plan to remove `ontos_lib.py` immediately is aggressive but acceptable if it's strictly internal.
- **Dependency Injection:** To fix the architecture violation (P5-1), Python best practice is either Dependency Injection (passing functions as args) or moving shared logic to a lower-level module (e.g., `ontos.common`). The spec's proposed "Option B" (DI) is sound.

---

## 3. Prioritization Review

| Issue | Spec Priority | Agree? | Suggested Priority |
|-------|---------------|--------|-------------------|
| P5-1 (Arch Violation) | Should | No | **Must** |
| P5-2 (Del ontos_lib) | Should | Yes | Should |
| P5-3 (Hooks Warning) | Could | No | **Should** |

**Reasoning:**
- **P5-1:** Architecture violations tend to ossify. Fixing circular imports/layer violations *before* v3.0.1 hardens the foundation.
- **P5-3:** False warnings ("Non-Ontos hooks") erode trust in the `doctor` command, which is the primary troubleshooting tool. This is a high-value UX fix.

---

## 4. UX Improvements Review

| Improvement | Will Help Users? | Suggestion |
|-------------|------------------|------------|
| Fix hooks warning | Yes | Critical for trust in `doctor` |
| Context map frontmatter | Yes | Enables Ontos to "read itself" |

---

## 5. Documentation Review

| Doc Change | Adequate? | Suggestion |
|------------|-----------|------------|
| README.md | Yes | Ensure badges point to new PyPI package |
| Migration Guide | Yes | Add section on "Verifying Upgrade" |
| Manual Updates | Yes | Add screenshots/examples for `doctor` output |

---

## 6. Release Notes Review

| Aspect | Good? | Suggestion |
|--------|-------|------------|
| Clear language | Yes | Group by user benefit (Docs, UX) vs Internal |
| Complete | Yes | Captures all key changes |
| User-friendly | Yes | - |

---

## 7. Issues Found

| # | Issue | Severity |
|---|-------|----------|
| P-1 | Architecture violation (P5-1) priority too low | Minor |
| P-2 | Missing verification of `pyproject.toml` URLs | Minor |

---

## 8. Verdict

**Recommendation:** Approve with suggestions

**Key Suggestions:**
1.  Elevate **P5-1 (Architecture Violation)** to **Must** to ensure clean codebase for future features.
2.  Elevate **P5-3 (Hooks Warning)** to **Should** to improve user trust.
3.  Add `ontos --version` verification step to Release Tasks.

---

**Review signed by:**
- **Role:** Peer Reviewer
- **Model:** Gemini 2.5 Pro
- **Date:** 2026-01-13
- **Review Type:** Spec Review (Phase 5)
