---
id: v2_codex_v2_5_2_review
type: strategy
status: draft
depends_on: [v2_5_2_dual_mode_remediation]
concepts: [architecture, migration, testing, scaffolding]
---

# Review: V2.5.2 Dual-Mode Remediation Plan (Codex V2)

**Date:** 2025-12-17  
**Reviewer:** Codex (Architect)  
**Scope:** Latest `v2.5.2_dual_mode_remediation.md`

---

## Verdict
- Do **not** treat as done yet. Core gaps remain on template sourcing, backward-compat coverage, and CI wiring. Implementation checklist is still unchecked despite FINAL status.

---

## Blocking Findings

1) Template source of truth still not addressed  
- Ref: plan lines ~205-248. `create_starter_files` writes inline `DECISION_HISTORY_TEMPLATE`/`COMMON_CONCEPTS_TEMPLATE`. The checklist promised loading from shipped reference files to prevent drift. Without sourcing from `.ontos-internal/reference/Common_Concepts.md` (and any decision-history template), user-mode vocab and starters will diverge from canonical content.

2) Backward compatibility only specified for `decision_history.md`  
- Ref: plan lines ~432-464. Helpers for legacy `archive/logs`, `archive/proposals`, and `reference/Common_Concepts.md` are mentioned but no code paths are defined. Pre-v2.5.2 installs may still fail consolidation/query until users manually migrate. Needs concrete helper logic (or init-based auto-fix) for all legacy locations.

3) CI matrix example lacks binding to actual mode selection  
- Ref: plan lines ~592-620. The matrix runs `pytest --mode=...`, but there is no documented fixture/flag in the plan to consume `--mode` (env var, conftest hook, etc.). As written, CI will not exercise user mode. Need explicit wiring instructions for how tests switch modes.

---

## Observations

- Status set to FINAL/active, but all Phase 1/2/3 checklist boxes remain unchecked. This creates ambiguity on whether work is done or pending. Consider marking completed items or reclassifying as “accepted tasks” until code lands.
- Migration warnings cover only `decision_history.md`; if `Common_Concepts.md` exists in an unexpected location, there is no warning or remediation path. Users can stay broken without guidance.

---

## Recommendations

- Implement template sourcing from canonical files (or a single shared constant) and update the plan to reflect the concrete mechanism.  
- Provide full backward-compat helper code for archive/logs, archive/proposals, and concepts, or move those via init with deprecation messaging.  
- Specify how `--mode` is honored in tests (e.g., conftest reading an env/CLI flag to configure DOCS_DIR/setup) so the CI matrix actually exercises both modes.  
- Align status with execution: check off completed items or keep the document in draft until code is merged.
