#!/usr/bin/env python3
"""CI gate: the weread-only handshake marker path must stay in sync across
three places: kual/bin/k4weread.sh (writer), the peer plugin repo's
weread/lib/only_mode.lua (reader), and every doc in this repo that quotes it.

Usage (from the repo root):
    python3 tools/check_marker_path.py [--peer-repo /path/to/weread_K4.koplugin]

The peer repo defaults to ../weread_K4.koplugin when present; CI clones it and
passes --peer-repo explicitly. A missing peer is reported as SKIP (a
single-repo checkout must still be able to run the rest of the gates).
"""
import argparse
import pathlib
import re
import sys

REQUIRED_DOCS = ("README.md", "docs/DESIGN.md", "docs/INSTALL.md")
MARKER_RE = re.compile(r"/mnt/us/[A-Za-z0-9_./-]*launch\.flag")
PEER_DEFAULT = "../weread_K4.koplugin"


def fail(message: str) -> int:
    print(f"marker path FAIL: {message}", file=sys.stderr)
    return 1


def writer_flag(script: str) -> str:
    m_dir = re.search(r"^MARKER_DIR=(\S+)$", script, re.M)
    m_flag = re.search(r"^MARKER_FLAG=\$MARKER_DIR/(\S+)$", script, re.M)
    if not (m_dir and m_flag):
        raise ValueError("MARKER_DIR/MARKER_FLAG not found in k4weread.sh")
    return m_dir.group(1) + "/" + m_flag.group(1)


def peer_flag(peer_root: pathlib.Path) -> str:
    module = peer_root / "weread/lib/only_mode.lua"
    if not module.is_file():
        raise ValueError(f"peer module missing: {module}")
    text = module.read_text(encoding="utf-8")
    m_dir = re.search(r'^M\.FLAG_DIR\s*=\s*"([^"]+)"', text, re.M)
    m_name = re.search(r'^M\.FLAG_NAME\s*=\s*"([^"]+)"', text, re.M)
    if not (m_dir and m_name):
        raise ValueError("FLAG_DIR/FLAG_NAME not found in peer only_mode.lua")
    return m_dir.group(1) + "/" + m_name.group(1)


def docs_to_scan() -> list:
    return sorted(
        p for p in pathlib.Path(".").rglob("*.md")
        if "handoffs" not in p.parts
        and not p.name.endswith(".local.md")
        and ".git" not in p.parts
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--peer-repo", default=PEER_DEFAULT,
                    help="path to the weread_K4.koplugin checkout")
    args = ap.parse_args()

    try:
        flag = writer_flag(pathlib.Path("kual/bin/k4weread.sh").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return fail(str(e))
    if not flag.startswith("/mnt/us/") or not flag.endswith("/launch.flag"):
        return fail(f"writer path is not a device user-store marker: {flag}")

    peer = pathlib.Path(args.peer_repo)
    if peer.is_dir():
        try:
            other = peer_flag(peer)
        except (OSError, ValueError) as e:
            return fail(str(e))
        if other != flag:
            return fail(f"cross-repo drift: writer={flag} reader={other} ({peer})")
        print(f"peer marker path OK: {other} ({peer})")
    else:
        print(f"peer repo SKIP: {peer} not present (pass --peer-repo in CI)")

    docs = docs_to_scan()
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for found in MARKER_RE.findall(text):
            if found != flag:
                return fail(f"{doc} quotes a stale marker {found} (expected {flag})")

    for doc in REQUIRED_DOCS:
        if flag not in pathlib.Path(doc).read_text(encoding="utf-8"):
            return fail(f"{doc} does not mention {flag}")

    print(f"marker path OK: {flag} ({len(docs)} doc(s) scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
