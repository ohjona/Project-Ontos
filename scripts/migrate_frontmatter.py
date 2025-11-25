import os
import sys
import argparse
import yaml
import json

# Default directory to scan
DEFAULT_DOCS_DIR = 'docs'

def get_untagged_files(directory):
    """Recursively finds markdown files without YAML frontmatter."""
    untagged = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    if not content.startswith('---'):
                        untagged.append(filepath)
    return untagged

def generate_prompt(files):
    """Generates a prompt containing the content of untagged files."""
    prompt = """You are the Ontos Librarian. Analyze each document and generate YAML frontmatter metadata.

## Type Taxonomy (Select ONE per document)

| Type | Definition | Signal Words |
|------|------------|--------------|
| kernel | Immutable foundational principles that rarely change | mission, values, philosophy, principles |
| strategy | High-level decisions about goals, audiences, approaches | goals, roadmap, monetization, target market |
| product | User-facing features, journeys, requirements | user flow, feature spec, requirements, user story |
| atom | Technical implementation details and specifications | API, schema, config, implementation, technical spec |

## Classification Heuristic
When uncertain: "If this document changes, what else breaks?"
- Everything breaks → kernel
- Business direction changes → strategy  
- User experience changes → product
- Only implementation changes → atom

## Output Format
Output ONLY valid JSON. No markdown code blocks. No explanation.

{
  "filepath": {
    "id": "unique_snake_case_slug",
    "type": "kernel|strategy|product|atom",
    "status": "active",
    "depends_on": ["other_doc_ids_if_known"]
  }
}

## Files to Process:
"""
    for filepath in files:
        with open(filepath, 'r') as f:
            # Read first 500 chars to avoid token limits
            preview = f.read(500).replace('\n', ' ')
            prompt += f"\nFile: {filepath}\nContent Preview: {preview}...\n"
            
    return prompt

def call_llm_api(prompt):
    """Calls the configured LLM API."""
    provider = os.environ.get("ONTOS_LLM_PROVIDER", "anthropic").lower()
    api_key = os.environ.get("ONTOS_LLM_API_KEY")
    
    if not api_key:
        raise ValueError("ONTOS_LLM_API_KEY environment variable not set.")

    print(f"🤖 Calling {provider} API...")

    if provider == "anthropic":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except ImportError:
            raise ImportError("anthropic library not installed. Run `pip install anthropic`.")
            
    elif provider == "openai":
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("openai library not installed. Run `pip install openai`.")
            
    elif provider == "google":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(prompt)
            return response.text
        except ImportError:
            raise ImportError("google-generativeai library not installed. Run `pip install google-generativeai`.")
            
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'anthropic', 'openai', or 'google'.")

def apply_changes(changes, dry_run=True):
    """Applies the JSON changes to the files."""
    for filepath, meta in changes.items():
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            continue
            
        print(f"📄 {filepath}")
        print(f"   ID: {meta.get('id')}")
        print(f"   Type: {meta.get('type')}")
        print(f"   Depends: {meta.get('depends_on')}")
        
        if not dry_run:
            # Construct YAML frontmatter
            frontmatter = "---\n"
            frontmatter += yaml.dump(meta, sort_keys=False)
            frontmatter += "---\n\n"
            
            with open(filepath, 'r') as f:
                original_content = f.read()
                
            with open(filepath, 'w') as f:
                f.write(frontmatter + original_content)
            print("   ✅ Applied.")
        else:
            print("   👀 Dry Run (Not Applied)")

def main():
    parser = argparse.ArgumentParser(description='Migrate markdown files to Ontos format.')
    parser.add_argument('--dir', type=str, default=DEFAULT_DOCS_DIR, help='Directory to scan')
    parser.add_argument('--auto', action='store_true', help='Use LLM API to generate tags automatically')
    parser.add_argument('--apply', action='store_true', help='Actually write changes to files (requires --auto)')
    args = parser.parse_args()

    untagged_files = get_untagged_files(args.dir)
    
    if not untagged_files:
        print("✅ No untagged files found.")
        return

    print(f"Found {len(untagged_files)} untagged files.")
    prompt = generate_prompt(untagged_files)

    if args.auto:
        try:
            response_text = call_llm_api(prompt)
            # Clean up response to get just JSON
            json_str = response_text.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
                
            changes = json.loads(json_str)
            apply_changes(changes, dry_run=not args.apply)
            
            if not args.apply:
                print("\n💡 Run with --apply to write changes.")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("💡 Falling back to manual mode...")
            with open("migration_prompt.txt", "w") as f:
                f.write(prompt)
            print("📄 Prompt saved to 'migration_prompt.txt'. Copy this to your LLM.")
            
    else:
        # Manual Mode
        with open("migration_prompt.txt", "w") as f:
            f.write(prompt)
        print("📄 Prompt saved to 'migration_prompt.txt'.")
        print("1. Copy the content of 'migration_prompt.txt' to your LLM.")
        print("2. Save the JSON response to 'migration_plan.json'.")
        print("3. (Script to apply JSON not implemented in manual mode yet - use --auto for full flow)")

if __name__ == "__main__":
    main()
