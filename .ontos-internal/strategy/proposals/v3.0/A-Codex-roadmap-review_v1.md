# Ontos v3.0 Implementation Roadmap: Peer Review

**Reviewer:** GPT-5.2 Thinking
**Date:** 2026-01-11
**Roadmap Version:** 1.0

---

## 1. Architecture Coverage Check

### 1.1 Module Coverage

| Architecture Module       | Roadmap Phase          | Status     |
| ------------------------- | ---------------------- | ---------- |
| `__init__.py`             | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `__main__.py`             | Phase 1 (v3.0.0-alpha) | ✅ Covered  |
| `cli.py`                  | Phase 4 (v3.0.0)       | ✅ Covered  |
| `version.py`              | Phase 1 (v3.0.0-alpha) | ✅ Covered  |
| `commands/__init__.py`    | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/consolidate.py` | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/deinit.py`      | v3.1.0                 | ✅ Covered  |
| `commands/doctor.py`      | Phase 4 (v3.0.0)       | ✅ Covered  |
| `commands/export.py`      | Phase 4 (v3.0.0)       | ✅ Covered  |
| `commands/hook.py`        | Phase 4 (v3.0.0)       | ✅ Covered  |
| `commands/init.py`        | Phase 3 (v3.0.0-rc)    | ✅ Covered  |
| `commands/log.py`         | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `commands/map.py`         | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `commands/migrate.py`     | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/promote.py`     | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/query.py`       | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/scaffold.py`    | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/stub.py`        | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `commands/verify.py`      | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `core/__init__.py`        | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `core/config.py`          | Phase 3 (v3.0.0-rc)    | ✅ Covered  |
| `core/context.py`         | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `core/curation.py`        | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `core/frontmatter.py`     | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `core/graph.py`           | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/history.py`         | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/paths.py`           | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/proposals.py`       | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/schema.py`          | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `core/staleness.py`       | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/suggestions.py`     | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/tokens.py`          | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/types.py`           | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `core/validation.py`      | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `io/__init__.py`          | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `io/files.py`             | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `io/git.py`               | Phase 2 (v3.0.0-beta)  | ✅ Covered  |
| `io/toml.py`              | Phase 3 (v3.0.0-rc)    | ✅ Covered  |
| `mcp/server.py`           | v3.2.0+                | ⚠️ Partial |
| `ui/__init__.py`          | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `ui/json_output.py`       | Phase 4 (v3.0.0)       | ✅ Covered  |
| `ui/output.py`            | Phase 1 (v3.0.0-alpha) | ⚠️ Partial |
| `ui/progress.py`          | Phase 1 (v3.0.0-alpha) | ❌ Missing  |

**Coverage read:** the core migration spine is present. The roadmap is thin or silent on a few required modules, and one module in the architecture tree is not accounted for at all.

### 1.2 Interface Coverage

| Architecture Interface                                            | Roadmap Location                           | Status |
| ----------------------------------------------------------------- | ------------------------------------------ | ------ |
| `find_project_root()`                                             | Phase 2 / `io/files.py`                    | ✅      |
| `DependencyGraph.build(), detect_cycles()`                        | Phase 2 / `core/graph.py`                  | ✅      |
| `ValidationOrchestrator.validate_all()`                           | Phase 2 / `core/validation.py`             | ✅      |
| `SessionContext.commit()` and “all writes go through commit” rule | Phase 1 / `core/context.py`                | ⚠️     |
| `load_config(), write_config()`                                   | Phase 3 / `io/toml.py`                     | ✅      |
| Config resolution, precedence rules                               | Phase 3 / `core/config.py`                 | ✅      |
| JSON output plumbing                                              | Phase 4 / `ui/json_output.py` and `cli.py` | ✅      |
| Hook shim contract                                                | Phase 4 / `commands/hook.py`               | ✅      |

Main gap here is not “missing code”, it’s missing enforcement. The architecture’s guardrails are stated, but the roadmap rarely turns them into explicit checks.

### 1.3 Command Coverage

| Architecture Command | Roadmap Phase         | JSON Support Noted? | Status |
| -------------------- | --------------------- | ------------------- | ------ |
| `ontos map`          | Phase 2 (v3.0.0-beta) | Yes                 | ✅      |
| `ontos log`          | Phase 2 (v3.0.0-beta) | Yes                 | ✅      |
| `ontos verify`       | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos query`        | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos migrate`      | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos consolidate`  | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos promote`      | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos scaffold`     | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos stub`         | Phase 2 (v3.0.0-beta) | Yes                 | ⚠️     |
| `ontos init`         | Phase 3 (v3.0.0-rc)   | Yes                 | ✅      |
| `ontos doctor`       | Phase 4 (v3.0.0)      | Yes                 | ✅      |
| `ontos hook`         | Phase 4 (v3.0.0)      | No                  | ✅      |
| `ontos export`       | Phase 4 (v3.0.0)      | No                  | ✅      |
| `ontos deinit`       | v3.1.0                | Not specified       | ⚠️     |

The command checklist is comprehensive, but the roadmap only provides detailed task breakdowns for a subset of these commands. That mismatch is the biggest “verification” problem in the whole doc.

### 1.4 Coverage Gaps

1. `ui/progress.py` is in the architecture target tree but never planned in the roadmap.
2. The `.ontos.toml` default template in the roadmap does not include the `[hooks]` section shown in the architecture’s default config example.
3. Several Phase 2 commands appear in the checklist, but do not appear anywhere else as implementation tasks, acceptance criteria, or dependency callouts.

---

## 2. Sequencing Analysis

### 2.1 Dependency Flow Check

| Phase                | Depends On | Prerequisites Met? | Issues                                                                            |
| -------------------- | ---------- | ------------------ | --------------------------------------------------------------------------------- |
| Phase 0 Pre-release  | none       | ✅                  | Section content is stubbed with placeholders, which weakens the whole safety net. |
| Phase 1 v3.0.0-alpha | Phase 0    | ✅                  | Makes sense to freeze behavior before moving files.                               |
| Phase 2 v3.0.0-beta  | Phase 1    | ✅                  | Correct place for God Script decomposition and core extraction.                   |
| Phase 3 v3.0.0-rc    | Phase 2    | ✅                  | Config and init naturally follow once `io/files` exists.                          |
| Phase 4 v3.0.0       | Phase 3    | ✅                  | Full CLI, JSON output, doctor, hooks, export belong here.                         |
| v3.1.0               | v3.0.0     | ✅                  | Bridge items like deinit are logically post v3.0.                                 |
| v3.2.0+              | v3.1.0     | ✅                  | Protocol prep after baseline stability is reasonable.                             |

### 2.2 Sequencing Concerns

* **Phase 2 checklist vs Phase 2 tasks conflict.** The checklist says verify, query, migrate, consolidate, promote, scaffold, stub land in Phase 2, but Phase 2 detailed work is centered on core extraction and map and log. If the intent is “ported enough to pass golden master but still not on the new CLI”, that needs to be stated clearly and reflected in acceptance criteria.
* **JSON timing needs one sentence.** Phase 2 claims JSON support for commands, but the JSON output handler is built in Phase 4. This can still be correct if Phase 2 “JSON support” means returning JSON-serializable structures and not printing. Right now it reads like an output feature arrives before its output system.
* **`io/toml.py` timing is OK but needs clarity.** Architecture examples sometimes treat `io/toml` as present earlier as a stub. Roadmap creates it in Phase 3. That is fine, but it should explicitly say whether Phase 1 creates the stub file or Phase 3 creates it from scratch.

### 2.3 Parallelization Assessment

| Roadmap Says Parallelizable        | Actually Parallelizable? | Notes                                                                                              |
| ---------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------- |
| `io/toml.py` after Phase 1         | ✅ Yes                    | Real dependency is on config schema decisions, not on the core decomposition.                      |
| `commands/hook.py` after Phase 1   | ⚠️ Mostly                | Can start early, but will still need final `find_project_root` behavior and config keys to settle. |
| `commands/export.py` after Phase 1 | ✅ Yes                    | If it reads from an abstracted context provider and avoids hard ties to Phase 2 internals.         |

### 2.4 Critical Path Assessment

The roadmap identifies the right critical path at a high level, but the “Dependencies & Sequencing” section includes placeholder ellipses. That’s a doc completeness issue, but it matters because Phase 2 risk is high and the team needs a precise dependency graph to avoid rework.

---

## 3. Completeness Review

### 3.1 Missing Tasks

| Gap                                                                                                                          | Should Be In           | Impact |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------ |
| Implementations or explicit migration plan for `verify/query/migrate/consolidate/promote/scaffold/stub` beyond the checklist | Phase 2 or Phase 4     | High   |
| Add `ui/progress.py` plan or explicitly defer it                                                                             | Phase 4 or v3.0.1+     | Medium |
| Align `.ontos.toml` template with architecture’s `[hooks]` section and key names                                             | Phase 3                | High   |
| Replace placeholder “...” blocks in Pre-release and Dependencies sections with real steps                                    | Phase 0 and Section 11 | High   |

### 3.2 Missing Acceptance Criteria

| Phase   | Criteria Gap                                          | Suggested Criteria                                                                                                         |
| ------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Phase 0 | Pre-release section is not concrete enough            | Enumerate which v2 commands have golden masters and what fixtures represent “canonical repos”.                             |
| Phase 2 | Checklist commands are not reflected in exit criteria | Either remove them from Phase 2 checklist or add explicit “command parity” checks for the commands truly expected in beta. |
| Phase 3 | Config parity not fully testable as written           | Add a test that confirms config precedence and hook config keys match the architecture sample config.                      |

### 3.3 Missing Risk Items

| Unacknowledged Risk                            | Phase         | Why It Matters                                                                                                             |
| ---------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| “architecture reference version mismatch” risk | Whole roadmap | Roadmap claims it implements architecture v1.4, but the attached architecture doc is v1.3. This is a coordination risk.    |
| “config schema drift” risk                     | Phase 3       | You already have drift between roadmap template and architecture example. This will create churn in init and hook install. |

### 3.4 Handoff Gaps

| From Phase | To Phase | Unclear Handoff                                                                                                                       |
| ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 0    | Phase 1  | What exact scripts and outputs are frozen, which fixtures exist, and how many commands are covered.                                   |
| Phase 2    | Phase 4  | If Phase 2 “JSON support” is data-return only, that contract needs to be explicitly defined so Phase 4 output work does not break it. |
| Phase 3    | Phase 4  | `.ontos.toml` schema and hook config keys must be final before implementing `hook` and `doctor` checks. Right now the docs disagree.  |

---

## 4. Feasibility Concerns

### 4.1 Estimate Assessment

| Phase   | Roadmap Estimate | My Assessment | Concern                                                                                 |
| ------- | ---------------- | ------------- | --------------------------------------------------------------------------------------- |
| Phase 0 | 2-3 days         | Optimistic    | If golden masters cover more than map and log, this balloons fast.                      |
| Phase 1 | 1-2 days         | Reasonable    | Mostly mechanical moves plus packaging wiring.                                          |
| Phase 2 | 5-8 days         | Optimistic    | God Script decomposition plus behavior parity is usually where hidden coupling lives.   |
| Phase 3 | 3-5 days         | Reasonable    | If config keys and precedence rules are frozen early.                                   |
| Phase 4 | 4-6 days         | Reasonable    | CLI and JSON output can be contained, but only if Phase 2 command contracts are stable. |

### 4.2 Technical Feasibility

| Task                                                   | Concern                                                                                          | Severity |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | -------- |
| Decomposing God Script into orchestration plus modules | High chance of subtle behavior drift, especially around file discovery and log ordering          | High     |
| Hook shim and cross-platform execution                 | Windows “best-effort” is fine, but you still need deterministic behavior and clear failure modes | Medium   |
| JSON output for all commands                           | Easy to promise, hard to enforce without a uniform output contract and tests                     | Medium   |

### 4.3 Dependency Risks

| External Dependency              | Risk                                                                     | Mitigation in Roadmap? |
| -------------------------------- | ------------------------------------------------------------------------ | ---------------------- |
| Git availability and repo states | Detached HEAD, submodules, worktrees can break naïve git wrappers        | Partial                |
| TOML parsing dependency          | Python version differences, tomllib vs tomli                             | Partial                |
| Packaging and entry points       | “pip install ontos” reliability, test PyPI vs PyPI, platform differences | Yes                    |

---

## 5. Consistency Check

### 5.1 Internal Contradictions

| Contradiction                                                                         | Location 1          | Location 2                                                                                                 |
| ------------------------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------- |
| Commands listed as Phase 2 deliverables but not implemented anywhere in Phase 2 tasks | Phase 6.2 checklist | Phase 4 detailed work focuses on only a subset and Phase 2 tasks only detail map and log plus core modules |
| Golden master scope unclear                                                           | Phase 0 is stubbed  | Phase 4 exit criteria says “Golden Master tests pass” for full release                                     |

### 5.2 Terminology Consistency

| Term                                         | Usage Issue                                                                                           |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| “Phase” vs “v3.0.0-beta/rc/release”          | Mixed naming is fine, but a single mapping table would prevent confusion in checklists and estimates. |
| “Config migration” vs “init” vs “activation” | The roadmap uses all three, but config keys are not fully consistent with the architecture example.   |

### 5.3 Version Number Consistency

* Roadmap says it implements “Technical Architecture v1.4”, but the provided architecture doc header shows v1.3. This needs resolution or you risk reviewing against the wrong source.

---

## 6. Recommendations

### 6.1 Critical Must Fix

| Issue                                                                                           | Section     | Recommended Fix                                                                                                     |
| ----------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------- |
| Phase 2 command checklist is not backed by Phase 2 tasks or Phase 2 acceptance criteria         | 6.2 and 4.x | Either move those commands to Phase 4 in the checklist, or add explicit Phase 2 task breakdowns and tests for each. |
| `.ontos.toml` default template does not match architecture example config, especially `[hooks]` | 5.6         | Update the template to include `[hooks]` and align key names with the architecture.                                 |
| Placeholders in Pre-release and Dependencies sections                                           | 2 and 11    | Replace “...” with concrete steps, fixtures, and dependency graph content.                                          |

### 6.2 Major Should Fix

| Issue                                   | Section             | Recommended Fix                                                                                                           |
| --------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Architecture reference version mismatch | Header / references | Update either the roadmap reference or the provided architecture doc so “source of truth” is unambiguous.                 |
| JSON support timing ambiguity           | 6.2, 4.x, 6.x       | Add a one-line contract: Phase 2 commands return JSON-serializable data structures, Phase 4 owns printing and formatting. |

### 6.3 Minor Nice to Fix

| Issue                                     | Section  | Recommended Fix                                                               |
| ----------------------------------------- | -------- | ----------------------------------------------------------------------------- |
| `ui/progress.py` not accounted for        | Coverage | Add it to v3.0.1+ polish or explicitly remove from target tree if not needed. |
| `ontos deinit` JSON support not specified | v3.1.0   | Decide and document whether it supports `--json` like other commands.         |

### 6.4 Suggestions Optional Improvements

* Add a single “Phase to artifact” table at the top: tags, command availability, and what “working” means at each tag.
* Make golden master scope explicit: which commands, which fixtures, what outputs are asserted.

---

## 7. Summary Assessment

### 7.1 Overall Verdict

| Aspect                 | Rating   | Notes                                                                                                        |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| Architecture Alignment | Adequate | Core decomposition and config migration align, but config template drift and one missing module need fixing. |
| Sequencing Logic       | Strong   | The high-level order is right and dependencies mostly flow.                                                  |
| Completeness           | Weak     | Several sections are stubbed and several commands exist only as checklist rows.                              |
| Feasibility            | Adequate | Estimates are plausible except Phase 2 looks optimistic given the risk profile.                              |
| Consistency            | Adequate | Main issues are command checklist vs tasks, and roadmap vs architecture version mismatch.                    |

### 7.2 Recommendation

**Overall:** Approve with Changes

### 7.3 Confidence Level

**Medium** — the plan’s spine is solid, but the doc has real “missing work” ambiguity around Phase 2 commands and config schema details.

### 7.4 Key Strengths

* Correct top-level sequencing: freeze behavior, restructure packages, decompose core, then migrate config and finally ship the new CLI.
* Phase 2 correctly calls out the God Script decomposition as a major effort and includes refactor targets beyond just new modules.

### 7.5 Key Concerns

1. Phase 2 command scope is internally inconsistent: checklist promises more than the tasks define.
2. `.ontos.toml` schema drift between architecture example and roadmap template will cause churn in init and hooks.
3. Placeholder sections undermine the roadmap’s “execution readiness”, especially the pre-release safety net.

---

*End of Review*