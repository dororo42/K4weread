#!/bin/sh
# Build the K4weread release zip (kual/ extension + docs + README/LICENSE)
# and its sha256. The zip unpacks into a top-level K4weread/ directory
# (same discipline as weread_K4.koplugin's build_release.sh — flat zips
# scatter files and break installs).
#
# Version single source of truth: the <version> field in kual/config.xml.

set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$REPO_ROOT"

VERSION=$(sed -n 's:.*<version>\(.*\)</version>.*:\1:p' kual/config.xml | head -n 1)
if [ -z "$VERSION" ]; then
    echo "error: cannot read <version> from kual/config.xml" >&2
    exit 1
fi

OUT="K4weread-v${VERSION}.zip"
rm -f "$OUT" "${OUT}.sha256"

# Runtime content: the extension itself plus everything a user needs
# offline (docs + license). CI artifacts and handoffs are excluded.
STAGE="K4weread"
rm -rf "${STAGE}"   # 清掉上次中断留下的暂存文件，保证重复构建结果一致
mkdir -p "${STAGE}"
cp -r kual README.md docs LICENSE "${STAGE}/"
find "${STAGE}" -type d -name '__MACOSX' -prune -exec rm -rf {} + 2>/dev/null || true

# zip -r includes the top dir; keep entries platform-clean (no junk).
zip -r -q "$OUT" "${STAGE}"
rm -rf "${STAGE}"

sha256sum "$OUT" | tee "${OUT}.sha256"
echo "built ${OUT} (version ${VERSION})"
