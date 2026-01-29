"""Tests for migration-report command."""

import json
import subprocess
import sys
import pytest
from pathlib import Path


class TestMigrationReportCommand:
    """Tests for ontos migration-report command."""

    def test_migration_report_help(self):
        """Verify --help works."""
        result = subprocess.run(
            [sys.executable, "-m", "ontos", "migration-report", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "--output" in result.stdout
        assert "--format" in result.stdout

    def test_migration_report_markdown(self, tmp_path):
        """Generate markdown report."""
        config = tmp_path / ".ontos.toml"
        config.write_text("[ontos]\nversion = '3.2'\n")
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "k.md").write_text("---\nid: k1\ntype: kernel\nstatus: active\n---\n")
        (docs / "a.md").write_text("---\nid: a1\ntype: atom\nstatus: active\n---\n")

        output = tmp_path / "report.md"

        result = subprocess.run(
            [sys.executable, "-m", "ontos", "migration-report", "-o", str(output)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        assert result.returncode == 0
        assert output.exists()
        content = output.read_text()
        assert "# Migration Report" in content
        assert "Safe to migrate" in content or "Safe to Migrate" in content

    def test_migration_report_json(self, tmp_path):
        """Generate JSON report."""
        config = tmp_path / ".ontos.toml"
        config.write_text("[ontos]\nversion = '3.2'\n")
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "k.md").write_text("---\nid: k1\ntype: kernel\nstatus: active\n---\n")

        output = tmp_path / "report.json"

        result = subprocess.run(
            [sys.executable, "-m", "ontos", "migration-report", "--format", "json", "-o", str(output)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        assert result.returncode == 0
        data = json.loads(output.read_text())
        assert data["schema_version"] == "ontos-migration-report-v1"
        assert "summary" in data
        assert "classifications" in data


class TestMigrateConvenienceCommand:
    """Tests for ontos migrate convenience command."""

    def test_migrate_help(self):
        """Verify --help works."""
        result = subprocess.run(
            [sys.executable, "-m", "ontos", "migrate", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "--out-dir" in result.stdout

    def test_migrate_creates_artifacts(self, tmp_path):
        """Migrate creates both files."""
        config = tmp_path / ".ontos.toml"
        config.write_text("[ontos]\nversion = '3.2'\n")
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "test.md").write_text("---\nid: test\ntype: atom\nstatus: active\n---\n")

        out_dir = tmp_path / "migration"

        result = subprocess.run(
            [sys.executable, "-m", "ontos", "migrate", "--out-dir", str(out_dir)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        assert result.returncode == 0
        assert (out_dir / "snapshot.json").exists()
        assert (out_dir / "analysis.md").exists()
