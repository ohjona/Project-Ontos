"""Scaffold a new session log file for Ontos."""

import os
import re
import datetime
import subprocess
import argparse
import sys

from config import __version__, LOGS_DIR

# Valid slug pattern: lowercase letters, numbers, and hyphens
VALID_SLUG_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$')
MAX_SLUG_LENGTH = 50


def validate_topic_slug(slug: str) -> tuple[bool, str]:
    """Validate topic slug for use in filenames.

    Args:
        slug: The topic slug to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not slug:
        return False, "Topic slug cannot be empty."

    if len(slug) > MAX_SLUG_LENGTH:
        return False, f"Topic slug too long (max {MAX_SLUG_LENGTH} characters)."

    # Convert to lowercase for validation
    slug_lower = slug.lower()

    if not VALID_SLUG_PATTERN.match(slug_lower):
        return False, (
            "Invalid topic slug. Use lowercase letters, numbers, and hyphens only.\n"
            "  Examples: 'auth-refactor', 'bug-fix', 'feature-123'"
        )

    # Check for reserved names on Windows
    reserved = {'con', 'prn', 'aux', 'nul', 'com1', 'lpt1'}
    if slug_lower in reserved:
        return False, f"'{slug}' is a reserved name and cannot be used."

    return True, ""


def get_daily_git_log() -> str:
    """Gets the git log for the current day.

    Returns:
        Formatted git log string or error message.
    """
    try:
        result = subprocess.run(
            ['git', 'log', '--since=midnight', '--pretty=format:%h - %s'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return "Git log unavailable (not a git repository or git not installed)."

        logs = result.stdout.strip()
        if not logs:
            return "No commits found for today."
        return logs
    except subprocess.TimeoutExpired:
        return "Git log timed out."
    except FileNotFoundError:
        return "Git is not installed or not in PATH."
    except Exception as e:
        return f"Error running git: {e}"


def create_log_file(topic_slug: str, quiet: bool = False) -> str:
    """Creates a new session log file with a template.

    Args:
        topic_slug: Short slug describing the session.
        quiet: Suppress output if True.

    Returns:
        Path to the created log file, or empty string on error.
    """
    # Normalize slug to lowercase
    topic_slug = topic_slug.lower()

    try:
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)
            if not quiet:
                print(f"Created directory: {LOGS_DIR}")
    except (IOError, OSError, PermissionError) as e:
        print(f"Error: Failed to create directory {LOGS_DIR}: {e}")
        return ""

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_{topic_slug}.md"
    filepath = os.path.join(LOGS_DIR, filename)

    if os.path.exists(filepath):
        if not quiet:
            print(f"Log file already exists: {filepath}")
        return filepath

    daily_log = get_daily_git_log()

    content = f"""---
id: log_{today.replace('-', '')}_{topic_slug.replace('-', '_')}
type: atom
status: active
depends_on: []
---

# Session Log: {topic_slug.replace('-', ' ').title()}
Date: {today}

## 1. Goal
<!-- [AGENT: Fill this in. What was the primary objective of this session?] -->

## 2. Key Decisions
<!-- [AGENT: Fill this in. What architectural or design choices were made?] -->
-

## 3. Changes Made
<!-- [AGENT: Fill this in. Summary of file changes.] -->
-

## 4. Next Steps
<!-- [AGENT: Fill this in. What should the next agent work on?] -->
-

---
## Raw Session History
```text
{daily_log}
```
"""

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except (IOError, OSError, PermissionError) as e:
        print(f"Error: Failed to write log file: {e}")
        return ""

    if not quiet:
        print(f"Created session log: {filepath}")
    return filepath


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scaffold a new session log file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 end_session.py auth-refactor       # Create log for auth refactor session
  python3 end_session.py bug-fix --quiet     # Create log without output

Slug format:
  - Use lowercase letters, numbers, and hyphens
  - Examples: 'auth-refactor', 'v2-migration', 'fix-123'
"""
    )
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('topic', type=str, nargs='?', help='Short slug describing the session (e.g. auth-refactor)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress non-error output')
    args = parser.parse_args()

    if not args.topic:
        parser.print_help()
        sys.exit(1)

    # Validate topic slug
    is_valid, error_msg = validate_topic_slug(args.topic)
    if not is_valid:
        print(f"Error: {error_msg}")
        sys.exit(1)

    result = create_log_file(args.topic, args.quiet)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
