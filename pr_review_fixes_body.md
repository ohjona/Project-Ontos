## Summary

Addressing findings from adversarial code review #51.

## Changes

### 1. Robust Initialization Cleanup (X-M1)
- Improved `KeyboardInterrupt` (Ctrl+C) handling in `init_command`.
- Initialization now tracks all created directories and files, ensuring they are removed if aborted at the hook consent prompt.
- Prevents partial initialization state (orphaned `docs/` or `Ontos_Context_Map.md`).

### 2. Enhanced Test Assertions (X-M2)
- Updated `test_hook_collision_force_overwrites` to explicitly verify that foreign hook content is replaced, not just appended to.

### 3. Filled Coverage Gaps
- **EOF Handling**: Added `test_ctrl_d_skips_hooks` to verify initialization proceeds while skipping hooks on EOF.
- **Environment Detection**: Added `test_non_tty_auto_installs_hooks` to verify CI/non-TTY behavior.
- **Cleanup Verification**: Added assertion to `test_ctrl_c_aborts_init_and_cleans_up` to verify directory/map removal.

## Testing

- [x] `pytest tests/commands/test_init_phase3.py` (20 tests passed)
- [x] Full test suite `pytest tests/` (429 tests passed)
- [x] Manual verification of directory cleanup on Ctrl+C
