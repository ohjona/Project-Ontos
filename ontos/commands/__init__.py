"""
Commands module - High-level command orchestration.

This module contains command implementations that orchestrate
core logic and I/O operations. Commands may import from all layers.

Phase 2 creates map.py and log.py as the primary orchestration modules.
"""

from ontos.commands.map import (
    GenerateMapOptions,
    generate_context_map,
)

from ontos.commands.log import (
    EndSessionOptions,
    create_session_log,
    suggest_session_impacts,
    validate_session_concepts,
)

__all__ = [
    # map command
    "GenerateMapOptions",
    "generate_context_map",
    # log command
    "EndSessionOptions",
    "create_session_log",
    "suggest_session_impacts",
    "validate_session_concepts",
]
