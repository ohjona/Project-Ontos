"""Pre-commit hook for Ontos auto-consolidation (v2.5).

Safety features (from architectural review):
- CI detection: Skips in automated environments
- Rebase detection: Skips during rebase/cherry-pick
- Explicit staging: Only stages Ontos files, never user files
- Try/except wrapper: Guarantees return 0
- Dual condition: Count AND old_logs must both be true
"""

import os
import sys
import subprocess
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ontos_lib import resolve_config
from ontos_config_defaults import PROJECT_ROOT, is_ontos_repo


def get_logs_dir() -> str:
    """Get the logs directory path based on mode (contributor vs user)."""
    if is_ontos_repo():
        return os.path.join(PROJECT_ROOT, '.ontos-internal', 'logs')
    else:
        return os.path.join(PROJECT_ROOT, 'docs', 'logs')


def get_mode() -> str:
    """Get current Ontos mode."""
    return resolve_config('ONTOS_MODE', 'prompted')


def get_log_count() -> int:
    """Count active logs in logs directory."""
    logs_dir = get_logs_dir()
    if not os.path.exists(logs_dir):
        return 0
    return len([f for f in os.listdir(logs_dir)
                if f.endswith('.md') and f[0].isdigit()])


def get_logs_older_than(days: int) -> list:
    """Get list of log filenames older than N days."""
    logs_dir = get_logs_dir()
    if not os.path.exists(logs_dir):
        return []

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    old_logs = []

    for filename in os.listdir(logs_dir):
        if not filename.endswith('.md') or not filename[0].isdigit():
            continue
        try:
            log_date = datetime.datetime.strptime(filename[:10], '%Y-%m-%d')
            if log_date < cutoff:
                old_logs.append(filename)
        except ValueError:
            continue

    return old_logs


def is_ci_environment() -> bool:
    """Detect CI/CD environments where hook should be skipped."""
    ci_indicators = [
        'CI',                    # Generic (GitHub Actions, GitLab CI, etc.)
        'CONTINUOUS_INTEGRATION', # Travis CI
        'GITHUB_ACTIONS',        # GitHub Actions
        'GITLAB_CI',             # GitLab CI
        'JENKINS_URL',           # Jenkins
        'CIRCLECI',              # CircleCI
        'BUILDKITE',             # Buildkite
        'TF_BUILD',              # Azure Pipelines
    ]
    return any(os.environ.get(var) for var in ci_indicators)


def is_special_git_operation() -> bool:
    """Detect rebase, cherry-pick, etc. where hook should be skipped."""
    result = subprocess.run(
        ['git', 'rev-parse', '--git-dir'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return False

    git_dir = result.stdout.strip()

    # Rebase in progress
    if (os.path.exists(os.path.join(git_dir, 'rebase-merge')) or
        os.path.exists(os.path.join(git_dir, 'rebase-apply'))):
        return True

    # Cherry-pick in progress
    if os.path.exists(os.path.join(git_dir, 'CHERRY_PICK_HEAD')):
        return True

    return False


def should_consolidate() -> bool:
    """Check if consolidation should run.

    Uses DUAL CONDITION (from architectural review):
    - Count must exceed threshold AND
    - There must be logs old enough to consolidate

    This prevents confusing "nothing to consolidate" messages.
    """
    mode = get_mode()

    # Only auto-consolidate in automated mode
    if mode != 'automated':
        return False

    # Skip in CI environments
    if is_ci_environment():
        return False

    # Skip during rebase/cherry-pick
    if is_special_git_operation():
        return False

    # Skip if explicitly disabled
    if os.environ.get('ONTOS_SKIP_HOOKS', '').lower() in ('1', 'true', 'yes'):
        return False

    # Check if feature is enabled (allows override)
    if not resolve_config('AUTO_CONSOLIDATE_ON_COMMIT', True):
        return False

    # DUAL CONDITION: Count high AND old logs exist
    log_count = get_log_count()
    threshold_count = resolve_config('LOG_RETENTION_COUNT', 15)

    if log_count <= threshold_count:
        return False  # Count is fine

    # Count is high - are there old logs to consolidate?
    threshold_days = resolve_config('CONSOLIDATION_THRESHOLD_DAYS', 30)
    old_logs = get_logs_older_than(threshold_days)

    return len(old_logs) > 0


def run_consolidation() -> tuple:
    """Run consolidation in quiet, auto mode.

    Returns:
        (success, output) tuple
    """
    script = os.path.join(PROJECT_ROOT, '.ontos', 'scripts', 'ontos_consolidate.py')
    threshold_days = resolve_config('CONSOLIDATION_THRESHOLD_DAYS', 30)

    result = subprocess.run(
        [sys.executable, script, '--all', '--quiet', '--days', str(threshold_days)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout + result.stderr


def stage_consolidated_files() -> None:
    """Stage ONLY files modified by consolidation.

    CRITICAL: Do NOT use 'git add -u' which stages ALL tracked files.
    Only stage specific Ontos-managed paths.
    """
    # Determine paths based on mode (contributor vs user)
    if is_ontos_repo():
        decision_history = os.path.join(PROJECT_ROOT, '.ontos-internal', 'strategy', 'decision_history.md')
        archive_dir = os.path.join(PROJECT_ROOT, '.ontos-internal', 'archive')
        logs_dir = os.path.join(PROJECT_ROOT, '.ontos-internal', 'logs')
    else:
        decision_history = os.path.join(PROJECT_ROOT, 'docs', 'decision_history.md')
        archive_dir = os.path.join(PROJECT_ROOT, 'docs', 'archive')
        logs_dir = os.path.join(PROJECT_ROOT, 'docs', 'logs')

    # Stage ONLY Ontos-managed files
    if os.path.exists(decision_history):
        subprocess.run(['git', 'add', decision_history], capture_output=True)

    if os.path.exists(archive_dir):
        subprocess.run(['git', 'add', archive_dir], capture_output=True)

    # Stage logs directory (captures moved/deleted logs)
    if os.path.exists(logs_dir):
        subprocess.run(['git', 'add', logs_dir], capture_output=True)


def main() -> int:
    """Main entry point for pre-commit hook.

    Returns:
        0 ALWAYS (never block commit) - wrapped in try/except
    """
    try:
        verbose = os.environ.get('ONTOS_VERBOSE', '').lower() in ('1', 'true')

        if verbose:
            print("   [Ontos pre-commit hook running...]")

        if not should_consolidate():
            if verbose:
                print("   [Ontos: No consolidation needed]")
            return 0

        log_count = get_log_count()
        threshold = resolve_config('LOG_RETENTION_COUNT', 15)

        print(f"   Auto-consolidating ({log_count} logs > {threshold} threshold)...")

        success, output = run_consolidation()

        if success:
            stage_consolidated_files()
            print("   Consolidated and staged")
        else:
            # Check if it's a "no work" vs "real error"
            if "No logs older than" in output or "No logs found" in output:
                if verbose:
                    print("   [Ontos: No old logs to consolidate]")
            else:
                # Surface real errors (permission, disk, etc.)
                print(f"   Warning: Consolidation issue: {output[:200]}")

        return 0  # Never block commit

    except Exception as e:
        # Guarantee return 0 even on unexpected errors
        print(f"   Warning: Ontos pre-commit hook error: {e}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
