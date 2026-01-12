# Ontos v3.0 Implementation Roadmap: Peer Review

**Reviewer:** Peer Architect [Gemini DeepThink]
**Date:** 2026-01-12
**Roadmap Version:** 1.0

---

## 1. Architecture Coverage Check

### 1.1 Module Coverage

| Architecture Module | Roadmap Phase | Status |
| --- | --- | --- |
| `core/graph.py` | Phase 2 | ✅ Covered |
| `core/validation.py` | Phase 2 | ✅ Covered |
| `core/types.py` | Phase 2 | ✅ Covered |
| `io/git.py` | Phase 2 | ✅ Covered |
| `io/files.py` | Phase 2 | ✅ Covered |
| `io/toml.py` | **Phase 3** | ❌ **Sequencing Error** (Required in Phase 2) |
| `ui/json_output.py` | **Missing** | ❌ **Missing** (Arch 3.1 lists as NEW) |
| `ui/progress.py` | **Missing** | ❌ **Missing** (Arch 3.1 lists as NEW) |
| `commands/map.py` | Phase 2 | ✅ Covered |
| `commands/log.py` | Phase 2 | ✅ Covered |
| `commands/init.py` | Phase 3 | ✅ Covered |
| `commands/verify.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/query.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/scaffold.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/stub.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/promote.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/migrate.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/consolidate.py` | **Missing** | ❌ **Orphaned** (Not scheduled for migration) |
| `commands/export.py` | **Missing** | ❌ **Missing** (Arch 1.4 / Roadmap 1.2 list it) |

### 1.2 Interface Coverage

| Architecture Interface | Roadmap Location | Status |
| --- | --- | --- |
| `find_project_root()` | Phase 2 (4.7) | ✅ Covered |
| `ValidationOrchestrator` | Phase 2 (4.4) | ✅ Covered |
| `summarize_graph()` (Q8) | **Missing** | ❌ **Missing** (Strategy Critical) |

### 1.3 Command Coverage

| Architecture Command | Roadmap Phase | JSON Support Noted? | Status |
| --- | --- | --- | --- |
| `ontos map` | Phase 2 | Yes (4.8) | ✅ Covered |
| `ontos log` | Phase 2 | Implicit | ✅ Covered |
| `ontos init` | Phase 3 | N/A | ✅ Covered |
| `ontos export` | **Missing** | N/A | ❌ **Missing Tasks** |

### 1.4 Coverage Gaps

1. **Orphaned Commands:** The roadmap focuses entirely on decomposing the two "God Scripts" (`map`, `log`) but omits the migration of the ~7 other existing scripts (`verify`, `query`, `consolidate`, `promote`, `migrate`, `scaffold`, `stub`). These are listed in Architecture Section 3.1. Without explicit tasks to migrate them to the new `ontos/commands/` structure, they will be lost in the v3.0 transition, breaking existing workflows.
2. **Missing Modules:** `ui/json_output.py` and `ui/progress.py` are defined in Architecture 3.1 but do not appear in Roadmap deliverables.
3. **Q8 Strategy Gap:** The "Auto-summary" feature (Critical priority in Strategy) is missing. `core/graph.py` tasks include `calculate_depths` but lack the actual summarization logic.
4. **Export Feature:** `ontos export` is listed in Roadmap Scope Summary (1.2) but has no implementation tasks.

---

## 2. Sequencing Analysis

### 2.1 Dependency Flow Check

| Phase | Depends On | Prerequisites Met? | Issues |
| --- | --- | --- | --- |
| Phase 1 (Alpha) | Phase 0 | ✅ |  |
| Phase 2 (Beta) | Phase 1 | ❌ **Blocking** | **CRITICAL:** Task 4.8 (`commands/map.py`) explicitly states: "Load config via `io/toml.py`". However, `io/toml.py` is not scheduled for creation until Phase 3 (Section 5.1). The Command layer cannot function without the IO layer. |
| Phase 3 (RC) | Phase 2 | ✅ |  |

### 2.2 Sequencing Concerns

**Config Loading Deadlock:**

* **Issue:** Phase 2 constructs the primary commands (`map`, `log`). These commands depend on `OntosConfig` to locate files. The loader for this config (`io/toml.py`) is scheduled for Phase 3.
* **Result:** Developers implementing Phase 2 will be forced to mock the configuration layer or write throwaway code, increasing waste and risk.

### 2.3 Critical Path Assessment

The critical path is broken at Phase 2. The `io/toml.py` module must be moved to Phase 2 (or Phase 2a) to serve as the foundation for the commands.

---

## 3. Completeness Review

### 3.1 Missing Tasks

| Gap | Should Be In | Impact |
| --- | --- | --- |
| **Create `io/toml.py**` | Phase 2 | **High** (Blocks `map` and `log` commands) |
| **Migrate Minor Commands** | Phase 2 or 3 | **High** (CLI missing ~70% of commands) |
| **Implement Q8 Logic** | Phase 2 (`core/graph.py`) | **High** (Critical Strategy Item) |
| **Create UI Modules** | Phase 2 | **Medium** (Missing dependencies) |
| **Implement `commands/export.py**` | Phase 3 or 4 | **Medium** (Missing Feature) |
| **Update `cli.py` dispatch** | Phase 2 | **Medium** (Commands unreachable) |

### 3.2 Missing Acceptance Criteria

| Phase | Criteria Gap | Suggested Criteria |
| --- | --- | --- |
| Phase 2 | Config Integration | "Commands successfully load config from .ontos.toml" |
| Phase 2 | Command Parity | "All minor commands (verify, etc.) migrated and functional" |

### 3.4 Handoff Gaps

**Golden Master Config Data:**

* **Gap:** The Golden Master tests (Phase 0) capture v2.9 output using the old `ontos_config.py`. The new Phase 2 commands will attempt to read `.ontos.toml`. The Golden Master fixtures (snapshots of old repos) will not have `.ontos.toml` files.
* **Impact:** The new commands will fail in the test harness due to missing config.
* **Fix:** Phase 2 needs a task to "Generate .ontos.toml for Golden Master fixtures" to bridge the gap.

---

## 4. Feasibility Concerns

### 4.1 Estimate Assessment

| Phase | Roadmap Estimate | My Assessment | Concern |
| --- | --- | --- | --- |
| Phase 2 | Decompose 2 God Scripts | **Optimistic** | Phase 2 is a "Big Bang" refactor. It attempts to build the Core, IO, Types, Validation layers AND refactor the two largest scripts simultaneously. |

### 4.2 Technical Feasibility

| Task | Concern | Severity |
| --- | --- | --- |
| `map.py` without `toml.py` | Building the main command without the config loader is architecturally impossible without mocking. | High |

---

## 5. Consistency Check

### 5.1 Internal Contradictions

| Contradiction | Location 1 | Location 2 |
| --- | --- | --- |
| **Config Loader Timing** | 4.8 (`map.py` uses `io/toml`) | 5.1 (`io/toml` created in Phase 3) |
| **Export Feature** | 1.2 (Scope includes `export`) | 4 & 5 (No tasks to create it) |

---

## 6. Recommendations

### 6.1 Critical (Must Fix)

| Issue | Section | Recommended Fix |
| --- | --- | --- |
| **Sequencing Deadlock** | 4.1 & 5.1 | **Move `io/toml.py` from Phase 3 to Phase 2.** It is a strict prerequisite for Command implementation. |
| **Orphaned Commands** | 4.1 / 5.1 | **Add "Migrate Minor Commands" tasks.** Explicitly list `verify`, `query`, `scaffold`, `promote`, `migrate`, `stub`, `consolidate` for migration to `commands/`. |
| **Missing Q8 Logic** | 4.3 | **Add `summarize_graph` task.** Add task to implement graph summarization/truncation in `core/graph.py` (Strategy Critical). |

### 6.2 Major (Should Fix)

| Issue | Section | Recommended Fix |
| --- | --- | --- |
| **Phase 2 Overload** | 4.0 | **Split Phase 2.** Create **Phase 2a (Foundation)**: Core types, IO layer, Validation; and **Phase 2b (Decomposition)**: Map/Log/Commands. |
| **Golden Master Config** | 4.1 | **Add Config Gen Task.** "Generate .ontos.toml for Golden Master fixtures" to allow new commands to run in test environment. |
| **Missing Export** | 5.1 | **Add Export Tasks.** Add `commands/export.py` tasks to Phase 3 or 4. |

### 6.3 Minor (Nice to Fix)

| Issue | Section | Recommended Fix |
| --- | --- | --- |
| **Missing UI Modules** | 4.1 | Add `ui/json_output.py` and `ui/progress.py` to Phase 2 deliverables. |

---

## 7. Summary Assessment

### 7.1 Overall Verdict

| Aspect | Rating | Notes |
| --- | --- | --- |
| Architecture Alignment | **Adequate** | Major components aligned, but ~7 minor commands and UI modules missing. |
| Sequencing Logic | **Weak** | **Critical Blocking Error:** Command layer scheduled before its I/O dependency (`toml`). |
| Completeness | **Weak** | Missing tasks for minor commands, export feature, and Q8 logic. |
| Feasibility | **Adequate** | Phase 2 is risky/dense; Golden Master strategy mitigates this well. |
| Consistency | **Strong** | Terminology and versioning consistent. |

### 7.2 Recommendation

**Approve with Changes**

**Required Changes:**

1. Resolve the `io/toml.py` sequencing deadlock (move to Phase 2).
2. Add tasks to migrate the ~7 orphaned minor commands.
3. Add tasks for Q8 Auto-summary logic.
4. Add tasks for `ontos export`.

### 7.3 Confidence Level

**High** — The dependency error on `io/toml.py` renders Phase 2 unimplementable as written. The omission of minor commands would result in a significant regression in CLI functionality.

### 7.4 Key Strengths

1. **Golden Master Strategy:** This is the correct approach to de-risk the massive refactor.
2. **Explicit Decomposition:** The line-by-line mapping of old scripts to new modules (Section 4.1) is excellent.

### 7.5 Key Concerns

1. **Sequencing Deadlock:** `io/toml.py` must exist before Phase 2.
2. **Orphaned Commands:** Missing migration plan for `verify`, `query`, `promote`, etc.
3. **Phase 2 Complexity:** Phase 2 is overloaded; splitting it would improve manageability.