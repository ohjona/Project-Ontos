# Deploying Ontos to Your Repository

This guide explains how to integrate the Ontos "Manual MVP" workflow into an existing project.

## 1. Installation

### A. Copy Files
Copy the following files from the Ontos repository to your project root:

1.  `scripts/generate_context_map.py` -> `scripts/generate_context_map.py`
2.  `docs/template.md` -> `docs/template.md` (Optional, for reference)

### B. Setup Directory
Ensure you have a `docs/` directory. We recommend the following structure:
```bash
mkdir -p docs/kernel docs/strategy docs/product docs/atom
```

### C. Dependencies
Ensure you have Python 3 installed. You will need the `PyYAML` library:
```bash
pip install pyyaml
```

## 2. Configuration (The Migration)

The core of Ontos is the **YAML Frontmatter**. You need to add this to your existing documentation.

### Step 1: Inventory
Identify your key documentation files (README, Architecture docs, API specs).

### Step 2: Add Frontmatter
Add the following header to the top of each markdown file:

```yaml
---
id: unique_id_for_this_file  # e.g., 'auth_flow', 'database_schema'
type: atom                   # Options: kernel, strategy, product, atom
status: active
depends_on: []               # e.g., ['system_architecture']
---
```

**Tips:**
- **IDs** must be unique across the project.
- **depends_on** is where the magic happens. Link "Feature Specs" to "Product Requirements".

## 3. Usage Workflow

### A. Generate the Map
Run the script to index your knowledge base:
```bash
python3 scripts/generate_context_map.py
```
This creates `CONTEXT_MAP.md`. **Commit this file.** It serves as the "Sitemap" for the LLM.

### B. "Vibe Coding" (The AI Workflow)
When you start a chat with Claude/ChatGPT/Gemini:

1.  **Copy the Context Map**: Paste the content of `CONTEXT_MAP.md` into the chat first.
2.  **Ask for Context**:
    > "I'm working on the `auth_flow`. Check the Context Map, tell me which files I need to read, and I will paste them."
3.  **Paste Files**: The AI will say "I need `docs/auth/login.md`". You copy/paste that file.

### C. Maintenance
- **New File**: Add frontmatter, run script.
- **Changed Logic**: Update the doc, run script.

## 4. CI/CD Integration (Optional)
You can add a GitHub Action to ensure `CONTEXT_MAP.md` is always up to date:

```yaml
# .github/workflows/ontos.yml
name: Update Context Map
on:
  push:
    paths:
      - 'docs/**/*.md'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install pyyaml
      - name: Generate Map
        run: python scripts/generate_context_map.py
      - name: Commit changes
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "chore: update context map"
          file_pattern: CONTEXT_MAP.md
```
