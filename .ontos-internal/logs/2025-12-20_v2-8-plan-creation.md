---
id: log_20251220_v2_8_plan_creation
type: log
status: active
event_type: decision
concepts: []
impacts: [v2_8_implementation_plan]
---

# Session Log: V2 8 Plan Creation
Date: 2025-12-20 01:23 KST
Source: Claude Opus 4.5
Event Type: decision

## 1. Goal
Create comprehensive v2.8 implementation plan for LLM Review Board review.

## 2. Key Decisions
- **Feature 1: Context Object Refactor** - Split ontos_lib.py into ontos/core/ (pure functions) and ontos/ui/ (I/O)
- **Feature 2: Unified CLI** - Create ontos.py dispatcher replacing direct script invocation
- **SessionContext dataclass** - Transaction pattern with commit/rollback for file writes
- **Backwards compatibility** - ontos_lib.py becomes a shim re-exporting from new locations

## 3. Alternatives Considered
- Single monolithic refactor vs. phased approach → Chose phased (library split first, CLI second)
- Global config object vs. dependency injection → Left as Open Question (Q4) for LLM Review Board

## 4. Changes Made
- Created `.ontos-internal/strategy/proposals/v2.8/v2.8_implementation_plan.md` (784 lines)
- Plan includes 10 open questions for LLM reviewers (Q1-Q10)
- Defined 5 implementation phases with success criteria

## 5. Next Steps
- Share plan with LLM Review Board (Claude, Codex, Gemini)
- Address open questions based on reviewer feedback
- Update plan status from draft to active after approval
