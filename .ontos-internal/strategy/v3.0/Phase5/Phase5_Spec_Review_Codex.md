# Phase 5 Spec Review: Adversarial Reviewer

**Reviewer:** Codex (Adversarial)
**Model:** Codex (OpenAI)
**Date:** 2026-01-13
**Spec Version:** 1.0

---

## 1. Summary

| Aspect | Risk Level |
|--------|------------|
| Regression risk | Med |
| Incomplete fixes | Some |
| New edge cases | Some |

**Recommendation:** Request Changes

---

## 2. Regression Risk Analysis

| Fix | Could Regress? | What Could Break? | Mitigation |
|-----|----------------|-------------------|------------|
| P5-2 remove `ontos_lib.py` | High | Legacy tests/imports and scripts that still rely on shim | Explicit deprecation scan + test updates before delete |
| P5-3 smarter hook detection | Med | False positives mark foreign hooks as Ontos | Add negative tests (foreign hook content) |
| P5-4 add frontmatter to context map | Med | Downstream parsing expectations or diff noise | Golden Master update + validation test |
| P5-1 defer core/io violation | Low | Keeps technical debt unresolved | Documented deferral + architecture lint check |

---

## 3. Fix Completeness Attack

| Fix | Fully Addresses Issue? | Gap |
|-----|------------------------|-----|
| P5-1 defer core/io violation | No | Architecture violation remains, only documented |
| P5-2 remove `ontos_lib.py` | Partial | Spec doesn’t enumerate all import sites; risk of latent references |
| P5-3 hook detection leniency | Partial | Only matches marker or strings; no validation of actual dispatcher |
| P5-4 frontmatter | Yes | Requires map generator update and golden baselines |
| P5-5/6/7 docs | Yes | Must ensure CLI flags and new behavior match code |

---

## 4. New Edge Cases

| Fix | New Edge Case Introduced? | Description |
|-----|---------------------------|-------------|
| P5-3 hook detection | Yes | Any hook containing "ontos hook" in comments is treated as Ontos |
| P5-4 frontmatter | Yes | Frontmatter insertion might break tools expecting header at line 1 |
| P5-2 remove `ontos_lib.py` | Yes | Hidden import in tests or user scripts breaks with hard error |

---

## 5. Test Coverage Check

| Fix | Test Proposed? | Adequate? | Missing |
|-----|----------------|-----------|---------|
| P5-3 hook detection | Yes | No | Negative cases (foreign hooks, empty hooks, binary hooks) |
| P5-4 frontmatter | Yes | No | Golden Master update + map output snapshot |
| P5-2 remove `ontos_lib.py` | No | No | Explicit import scan test + failure message coverage |

---

## 6. Issues Found

| # | Issue | Risk | Impact |
|---|-------|------|--------|
| X-1 | Removing `ontos_lib.py` without full import inventory | Regression | Breaks legacy scripts/tests/users unexpectedly |
| X-2 | Hook detection based on string matching only | Edge | False positives, warning suppression for foreign hooks |
| X-3 | Frontmatter insertion impacts golden baselines | Regression | Golden Master failures unless updated |

---

## 7. Verdict

**Recommendation:** Request Changes

---

**Review signed by:**
- **Role:** Adversarial Reviewer
- **Model:** Codex (OpenAI)
- **Date:** 2026-01-13
- **Review Type:** Spec Review (Phase 5)
