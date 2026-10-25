#!/usr/bin/env python3
"""Create a numbered OpenSCAD revision snapshot and build artifacts."""

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, NoReturn, Tuple


REV_RE = re.compile(r"^rev_(\d+)(?:\.json)?$")


def info(message: str) -> None:
    print(f"[rev] {message}")


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def format_cmd(cmd: List[str]) -> str:
    if os.name == "nt":
        return subprocess.list2cmdline(cmd)
    return " ".join(shlex.quote(part) for part in cmd)


def get_revision_number(name: str) -> int:
    match = REV_RE.match(name)
    return int(match.group(1)) if match else 0


def load_config(path: Path) -> dict:
    if not path.exists():
        fail(f"Base config not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON config '{path}': {exc}")
    if not isinstance(data, dict):
        fail(f"Base config must be a JSON object: {path}")
    return data


def highest_revision_numbers(revisions_dir: Path, configs_dir: Path) -> Tuple[int, int]:
    """Return (highest revision directory, highest config) numbers; 0 when none."""
    revision_max = 0
    if revisions_dir.exists():
        for child in revisions_dir.iterdir():
            if child.is_dir():
                revision_max = max(revision_max, get_revision_number(child.name))
    config_max = 0
    if configs_dir.exists():
        for child in configs_dir.glob("rev_*.json"):
            config_max = max(config_max, get_revision_number(child.name))
    return revision_max, config_max


def next_revision_name(revisions_dir: Path, configs_dir: Path) -> str:
    return f"rev_{max(highest_revision_numbers(revisions_dir, configs_dir)) + 1:04d}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new numbered config + revision snapshot for a design.")
    parser.add_argument("--design", default="example_box", help="Design folder under designs/<design>.")
    parser.add_argument("--base-config", required=True, help="Staged rev_N.json candidate to publish, or a published config to copy forward.")
    parser.add_argument("--part-name", help="Output base filename (defaults to config['part']).")
    parser.add_argument("--revisions-dir", help="Override revisions directory (default: revisions/<design>).")
    parser.add_argument("--configs-dir", help="Override configs directory (default: designs/<design>/configs).")
    parser.add_argument("--main-scad", help="Override main.scad path.")
    parser.add_argument("--openscad-path", help="Explicit path to openscad executable.")
    parser.add_argument("--dry-run", action="store_true", help="Print the selected revision and build command without writing files.")
    args = parser.parse_args()

    base_config = Path(args.base_config)
    config_data = load_config(base_config)

    revisions_dir = Path(args.revisions_dir) if args.revisions_dir else Path("revisions") / args.design
    configs_dir = Path(args.configs_dir) if args.configs_dir else Path("designs") / args.design / "configs"
    main_scad = (
        Path(args.main_scad)
        if args.main_scad
        else Path("designs") / args.design / "src" / "main.scad"
    )

    # The staged candidate publishes under its own number only when it is the
    # newest config and no revision at or above it exists. Older configs never
    # publish out of order (most historical configs have no revision folder);
    # they are copied forward to the next unused number instead.
    base_number = get_revision_number(base_config.name)
    revision_max, config_max = highest_revision_numbers(revisions_dir, configs_dir)
    publish_in_place = (
        base_number > 0
        and base_config.name == f"rev_{base_number:04d}.json"
        and base_config.resolve().parent == configs_dir.resolve()
        and base_number == config_max
        and revision_max < base_number
    )
    if publish_in_place:
        rev_name = f"rev_{base_number:04d}"
    else:
        rev_name = next_revision_name(revisions_dir, configs_dir)
    rev_dir = revisions_dir / rev_name
    config_path = configs_dir / f"{rev_name}.json"
    params_path = rev_dir / "params.json"

    if rev_dir.exists():
        fail(f"Revision directory already exists: {rev_dir}")
    if not publish_in_place and config_path.exists():
        fail(f"Revision config already exists: {config_path}")

    info(f"Creating {rev_name}")
    info(f"Design: {args.design}")
    info(f"BaseConfig: {base_config}")
    if publish_in_place:
        info(f"Mode: publishing staged candidate {config_path} as {rev_name}")
    else:
        info(f"Mode: copying {base_config} to the next unused revision {rev_name}")

    parts_manifest = Path("designs") / args.design / "parts.json"
    if parts_manifest.exists():
        canonical_revisions_dir = Path("revisions") / args.design
        if revisions_dir.resolve() != canonical_revisions_dir.resolve():
            fail(
                "Manifest-driven designs require the canonical revision directory: "
                f"{canonical_revisions_dir}"
            )
        build_script = Path(__file__).with_name("scad_build_all.py")
        build_cmd = [
            sys.executable,
            str(build_script),
            "--design",
            args.design,
            "--config",
            str(config_path),
            "--destination",
            "revision",
            "--main-scad",
            str(main_scad),
        ]
    else:
        part_name = args.part_name or config_data.get("part")
        if not isinstance(part_name, str) or not part_name.strip():
            fail("No --part-name provided and base config is missing a non-empty 'part' field.")
        part_name = part_name.strip()
        build_script = Path(__file__).with_name("scad_build.py")
        build_cmd = [
            sys.executable,
            str(build_script),
            "--design",
            args.design,
            "--config",
            str(config_path),
            "--part-name",
            part_name,
            "--out-dir",
            str(rev_dir),
            "--main-scad",
            str(main_scad),
        ]
    if args.openscad_path:
        build_cmd.extend(["--openscad-path", args.openscad_path])

    if args.dry_run:
        info("DryRun enabled; no files will be written and OpenSCAD will not run.")
        if not publish_in_place:
            info(f"Would write: {config_path}")
        info(f"Would run: {format_cmd(build_cmd)}")
        info(f"Would write: {params_path}")
        return 0

    # Anything created below is removed again if publication fails, so a failed
    # attempt never consumes a revision number.
    created_config = False
    try:
        if not publish_in_place:
            configs_dir.mkdir(parents=True, exist_ok=True)
            config_path.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")
            created_config = True
        if not parts_manifest.exists():
            rev_dir.mkdir(parents=True, exist_ok=False)
        info(f"Building artifacts into: {rev_dir}")
        info(f"Invoking: {format_cmd(build_cmd)}")
        subprocess.run(build_cmd, check=True)
        rev_dir.mkdir(parents=True, exist_ok=True)
        # Byte copy: revision audits compare params.json and the config by hash.
        shutil.copyfile(config_path, params_path)
    except BaseException:
        if rev_dir.exists():
            info(f"Publication failed; removing {rev_dir}")
            shutil.rmtree(rev_dir)
        if created_config:
            info(f"Publication failed; removing {config_path}")
            config_path.unlink()
        raise

    info(f"Revision ready: {rev_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode)
