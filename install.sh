#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOML_FILE="$ROOT_DIR/school_pathfinder.toml"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
INCLUDE_OPTIONAL=false
DRY_RUN=false

usage() {
  printf 'Usage: %s [--include-optional] [--dry-run]\n' "$(basename "$0")"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --include-optional)
      INCLUDE_OPTIONAL=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -f "$TOML_FILE" ]]; then
  printf 'Could not find %s\n' "$TOML_FILE" >&2
  exit 1
fi

find_python() {
  if [[ -x "$VENV_DIR/bin/python" ]]; then
    printf '%s\n' "$VENV_DIR/bin/python"
    return
  fi

  for candidate in "${PYTHON:-}" python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
    if [[ -n "$candidate" ]] && command -v "$candidate" >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return
    fi
  done

  printf 'Could not find a Python interpreter. Set PYTHON=/path/to/python and try again.\n' >&2
  exit 1
}

PYTHON_BIN="$(find_python)"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  printf 'Creating virtual environment at %s using %s\n' "$VENV_DIR" "$PYTHON_BIN"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
  PYTHON_BIN="$VENV_DIR/bin/python"
fi

REQ_FILE="$(mktemp)"
trap 'rm -f "$REQ_FILE"' EXIT

"$PYTHON_BIN" - "$TOML_FILE" "$REQ_FILE" "$INCLUDE_OPTIONAL" <<'PY'
import sys
import tomllib

toml_file, req_file, include_optional = sys.argv[1:]

with open(toml_file, "rb") as file:
    config = tomllib.load(file)

dependencies = list(config.get("project", {}).get("dependencies", []))

if include_optional == "true":
    for group in config.get("project", {}).get("optional-dependencies", {}).values():
        dependencies.extend(group)
    for group in config.get("dependency-groups", {}).values():
        dependencies.extend(group)

with open(req_file, "w", encoding="utf-8") as file:
    for dependency in dependencies:
        file.write(f"{dependency}\n")
PY

printf 'Using Python: '
"$PYTHON_BIN" --version

if [[ ! -s "$REQ_FILE" ]]; then
  printf 'No dependencies found in %s\n' "$TOML_FILE"
  exit 0
fi

printf 'Installing dependencies from %s:\n' "$TOML_FILE"
sed 's/^/  - /' "$REQ_FILE"

if [[ "$DRY_RUN" == true ]]; then
  printf 'Dry run only. No packages installed.\n'
  exit 0
fi

"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r "$REQ_FILE"

printf 'Installation complete.\n'
