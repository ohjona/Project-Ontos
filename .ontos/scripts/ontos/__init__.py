"""Ontos - Context Management System.

v2.8: Unified package structure for clean architecture.

Package structure:
    ontos.core - Pure logic (no I/O except marked impure functions)
    ontos.ui   - I/O layer (CLI, output, prompts)
"""

from ontos.core.context import SessionContext
from ontos.core.frontmatter import parse_frontmatter, normalize_depends_on
from ontos.core.staleness import (
    ModifiedSource,
    normalize_describes,
    parse_describes_verified,
    validate_describes_field,
    detect_describes_cycles,
    check_staleness,
    get_file_modification_date,
    clear_git_cache,
)
from ontos.core.history import (
    ParsedLog,
    parse_log_for_history,
    sort_logs_deterministically,
    generate_decision_history,
)

__version__ = "2.8.0"
