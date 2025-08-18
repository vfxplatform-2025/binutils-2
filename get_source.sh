#!/bin/bash
set -e

VERSION=2.40
ARCHIVE=binutils-${VERSION}.tar.xz
URL=https://ftp.gnu.org/gnu/binutils/${ARCHIVE}
SRC_DIR=binutils-${VERSION}

cd source

if [ ! -f "$ARCHIVE" ]; then
    echo "⬇️  Downloading $ARCHIVE"
    wget "$URL"
fi

if [ -d "$SRC_DIR" ]; then
    echo "🧹 Removing old source: $SRC_DIR"
    rm -rf "$SRC_DIR"
fi

echo "📦 Extracting $ARCHIVE"
tar -xf "$ARCHIVE"

echo "✅ Extracted to: $SRC_DIR"

