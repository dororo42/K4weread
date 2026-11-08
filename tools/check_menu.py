#!/usr/bin/env python3
"""CI gate: menu.json must parse and only contain the verified option set.

KUAL v2.7 parse.awk only reads type="json" menus; on-device facts (2026-11-08,
/mnt/us/extensions/koreader/menu.json) verified the option vocabulary:
name / priority / action / params / internal / exitmenu / refresh / if.
K4weread deliberately uses only the default exit-KUAL action path (no
exitmenu key) — same as the KOReader extension's Start item.

2026-11-08 audit: replaced assert-based checks (silently disabled by -O) with
explicit exit codes, and a hard-coded two-element action sequence with a set
check so adding a third menu item does not break the gate.
"""
import json
import pathlib
import sys

ALLOWED_KEYS = {"name", "priority", "action", "params", "internal", "items"}
EXPECTED_ACTIONS = {"bin/k4weread.sh"}


def fail(message: str) -> int:
    print(f"menu.json FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    try:
        data = json.loads(pathlib.Path("kual/menu.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return fail(f"cannot parse: {e}")

    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return fail("items must be a non-empty list")

    seen_actions = []

    def walk(node) -> str:
        if not isinstance(node, dict):
            return "menu node is not an object"
        unknown = set(node) - ALLOWED_KEYS
        if unknown:
            return f"unknown menu option(s) {sorted(unknown)} in {node.get('name')}"
        if "action" in node:
            seen_actions.append(node["action"])
        for child in node.get("items", []):
            error = walk(child)
            if error:
                return error
        return ""

    for item in items:
        error = walk(item)
        if error:
            return fail(error)

    if not seen_actions or set(seen_actions) != EXPECTED_ACTIONS:
        return fail(f"unexpected action set {seen_actions}; "
                    f"expected only {sorted(EXPECTED_ACTIONS)}")
    print(f"menu.json OK: {len(items)} top-level item(s), actions={seen_actions}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
