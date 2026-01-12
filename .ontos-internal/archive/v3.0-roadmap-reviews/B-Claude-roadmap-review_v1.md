# Ontos v3.0 Implementation Roadmap: Peer Review

**Reviewer:** Claude Opus 4.5
**Date:** 2026-01-12
**Roadmap Version:** 1.0

---

## 1. Architecture Coverage Check

### 1.1 Module Coverage

| Architecture Module | Roadmap Phase | Status | Notes |
|---------------------|---------------|--------|-------|
| `core/context.py` | — (EXISTS) | ⚠️ Partial | Not explicitly listed in any phase; implied to be moved in Phase 1 |
| `core/frontmatter.py` | — (EXISTS) | ⚠️ Partial | Not explicitly listed; implied |
| `core/staleness.py` | Phase 2 (Section 4.2, 4.10) | ✅ Covered | Listed as REFACTOR |
| `core/schema.py` | — (EXISTS) | ⚠️ Partial | Not explicitly listed; implied |
| `core/curation.py` | — (EXISTS) | ⚠️ Partial | Not explicitly listed; implied |
| `core/history.py` | Phase 2 (Section 4.2, 4.10) | ✅ Covered | Listed as REFACTOR |
| `core/paths.py` | Phase 2 (Section 4.2, 4.10) | ✅ Covered | Listed as REFACTOR |
| `core/config.py` | — (EXISTS) | ⚠️ Partial | Not explicitly listed; implied |
| `core/proposals.py` | Phase 2 (Section 4.2, 4.10) | ✅ Covered | Listed as REFACTOR |
| `core/graph.py` | Phase 2 (Section 4.1, 4.3) | ✅ Covered | Detailed task list |
| `core/validation.py` | Phase 2 (Section 4.1, 4.4) | ✅ Covered | Detailed task list |
| `core/types.py` | Phase 2 (Section 4.1, 4.5) | ✅ Covered | Detailed task list |
| `core/suggestions.py` | Phase 2 (Section 4.1) | ✅ Covered | Listed with line estimate |
| `core/tokens.py` | Phase 2 (Section 4.1) | ✅ Covered | Listed with line estimate |
| `io/git.py` | Phase 2 (Section 4.1, 4.6) | ✅ Covered | Detailed task list |
| `io/files.py` | Phase 2 (Section 4.1, 4.7) | ✅ Covered | Detailed task list |
| `io/toml.py` | Phase 3 (Section 5.2, 5.3) | ✅ Covered | Detailed task list |
| `ui/output.py` | Phase 1 | ⚠️ Partial | Mentioned in move; no modifications noted |
| `ui/json_output.py` | Phase 4 (Section 6.7) | ✅ Covered | Detailed task list |
| `ui/progress.py` | — | ❌ Missing | Architecture lists this; not in roadmap |
| `mcp/__init__.py` | v3.2.0+ (Section 9) | ✅ Covered | Explicitly deferred |
| `mcp/server.py` | v3.2.0+ (Section 9) | ✅ Covered | Explicitly deferred |

### 1.2 Command Coverage

| Architecture Command | Roadmap Phase | JSON Support | Status | Notes |
|----------------------|---------------|--------------|--------|-------|
| `ontos init` | Phase 3/4 (Section 5.4) | ✅ Yes | ✅ Covered | Detailed spec |
| `ontos map` | Phase 2/4 (Section 4.8) | ✅ Yes | ✅ Covered | From God Script |
| `ontos log` | Phase 2/4 (Section 4.9) | ✅ Yes | ✅ Covered | From God Script |
| `ontos doctor` | Phase 4 (Section 6.4) | ✅ Yes | ✅ Covered | Detailed spec |
| `ontos export` | Phase 4 (Section 6.6) | ❌ No | ✅ Covered | Template included |
| `ontos verify` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos query` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos migrate` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos consolidate` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos promote` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos scaffold` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos stub` | Phase 2 | ✅ Yes | ⚠️ Partial | Listed in table but no detailed tasks |
| `ontos hook` | Phase 4 (Section 6.5) | ❌ No | ✅ Covered | Detailed spec |

### 1.3 Interface Coverage

| Architecture Interface | Roadmap Location | Status |
|------------------------|------------------|--------|
| `find_project_root()` | Phase 2 / Section 4.7 (io/files.py) | ✅ Covered |
| `ValidationOrchestrator` | Phase 2 / Section 4.4 | ✅ Covered |
| `SessionContext` | — (EXISTS) | ⚠️ Partial |
| `OntosConfig` dataclass | Phase 2 / Section 4.5 | ✅ Covered |
| `DependencyGraph` dataclass | Phase 2 / Section 4.3 | ✅ Covered |
| Q4 Confirmation flow | Phase 2 / Section 4.9 | ⚠️ Partial |
| Q5 Version checking | Phase 3 / Section 5.6 | ✅ Covered |

### 1.4 Coverage Gaps

**Critical Gaps:**
1. **`ui/progress.py`** — Architecture Section 3.1 lists this as NEW; roadmap has no mention.

**Minor Gaps (existing modules not explicitly listed):**
2. Six "EXISTS" core modules (`context.py`, `frontmatter.py`, `schema.py`, `curation.py`, `config.py`) are implicitly moved in Phase 1 but not explicitly listed. Phase 1 says "Move `ontos/core/` modules (no changes to code yet)" which covers them, but explicit enumeration would reduce ambiguity.

**Partial Gaps (commands listed but not detailed):**
3. Commands `verify`, `query`, `migrate`, `consolidate`, `promote`, `scaffold`, `stub` appear in the Phase 4 table as "Migrate" but have no detailed task lists. These are existing scripts being converted, so they may need less detail, but the absence is notable.

---

## 2. Sequencing Analysis

### 2.1 Dependency Flow Check

| Phase | Depends On | Prerequisites Met? | Issues |
|-------|------------|-------------------|--------|
| Phase 0 (Golden Master) | None | ✅ Yes | N/A |
| Phase 1 (alpha) | Phase 0 | ✅ Yes | None |
| Phase 2 (beta) | Phase 1 | ✅ Yes | None |
| Phase 3 (rc) | Phase 2 | ✅ Yes | None |
| Phase 4 (release) | Phase 3 | ✅ Yes | None |
| v3.1.0 | v3.0.x | ✅ Yes | None |

**Dependency flow is correct.** Each phase properly builds on the previous one.

### 2.2 Sequencing Concerns

**Concern 1: `io/toml.py` in Phase 3 vs Phase 2 needs**

Section 4.8 (`commands/map.py`) says "Load config via `io/toml.py`" but `io/toml.py` is scheduled for Phase 3. This creates a sequencing issue.

**Resolution:** Looking more carefully, Phase 2 `commands/map.py` must rely on the existing config loading mechanism (the old `ontos_config.py` pattern) until Phase 3. The roadmap doesn't explicitly state this transitional approach.

**Recommendation:** Add note to Phase 2: "Commands use existing config loading pattern; `io/toml.py` replaces this in Phase 3."

---

**Concern 2: Q4 Confirmation Step Not Detailed**

Architecture Section 5.3 shows a detailed confirmation flow for `ontos log` (step 5: "CONFIRM CHANGES"). The roadmap's `commands/log.py` tasks (Section 4.9) don't explicitly include the confirmation step implementation.

**Recommendation:** Add explicit task to Section 4.9:
- [ ] Implement confirmation step per Q4 decision
  - Display changed files to user
  - Prompt for confirmation unless `--auto` flag

---

### 2.3 Parallelization Assessment

| Roadmap Says Parallelizable | Actually Parallelizable? | Notes |
|-----------------------------|-------------------------|-------|
| `io/toml.py` after Phase 1 | ✅ Yes | Independent of God Script decomposition |
| `commands/doctor.py` after Phase 2 | ✅ Yes | New command, no dependencies |
| `ui/json_output.py` after Phase 2 | ✅ Yes | Independent formatting layer |
| Documentation after Phase 3 | ✅ Yes | Can draft while Phase 4 completes |
| `commands/export.py` after Phase 3 | ✅ Yes | New command, independent |

**Assessment:** Parallelization opportunities are correctly identified. No issues.

### 2.4 Critical Path Assessment

Roadmap identifies critical path as:
1. Phase 0 (Golden Master) — Blocks everything
2. Phase 2 (God Script Decomposition) — Highest risk, longest duration
3. Phase 4 (CLI) — Cannot ship without complete CLI

**Assessment:** Critical path is correctly identified. The roadmap properly flags Phase 2 as highest risk.

---

## 3. Completeness Review

### 3.1 Missing Tasks

| Gap | Should Be In | Impact | Severity |
|-----|--------------|--------|----------|
| `ui/progress.py` creation | Phase 2 or 4 | Progress indicators missing from CLI | Medium |
| Q4 confirmation implementation | Phase 2 (Section 4.9) | User confirmation not implemented | Medium |
| Commands `verify`, `query`, etc. task details | Phase 2 | Implementation guidance missing | Low |
| "EXISTS" module explicit listing | Phase 1 | Ambiguity in what gets moved | Low |
| Transitional config note | Phase 2 | Unclear how config works before Phase 3 | Low |

### 3.2 Missing Acceptance Criteria

| Phase | Criteria Gap | Suggested Criteria |
|-------|--------------|-------------------|
| Phase 2 | No criterion for Q4 confirmation | "Confirmation step works per architecture Section 5.3" |
| Phase 2 | No criterion for "Migrate" commands | "Commands `verify`, `query`, etc. work with existing behavior" |
| Phase 4 | No criterion for Windows testing | "Shim hooks tested on Windows (best-effort documented)" |

### 3.3 Missing Risk Items

| Unacknowledged Risk | Phase | Why It Matters |
|---------------------|-------|----------------|
| Config transition (Phase 2→3) | Phase 2/3 | Commands need config loading before `io/toml.py` exists |
| PyPI name availability | Phase 1 | `ontos` may not be available; fallback needed |
| Test fixture maintenance | All | Golden Master fixtures may drift from real projects |

### 3.4 Handoff Gaps

| From Phase | To Phase | Unclear Handoff |
|------------|----------|-----------------|
| Phase 2 | Phase 3 | How do commands load config in Phase 2 without `io/toml.py`? |
| Phase 4 | v3.0.1 | What constitutes "stability" for v3.0.x before v3.1.0? |

---

## 4. Feasibility Concerns

### 4.1 Estimate Assessment

| Phase | Roadmap Estimate | My Assessment | Notes |
|-------|------------------|---------------|-------|
| Phase 0 | 2-3 days | Reasonable | Fixture creation is straightforward |
| Phase 1 | 1-2 days | Reasonable | Mostly file moves and import fixes |
| Phase 2 | 5-8 days | **Optimistic** | God Script decomposition with hidden coupling is complex |
| Phase 3 | 2-3 days | Reasonable | Config is well-specified |
| Phase 4 | 3-5 days | Reasonable | CLI wiring is mechanical |
| Phase 5 | 2-3 days | Reasonable | Polish work |
| **Total** | 15-24 days | 20-30 days | Phase 2 risk-adjusted |

**Phase 2 Concern:** The roadmap acknowledges Phase 2 as "Highest Risk" but the 5-8 day estimate may be optimistic given:
- 3,199 lines of code to decompose (1,904 + 1,295)
- 4 modules requiring I/O extraction refactoring
- ~500-750 unaccounted lines
- Integration testing complexity

**Recommendation:** The "Risk-Adjusted Estimate" section (Section 12.2) is appropriately conservative (15-30 days range). Ensure planning uses the realistic/pessimistic end.

### 4.2 Technical Feasibility

| Task | Concern | Severity |
|------|---------|----------|
| TOML write without library | Writing TOML with template-based approach may lose structure | Low |
| Hook collision detection | Identifying "is this an Ontos hook?" may be fragile | Low |
| Golden Master timestamp normalization | Timestamps in output may be hard to normalize consistently | Medium |

### 4.3 Dependency Risks

| External Dependency | Risk | Mitigation in Roadmap? |
|---------------------|------|------------------------|
| PyPI availability for `ontos` name | Name may be taken | ⚠️ Partial (Q1 in Section 14) |
| `tomli` for Python 3.9-3.10 | Bundling adds complexity | ✅ Yes (Section 5.2) |
| Git availability | CLI assumes git installed | ❌ No explicit handling |

---

## 5. Consistency Check

### 5.1 Internal Contradictions

| Contradiction | Location 1 | Location 2 | Severity |
|---------------|------------|------------|----------|
| God Script line count | Section 1.3: "1,904 lines" + "1,295 lines" = 3,199 | Section 1.2: "3,199-line God Scripts" | ✅ Consistent |
| Config loading timing | Section 4.8 implies `io/toml.py` needed | Section 5 places `io/toml.py` in Phase 3 | ⚠️ Minor |
| Module count | Architecture: 10 core modules | Roadmap: doesn't enumerate | ⚠️ Minor |

### 5.2 Terminology Consistency

| Term | Usage Issue |
|------|-------------|
| "God Script" | Consistent throughout ✅ |
| "Golden Master" | Consistent throughout ✅ |
| "Shim hooks" | Consistent throughout ✅ |

### 5.3 Version Number Consistency

| Location | Version | Consistent? |
|----------|---------|-------------|
| Document header | 1.0 | ✅ |
| pyproject.toml spec | 3.0.0a1 | ✅ |
| All phase tags | Correct progression | ✅ |

**Version numbers are consistent throughout.**

---

## 6. Recommendations

### 6.1 Critical (Must Fix)

None. The roadmap has no critical blocking issues.

### 6.2 Major (Should Fix)

| Issue | Section | Recommended Fix |
|-------|---------|-----------------|
| Missing `ui/progress.py` | Section 4.1 or 6.1 | Add: "Create `ui/progress.py` for progress indicators" |
| Q4 confirmation not in tasks | Section 4.9 | Add explicit confirmation implementation task |
| Config loading transition unclear | Section 4 | Add note: "Phase 2 commands use existing config loading; `io/toml.py` replaces in Phase 3" |

### 6.3 Minor (Nice to Fix)

| Issue | Section | Recommended Fix |
|-------|---------|-----------------|
| "EXISTS" modules not explicitly listed | Section 3.1 | Add: "EXISTS modules (context.py, frontmatter.py, schema.py, curation.py, config.py) move without changes" |
| "Migrate" commands lack detail | Section 6.2 | Add brief notes: "These commands migrate from existing scripts with minimal changes" |
| Git unavailable not handled | Section 6.5 | Add: "If git not installed, `ontos init` exits with error code 4 and helpful message" |
| PyPI name risk | Section 14 | Promote Q1 to resolved decision or add fallback plan |

### 6.4 Suggestions (Optional Improvements)

1. **Add a dependency diagram for Phase 2 modules** — Would help visualize which modules depend on each other during decomposition.

2. **Add rollback strategy for each phase** — If Phase 2 decomposition fails catastrophically, what's the recovery plan?

3. **Add "definition of done" for each module** — Beyond acceptance criteria, what does "complete" mean for `core/graph.py` specifically?

4. **Consider splitting Phase 2** — Phase 2 is very dense. Could be 2a (extract core modules) and 2b (create commands), reducing risk.

---

## 7. Summary Assessment

### 7.1 Overall Verdict

| Aspect | Rating | Notes |
|--------|--------|-------|
| Architecture Alignment | **Strong** | All major components covered; minor gaps in existing module enumeration |
| Sequencing Logic | **Strong** | Dependencies flow correctly; minor config timing clarification needed |
| Completeness | **Adequate** | Main paths covered; some detail missing for "Migrate" commands |
| Feasibility | **Adequate** | Phase 2 estimates optimistic but risk-adjusted section compensates |
| Consistency | **Strong** | Terminology and versioning consistent throughout |

### 7.2 Recommendation

**Overall:** ✅ **Approve with Minor Changes**

The roadmap correctly translates the approved architecture into a buildable implementation plan. The phase structure is logical, dependencies flow correctly, and high-risk areas are appropriately flagged. 

### 7.3 Confidence Level

**High** — The roadmap is well-structured and comprehensive. The gaps identified are minor and don't affect the ability to begin implementation.

### 7.4 Key Strengths

1. **Detailed task breakdown** — Phase 2-4 tasks are exceptionally well-specified with code snippets
2. **Risk awareness** — Phase 2 is correctly flagged as highest risk with mitigations
3. **Golden Master strategy** — Excellent safety net for high-risk decomposition
4. **Parallelization identified** — Good understanding of what can be done concurrently
5. **Progressive refinement** — v3.0 → v3.1 → v3.2 → v4.0 progression is clear

### 7.5 Key Concerns (Ranked by Severity)

1. **Missing `ui/progress.py`** — Architecture component not in roadmap (Medium)
2. **Q4 confirmation implementation missing from tasks** — Required feature not explicitly tasked (Medium)
3. **Phase 2 estimate potentially optimistic** — Risk-adjusted range compensates, but watch closely (Low)

---

## 8. Verification Checklist Summary

| Architecture Section | Roadmap Coverage |
|---------------------|------------------|
| Section 2 (Distribution Model) | ✅ Covered (pip, global CLI, local data) |
| Section 3 (Package Structure) | ✅ Covered (Phase 1) |
| Section 4 (Module Specs) | ✅ Mostly Covered (missing progress.py) |
| Section 5 (Data Flows) | ✅ Covered (Q4 confirmation needs explicit task) |
| Section 6 (Configuration) | ✅ Covered (Phase 3) |
| Section 7 (CLI Architecture) | ✅ Covered (Phase 4) |
| Section 8 (Git Integration) | ✅ Covered (Phase 3-4) |
| Section 9 (Scalability) | ⚠️ Implicit (depth flags, auto-summary not detailed) |
| Section 10 (Testing) | ✅ Covered (Phase 0, coverage targets) |
| Section 11 (v4.0 Extension Points) | ✅ Covered (Sections 9-10) |
| Section 12 (Constraints) | ✅ Covered (Python version, deps, behavioral) |
| Section 13 (Migration Strategy) | ✅ Covered (Phase 1-4 map to migration phases) |

---

*End of Review*

*Reviewer: Claude Opus 4.5 — 2026-01-12*