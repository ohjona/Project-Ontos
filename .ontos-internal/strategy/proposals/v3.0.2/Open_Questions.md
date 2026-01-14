# v3.0.2: Open Questions & Next Steps

**Author:** Chief Architect (Claude Opus 4.5)
**Date:** 2026-01-14
**Status:** Planning

---

## 1. Usage & Activation

### Q1.1: How does "Activate Ontos" work now?

**Question:** How does activating Ontos work now that it's a Python package?

**Context:**
- Previously used script-based activation
- Now installed via `pip install ontos`
- Need to document the new activation flow

**To Research:**
- What triggers Ontos activation in a project?
- Is it `ontos init`? Git hooks? Manual invocation?

---

### Q1.2: Keeping LLM "Dialed In"

**Question:** How are we forcing the LLM to stay in "Ontos-activated" state?

**Context:**
- LLMs can drift from instructions over long sessions
- Ontos relies on LLM following specific workflows
- Need mechanism to reinforce Ontos patterns

**To Research:**
- System prompt injection?
- Context map as persistent reminder?
- Hook-based reminders?

---

### Q1.3: CLI Command Reference

**Question:** What do the `ontos` commands do now?

**Commands to Document:**
```bash
ontos --help
ontos init --help
ontos doctor
ontos map
```

**To Research:**
- Full command inventory
- Each command's purpose and options
- Common workflows

---

### Q1.4: Cross-LLM Compatibility

**Question:** Does Ontos work reliably across different LLM CLIs?

**Known Issues:**
- **Gemini CLI:** API error when parallel file reads have mixed success/failure
  - Error: "number of function response parts must equal function call parts"
  - Triggered when one file not found alongside successful reads
- **Codex:** Unknown — needs testing

**Context:**
- Ontos claims to be "tool-agnostic"
- But activation flow depends on LLM tool-calling behavior
- Different LLMs handle errors differently

**To Research:**
- Test activation on Claude Code, Gemini CLI, Codex
- Document compatibility matrix
- Identify workarounds for each platform

---

## 2. Value & Effectiveness

### Q2.1: Does Ontos Actually Help?

**Question:** Do we know if Ontos actually helps with context window usage, time, or quality?

**Context:**
- Core value proposition is better LLM context management
- No empirical measurement yet
- Need to validate claims

**To Research:**
- How would we measure effectiveness?
- What metrics matter? (tokens saved, accuracy, time)
- Can we A/B test with/without Ontos?

---

### Q2.2: What's Our Actual Strength?

**Question:** What is Ontos's actual strength now?

**To Research:**
- Document-as-context approach
- Dependency tracking
- Staleness detection
- Session continuity
- What differentiates us?

---

## 3. Publishing & Distribution

### Q3.1: PyPI Publishing

**Question:** Do you have PyPI credentials configured for this project?

**Context:**
- v3.0.1 is merged but not published to PyPI
- Users cannot `pip install ontos` until published
- Requires PyPI account with upload permissions

**Options:**
1. Use existing PyPI credentials (if configured)
2. Create new PyPI account for project
3. Use GitHub Actions for automated publishing
4. Keep as source-only distribution for now

---

### Q3.2: PyPI Name Ownership

**Question:** Can I officially claim the name "ontos" on PyPI now?

**To Research:**
- PyPI namespace rules
- Is "ontos" available or taken?
- Process for registering package name
- Trademark considerations?

---

### Q3.3: Package Contents Exposure

**Question:** Will people see all the internal documents when they install Ontos? (e.g., `pip install ontos`)

**Context:**
- `.ontos-internal/` contains strategy docs, decision history, roadmaps
- Source repo has full history and planning documents
- PyPI package may or may not include these

**To Research:**
- What does `python -m build` actually include?
- Does `MANIFEST.in` or `pyproject.toml` control this?
- Are `.ontos-internal/`, `docs/`, `tests/` excluded from wheel?
- What about sdist (source distribution)?

---

### Q3.4: Release Announcements

**Question:** What channels should be used for release announcements?

**Options:**
1. GitHub Releases only (minimal)
2. GitHub Releases + README badge
3. GitHub Releases + external channels (Discord/Slack/Twitter)
4. No public announcements (internal project)

---

## 4. Business & Licensing

### Q4.1: Open Source vs Closed Source

**Question:** If I want to make this not open source, what should I do?

**Sub-questions:**
- What's the distribution model?
- What documents should I remove or add?

**To Research:**
- Current license status
- License change implications (if any contributors)
- Private PyPI options (e.g., AWS CodeArtifact, private index)
- Source code protection strategies

**Options for Closed Source:**
1. Private GitHub repo + private PyPI
2. License change (if sole contributor)
3. Dual licensing (open core + commercial)
4. SaaS model (no distribution)

---

## 5. Technical Debt

### Q5.1: Architecture Violation

**Issue:** `ontos/core/config.py:229` imports from `ontos.io.git`

**Question:** Should this be fixed in v3.0.2 or tracked for later?

**Context:**
- Violates core/ → io/ constraint
- Pre-existing, not introduced by Phase 5
- Requires refactoring to inject dependency

---

### Q5.2: Test Count Reduction

**Observation:** Tests dropped from 411 to 395 between reviews

**Question:** Is this expected? Were tests removed intentionally?

**To Do:** Audit test changes to confirm intentional

---

### Q5.3: Golden Master Framework

**Question:** Should golden tests be expanded for v3.0.2?

**Context:**
- Currently only 2 golden tests
- Framework exists but underutilized
- Could catch output regressions

---

## Summary: Questions by Priority

| Priority | Question | Category |
|----------|----------|----------|
| **High** | PyPI publishing setup | Publishing |
| **High** | Does Ontos actually help? | Value |
| **High** | Open source decision | Business |
| **High** | Package contents exposure | Publishing |
| **Medium** | How does activation work? | Usage |
| **Medium** | CLI documentation | Usage |
| **Medium** | PyPI name ownership | Publishing |
| **Low** | Architecture violation | Tech Debt |
| **Low** | Golden test expansion | Tech Debt |

---

## Next Steps

1. **Decide:** Open source or closed source?
2. **Research:** PyPI name availability and publishing
3. **Document:** Current CLI and activation flow
4. **Measure:** How would we validate Ontos effectiveness?

---

**Document signed by:**
- **Role:** Chief Architect
- **Model:** Claude Opus 4.5
- **Date:** 2026-01-14
