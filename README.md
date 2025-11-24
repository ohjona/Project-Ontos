# Ontos: The Manual MVP Playbook

**Turn your documentation into a queryable database for LLMs.**

Ontos is a "Manual MVP" framework for managing project context. It structures your documentation with YAML frontmatter, allowing you to treat your `docs/` folder like a database. This enables LLMs to understand the relationships between your files (Strategy -> Product -> Features) and generate accurate context maps.

## 🚀 Getting Started

This repository serves as a template and guide. To use this approach in your own project, follow these steps.

### 1. Setup Directory Structure

Create a `docs/` directory with the following hierarchy to organize your "knowledge atoms":

```bash
mkdir -p docs/kernel docs/strategy docs/product docs/atom
```

- **Kernel**: Core principles, mission, values.
- **Strategy**: High-level goals, monetization, target audience.
- **Product**: User journeys, feature sets.
- **Atom**: Specific implementation details, specs, individual features.

### 2. The "Database" Record (YAML Frontmatter)

Every markdown file in `docs/` **MUST** start with this standard YAML header. This is what allows the system to link everything together.

```yaml
---
id: unique_slug_name  # REQUIRED. Stable ID. Never change this even if filename changes.
type: atom            # Options: [kernel, strategy, product, atom]
status: active        # Options: [draft, active, deprecated]
owner: role           # Optional. Who is responsible?
depends_on: []        # List of IDs this document depends on (e.g. [strategy_monetization])
---
```

*See `docs/template.md` for a copy-pasteable version.*

### 3. Automation (The Context Map)

Instead of manually maintaining a table of contents, use the included script to generate a `CONTEXT_MAP.md`. This file visualizes your project's knowledge graph and validates links.

1.  Copy `scripts/generate_context_map.py` to your project.
2.  Run it whenever you add or move files:

```bash
python3 scripts/generate_context_map.py
```

This will generate `CONTEXT_MAP.md` in your root directory.

## 📖 The Workflow

### Phase 1: Vibe Coding (Usage)
When you need to work on a feature, use the Context Map to find the relevant IDs.

**Prompt to LLM:**
> "@CONTEXT_MAP.md
> I want to update the Login flow.
> 1. Check the Context Map to find the ID `feature_login`.
> 2. Look at its `depends_on` list.
> 3. Retrieve the content for those specific Parent IDs.
> 4. Use that context to write the code."

### Phase 2: The Update Loop (Write-Back)
If you make a decision during a chat (e.g., changing pricing), update the corresponding documentation file immediately.

**Prompt to LLM:**
> "We just decided to change the pricing to $30/month.
> 1. Find the file with id: `strategy_monetization`.
> 2. Update the markdown content."

### Phase 3: Session Commit (Archival)
At the end of a session, archive your decisions.

**Prompt to LLM:**
> "We are finishing this session.
> 1. Summarize our decisions and files modified.
> 2. Create a log entry in `docs/logs/YYYY-MM-DD_topic.md`.
> 3. Generate git commands to commit."

## 📂 Repository Structure

- `docs/`: Your knowledge base.
- `scripts/`: Automation tools.
- `CONTEXT_MAP.md`: The auto-generated map of your project (Do not edit manually).
- `20251123_Project Ontos The Manual MVP Playbook.md`: The original manifesto/playbook for this approach.
