# Phase 5 Spec Review: Consolidation

**Date:** 2026-01-13
**Spec Version:** 1.0
**Reviews Consolidated:** 3 (Peer, Alignment, Adversarial)

---

## 1. Verdict Summary

| Reviewer | Role | Model | Verdict | Blocking Issues |
|----------|------|-------|---------|-----------------|
| Gemini | Peer | Gemini 2.5 Pro | Approve with suggestions | 0 |
| Claude | Alignment | Claude Opus 4.5 | Approve | 0 |
| Codex | Adversarial | Codex (OpenAI) | Request Changes | 3 |

**Consensus:** 2/3 Approve

**Overall Recommendation:** Needs revision — address Codex's regression risks before implementation.

---

## 2. Blocking Issues

Issues that MUST be resolved before implementation.

| # | Issue | Flagged By | Category | Impact |
|---|-------|------------|----------|--------|
| B1 | Removing `ontos_lib.py` without full import inventory | Codex | Regression | Breaks legacy scripts/tests/users unexpectedly with hard errors |
| B2 | Hook detection based on string matching only | Codex | Edge Case | False positives could suppress warnings for foreign hooks |
| B3 | Frontmatter insertion impacts golden baselines | Codex | Regression | Golden Master test failures unless updated preemptively |

**Total Blocking:** 3

---

## 3. Required Actions for Chief Architect

Specific actions to resolve blocking issues.

| Priority | Action | Addresses Issue | Complexity |
|----------|--------|-----------------|------------|
| 1 | Add deprecation scan test: enumerate all `ontos_lib` import sites in tests/scripts before deletion | B1 | Low |
| 2 | Add negative test cases for hook detection: foreign hooks, empty hooks, binary hooks | B2 | Low |
| 3 | Update Golden Master baselines to include new frontmatter before merging P5-4 | B3 | Low |
| 4 | Elevate P5-1 (Arch Violation) to **Must** priority to prevent debt ossification | Gemini P-1 | Med |
| 5 | Elevate P5-3 (Hooks Warning) to **Should** priority for UX trust | Gemini P-2 | Low |
| 6 | Add `ontos --version` verification step to Release Tasks | Gemini suggestion | Low |

---

## 4. Backward Compatibility Status

**From Claude (Alignment):**

| Aspect | Status |
|--------|--------|
| Breaking changes found | None |
| Architecture violations | None (P5-1 deferred or uses DI) |
| Exit code changes | None |
| API changes | None |

**Verdict:** Backward compatible — all changes are additive, documentation, or deprecated code removal.

---

## 5. Regression Risk Status

**From Codex (Adversarial):**

| Risk Level | Fix Count |
|------------|-----------|
| High risk | 1 (P5-2 `ontos_lib.py` removal) |
| Medium risk | 2 (P5-3 hook detection, P5-4 frontmatter) |
| Low risk | 1 (P5-1 deferral) |

**Top Risks:**
1. P5-2: Hidden imports in tests or user scripts break with hard error after `ontos_lib.py` removal
2. P5-4: Frontmatter insertion may break tools expecting header at line 1

**Verdict:** Medium-high risk requires mitigation — add explicit tests before merge.

---

## 6. Issue Coverage Status

**From Gemini (Peer):**

| Aspect | Status |
|--------|--------|
| All known issues captured | No: missing `--version` verification, `pyproject.toml` URL check |
| Prioritization appropriate | No: P5-1 should be Must, P5-3 should be Should |
| Release notes adequate | Yes |

---

## 7. All Issues by Severity

### 7.1 Critical (Blocking)

| # | Issue | From | Category | Recommendation |
|---|-------|------|----------|----------------|
| C1 | Removing `ontos_lib.py` without import scan | Codex | Regression | Add explicit import inventory test |
| C2 | Hook detection string-matching false positives | Codex | Edge Case | Add negative test cases |
| C3 | Frontmatter breaks golden baselines | Codex | Regression | Pre-update baselines |

### 7.2 Major (Should Fix)

| # | Issue | From | Category | Recommendation |
|---|-------|------|----------|----------------|
| M1 | P5-1 Architecture Violation priority too low | Gemini | Prioritization | Elevate to Must |
| M2 | P5-3 Hooks Warning priority too low | Gemini | Prioritization | Elevate to Should |
| M3 | Missing `ontos --version` verification | Gemini | Completeness | Add to Release Tasks |

### 7.3 Minor (Consider)

| # | Issue | From | Category | Recommendation |
|---|-------|------|----------|----------------|
| m1 | Missing `pyproject.toml` URL verification | Gemini | Completeness | Add check for broken docs links |
| m2 | Migration Guide could add "Verifying Upgrade" section | Gemini | Documentation | Enhance for user confidence |

---

## 8. Reviewer Agreement Analysis

### 8.1 Strong Agreement (All 3 Reviewers)

| Topic | Consensus |
|-------|-----------|
| P5-1 Option A (defer) is acceptable | All agree deferral is appropriate for patch release |
| P5-3 smarter hook detection is valuable | All agree this improves UX |
| No CLI/API breaking changes | All confirm backward compatibility |

### 8.2 Majority Agreement (2 of 3)

| Topic | Majority View | Dissenting View |
|-------|---------------|-----------------|
| Spec readiness | Claude + Gemini: Approve/Approve with suggestions | Codex: Request Changes (needs test coverage) |

### 8.3 Unique Concerns (Single Reviewer)

| Concern | From | Should Address? |
|---------|------|-----------------|
| Missing `--version` verification step | Gemini | Yes — common release validation |
| P5-1 should be Must priority | Gemini | Yes — prevents debt ossification |
| Full import scan before `ontos_lib.py` removal | Codex | Yes — prevents latent breakage |
| Negative test cases for hook detection | Codex | Yes — prevents false positives |

---

## 9. Positive Observations

Strengths noted by reviewers.

| Strength | Noted By |
|----------|----------|
| Issue coverage is complete | Gemini |
| Migration guide is crucial and included | Gemini |
| Appropriate scope for patch release (polish, docs, distribution) | Claude |
| All changes are additive or remove deprecated code | Claude |
| Both CA recommendations (Q1, Q2) align with patch release principles | Claude |
| Architecture maintained (defer or DI pattern) | Claude |

---

## 10. Decision Summary

### 10.1 Spec Readiness

| Criterion | Status |
|-----------|--------|
| No blocking issues OR all addressable | ✅ (3 blocking, all Low complexity to fix) |
| Backward compatible | ✅ |
| Regression risk acceptable | ❌ (Medium-high, needs mitigation) |
| Issue coverage adequate | ❌ (missing verification steps) |

### 10.2 Recommendation

**Status:** Needs Minor Revision

**Chief Architect must:**
1. Add import inventory test for `ontos_lib.py` before removal
2. Add negative test cases for hook detection
3. Update Golden Master baselines before P5-4 merge
4. Elevate P5-1 to Must priority
5. Add `ontos --version` verification to Release Tasks
6. Update spec to v1.1

---

**Consolidation signed by:**
- **Role:** Review Consolidator
- **Model:** Antigravity (Gemini 2.5 Pro)
- **Date:** 2026-01-13
- **Review Type:** Spec Review Consolidation (Phase 5)
