#!/usr/bin/env bash
# Rebase the Skwila fork branch onto the latest upstream release (or a given tag).
# Usage: scripts/sync-upstream.sh [upstream-tag]   (default: latest upstream tag)
set -euo pipefail
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream https://github.com/delphiki/hass-pronote
git fetch upstream --tags --force
TARGET="${1:-$(git tag --list '[0-9]*' --sort=-v:refname | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | head -1)}"
echo "Rebasing skwila onto upstream $TARGET"
git checkout skwila
git rebase "$TARGET"
echo "Run tests, then: git push --force-with-lease origin skwila && gh release create ${TARGET}-skwila.1 --target skwila"
