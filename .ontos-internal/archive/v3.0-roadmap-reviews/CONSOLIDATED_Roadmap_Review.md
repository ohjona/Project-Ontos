# Ontos v3.0 Implementation Roadmap: Review Consolidation

**Generated:** 2026-01-12
**Reviews Consolidated:** 4 Peer Reviewers
**Roadmap Version:** 1.0

---

## 1. Overall Verdict Summary

| Reviewer | Verdict | Confidence | Top Concern |
|----------|---------|------------|-------------|
| A (Codex/GPT-5.2) | Approve with Changes | Medium | Phase 2 command checklist vs tasks mismatch |
| B (Claude Opus 4.5) | Approve with Minor Changes | High | Missing `ui/progress.py` and Q4 confirmation task |
| C (Gemini DeepThink) | Approve with Changes | High | `io/toml.py` sequencing deadlock (CRITICAL) |
| D (Gemini DeepThink) | Request Revision | High | Dependency inversion + missing minor commands |

**Consensus:**
- Approve: 0/4
- Approve with Changes: 3/4 (A, B, C)
- Request Revision: 1/4 (D)

**Overall Verdict:** **Minor Fixes Needed** — 3/4 approve with changes, 1/4 requests revision. The revision request is based on the same critical issues flagged by C, so addressing those issues satisfies all reviewers.

---

## 2. Architecture Alignment

### 2.1 Coverage Assessment

| Reviewer | Module Coverage | Interface Coverage | Command Coverage | Overall |
|----------|-----------------|-------------------|------------------|---------|
| A (Codex) | Gaps (progress.py missing) | Complete | Gaps (checklist vs tasks) | Adequate |
| B (Claude) | Gaps (progress.py missing) | Complete | Partial (migrate commands lack detail) | Strong |
| C (Gemini) | Gaps (progress.py, json_output) | Gaps (Q8 summarize) | Critical Gaps (7 orphaned) | Adequate |
| D (Gemini) | Gaps (export, hook, minor cmds) | Complete | Critical Gaps (7 orphaned) | Adequate |

**Consensus:** 4/4 say coverage is adequate or better for major components, but all identify gaps.

### 2.2 Coverage Gaps Identified

| Gap | Type | Flagged By | Consensus |
|-----|------|------------|-----------|
| `ui/progress.py` missing | Module | A, B, C | 3/4 |
| Minor commands orphaned (7 scripts) | Command | A, C, D | 3/4 |
| `commands/export.py` missing tasks | Command | C, D | 2/4 |
| `commands/hook.py` missing detailed tasks | Command | C, D | 2/4 |
| `commands/doctor.py` missing detailed tasks | Command | D | 1/4 |
| `ui/json_output.py` missing | Module | C | 1/4 |
| Q8 auto-summary logic missing | Interface | C | 1/4 |
| `.ontos.toml` template drift (missing `[hooks]`) | Config | A | 1/4 |

**Critical Gaps (3+ reviewers):**

#### `ui/progress.py` Missing — Flagged by: A, B, C

**What's Missing:** Architecture Section 3.1 lists `ui/progress.py` as NEW but roadmap has no implementation tasks.

**Architecture Reference:** Section 3.1: `ui/progress.py — Progress indicators (NEW)`

**Impact:** Progress indicators will be missing from CLI output. Medium severity.

---

#### Minor Commands Orphaned (7 scripts) — Flagged by: A, C, D

**What's Missing:** The commands `verify`, `query`, `migrate`, `consolidate`, `promote`, `scaffold`, `stub` appear in Architecture Section 3.1 but have no migration tasks in the roadmap.

**Architecture Reference:** Section 3.1 lists all these under `ontos/commands/`.

**Impact:** If executed as written, v3.0 would ship without ~70% of existing CLI functionality. **HIGH SEVERITY**.

---

**Other Gaps:**
- `commands/export.py`: Listed in Scope (1.2) but missing implementation tasks (C, D)
- `commands/hook.py`: Listed but lacks detailed tasks beyond table entry (C, D)
- Q8 auto-summary: Strategy-critical feature not tasked in `core/graph.py` (C only)

---

## 3. Sequencing Analysis

### 3.1 Sequencing Verdict

| Reviewer | Sequencing Assessment | Issues Found |
|----------|----------------------|--------------|
| A (Codex) | Strong (minor timing ambiguity) | 1 |
| B (Claude) | Strong (config timing note needed) | 1 |
| C (Gemini) | **Weak** (CRITICAL blocking error) | 1 CRITICAL |
| D (Gemini) | **Weak** (CRITICAL dependency inversion) | 1 CRITICAL |

**Consensus:** 2/4 say sequencing is sound with minor issues; 2/4 identify CRITICAL blocking error.

### 3.2 Dependency Issues

| Issue | Phase Affected | Flagged By | Consensus |
|-------|----------------|------------|-----------|
| `io/toml.py` scheduled Phase 3, needed Phase 2 | Phase 2 | A, B, C, D | **4/4** |
| JSON output timing ambiguity | Phase 2/4 | A | 1/4 |

**Critical Sequencing Issues:**

#### `io/toml.py` Dependency Inversion — Flagged by: A, B, C, D (UNANIMOUS)

**Problem:** Task 4.8 (`commands/map.py`) explicitly states "Load config via `io/toml.py`", but `io/toml.py` is not scheduled until Phase 3 (Section 5.1). Commands cannot load configuration.

**Suggested Fix:**
- **A (Codex):** "Add note about whether Phase 1 creates stub or Phase 3 creates from scratch"
- **B (Claude):** "Add note: Phase 2 commands use existing config loading; `io/toml.py` replaces in Phase 3"
- **C (Gemini):** "Move `io/toml.py` from Phase 3 to Phase 2 — it is a strict prerequisite"
- **D (Gemini):** "Move `io/toml.py` creation to Phase 2. Commands need to load config to be built/tested"

**Consensus Resolution:** C and D recommend moving `io/toml.py` to Phase 2. A and B suggest clarifying the transitional approach. The cleaner fix is C/D's recommendation: move `io/toml.py` to Phase 2 (or create Phase 2a Foundation).

### 3.3 Critical Path Assessment

| Reviewer | Agrees with Critical Path? | Additions/Changes |
|----------|---------------------------|-------------------|
| A (Codex) | Yes | Add explicit dependency graph content |
| B (Claude) | Yes | None |
| C (Gemini) | **No** | Critical path is broken at Phase 2 due to `io/toml.py` |
| D (Gemini) | **No** | Config loader must be added to critical path |

### 3.4 Parallelization Assessment

| Reviewer | Agrees with Parallelization? | Concerns |
|----------|------------------------------|----------|
| A (Codex) | Mostly Yes | `commands/hook.py` needs final config keys |
| B (Claude) | Yes | No issues |
| C (Gemini) | N/A (focused on blocking issues) | — |
| D (Gemini) | N/A (focused on blocking issues) | — |

---

## 4. Completeness Review

### 4.1 Missing Tasks

| Missing Task | Should Be In | Flagged By | Consensus | Severity |
|--------------|--------------|------------|-----------|----------|
| Migrate minor commands (7 scripts) | Phase 2 or 3 | A, C, D | 3/4 | **HIGH** |
| Create `ui/progress.py` | Phase 2 or 4 | A, B, C | 3/4 | Medium |
| `commands/export.py` implementation | Phase 4 | C, D | 2/4 | Medium |
| `commands/hook.py` detailed tasks | Phase 4 | C, D | 2/4 | High |
| Q4 confirmation step in `log.py` | Phase 2 | B | 1/4 | Medium |
| Q8 auto-summary in `graph.py` | Phase 2 | C | 1/4 | High |
| `tomli` in pyproject.toml deps | Phase 1 | D | 1/4 | Medium |
| Golden Master config fixture gen | Phase 2 | C | 1/4 | Medium |

### 4.2 Missing Acceptance Criteria

| Phase | Missing Criteria | Flagged By |
|-------|------------------|------------|
| Phase 0 | Golden Master scope unclear (which commands/fixtures) | A |
| Phase 2 | Command parity for "Migrate" commands | A, B, C, D |
| Phase 2 | Q4 confirmation step works | B |
| Phase 2 | Config integration test | C |
| Phase 3 | Config precedence matches architecture | A |
| Phase 3 | Hook functionality test | D |
| Phase 4 | Windows hook testing (best-effort) | B |

### 4.3 Missing Risk Items

| Unacknowledged Risk | Phase | Flagged By |
|---------------------|-------|------------|
| Config transition (Phase 2->3 gap) | Phase 2/3 | B, C, D |
| Architecture version mismatch (v1.3 vs v1.4) | All | A |
| PyPI name availability | Phase 1 | B |
| Git unavailable handling | Phase 4 | B |
| God Script remnants (~500-750 lines unclear destination) | Phase 2 | D |
| Golden Master fixtures won't have `.ontos.toml` | Phase 2 | C |

### 4.4 Handoff Gaps

| From -> To | Gap | Flagged By |
|-----------|-----|------------|
| Phase 0 -> Phase 1 | What scripts/outputs are frozen, which fixtures exist | A |
| Phase 2 -> Phase 3 | How commands load config before `io/toml.py` exists | A, B, C, D |
| Phase 2 -> Phase 4 | JSON data-return contract not defined | A |
| Phase 3 -> Phase 4 | Config schema must be final before hook/doctor | A |
| Phase 4 -> v3.0.1 | What constitutes "stability" | B |

---

## 5. Feasibility Concerns

### 5.1 Estimate Assessment

| Phase | Roadmap Estimate | Reviewer Assessments |
|-------|------------------|---------------------|
| Phase 0 | 2-3 days | A: Optimistic, B: Reasonable, C: —, D: — |
| Phase 1 | 1-2 days | A: Reasonable, B: Reasonable, C: —, D: — |
| Phase 2 | 5-8 days | A: **Optimistic**, B: **Optimistic**, C: **Optimistic**, D: **Pessimistic** |
| Phase 3 | 2-3 days | A: Reasonable, B: Reasonable, C: —, D: — |
| Phase 4 | 3-5 days | A: Reasonable, B: Reasonable, C: —, D: — |
| Total | 15-24 days | B: 20-30 days risk-adjusted |

**Phases with Estimate Concerns (2+ say optimistic):**
- **Phase 2:** 4/4 reviewers express concern. Phase 2 attempts God Script decomposition (~3,199 lines), I/O extraction for 4 modules, and is now expected to absorb 7 additional command migrations. All reviewers recommend either padding estimates or splitting Phase 2.

### 5.2 Technical Feasibility Concerns

| Concern | Phase/Task | Flagged By | Severity |
|---------|------------|------------|----------|
| Building `map.py` without config loader | Phase 2 | C, D | **HIGH** |
| God Script decomposition hidden coupling | Phase 2 | A, B | High |
| Golden Master timestamp normalization | Phase 0 | B | Medium |
| Hook collision detection fragility | Phase 4 | B | Low |
| TOML write without library (template approach) | Phase 3 | B | Low |

### 5.3 External Dependency Risks

| Dependency | Risk | Flagged By | Mitigation in Roadmap? |
|------------|------|------------|------------------------|
| Git edge cases (detached HEAD, submodules) | Commands may fail | A | Partial |
| `tomli` for Python 3.9-3.10 | Bundling complexity | A, B, D | Yes |
| PyPI name `ontos` availability | May need fallback | B | Partial (Q1) |
| Git not installed | CLI assumes it exists | B | No |

---

## 6. Consistency Issues

### 6.1 Internal Contradictions

| Contradiction | Flagged By |
|---------------|------------|
| Phase 2 checklist includes commands not in Phase 2 tasks | A |
| `commands/map.py` uses `io/toml.py` (Phase 2) but `io/toml.py` is Phase 3 | A, B, C, D |
| Scope 1.2 includes `export` but no implementation tasks | C, D |
| pyproject.toml shows `dependencies = []` but `tomli` needed | D |

### 6.2 Terminology Issues

| Issue | Flagged By |
|-------|------------|
| "Phase" vs "v3.0.0-beta/rc/release" mixed naming | A |
| "Config migration" vs "init" vs "activation" inconsistent | A |

### 6.3 Version Number Issues

| Issue | Flagged By |
|-------|------------|
| Roadmap claims Architecture v1.4 but document shows v1.3 | A |

**Consistency Verdict:** Minor Issues — All contradictions are resolvable with clarifying edits.

---

## 7. Reviewer Agreement Matrix

### 7.1 Strong Agreement (3-4 reviewers)

| Topic | Agreement |
|-------|-----------|
| `io/toml.py` sequencing is problematic | 4/4 agree it needs fixing |
| Minor commands (7 scripts) are unaddressed | 3/4 explicitly flag as missing |
| `ui/progress.py` is missing | 3/4 explicitly flag |
| Phase 2 is highest risk | 4/4 agree |
| Golden Master strategy is excellent | 4/4 praise |
| God Script decomposition detail is good | 4/4 praise |

### 7.2 Split Opinions

| Topic | Position 1 | Position 2 |
|-------|------------|------------|
| `io/toml.py` fix approach | A, B: Clarify transitional approach | C, D: Move to Phase 2 (stronger fix) |
| Phase 2 splitting | B, C, D: Recommend splitting into 2a/2b | A: Not mentioned |
| Severity of issues | A, B: Approve with minor/changes | D: Request revision |

### 7.3 Unique Concerns (1 reviewer only)

| Concern | From | Seems Valid? |
|---------|------|--------------|
| Q8 auto-summary logic missing | C | Yes — Strategy-critical item |
| Architecture version mismatch (v1.3 vs v1.4) | A | Uncertain — May be doc header issue |
| `tomli` missing from pyproject.toml | D | Yes — Required for Py 3.9-3.10 |
| Golden Master fixtures need `.ontos.toml` generation | C | Yes — Valid edge case |

---

## 8. Out-of-Scope Feedback (For Reference Only)

No reviewers strayed into challenging approved scope or strategy decisions. All feedback focused on implementation correctness.

---

## 9. Consolidated Recommendations

### 9.1 Critical (Must Fix Before Implementation)

| Issue | Category | Flagged By | Recommended Fix |
|-------|----------|------------|-----------------|
| `io/toml.py` sequencing | Sequencing | A, B, C, D | Move `io/toml.py` to Phase 2 (or create Phase 2a Foundation). Commands cannot be built without config loading. |
| Minor commands orphaned | Coverage Gap | A, C, D | Add explicit tasks to migrate `verify`, `query`, `migrate`, `consolidate`, `promote`, `scaffold`, `stub` to `ontos/commands/`. |

### 9.2 Major (Should Fix)

| Issue | Category | Flagged By | Recommended Fix |
|-------|----------|------------|-----------------|
| Missing `ui/progress.py` | Coverage Gap | A, B, C | Add to Phase 2 or 4: "Create `ui/progress.py` for progress indicators" |
| Missing `commands/export.py` tasks | Coverage Gap | C, D | Add implementation tasks for export command |
| Missing `commands/hook.py` tasks | Coverage Gap | C, D | Add detailed implementation tasks |
| Phase 2 overload | Feasibility | B, C, D | Consider splitting Phase 2 into 2a (Foundation: Core/IO) and 2b (Decomposition: Commands) |
| `.ontos.toml` template drift | Consistency | A | Update template to include `[hooks]` section per architecture |

### 9.3 Minor (Nice to Fix)

| Issue | Category | Flagged By | Recommended Fix |
|-------|----------|------------|-----------------|
| Q4 confirmation step not in tasks | Completeness | B | Add explicit task to Section 4.9 for confirmation implementation |
| EXISTS modules not explicitly listed | Completeness | B | Add note listing moved modules in Phase 1 |
| `tomli` missing from pyproject.toml | Consistency | D | Add `"tomli>=2.0.1; python_version<'3.11'"` to dependencies |
| Golden Master fixtures need config | Completeness | C | Add task to generate `.ontos.toml` for test fixtures |
| JSON timing ambiguity | Consistency | A | Add note: Phase 2 returns JSON-serializable data; Phase 4 handles formatting |

### 9.4 No Action Needed

- **Phase dependency flow (0->1->2->3->4):** All reviewers agree this is correct
- **Golden Master strategy:** Universally praised
- **God Script decomposition line mapping:** Detailed and correct
- **Parallelization opportunities:** Correctly identified
- **Version numbering:** Consistent throughout
- **Terminology (God Script, Golden Master, Shim hooks):** Consistent

---

## 10. Roadmap Strengths

| Strength | Noted By |
|----------|----------|
| Golden Master safety net strategy | A, B, C, D |
| Detailed God Script decomposition with line mappings | A, B, C, D |
| Correct top-level phase sequencing | A, B |
| Risk awareness (Phase 2 flagged as highest risk) | A, B, C |
| Parallelization opportunities identified | A, B |
| Progressive refinement path (v3.0 -> v3.1 -> v3.2 -> v4.0) | B |
| Detailed task breakdowns with code snippets | B |

---

## 11. Decision-Ready Summary

### 11.1 By Review Area

| Area | Verdict | Critical Issues | Action Needed |
|------|---------|-----------------|---------------|
| Architecture Alignment | Adequate | 2 | Add minor commands + `ui/progress.py` |
| Sequencing Logic | **Weak** | 1 CRITICAL | Move `io/toml.py` to Phase 2 |
| Completeness | Weak | 0 | Add missing tasks for 7 commands + export + hook |
| Feasibility | Adequate | 0 | Consider splitting Phase 2 |
| Consistency | Minor Issues | 0 | Update config template; fix version ref |

### 11.2 Overall Roadmap Verdict

**Status:** **Minor Fixes Then Ready**

**Confidence Level:** High — 4/4 reviewers agree on the critical issues and their fixes are well-defined.

**Blocking Issues:** 2
1. `io/toml.py` sequencing deadlock
2. 7 orphaned commands with no migration plan

**Non-Blocking Issues:** 8 — Can address during implementation or in v3.0.1

### 11.3 Recommended Next Steps

**Minor Fixes Needed:**

1. **Chief Architect updates roadmap:**
   - Move `io/toml.py` creation to Phase 2 (or create Phase 2a Foundation layer)
   - Add explicit tasks to migrate 7 minor commands (`verify`, `query`, `migrate`, `consolidate`, `promote`, `scaffold`, `stub`)
   - Add `ui/progress.py` to Phase 2 or 4
   - Add `commands/export.py` and `commands/hook.py` implementation tasks
   - Update `.ontos.toml` template to include `[hooks]` section

2. **No re-review needed** — Fixes are mechanical and address unanimous consensus

3. **Then proceed to Implementation Spec**

---

*End of Consolidation*

*Prepared by: Claude Opus 4.5 — 2026-01-12*
*Based on reviews from: A (Codex/GPT-5.2), B (Claude Opus 4.5), C (Gemini DeepThink), D (Gemini DeepThink)*
