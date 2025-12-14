---
id: log_20251214_v2_4_config_design
type: log
status: active
event_type: decision
concepts: [ux, config, tooling]
impacts: [v2_strategy]
---

# Session Log: V2 4 Config Design
Date: 2025-12-14 23:26 KST
Source: Claude Code
Event Type: decision

## 1. Goal
Design a two-tier configuration system for Ontos v2.4 that reduces friction for new users while preserving power-user flexibility.

## 2. Key Decisions
- **Three workflow modes:** automated, prompted, advisory (spectrum from zero-friction to full control)
- **Two-tier config:** High-level mode selection + low-level individual overrides
- **Session Appending:** One log per branch per day (from Gemini review) - prevents ghost log pollution
- **Auto-archive on push:** New feature for "automated" mode - creates session log automatically
- **`status: auto-generated`:** Quality signal for lint warnings (from Claude review)
- **Default mode = prompted:** Users should learn curation before automating (from Gemini review)
- **`ONTOS_SOURCE` env var:** CI and shared machine support (from Codex review)

**v1.2 additions (from second review round):**
- **🔴 No consolidation in pre-push:** "Dirty Push" paradox - warn only, don't mutate (Gemini+Claude consensus)
- **Branch validation in frontmatter:** Prevents wrong-log-appended bugs
- **Exact match before glob:** Fixes greedy pattern matching
- **Visible skip warnings:** "Zero friction" ≠ "zero visibility"
- **Commit deduplication:** Prevents duplicates on amend+push
- **`--enhance` flag:** Agent workflow for enriching auto-generated logs
- **Hook timeout:** Graceful degradation for slow hooks

## 3. Alternatives Considered
- Single-tier config only — rejected, too technical for new users
- Removing config options entirely — rejected, power users need flexibility
- Mode renaming (autopilot/guided/relaxed) — rejected, original names are clear
- Personas (solo/team/compliance) — rejected, over-engineering
- Telemetry — rejected, contradicts local-first philosophy
- "Minimal log is worse than no log" — rejected, breadcrumb is useful if marked auto-generated

## 4. Changes Made
- Created v2.4 design document (v1.0)
- Received architectural review from Claude, Codex, Gemini (v1)
- Critically analyzed v1 feedback (adopted 11 ideas, rejected 8)
- Revised proposal to v1.1 with Session Appending model
- Rolled back prototype implementation pending review
- Received second architectural review (v2) from Claude, Codex, Gemini
- Critically analyzed v2 feedback (adopted 10 items, rejected same as v1, deferred 1)
- Revised proposal to v1.2 addressing all critical issues

## 5. Next Steps
- Final review of v1.2 proposal
- Implement v2.4.0 with revised design
- Key implementations: session appending, branch validation, --enhance flag

---
## Raw Session History
```text
- PR #14 review (v2.3)
- Root directory cleanup, migrate script fix
- Designed consolidation automation (v2.3.2 prototype)
- Expanded to full config automation proposal
- Wrote v2.4 design document (v1.0)
- Rolled back implementation pending review
- Received Claude/Codex/Gemini feedback (v1)
- Critical analysis: adopted session appending, status:auto-generated, env var support
- Rejected: mode renaming, personas, telemetry, checksum drift detection
- Revised proposal to v1.1
- Received Claude/Codex/Gemini feedback (v2)
- Critical analysis v2: identified "Dirty Push" paradox as critical flaw
- Adopted: remove consolidation from pre-push, branch validation, exact match, deduplication
- Adopted: --enhance flag, hook timeout, visible skip warnings
- Deferred: mode orthogonality refactor (valid but complex for v2.4)
- Revised proposal to v1.2 - all critical issues addressed
```
