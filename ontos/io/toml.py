"""
TOML configuration loading and writing.

Supports Python 3.9+ with tomli fallback for older versions.

Phase 2 Decomposition - Created from Phase2-Implementation-Spec.md Section 4.8
"""

from pathlib import Path
from typing import Any, Dict, Optional

# Python 3.11+ has tomllib in stdlib
try:
    import tomllib
except ImportError:
    # Python 3.9-3.10 needs the tomli package
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore


def load_config(path: Path) -> Dict[str, Any]:
    """Load configuration from TOML file.

    Args:
        path: Path to .toml file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If TOML parsing fails or tomli not available
    """
    if tomllib is None:
        raise ValueError(
            "TOML support requires Python 3.11+ or the 'tomli' package. "
            "Install with: pip install tomli"
        )

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "rb") as f:
        return tomllib.load(f)


def load_config_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    """Load configuration from TOML file if it exists.

    Args:
        path: Path to .toml file

    Returns:
        Configuration dictionary or None if file doesn't exist
    """
    if not path.exists():
        return None
    try:
        return load_config(path)
    except (ValueError, FileNotFoundError):
        return None


def write_config(path: Path, config: Dict[str, Any]) -> None:
    """Write configuration to TOML file.

    Note: This is a simple implementation. For complex TOML writing,
    consider using the tomlkit package.

    Args:
        path: Destination path
        config: Configuration dictionary
    """
    lines = []
    for key, value in config.items():
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        elif isinstance(value, bool):
            lines.append(f'{key} = {str(value).lower()}')
        elif isinstance(value, (int, float)):
            lines.append(f'{key} = {value}')
        elif isinstance(value, list):
            items = ", ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in value)
            lines.append(f'{key} = [{items}]')
        elif isinstance(value, dict):
            lines.append(f'[{key}]')
            for k, v in value.items():
                if isinstance(v, str):
                    lines.append(f'{k} = "{v}"')
                else:
                    lines.append(f'{k} = {v}')
            lines.append('')

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple configuration dictionaries.

    Later configs override earlier ones.

    Args:
        *configs: Configuration dictionaries to merge

    Returns:
        Merged configuration
    """
    result: Dict[str, Any] = {}
    for config in configs:
        if config:
            for key, value in config.items():
                if isinstance(value, dict) and isinstance(result.get(key), dict):
                    # Deep merge for nested dicts
                    result[key] = {**result[key], **value}
                else:
                    result[key] = value
    return result
