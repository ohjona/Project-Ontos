---
id: v1_codex_v2_5_2_review
type: strategy
status: draft
depends_on: [v2_5_2_dual_mode_remediation]
concepts: [architecture, migration, testing, scaffolding]
---

# Review: V2.5.2 Dual-Mode Remediation Plan

**Date:** 2025-12-17  
**Reviewer:** Codex (Architect)  
**Scope:** Technical review of `.ontos-internal/strategy/proposals/v2.5.2_dual_mode_remediation.md`

---

## Verdict
- Do **not** ship as-is. Core migration logic is undefined, backward-compatibility is incomplete, and the testing plan will not actually catch user-mode regressions in CI.

---

## Major Findings

1) Migration code has an immediate `NameError`  
- Ref: proposal lines 384-399. `ontos_migrate_structure.py` uses `docs_dir` without defining or resolving it, so the script would crash before creating or moving anything. Migration is currently non-functional as written.

2) Backward compatibility only covers `decision_history.md`  
- Ref: lines 402-423. Legacy paths for `archive/logs`, `archive/proposals`, and `reference/Common_Concepts.md` are not handled. Users on pre-v2.5.2 installs will still hit missing-path failures in consolidation/query until they manually migrate. Either broaden helper fallbacks to all expected legacy locations or run auto-migration in init.

3) Template source of truth is unclear, risking drift  
- Ref: lines 204-248. `create_starter_files` writes `DECISION_HISTORY_TEMPLATE` and `COMMON_CONCEPTS_TEMPLATE` literals, but the authoritative content for `Common_Concepts.md` already lives in `.ontos-internal/reference/Common_Concepts.md`. If the template text diverges, user-mode vocabulary will fork. Recommend copying from the shipped reference or centralizing the template once, reused by both modes.

4) User-mode test fixture is brittle and non-failing by default  
- Ref: lines 433-451. Fixture uses repo-relative paths and `subprocess.run` without `check=True`; if init prompts or fails, tests will pass while scaffolding is incomplete. Use absolute `PROJECT_ROOT` references, `check=True`, and explicit assertions on exit code plus created paths to make the fixture reliable.

5) CI plan does not enforce dual-mode coverage  
- Ref: lines 539-544. Testing requirements are listed but not wired into CI. Without a contributor/user matrix (or parametrized marker) in the pipeline, user-mode regressions will continue to slip through. Make the CI change part of the acceptance criteria.

---

## Recommendations
- Fix migration: resolve `docs_dir` inside `migrate()` via `resolve_config('DOCS_DIR', 'docs')` (or pass it in) and add unit coverage that fails on missing definitions.  
- Expand backward-compatibility: add fallbacks for archive/logs, archive/proposals, and concepts; or auto-migrate in `ontos_init.py` with a prompt/flag to stay transparent.  
- Single source of truth for templates: load `Common_Concepts.md` (and decision-history starter if present) from the bundled reference; avoid duplicating literals that can drift.  
- Harden user-mode fixture: use absolute paths, `check=True`, non-interactive flag enforcement, and assert all expected directories/files.  
- CI enforcement: add a matrix or marker so the suite runs in both contributor and user modes; block release on user-mode failures.

---

## Approval
- Status: **Changes required**. Re-review after migration fix, compatibility coverage, template sourcing, fixture hardening, and CI dual-mode enforcement are implemented.
