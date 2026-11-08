#!/usr/bin/env python3
"""CI gate: menu.json must parse and only contain the verified option set.

KUAL v2.7 parse.awk only reads type="json" menus; on-device facts (2026-11-08,
/mnt/us/extensions/koreader/menu.json) verified the option vocabulary:
name / priority / action / params / internal / exitmenu / refresh / if.
K4weread deliberately uses only the default exit-KUAL action path (no
exitmenu key) — same as the KOReader extension's Start item.
"""
import json
import pathlib
import sys

ALLOWED_KEYS = {"name", "priority", "action", "params", "internal", "items"}

def main() -> int:
    path = pathlib.Path("kual/menu.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items")
    assert isinstance(items, list) and items, "items must be a non-empty list"

    seen_actions = []

    def walk(node: dict) -> None:
        unknown = set(node) - ALLOWED_KEYS
        assert not unknown, f"unknown menu option(s) {sorted(unknown)} in {node.get('name')}"
        if "action" in node:
            seen_actions.append(node["action"])
        for child in node.get("items", []):
            walk(child)

    for item in items:
        walk(item)

    assert seen_actions == ["bin/k4weread.sh", "bin/k4weread.sh"], seen_actions
    print(f"menu.json OK: {len(items)} top-level item(s), actions={seen_actions}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
