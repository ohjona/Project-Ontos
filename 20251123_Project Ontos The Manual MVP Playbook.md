# **Ontos: The Manual MVP Playbook**

## **Phase 0: The "Future-Proof" Setup**

To ensure we can automate this later, every document **MUST** start with this YAML header. This allows us to treat text files like database records.

**The Standard Header Template:**

\---  
id: unique\_slug\_name  \# REQUIRED. Stable ID. Never change this even if filename changes.  
type: \[kernel | strategy | product | atom\] \# REQUIRED. Defines the hierarchy level.  
status: \[draft | active | deprecated\] \# Optional. Helps LLM ignore old files.  
owner: \[role\] \# Optional. Who is responsible?  
depends\_on: \[id\_of\_parent\_doc, id\_of\_other\_doc\] \# The Logic Links.  
\---

### **Example: docs/features/stripe\_checkout.md**

\---  
id: feature\_stripe\_checkout  
type: atom  
status: active  
depends\_on: \[strategy\_monetization, journey\_user\_checkout\]  
\---  
\# Stripe Checkout Specification  
...

## **Phase 1: The "Architect" Prompt (Initialization)**

*Run this prompt to generate the visual map. Note: The LLM now relies on the YAML headers to do this accurately.*

**Prompt:**

"I am uploading my project documentation folder. Every file contains a YAML frontmatter block defining its ID, Type, and Dependencies.

Act as a System Architect. Read the YAML headers of all files to understand the graph structure.

Create a file called CONTEXT\_MAP.md that visualizes this graph.

1. **Hierarchy Tree:** Group files by their type (Kernel \-\> Strategy \-\> Product \-\> Atom).  
2. **Dependency Audit:** List any file that lists a depends\_on ID that does not exist (Broken Links).  
3. **The Index:** A lookup table of ID \-\> Filename so I can find things quickly.

Do not summarize content. Focus on validating the structural integrity of the YAML graph."

## **Phase 2: The "Weekly Ritual" (Automated Maintenance)**

**Do not manually edit CONTEXT\_MAP.md.** Instead, treat it as disposable. Regenerate it whenever you feel "lost" or at a set interval (e.g., Friday afternoons).

**The "Regeneration" Prompt (Paste this into Gemini/Claude with your full /docs folder):**

"I am uploading the latest version of my documentation folder.

**Task:** Regenerate the CONTEXT\_MAP.md file from scratch.

1. **Scan:** Read the YAML frontmatter of every file.  
2. **Validate:** Check if any depends\_on links are broken (referencing IDs that no longer exist).  
3. **Visualize:** Output a clean, ASCII-style tree of the project hierarchy.  
4. **Index:** List all valid IDs and their current filenames.

**Output format:** precise Markdown. I will overwrite my existing map with your output."

## **Phase 3: Vibe Coding (The Usage)**

*How to use the map to save tokens and improve context.*

**Scenario:** You want to update the login feature.

**The Prompt to Cursor/Claude:**

"@CONTEXT\_MAP.md  
I want to update the Login flow.

1. Check the Context Map to find the ID feature\_login.  
2. Look at its depends\_on list.  
3. Retrieve the content for those specific Parent IDs.  
4. Use that context to write the code."

## **Phase 4: The Update Loop (The Write-Back)**

*When you make a decision in Chat, update the docs.*

**The Prompt:**

"We just decided to change the pricing to $30/month.

1. Find the file with id: strategy\_monetization.  
2. Update the markdown content.

## **Phase 5: The "Session Commit" (Archival)**

*Run this at the end of a coding session to save your "Decision History" to the repo.*

**The Prompt:**

"We are finishing this session. I want to archive our decisions.

1. **Summarize:** Review our entire conversation above. Extract key **Decisions Made** (e.g., 'Switched to Stripe v12'), **Alternatives Rejected** (e.g., 'Rejection of PayPal due to fees'), and **Files Modified**.  
2. **Format:** Create a markdown log entry.  
3. **Action:** Write this content to a new file: docs/logs/YYYY-MM-DD\_topic\_slug.md (use today's date and a short topic slug).  
4. **Git:** Generate the git commands to commit and push this log file."

**Example Output from LLM:**

\# LLM generates this command for you to run:  
echo "\# Session Log: Stripe Refactor  
\#\# Decisions  
\- Bumped fees to 3.3%  
\- Removed PayPal support  
\#\# Context Used  
\- strategy\_monetization.md" \> docs/logs/2024-03-20\_stripe-refactor.md

git add docs/logs/  
git commit \-m "chore: archive session log for stripe refactor"  
git push  
