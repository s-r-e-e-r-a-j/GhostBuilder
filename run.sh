#!/usr/bin/env bash

set -e

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed!"
    exit 1
fi

echo " Running GhostBuilder..."
python3 -m ghostbuilder || {
    echo "Failed to execute GhostBuilder!"
    exit 1
}

echo "Done."
