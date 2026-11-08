#!/usr/bin/env python3
"""CI gate: the weread-only handshake marker path must stay in sync between
kual/bin/k4weread.sh (writer) and the documented plugin contract (reader,
weread_K4.koplugin weread/lib/only_mode.lua).

Single source here is k4weread.sh's MARKER_FLAG assignment; the plugin repo
carries the same literal — this gate pins the K4weread side and greps every
doc that mentions the path so a rename cannot go half-done.
"""
import pathlib
import re
import sys

def main() -> int:
    script = pathlib.Path("kual/bin/k4weread.sh").read_text(encoding="utf-8")
    m_dir = re.search(r"^MARKER_DIR=(\S+)$", script, re.M)
    m_flag = re.search(r"^MARKER_FLAG=\$MARKER_DIR/(\S+)$", script, re.M)
    assert m_dir and m_flag, "MARKER_DIR/MARKER_FLAG not found in k4weread.sh"
    flag = m_dir.group(1) + "/" + m_flag.group(1)
    assert flag.startswith("/mnt/us/k4weread/"), flag

    for doc in ("README.md", "docs/DESIGN.md", "docs/INSTALL.md"):
        text = pathlib.Path(doc).read_text(encoding="utf-8")
        assert flag in text, f"{doc} does not mention {flag}"

    print(f"marker path OK: {flag}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
