#!/usr/bin/env python3
"""CI gate: docs must quote the current release asset, the plugin floor and a
resolvable handoff pointer.

2026-11-12 three-repo audit (F-1 / F-2 / F-3 / F-7): docs/INSTALL.md still
quoted K4weread-v0.1.1.zip while config.xml said 0.1.2; README and INSTALL
disagreed on the minimum plugin version; the AGENTS.md handoff pointer was 16
commits behind. The version itself has ONE source of truth (kual/config.xml);
this gate only pins the docs that quote it.

Usage (from the repo root):
    python3 tools/check_docs_consistency.py [--repo-root /path/to/K4weread]
"""
import argparse
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

DOC_FILES = ("README.md", "docs/INSTALL.md")
ASSET_RE = re.compile(r"K4weread-v(\d+\.\d+(?:\.\d+)?)\.zip")
PEER_FLOOR_RE = re.compile(r"v9\.\d+\+")
PEER_FLOOR = "v9.9+"  # pinned floor, deliberately bumped in one change
POINTER_RE = re.compile(r"^- Latest:\s*`([^`]+)`", re.M)


def fail(message: str) -> int:
    print(f"docs consistency FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=".", help="repository root")
    root = pathlib.Path(ap.parse_args().repo_root)

    try:
        cfg = ET.fromstring((root / "kual/config.xml").read_text(encoding="utf-8"))
        version = (cfg.findtext("./information/version") or "").strip()
    except (OSError, ET.ParseError) as e:
        return fail(f"cannot read config.xml version: {e}")
    if not version:
        return fail("config.xml has no <version>")

    expected_asset = f"K4weread-v{version}.zip"
    texts = {}
    for rel in DOC_FILES:
        try:
            texts[rel] = (root / rel).read_text(encoding="utf-8")
        except OSError as e:
            return fail(f"cannot read {rel}: {e}")

    for rel, text in texts.items():
        found = ASSET_RE.findall(text)
        if not found:
            return fail(f"{rel} does not quote any K4weread-v*.zip asset")
        for v in found:
            if f"K4weread-v{v}.zip" != expected_asset:
                return fail(f"{rel} quotes stale asset K4weread-v{v}.zip "
                            f"(expected {expected_asset})")

    for rel, text in texts.items():
        floors = set(PEER_FLOOR_RE.findall(text))
        if not floors:
            return fail(f"{rel} does not state a plugin floor (expected {PEER_FLOOR})")
        if floors != {PEER_FLOOR}:
            return fail(f"{rel} plugin floor drift {sorted(floors)} "
                        f"(expected {PEER_FLOOR})")

    # handoffs/ is local-only (gitignored, absent in CI): the pointer can only
    # be resolved on a workstation, never in the workflow checkout.
    try:
        agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    except OSError as e:
        return fail(f"cannot read AGENTS.md: {e}")
    m = POINTER_RE.search(agents)
    if not m:
        return fail("AGENTS.md has no '- Latest:' handoff pointer")
    if (root / "handoffs").is_dir():
        if not (root / m.group(1)).is_file():
            return fail(f"handoff pointer target missing: {m.group(1)}")
        print(f"handoff pointer OK: {m.group(1)}")
    else:
        print("handoff pointer SKIP: handoffs/ absent (CI checkout)")

    print(f"docs consistency OK: asset={expected_asset}, plugin floor={PEER_FLOOR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
