#!/usr/bin/env python3
"""CI gate: config.xml well-formedness + version field + json menu reference.

2026-11-08 audit: explicit exit codes instead of assert, a real semver-ish
version pattern, and a None-safe menu.text read.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


def fail(message: str) -> int:
    print(f"config.xml FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    try:
        root = ET.fromstring(pathlib.Path("kual/config.xml").read_text(encoding="utf-8"))
    except (OSError, ET.ParseError) as e:
        return fail(f"cannot parse: {e}")

    if root.tag != "extension":
        return fail(f"root tag is {root.tag!r}, expected 'extension'")
    version = root.findtext("./information/version")
    if not version or not re.fullmatch(r"\d+\.\d+(\.\d+)?", version.strip()):
        return fail(f"bad version: {version!r}")
    menu = root.find("./menus/menu")
    if menu is None:
        return fail("missing <menus><menu>")
    if menu.get("type") != "json":
        return fail(f"menu type is {menu.get('type')!r}, expected 'json'")
    if (menu.text or "").strip() != "menu.json":
        return fail(f"menu reference is {(menu.text or '')!r}, expected 'menu.json'")
    print(f"config.xml OK: version={version.strip()}, menu type=json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
