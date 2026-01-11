---
id: constitution
type: kernel
status: active
depends_on: [mission]
---

# Project Ontos: Constitution

*The Core Invariants That Define Ontos*

These are the foundational rules that Ontos will never compromise on. Any implementation agent must respect these constraints.

---

## Core Invariants

1. **Zero-Dependency (V2.x):** V2 tools must run on **Python Standard Library (3.9+) ONLY**. No pip install.

2. **System Package (V3.x):** V3.0 moves logic to PyPI (pip install ontos). This is the only time we introduce dependencies (e.g., boto3, mcp).

3. **Local-First:** Data lives in the user's git repo. Logic lives in the System (V3).

4. **Functional Core, Imperative Shell:** Logic must be separated from I/O. The "Brain" (Logic) never calls print() or input().

5. **The Librarian's Wager:** We trade **Higher Friction** (manual curation) for **Higher Signal** (deterministic context).

6. **Deterministic Purity:** We reject probabilistic retrieval (Vector/Semantic Search) in favor of structural graph traversal.

---

*These invariants are referenced by [Technical Architecture](../strategy/technical_architecture.md) and apply to all implementation work.*
