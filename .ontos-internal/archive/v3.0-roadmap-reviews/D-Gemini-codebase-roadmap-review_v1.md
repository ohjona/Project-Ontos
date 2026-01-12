# Ontos v3.0 Implementation Roadmap: Peer Review

**Reviewer:** LLM [D] (Gemini DeepThink)
**Date:** 2026-01-12
**Roadmap Version:** 1.0

---

## 1. Architecture Coverage Check

### 1.1 Module Coverage

| Architecture Module | Roadmap Phase | Status | Notes |
| --- | --- | --- | --- |
| `core/graph.py` | Phase 2 | ✅ Covered | Detailed tasks in 4.3 |
| `core/validation.py` | Phase 2 | ✅ Covered | Detailed tasks in 4.4 |
| `io/files.py` | Phase 2 | ✅ Covered | Detailed tasks in 4.7 |
| `io/git.py` | Phase 2 | ✅ Covered | Detailed tasks in 4.6 |
| `io/toml.py` | Phase 3 | ❌ **Late** | **Critical Sequence Error:** Required by Phase 2 commands (see Sec 2) |
| `commands/map.py` | Phase 2 | ✅ Covered | Detailed tasks in 4.8 |
| `commands/log.py` | Phase 2 | ✅ Covered | Detailed tasks in 4.9 |
| `commands/init.py` | Phase 3 | ✅ Covered | Deliverable in 5.1 |
| `commands/doctor.py` | Phase 2 | ⚠️ Partial | Listed in 4.1 table, but **no detailed tasks** defined. |
| `commands/hook.py` | Phase 2 | ⚠️ Partial | Listed in 4.1 table, but **no detailed tasks** defined. |
| `commands/export.py` | **Missing** | ❌ Missing | Scope 1.2 lists it; Missing from 4.1 table & detailed tasks. |
| `commands/verify.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |
| `commands/promote.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |
| `commands/stub.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |
| `commands/scaffold.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |
| `commands/query.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |
| `commands/migrate.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |
| `commands/consolidate.py` | **Missing** | ❌ Missing | Architecture 3.1 lists it; no migration task. |

### 1.2 Interface Coverage

| Architecture Interface | Roadmap Location | Status |
| --- | --- | --- |
| `find_project_root()` | Phase 2 (4.7) | ✅ Covered |
| `write_text_file()` | Phase 2 (4.7) | ✅ Covered |
| `ValidationOrchestrator` | Phase 2 (4.4) | ✅ Covered |
| `DependencyGraph` | Phase 2 (4.3) | ✅ Covered |
| `OntosConfig` | Phase 2 (4.5) | ✅ Covered |

### 1.3 Command Coverage

| Architecture Command | Roadmap Phase | Status |
| --- | --- | --- |
| `ontos map` | Phase 2 | ✅ Covered |
| `ontos log` | Phase 2 | ✅ Covered |
| `ontos init` | Phase 3 | ✅ Covered |
| `ontos doctor` | Phase 2 (implied) | ⚠️ Missing implementation details |
| `ontos export` | — | ❌ Missing implementation tasks |
| `ontos hook` | — | ❌ Missing implementation tasks |
| `ontos [verify/promote/etc]` | — | ❌ Missing migration tasks for 7 legacy scripts |

### 1.4 Coverage Gaps

1. **Migration of Minor Commands:** The Architecture (Sec 3.1) explicitly lists `verify`, `query`, `migrate`, `consolidate`, `promote`, `scaffold`, `stub` in the `ontos/commands/` directory. The Roadmap ignores these entirely. If executed as written, v3.0 will launch without 70% of existing functionality.
2. **`commands/export.py`:** Explicitly listed in Roadmap Scope Summary (1.2) as a v3.0 feature but absent from implementation phases.
3. **`commands/hook.py`:** Architecture 1.4 defines this module for dispatching hooks. Roadmap Phase 4.1 lists it, but no detailed implementation tasks exist (unlike `map`/`log`).

---

## 2. Sequencing Analysis

### 2.1 Dependency Flow Check

| Phase | Depends On | Prerequisites Met? | Issues |
| --- | --- | --- | --- |
| Phase 0 | None | ✅ |  |
| Phase 1 | Phase 0 | ✅ |  |
| Phase 2 | Phase 1 | ❌ **NO** | **BLOCKER:** Task 4.8 (`commands/map.py`) requires "Load config via `io/toml.py`", but `io/toml.py` is not built until Phase 3 (5.1). |
| Phase 3 | Phase 2 | ✅ |  |

### 2.2 Sequencing Concerns

**Critical Dependency Inversion (TOML Loader):**

* **Issue:** Phase 2 involves building `commands/map.py` and `commands/log.py`.
* **Roadmap:** Task 4.8 explicitly states: "Load config via `io/toml.py`".
* **Conflict:** `io/toml.py` is listed as a deliverable for Phase 3 (Section 5.1).
* **Result:** Developers cannot complete Phase 2 because they cannot load configuration.

### 2.3 Critical Path Assessment

The critical path is Phase 2 (Decomposition). Adding the config loader (`io/toml.py`) to this path is necessary for the refactored commands to function.

---

## 3. Completeness Review

### 3.1 Missing Tasks

| Gap | Should Be In | Impact |
| --- | --- | --- |
| **Migration of Minor Commands** | Phase 2 (or 2b) | **High.** `verify`, `promote`, `stub`, `scaffold`, etc. must be ported to the new `ontos/commands/` structure. |
| **`commands/export.py` Logic** | Phase 4 | **Medium.** Listed in Scope (1.2), but missing from implementation steps. |
| **`commands/hook.py` Logic** | Phase 3 | **High.** The shim hooks delegate to this command. Without it, hooks crash. |
| **`tomli` Dependency Definition** | Phase 1 (3.2) | **Medium.** `pyproject.toml` spec lists `dependencies = []`. Must include `tomli; python_version < "3.11"`. |

### 3.2 Missing Acceptance Criteria

| Phase | Criteria Gap | Suggested Criteria |
| --- | --- | --- |
| Phase 2 | Minor Command Migration | "All v2 scripts ported to `ontos/commands/` and accessible via CLI" |
| Phase 3 | Hook Functionality | "Pre-push hook successfully invokes `ontos hook pre-push`" |

### 3.4 Handoff Gaps

* **God Script Remnants:** Roadmap mentions "Unaccounted lines (~500-750)". Phase 2 Exit Criteria says "God Scripts reduced to <300 lines". It is unclear *where* the remaining logic goes if not into the specified modules. There is a risk of "orphan logic" being deleted accidentally.

---

## 4. Feasibility Concerns

### 4.1 Estimate Assessment

| Phase | Roadmap Estimate | My Assessment | Concern |
| --- | --- | --- | --- |
| Phase 2 | "Highest Risk" | **Pessimistic** | Migrating 2 God Scripts + 8 minor scripts (forgotten) + IO extraction is a massive workload. |

### 4.2 Technical Feasibility

| Task | Concern | Severity |
| --- | --- | --- |
| `io/toml.py` in Phase 3 | Commands in Phase 2 need config to run/test. Circular dependency. | **High** |

---

## 5. Consistency Check

### 5.1 Internal Contradictions

| Contradiction | Location 1 | Location 2 |
| --- | --- | --- |
| **Export Feature** | Sec 1.2: "v3.0 includes `ontos export`" | Sec 3/4/5: No tasks to build `export.py` |
| **Dependencies** | Sec 5.2: Mentions `tomli` | Sec 3.2: `dependencies = []` |

---

## 6. Recommendations

### 6.1 Critical (Must Fix)

| Issue | Section | Recommended Fix |
| --- | --- | --- |
| **Dependency Inversion** | Sec 4 vs 5 | **Move `io/toml.py` creation to Phase 2.** Commands need to load config to be built/tested. |
| **Missing Minor Commands** | Sec 3.3 or 4.1 | **Add tasks to move/wrap** `ontos_verify.py`, `ontos_promote.py`, `ontos_scaffold.py`, `ontos_stub.py`, `ontos_migrate.py`, `ontos_consolidate.py`, `ontos_query.py` into `ontos/commands/`. |

### 6.2 Major (Should Fix)

| Issue | Section | Recommended Fix |
| --- | --- | --- |
| **Missing `hook` Tasks** | Sec 4.x | Add detailed implementation tasks for `commands/hook.py`. |
| **Missing `export` Tasks** | Sec 4.x | Add detailed implementation tasks for `commands/export.py`. |
| **Missing `doctor` Tasks** | Sec 4.x | Add detailed implementation tasks for `commands/doctor.py`. |
| **Missing `tomli` Dep** | Sec 3.2 | Update `pyproject.toml` spec: `dependencies = ["tomli>=2.0.1; python_version<'3.11'"]`. |

### 6.3 Minor (Nice to Fix)

| Issue | Section | Recommended Fix |
| --- | --- | --- |
| **Split Phase 2** | Sec 4 | Consider splitting Phase 2 into **2a (Core/IO/Refactor)** and **2b (Commands)**. Current scope is extremely large. |

---

## 7. Summary Assessment

### 7.1 Overall Verdict

| Aspect | Rating | Notes |
| --- | --- | --- |
| Architecture Alignment | **Adequate** | Covers the major architectural shifts but misses 7+ commands. |
| Sequencing Logic | **Weak** | **Critical flaw:** Config loader placed *after* the commands that use it. |
| Completeness | **Weak** | Misses tasks for `export`, `hook`, `doctor` logic, and legacy script migration. |
| Feasibility | **Adequate** | Estimates are reasonable barring the missing scope. |

### 7.2 Recommendation

**Request Revision**

**Reasoning:**

1. **Blocking Sequence Error:** You cannot build Phase 2 commands without the Phase 3 config loader.
2. **Scope Gap:** The roadmap forgets to migrate the 7+ "minor" scripts (`verify`, `promote`, etc.). Shipping v3.0 without them would be a massive functional regression.

### 7.3 Confidence Level

**High** — The dependency inversion is a logical impossibility for implementation, and the missing commands are a clear regression from v2.9.

### 7.4 Key Strengths

* **Golden Master Strategy:** Excellent risk mitigation for the God Script refactor.
* **God Script Decomposition:** Very detailed breakdown of the two largest files.

### 7.5 Key Concerns

1. **Sequencing:** `io/toml.py` must exist before commands can use it.
2. **Legacy Script Migration:** Roadmap ignores `ontos_verify`, `ontos_promote`, etc. They need a home in `ontos/commands/`.
3. **Missing Features:** `export` and `hook` commands defined in architecture but missing from roadmap tasks.