"""Rebuild governed multipart CAD outputs whose installed build no longer passes audit.

Designed for VS Code's preLaunchTask. Only complete printable-manifest builds
and their installed-output audits run automatically; the expensive, supplementary
assembly review remains an explicit release-checkpoint command.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build_command(design: str, config: Path) -> list[str]:
    return [sys.executable, "scripts/scad_build_all.py", "--design", design,
            "--config", str(config.relative_to(ROOT)), "--destination", "current"]


def is_current(design: str, config: Path) -> bool:
    """The installed build is current exactly when its hash audit passes.

    File mtimes are not used: checkouts and clones rewrite them, and content
    hashes already record what each build was made from.
    """
    result = subprocess.run([*build_command(design, config), "--audit-only"], cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode:
        reason = (result.stderr or result.stdout).strip().splitlines()
        print(f"STALE {design}: {reason[-1] if reason else 'audit failed'}")
    return result.returncode == 0


def configured_path(design: Path) -> Path | None:
    manifest = ROOT / "output" / design.name / "build_manifest.json"
    if manifest.is_file():
        try:
            value = json.loads(manifest.read_text(encoding="utf-8"))["config"]["path"]
            candidate = ROOT / value
            if candidate.is_file():
                return candidate
        except (KeyError, TypeError, json.JSONDecodeError):
            pass
    configs = sorted((design / "configs").glob("*.json")) if (design / "configs").is_dir() else []
    return configs[0] if len(configs) == 1 else None


def audit(design: str, config: Path) -> int:
    command = build_command(design, config)
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        return result.returncode
    result = subprocess.run([*command, "--audit-only"], cwd=ROOT)
    if result.returncode:
        return result.returncode
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="scan every multipart design")
    args = parser.parse_args()
    if not args.all:
        parser.error("--all is required by the VS Code hook")

    failures = 0
    for design in sorted((ROOT / "designs").iterdir()):
        if not design.is_dir() or not (design / "parts.json").is_file():
            continue
        config = configured_path(design)
        manifest = ROOT / "output" / design.name / "build_manifest.json"
        if config is None:
            print(f"ERROR {design.name}: no installed config and multiple/no configs; build once explicitly.")
            failures += 1
            continue
        if not manifest.is_file() or not is_current(design.name, config):
            print(f"REBUILD {design.name}: installed build is missing or fails audit")
            failures += bool(audit(design.name, config))
        else:
            print(f"CURRENT {design.name}: {config.relative_to(ROOT)}")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
