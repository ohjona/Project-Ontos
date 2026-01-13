"""Config file I/O operations."""
from pathlib import Path
from typing import Optional

from ontos.core.config import (
    OntosConfig,
    ConfigError,
    default_config,
    dict_to_config,
    config_to_dict,
)
from ontos.io.toml import load_config_if_exists, write_config

CONFIG_FILENAME = ".ontos.toml"


def find_config(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find .ontos.toml walking up directory tree."""
    path = start_path or Path.cwd()
    for parent in [path] + list(path.parents):
        config_path = parent / CONFIG_FILENAME
        if config_path.exists():
            return config_path
    return None


def load_project_config(
    config_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> OntosConfig:
    """Load config from file, or return defaults if not found."""
    if config_path is None:
        config_path = find_config()

    if config_path is None:
        return default_config()

    # Error handling for malformed TOML
    try:
        data = load_config_if_exists(config_path)
    except Exception as e:
        raise ConfigError(f"Failed to parse {config_path}: {e}") from e

    if data is None:
        return default_config()

    # Use config file's parent as repo root if not specified
    effective_repo_root = repo_root or config_path.parent

    return dict_to_config(data, repo_root=effective_repo_root)


def save_project_config(config: OntosConfig, path: Path) -> None:
    """Save configuration to .ontos.toml file."""
    data = config_to_dict(config)
    write_config(path, data)


def config_exists(path: Optional[Path] = None) -> bool:
    """Check if .ontos.toml exists."""
    check_path = path or Path.cwd() / CONFIG_FILENAME
    return check_path.exists()
