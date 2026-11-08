#!/usr/bin/env python3
"""CI gate: config.xml well-formedness + version field + json menu reference."""
import pathlib
import sys
import xml.etree.ElementTree as ET

def main() -> int:
    path = pathlib.Path("kual/config.xml")
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    assert root.tag == "extension", root.tag
    version = root.findtext("./information/version")
    assert version and version.count(".") >= 1, f"bad version: {version!r}"
    menu = root.find("./menus/menu")
    assert menu is not None, "missing <menus><menu>"
    assert menu.get("type") == "json", menu.get("type")
    assert menu.text.strip() == "menu.json", menu.text
    print(f"config.xml OK: version={version}, menu type=json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
