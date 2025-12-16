# S3 Archive Integration - Implementation Plan

**Date:** 2025-12-16
**Status:** Draft - Awaiting Approval
**Approach:** Option A (Consolidation Only → S3) + MCP Integration
**Prerequisite:** [S3 Archive Analysis](.ontos-internal/planning/s3-archive-analysis.md)

---

## Overview

This plan modifies the consolidation process to upload archived logs to AWS S3 instead of moving them to a local `archive/` directory. Active session logs remain local for offline capability and fast access.

---

## 1. Configuration Schema

### 1.1 New Settings in `ontos_config_defaults.py`

```python
# =============================================================================
# S3 ARCHIVE INTEGRATION (v2.5+)
# =============================================================================
# Optional S3 storage for archived logs. When enabled, consolidated logs
# are uploaded to S3 instead of moved to the local archive/ directory.
#
# IMPORTANT: Users must bring their own S3 bucket. Ontos does not provision
# or manage S3 resources.

# Enable S3 archiving (requires MCP server or boto3)
S3_ARCHIVE_ENABLED = False

# S3 bucket name (required if S3_ARCHIVE_ENABLED is True)
# Example: "my-company-ontos-archive"
S3_BUCKET = None

# S3 key prefix (optional path within bucket)
# Example: "ontos/archive/" → s3://bucket/ontos/archive/2025-12-15_log.md
S3_PREFIX = "ontos/archive/"

# AWS region (optional, uses default if not set)
# Example: "us-west-2"
S3_REGION = None

# Use MCP for S3 operations (recommended)
# - True: Use MCP server (user must configure in Claude Code settings)
# - False: Use boto3 directly (requires boto3 installed + credentials)
S3_USE_MCP = True

# MCP tool name for S3 operations
# Default assumes standard MCP S3 server naming convention
S3_MCP_TOOL_PREFIX = "mcp__s3"

# Fallback behavior when S3 upload fails
# - "local": Save to local archive/ directory (default, safest)
# - "fail": Fail the consolidation operation
# - "skip": Skip archiving (log stays in logs/ directory)
S3_FALLBACK_BEHAVIOR = "local"

# Retry configuration for transient failures
S3_RETRY_COUNT = 2
S3_RETRY_DELAY_SECONDS = 2
```

### 1.2 User Override Example in `ontos_config.py`

```python
# =============================================================================
# S3 ARCHIVE CONFIGURATION
# =============================================================================

S3_ARCHIVE_ENABLED = True
S3_BUCKET = "my-project-archives"
S3_PREFIX = "ontos/logs/"
S3_REGION = "us-east-1"

# Use MCP (recommended) - configure your MCP server in Claude Code settings
S3_USE_MCP = True
```

---

## 2. MCP Integration Design

### 2.1 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ontos_consolidate.py                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  consolidate_log()                                                      │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     S3ArchiveHandler                             │   │
│  │                                                                  │   │
│  │  ┌──────────────┐        ┌───────────────┐                      │   │
│  │  │ MCP Strategy │   OR   │ Boto3 Strategy│                      │   │
│  │  │ (preferred)  │        │ (fallback)    │                      │   │
│  │  └──────┬───────┘        └───────┬───────┘                      │   │
│  │         │                        │                               │   │
│  │         ▼                        ▼                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │                    upload_to_s3()                        │    │   │
│  │  │  - Read local file                                       │    │   │
│  │  │  - Upload to S3 (MCP tool call or boto3)                 │    │   │
│  │  │  - Return S3 URL on success                              │    │   │
│  │  │  - Raise S3UploadError on failure                        │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  │                          │                                       │   │
│  │                          ▼                                       │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │                  Fallback Handler                        │    │   │
│  │  │  - On S3 failure: save to local archive/                 │    │   │
│  │  │  - Record failure in .ontos/s3_failures.json             │    │   │
│  │  │  - Return local path with warning flag                   │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 MCP Tool Discovery

The implementation should dynamically discover available MCP S3 tools:

```python
def discover_mcp_s3_tools() -> dict:
    """
    Discover available MCP S3 tools from environment.

    Returns dict with tool names for:
    - put_object: Upload file to S3
    - get_object: Download file from S3 (for verification)
    - list_objects: List bucket contents (optional)

    Returns None if no MCP S3 tools available.
    """
    # Check for common MCP S3 tool naming conventions:
    # - mcp__s3__put_object (official AWS)
    # - mcp__s3_put_object (community)
    # - mcp__aws_s3__upload (alternative naming)
```

### 2.3 MCP Configuration for Users

Users must configure their MCP server. Documentation will include setup for popular options:

**Option A: AWS Labs Official (awslabs/mcp)**
```json
{
  "mcpServers": {
    "s3": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-s3"],
      "env": {
        "AWS_PROFILE": "default"
      }
    }
  }
}
```

**Option B: Community Server (khuynh22/aws-s3-mcp-server)**
```json
{
  "mcpServers": {
    "s3": {
      "command": "npx",
      "args": ["-y", "aws-s3-mcp-server"],
      "env": {
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

---

## 3. Changes to `ontos_consolidate.py`

### 3.1 New Imports and Dependencies

```python
# New imports at top of file
import json
import time
from typing import Optional, Union
from dataclasses import dataclass
from enum import Enum

# Conditional imports
try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
```

### 3.2 New Classes

```python
class ArchiveLocation(Enum):
    """Where the archive was stored."""
    LOCAL = "local"
    S3 = "s3"
    FAILED = "failed"


@dataclass
class ArchiveResult:
    """Result of an archive operation."""
    location: ArchiveLocation
    path: str  # Local path or S3 URL
    fallback_used: bool = False
    error_message: Optional[str] = None


class S3UploadError(Exception):
    """Raised when S3 upload fails."""
    pass
```

### 3.3 New Functions

```python
def get_s3_url(bucket: str, key: str) -> str:
    """Generate S3 URL for archived file."""
    return f"s3://{bucket}/{key}"


def upload_to_s3_mcp(filepath: str, bucket: str, key: str) -> str:
    """
    Upload file to S3 using MCP tool.

    This function is called BY the AI agent, not directly by Python.
    The actual implementation will be a prompt/instruction for the agent
    to use the MCP tool.

    Returns:
        S3 URL on success

    Raises:
        S3UploadError on failure
    """
    # This is a placeholder - actual MCP calls happen at agent level
    # See section 3.6 for agent integration design
    pass


def upload_to_s3_boto3(filepath: str, bucket: str, key: str, region: str = None) -> str:
    """
    Upload file to S3 using boto3 directly.

    Returns:
        S3 URL on success

    Raises:
        S3UploadError on failure
    """
    if not BOTO3_AVAILABLE:
        raise S3UploadError("boto3 not installed. Install with: pip install boto3")

    try:
        s3_client = boto3.client('s3', region_name=region)

        with open(filepath, 'rb') as f:
            s3_client.upload_fileobj(
                f,
                bucket,
                key,
                ExtraArgs={'ContentType': 'text/markdown; charset=utf-8'}
            )

        return get_s3_url(bucket, key)

    except Exception as e:
        raise S3UploadError(f"S3 upload failed: {e}")


def record_s3_failure(error_message: str, pending_file: str):
    """
    Record S3 failure for persistent warning.

    Creates/updates .ontos/s3_failures.json
    """
    failures_file = os.path.join(PROJECT_ROOT, '.ontos', 's3_failures.json')

    # Load existing failures
    if os.path.exists(failures_file):
        with open(failures_file, 'r') as f:
            failures = json.load(f)
    else:
        failures = {"failures": [], "pending_uploads": []}

    # Add new failure
    failures["last_failure"] = datetime.datetime.now().isoformat()
    failures["last_error"] = error_message

    # Track pending upload
    if pending_file not in failures["pending_uploads"]:
        failures["pending_uploads"].append(pending_file)

    # Write back
    os.makedirs(os.path.dirname(failures_file), exist_ok=True)
    with open(failures_file, 'w') as f:
        json.dump(failures, f, indent=2)


def check_s3_failures() -> Optional[dict]:
    """
    Check for pending S3 failures.

    Returns:
        Failure info dict if failures exist, None otherwise
    """
    failures_file = os.path.join(PROJECT_ROOT, '.ontos', 's3_failures.json')

    if not os.path.exists(failures_file):
        return None

    with open(failures_file, 'r') as f:
        failures = json.load(f)

    if failures.get("pending_uploads"):
        return failures

    return None


def clear_s3_failure(filepath: str):
    """Remove a file from pending uploads after successful sync."""
    failures_file = os.path.join(PROJECT_ROOT, '.ontos', 's3_failures.json')

    if not os.path.exists(failures_file):
        return

    with open(failures_file, 'r') as f:
        failures = json.load(f)

    if filepath in failures.get("pending_uploads", []):
        failures["pending_uploads"].remove(filepath)

    # Clear last_failure if no pending uploads
    if not failures["pending_uploads"]:
        failures.pop("last_failure", None)
        failures.pop("last_error", None)

    with open(failures_file, 'w') as f:
        json.dump(failures, f, indent=2)


def print_s3_warning():
    """Print S3 integration warning if failures exist."""
    failures = check_s3_failures()
    if failures:
        pending_count = len(failures.get("pending_uploads", []))
        print(f"""
⚠️  S3 INTEGRATION DEGRADED
    Last failure: {failures.get('last_failure', 'Unknown')}
    Reason: {failures.get('last_error', 'Unknown')}
    Pending uploads: {pending_count} file(s)

    Archives are being saved locally. Run 'ontos s3-sync' to retry.
""")
```

### 3.4 Modified `archive_log()` Function

```python
def archive_log(filepath: str, dry_run: bool = False) -> ArchiveResult:
    """
    Archive log to S3 or local directory.

    If S3 is enabled:
        1. Attempt S3 upload
        2. On failure, fall back to local archive (if configured)
        3. Record failure for persistent warning

    If S3 is disabled:
        - Move to local archive/ directory (existing behavior)

    Returns:
        ArchiveResult with location, path, and any error info
    """
    filename = os.path.basename(filepath)

    # Import config (avoid circular import issues)
    from ontos_config import (
        S3_ARCHIVE_ENABLED, S3_BUCKET, S3_PREFIX, S3_REGION,
        S3_USE_MCP, S3_FALLBACK_BEHAVIOR, S3_RETRY_COUNT, S3_RETRY_DELAY_SECONDS
    )

    # --- DRY RUN ---
    if dry_run:
        if S3_ARCHIVE_ENABLED and S3_BUCKET:
            s3_key = f"{S3_PREFIX.rstrip('/')}/{filename}"
            return ArchiveResult(
                location=ArchiveLocation.S3,
                path=get_s3_url(S3_BUCKET, s3_key)
            )
        else:
            rel_path = os.path.relpath(os.path.join(ARCHIVE_DIR, filename), PROJECT_ROOT)
            return ArchiveResult(location=ArchiveLocation.LOCAL, path=rel_path)

    # --- S3 ARCHIVING ---
    if S3_ARCHIVE_ENABLED and S3_BUCKET:
        s3_key = f"{S3_PREFIX.rstrip('/')}/{filename}"
        s3_url = get_s3_url(S3_BUCKET, s3_key)

        # Attempt upload with retries
        last_error = None
        for attempt in range(S3_RETRY_COUNT + 1):
            try:
                if S3_USE_MCP:
                    # MCP upload - see section 3.6
                    upload_to_s3_mcp(filepath, S3_BUCKET, s3_key)
                else:
                    # Direct boto3 upload
                    upload_to_s3_boto3(filepath, S3_BUCKET, s3_key, S3_REGION)

                # Success - delete local file
                os.remove(filepath)
                return ArchiveResult(location=ArchiveLocation.S3, path=s3_url)

            except S3UploadError as e:
                last_error = str(e)
                if attempt < S3_RETRY_COUNT:
                    time.sleep(S3_RETRY_DELAY_SECONDS * (attempt + 1))
                    continue

        # All retries failed - handle fallback
        if S3_FALLBACK_BEHAVIOR == "local":
            # Fall back to local archive
            record_s3_failure(last_error, filepath)
            local_result = _archive_locally(filepath)
            if local_result:
                return ArchiveResult(
                    location=ArchiveLocation.LOCAL,
                    path=local_result,
                    fallback_used=True,
                    error_message=f"S3 failed, saved locally: {last_error}"
                )

        elif S3_FALLBACK_BEHAVIOR == "fail":
            record_s3_failure(last_error, filepath)
            return ArchiveResult(
                location=ArchiveLocation.FAILED,
                path=filepath,
                error_message=last_error
            )

        elif S3_FALLBACK_BEHAVIOR == "skip":
            record_s3_failure(last_error, filepath)
            return ArchiveResult(
                location=ArchiveLocation.FAILED,
                path=filepath,
                error_message=f"S3 failed, log not archived: {last_error}"
            )

    # --- LOCAL ARCHIVING (S3 disabled or not configured) ---
    local_path = _archive_locally(filepath)
    if local_path:
        return ArchiveResult(location=ArchiveLocation.LOCAL, path=local_path)

    return ArchiveResult(
        location=ArchiveLocation.FAILED,
        path=filepath,
        error_message="Failed to archive locally"
    )


def _archive_locally(filepath: str) -> Optional[str]:
    """Move file to local archive directory. Returns relative path or None."""
    filename = os.path.basename(filepath)
    archive_path = os.path.join(ARCHIVE_DIR, filename)
    rel_archive_path = os.path.relpath(archive_path, PROJECT_ROOT)

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    try:
        shutil.move(filepath, archive_path)
        return rel_archive_path
    except Exception as e:
        print(f"Error archiving {filepath}: {e}")
        return None
```

### 3.5 Modified `consolidate_log()` Function

```python
def consolidate_log(filepath: str, doc_id: str, frontmatter: dict,
                    dry_run: bool = False, quiet: bool = False,
                    auto: bool = False) -> bool:
    """Consolidate a single log file."""

    # ... existing code for summary extraction ...

    if dry_run:
        result = archive_log(filepath, dry_run=True)
        print(f"   [DRY RUN] Would archive to: {result.path}")
        return True

    # ... existing confirmation logic ...

    # Archive file
    result = archive_log(filepath, dry_run=False)

    if result.location == ArchiveLocation.FAILED:
        print(f"   ❌ Archive failed: {result.error_message}")
        return False

    # Warn if fallback was used
    if result.fallback_used:
        print(f"   ⚠️  S3 upload failed, saved locally: {result.path}")

    # Append to decision history with appropriate path
    if append_to_decision_history(date, slug, event_type, summary, impacts, result.path):
        location_str = "S3" if result.location == ArchiveLocation.S3 else "local archive"
        print(f"   ✅ Archived to {location_str} and recorded in decision_history.md")
        return True
    else:
        print(f"   ⚠️  File archived but failed to update decision_history.md")
        return False
```

### 3.6 MCP Integration Strategy

Since MCP tools are invoked by the AI agent (not directly by Python scripts), we need a hybrid approach:

**For CLI usage (humans running `python ontos_consolidate.py`):**
- Use boto3 directly (S3_USE_MCP = False)
- Requires boto3 installed and AWS credentials configured

**For agent usage (Claude Code running consolidation):**
- Agent detects S3 is enabled
- Agent uses MCP tools directly for upload
- Python script provides the file content and S3 key

```python
def get_mcp_upload_instructions(filepath: str, bucket: str, key: str) -> str:
    """
    Generate instructions for agent to perform MCP upload.

    Returns a structured prompt that the agent can execute.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return f"""
AGENT INSTRUCTION: Upload to S3 via MCP

Bucket: {bucket}
Key: {key}
Content-Type: text/markdown; charset=utf-8

Use the MCP S3 tool (mcp__s3__put_object or similar) to upload the following content:

---BEGIN CONTENT---
{content}
---END CONTENT---

After successful upload, confirm the S3 URL: s3://{bucket}/{key}
"""
```

---

## 4. Fallback Behavior and Warning System

### 4.1 Failure Recording

File: `.ontos/s3_failures.json`

```json
{
  "last_failure": "2025-12-16T10:30:00.123456",
  "last_error": "AccessDenied: Access Denied",
  "pending_uploads": [
    ".ontos-internal/archive/logs/2025-12-15_feature.md",
    ".ontos-internal/archive/logs/2025-12-14_bugfix.md"
  ]
}
```

### 4.2 Warning Integration Points

Modify the following scripts to check and display S3 warnings:

| Script | Integration Point |
|--------|-------------------|
| `ontos_consolidate.py` | At start of `main()` |
| `ontos_end_session.py` | At start of `main()` |
| `ontos_pre_push_check.py` | After archive check |
| `ontos_maintain.py` | At start of maintenance |
| `ontos_generate_context_map.py` | After generation completes |

### 4.3 Warning Output Format

```
⚠️  S3 INTEGRATION DEGRADED
    Last failure: 2025-12-16 10:30 UTC
    Reason: AccessDenied: Access Denied
    Pending uploads: 2 file(s)

    Archives are being saved locally. Run 'ontos s3-sync' to retry.
```

---

## 5. New CLI Command: `ontos s3-sync`

### 5.1 Purpose

Retry failed S3 uploads for files that fell back to local storage.

### 5.2 Implementation

New file: `.ontos/scripts/ontos_s3_sync.py`

```python
"""Sync local archives to S3 after failed uploads."""

def main():
    """
    1. Read .ontos/s3_failures.json
    2. For each pending upload:
       a. Check if local file exists
       b. Attempt S3 upload
       c. On success: delete local file, remove from pending
       d. On failure: report error, keep in pending
    3. Report summary
    """
    pass
```

### 5.3 CLI Integration

```bash
# Retry all failed uploads
python3 .ontos/scripts/ontos_s3_sync.py

# Dry run to see what would be synced
python3 .ontos/scripts/ontos_s3_sync.py --dry-run

# Force re-upload all local archives (not just failures)
python3 .ontos/scripts/ontos_s3_sync.py --all
```

---

## 6. Decision History Path Format

### 6.1 Current Format (Local)

```markdown
| 2025-12-13 | feature-x | feature | Added OAuth | auth | `.ontos-internal/archive/logs/2025-12-13_feature-x.md` |
```

### 6.2 New Format (S3)

```markdown
| 2025-12-13 | feature-x | feature | Added OAuth | auth | `s3://my-bucket/ontos/archive/2025-12-13_feature-x.md` |
```

### 6.3 Agent Instructions Update

Update `docs/reference/Ontos_Agent_Instructions.md`:

```markdown
## Historical Recall

The `archive/` directory is excluded from the Context Map to save tokens.

To understand rationale behind past decisions:

1. **Read** `docs/strategy/decision_history.md`
2. **Locate** the relevant entry by date, slug, or impacted document
3. **Retrieve** the archived content:
   - **Local path** (e.g., `.ontos-internal/archive/logs/...`): Read directly
   - **S3 URL** (e.g., `s3://bucket/...`): Use MCP S3 tool to fetch content
```

---

## 7. File Changes Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `ontos_config_defaults.py` | Add | S3 configuration constants |
| `ontos_config.py` | Document | Example S3 configuration |
| `ontos_consolidate.py` | Modify | S3 upload logic, fallback handling |
| `ontos_s3_sync.py` | New | Sync failed uploads to S3 |
| `ontos_end_session.py` | Modify | Add S3 warning check |
| `ontos_pre_push_check.py` | Modify | Add S3 warning check |
| `ontos_maintain.py` | Modify | Add S3 warning check |
| `ontos_generate_context_map.py` | Modify | Add S3 warning check |
| `Ontos_Agent_Instructions.md` | Modify | S3 URL retrieval instructions |
| `.gitignore` | Modify | Add `.ontos/s3_failures.json` |

---

## 8. Testing Plan

### 8.1 Unit Tests

| Test | Description |
|------|-------------|
| `test_s3_url_generation` | Verify S3 URL format |
| `test_archive_log_local` | Existing behavior unchanged when S3 disabled |
| `test_archive_log_s3_success` | S3 upload succeeds |
| `test_archive_log_s3_failure_fallback` | Falls back to local on S3 failure |
| `test_archive_log_s3_failure_fail` | Fails when fallback=fail |
| `test_s3_failure_recording` | Failures recorded to JSON |
| `test_s3_warning_display` | Warning shown when failures exist |

### 8.2 Integration Tests

| Test | Description |
|------|-------------|
| `test_consolidation_to_s3` | Full consolidation workflow with S3 |
| `test_consolidation_fallback` | Consolidation falls back gracefully |
| `test_s3_sync_retry` | Sync command retries failed uploads |
| `test_decision_history_s3_path` | S3 URL recorded in decision history |

### 8.3 Manual Testing

1. **S3 disabled**: Verify existing behavior unchanged
2. **S3 enabled, success**: Verify upload works
3. **S3 enabled, failure**: Verify fallback and warning
4. **S3 sync**: Verify retry works
5. **Agent workflow**: Verify agent can read S3 paths from decision history

---

## 9. Documentation Updates

### 9.1 New Section in Ontos Manual

```markdown
## S3 Archive Integration

Ontos can archive old session logs to AWS S3 instead of storing them locally.

### Setup

1. **Configure MCP Server** (recommended):
   Add to your Claude Code MCP settings...

2. **Enable in ontos_config.py**:
   ```python
   S3_ARCHIVE_ENABLED = True
   S3_BUCKET = "your-bucket-name"
   ```

3. **Test**: Run `python3 .ontos/scripts/ontos_consolidate.py --dry-run`

### Troubleshooting

If S3 uploads fail, archives are saved locally and a warning is displayed.
Run `ontos s3-sync` to retry failed uploads.
```

---

## 10. Migration Path

### 10.1 For Existing Users

1. S3 is **opt-in** - existing behavior unchanged by default
2. Users enable S3 when ready by setting `S3_ARCHIVE_ENABLED = True`
3. Existing local archives remain in place (no automatic migration)
4. Optional: Use `ontos s3-sync --all` to upload existing archives

### 10.2 Version Bump

- Current: v2.4.0
- After this feature: v2.5.0

---

## 11. Open Questions

1. **MCP tool naming**: Should we auto-discover MCP tools or require explicit configuration?
   - **Proposed**: Auto-discover with fallback to configuration

2. **Archive verification**: Should we verify S3 upload by reading back?
   - **Proposed**: No - adds latency, trust S3 success response

3. **Encryption**: Should we support S3 SSE configuration?
   - **Proposed**: Defer to v2.6 - users can configure bucket-level encryption

4. **Multi-region**: Should we support multi-region S3?
   - **Proposed**: Defer - single region is sufficient for v2.5

---

## 12. Implementation Order

1. **Phase 1: Configuration** (Low risk)
   - Add S3 settings to `ontos_config_defaults.py`
   - Document configuration in `ontos_config.py`

2. **Phase 2: Core Logic** (Medium risk)
   - Implement `S3ArchiveHandler` in `ontos_consolidate.py`
   - Implement fallback and failure recording

3. **Phase 3: Warning System** (Low risk)
   - Add warning checks to all entry points
   - Create `ontos_s3_sync.py`

4. **Phase 4: Agent Integration** (Medium risk)
   - Update Agent Instructions
   - Test MCP tool discovery

5. **Phase 5: Documentation** (Low risk)
   - Update Ontos Manual
   - Add troubleshooting guide

---

## Approval

- [ ] User approves overall approach
- [ ] User confirms MCP vs boto3 preference
- [ ] User confirms fallback behavior preference
- [ ] User confirms S3 URL format in decision_history.md

