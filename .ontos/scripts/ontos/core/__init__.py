"""Core module - Pure logic layer.

This module contains pure functions and classes that do NOT perform I/O,
except for functions explicitly marked as IMPURE in their docstrings.

IMPURE functions:
    - staleness.get_file_modification_date() - calls git subprocess
    - staleness.check_staleness() - uses get_file_modification_date()
"""

from ontos.core.context import SessionContext
from ontos.core.frontmatter import parse_frontmatter, normalize_depends_on
from ontos.core.staleness import (
    ModifiedSource,
    normalize_describes,
    validate_describes_field,
    check_staleness,
)
from ontos.core.history import generate_decision_history, ParsedLog
