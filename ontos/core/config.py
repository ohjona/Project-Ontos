"""Configuration helpers.

This module contains functions for resolving configuration values
and getting session source information.

PURE (after Phase 2 refactor): Functions accept optional callbacks for git operations.

For production use with git:
    from ontos.io.git import get_git_config, get_file_mtime
    source = get_source(git_username_provider=lambda: get_git_config("user.name"))
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable


# Branch names that should not be used as auto-slugs
BLOCKED_BRANCH_NAMES = {'main', 'master', 'dev', 'develop', 'HEAD'}


def get_source(
    git_username_provider: Optional[Callable[[], Optional[str]]] = None
) -> Optional[str]:
    """Get session log source with fallback chain.

    PURE: Accepts optional callback for git operations.

    For production use with git:
        from ontos.io.git import get_git_config
        source = get_source(git_username_provider=lambda: get_git_config("user.name"))

    Resolution order:
    1. ONTOS_SOURCE environment variable
    2. DEFAULT_SOURCE in config
    3. git config user.name (via provider)
    4. None (caller should prompt)

    Args:
        git_username_provider: Optional callback that returns git user.name or None.

    Returns:
        Source string or None if caller should prompt.
    """
    # 1. Environment variable
    env_source = os.environ.get('ONTOS_SOURCE')
    if env_source:
        return env_source

    # 2. Config default
    try:
        from ontos_config import DEFAULT_SOURCE
        if DEFAULT_SOURCE:
            return DEFAULT_SOURCE
    except (ImportError, AttributeError):
        pass

    # 3. Git user name via provider
    if git_username_provider is not None:
        try:
            git_username = git_username_provider()
            if git_username:
                return git_username
        except Exception:
            pass

    # 4. Caller should prompt
    return None


def get_git_last_modified(
    filepath: str,
    git_mtime_provider: Optional[Callable[[Path], Optional[datetime]]] = None
) -> Optional[datetime]:
    """Get the last git commit date for a file.

    PURE: Accepts optional callback for git operations.

    For production use with git:
        from ontos.io.git import get_file_mtime
        modified = get_git_last_modified(path, git_mtime_provider=get_file_mtime)

    Args:
        filepath: Path to the file to check.
        git_mtime_provider: Optional callback that takes a Path and returns
            a datetime from git history.

    Returns:
        datetime of last modification, or None if not tracked by git.
    """
    if git_mtime_provider is not None:
        try:
            return git_mtime_provider(Path(filepath))
        except Exception:
            pass
    return None
