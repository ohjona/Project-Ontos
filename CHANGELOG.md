# Changelog

All notable changes to this project will be documented in this file.

## [3.0.2] - 2026-01-18

### Fixed
- Fixed sys.path shadowing issue in legacy scripts where `ontos/_scripts/ontos.py`
  shadowed the `ontos` package, causing `ModuleNotFoundError: 'ontos' is not a package`
- Commands now working: `scaffold`, `stub`, `promote`, `migrate`

### Known Issues
- Commands `verify`, `query`, `consolidate` remain broken (deferred to v3.0.3)
- Legacy scripts ignore `.ontos.toml` settings (use native CLI commands which respect config)
