#!/bin/sh
# K4weread — KUAL menu entry script (Kindle 4 / K4B, KDK-1.0, FW 4.1.4).
#
# Deployed to /mnt/us/extensions/k4weread/bin/k4weread.sh and executed by
# KUAL's default action path: KUAL exits (suicide -> onStop), then runs this
# script in the background ({ cmd ; } 2>>/var/tmp/KUAL.log &) via MKK su as
# root, cwd = the extension directory. Same mechanism the on-device KOReader
# extension uses to start koreader.sh.
#
# WeRead-only handshake: "start" touches /mnt/us/k4weread/launch.flag BEFORE
# starting KOReader; the weread_K4.koplugin v9.0+ weread-only mode consumes
# (reads + deletes) the flag once at plugin init and opens the bookshelf.
# "koreader" (full mode) removes any stale flag first so a full session can
# never be hijacked by a leftover flag.
#
# Labels in menu.json are ASCII on purpose: Unicode menu labels on KDK-1.0
# KUAL are rendered through the C-3 font-run path which is still awaiting
# on-device verification (see docs/REAL_DEVICE_TEST.md B2). Switch to Chinese
# labels only after that test passes.

MARKER_DIR=/mnt/us/k4weread
MARKER_FLAG=$MARKER_DIR/launch.flag
KOREADER=/mnt/us/koreader/koreader.sh

case "$1" in
    start)
        if ! mkdir -p "$MARKER_DIR" 2>/dev/null || ! touch "$MARKER_FLAG" 2>/dev/null; then
            echo "k4weread: cannot create $MARKER_FLAG; weread-only mode unavailable" >&2
            exit 1
        fi
        sync
        exec "$KOREADER" --kual
        ;;
    koreader)
        rm -f "$MARKER_FLAG" 2>/dev/null
        sync
        exec "$KOREADER" --kual
        ;;
    *)
        echo "usage: k4weread.sh start|koreader"
        exit 2
        ;;
esac
