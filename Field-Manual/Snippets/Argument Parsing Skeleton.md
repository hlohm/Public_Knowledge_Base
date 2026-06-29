---
type: snippet
area: "Shells & Scripting"
tags: [bash, scripting, boilerplate, arguments]
status: working
---

# Argument Parsing Skeleton

> **Area:** [[Shells & Scripting]]

Named-flag argument parsing for bash scripts. Uses `getopts` for short options and a manual `case` loop for long options. Copy, replace placeholder names, and extend.

---

```bash
#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail
IFS=$'\n\t'

# ── defaults ──────────────────────────────────────────────────────────────────
OUTPUT=""
VERBOSE=false
DRY_RUN=false

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] <required-arg>

Options:
  -o, --output PATH    Output file path
  -v, --verbose        Enable verbose output
  -n, --dry-run        Show what would be done, without doing it
  -h, --help           Show this help message

Examples:
  $(basename "$0") -o result.txt input.txt
  $(basename "$0") --dry-run input.txt
EOF
}

# ── argument parsing ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)             # explicit end of options
            shift
            break
            ;;
        -*)
            echo "Error: unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
        *)              # first non-option arg; stop processing flags
            break
            ;;
    esac
done

# ── positional arguments ───────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
    echo "Error: required argument missing" >&2
    usage >&2
    exit 1
fi

INPUT="$1"
shift

# ── validation ─────────────────────────────────────────────────────────────────
if [[ ! -f "$INPUT" ]]; then
    echo "Error: input file not found: $INPUT" >&2
    exit 1
fi

# ── helpers ────────────────────────────────────────────────────────────────────
log() { [[ "$VERBOSE" == true ]] && echo "[INFO] $*" >&2 || true; }

# ── main ───────────────────────────────────────────────────────────────────────
log "Input: $INPUT"
log "Output: ${OUTPUT:-stdout}"

if [[ "$DRY_RUN" == true ]]; then
    echo "[dry-run] would process: $INPUT → ${OUTPUT:-stdout}"
    exit 0
fi

# ... actual work here ...
```

---

## Notes

- `shift 2` after flags that take an argument; `shift` for boolean flags
- `shift` at the `*)` case is intentionally absent — `break` exits the loop and leaves remaining args in `$@`
- After the loop, `$@` / `$1`, `$2`, … contain the remaining positional arguments
- `>&2` sends error messages to stderr, not stdout — important for scriptability
- Replace `required-arg` with a real argument name and description
