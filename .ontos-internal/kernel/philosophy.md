---
id: philosophy
type: kernel
status: active
depends_on: [mission]
---

# Project Ontos: Philosophy

*The Conscious Memory System for AI-Native Teams*

---

## The Scenario

Picture this: A new developer joins your team on Monday.

**Without Ontos:**

They clone the repo. They open Claude Code. They ask "How does auth work here?"

Claude reads the code. It guesses. It gives a technically accurate but contextually blind answer. It doesn't know you chose OAuth over SAML because your target users hate creating passwords. It doesn't know you rejected a popular auth library because of a licensing issue discovered three weeks ago. It doesn't know the auth refactor is half-done and there's a known bug in the refresh token flow.

The new developer spends their first week re-discovering context that already existed — just trapped in Slack threads, old PRs, and their teammates' heads.

**With Ontos:**

They clone the repo. They type "Activate Ontos."

Boom. They instantly have the exact same brain as you.

The context map shows them the project structure. The session logs show them WHY things are the way they are. When they ask Claude about auth, Claude loads `auth_flow.md` AND the three session logs that shaped it — including the one where you rejected that library, including the one where you documented the refresh token bug.

They're productive on day one. Not because they're smarter, but because the context transferred.

**This is the core value proposition:**

> Your project's memory shouldn't live in your head. It should live in your repo — structured, searchable, and instantly transferable to any team member, human or AI.

---

## The Core Insight: Dual Ontology

Project knowledge has two dimensions:

| Dimension | Question | Changes How? | Examples |
|-----------|----------|--------------|----------|
| **Space (Truth)** | What IS? | Through deliberate updates | Architecture, features, specs |
| **Time (History)** | What HAPPENED? | Through accumulation | Decisions, fixes, explorations |

**Space Ontology (The Graph)**
- `kernel` — foundational principles
- `strategy` — goals and direction
- `product` — user-facing specs
- `atom` — technical implementation

**Time Ontology (The Timeline)**
- `log` — temporal record of a working session

The `log` type doesn't participate in the dependency hierarchy. Instead, it connects to Space through an `impacts` field — creating a bridge between "what we decided" and "what it affected."

---

## Who This Is For

### Primary: Small Teams Using AI Coding Agents

- 1-5 developers working with Claude Code, Cursor, Windsurf, or similar
- Building products where decisions matter more than code volume
- Switching between AI tools depending on task (Claude for architecture, Cursor for implementation)
- **Onboarding new team members constantly** — contractors, new hires, or just an AI agent that's never seen your codebase before

The litmus test: Can a new person (or a fresh AI session) become productive in under 10 minutes? If your context is trapped in Slack, in someone's head, or in chat logs that expired — the answer is no. Ontos makes the answer yes.

### Secondary: Solo Developers with Multiple Projects

- Juggling 2-5 projects simultaneously
- Returning to projects after weeks of dormancy
- Frustrated by re-explaining context to every AI session

### Anti-Audience

We are NOT building for:

- **Large enterprises** — they have Confluence, Notion, internal wikis with dedicated doc teams
- **Real-time collaboration** — we're git-native, not Google Docs
- **People who want zero maintenance** — Ontos requires intent; that's the point

---

## Core Philosophy

### Intent Over Automation

Ontos requires you to structure knowledge explicitly. Tag sessions with intent. Connect decisions to documents. This friction is the feature.

Why? Because **curation creates signal**. The act of deciding "this session matters" and "it impacted these documents" forces clarity. You can't capture your way to understanding — you have to think.

### Portability Over Platform

Ontos is markdown files in your repo. No database. No cloud service. No account.

This means:
- Switch AI tools freely (Claude today, Cursor tomorrow, whatever next month)
- Your knowledge travels with `git clone`
- No vendor lock-in, ever

### Shared Memory Over Personal Memory

Individual memory doesn't transfer. What you remember about the project is useless to your teammate, your contractor, or the AI agent that just opened a fresh session.

Ontos encodes knowledge at the repo level. Everyone who clones the repo gets the same brain. That's the unlock.

### Structure Over Search

We don't rely on semantic search or vector databases to surface relevant context. The context map IS the query interface — a human-readable, agent-navigable index of your project's knowledge.

Structure is explicit. Search is probabilistic. For critical decisions, explicit wins.

---

## What's Explicitly Out of Scope

### No Cloud Service

Ontos is files in your repo. No accounts, no API keys, no vendor lock-in. This is a feature, not a limitation.

### No Real-Time Sync

We're git-native. If you want Google Docs-style collaboration, use Google Docs. Ontos is for async, version-controlled knowledge.

### No Automatic Capture

We will not silently record everything. Ontos requires intent because intent creates signal. The moment you remove human judgment from the capture process, you're building a haystack, not a library.

### No Complex Querying

Ontos doesn't include semantic search, vector databases, or natural language queries over the knowledge graph. The context map is the query interface. If you need more, you're probably building something else.

### No GUI

Ontos is markdown files and Python scripts. The interface is your editor and your AI agent. If you need a dashboard, you're not the target user.

---

## The Bet

We're betting that **curated knowledge beats captured data** in the AI-native workflow.

The easy path is to record everything and let search sort it out later. We're taking the harder path: record what matters, make it findable by structure, require human judgment in the loop.

Why we think this wins:

1. **Teams need shared context** — individual memory doesn't transfer; repo-level memory does
2. **Signal degrades over time** — noise compounds; curation doesn't
3. **AI agents improve** — they'll get better at navigating structured knowledge faster than they'll get better at extracting signal from noise
4. **Intent forces clarity** — the act of documenting a decision makes you understand it better

If we're right, Ontos becomes the standard way teams encode knowledge for AI-native development.

If we're wrong, we've still built a solid documentation system that works without AI.

---

## The Tagline

> **Project Ontos: The conscious memory system for AI-native teams.**
>
> *Clone the repo. Activate Ontos. Instant shared brain.*
>
> Truth + History. Portable. Version-controlled. Intent over automation.
