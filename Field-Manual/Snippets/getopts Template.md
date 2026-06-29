---
type: snippet
area: "Shells & Scripting"
tags: [sh, bash, scripting, boilerplate, arguments, posix]
status: working
---

# getopts Template

> **Area:** [[Shells & Scripting]]

POSIX-compatible argument parsing with `getopts`. Works in `sh`, `bash`, `dash`, and `ksh`. No long options (those require `getopt` or a manual loop — see [[Argument Parsing Skeleton]] for long options in bash).

---

```sh
#!/bin/sh
# POSIX-compatible argument parsing with getopts

# ── defaults ───────────────────────────────────────────────────────────────────
OUTPUT=""
VERBOSE=0

usage() {
    printf 'Usage: %s [-o output] [-v] [-h] <file>\n' "$(basename "$0")"
    printf '\n'
    printf 'Options:\n'
    printf '  -o FILE   Output file\n'
    printf '  -v        Verbose output\n'
    printf '  -h        Show this help\n'
}

# ── getopts loop ────────────────────────────────────────────────────────────────
# The leading : in optstring enables silent error handling (we handle errors manually)
# A : after a letter means that option requires an argument
while getopts ':o:vh' opt; do
    case "$opt" in
        o) OUTPUT="$OPTARG" ;;
        v) VERBOSE=1 ;;
        h) usage; exit 0 ;;
        :)
            printf 'Error: option -%s requires an argument\n' "$OPTARG" >&2
            usage >&2
            exit 1
            ;;
        ?)
            printf 'Error: unknown option: -%s\n' "$OPTARG" >&2
            usage >&2
            exit 1
            ;;
    esac
done

# ── skip processed options ─────────────────────────────────────────────────────
shift $((OPTIND - 1))

# ── positional arguments ───────────────────────────────────────────────────────
if [ $# -lt 1 ]; then
    printf 'Error: file argument required\n' >&2
    usage >&2
    exit 1
fi

INPUT="$1"
shift

# ── main ───────────────────────────────────────────────────────────────────────
if [ "$VERBOSE" -eq 1 ]; then
    printf '[INFO] Input: %s\n' "$INPUT" >&2
    printf '[INFO] Output: %s\n' "${OUTPUT:-stdout}" >&2
fi

# ... actual work here ...
```

---

## How getopts works

- `getopts ':o:vh' opt` — colon at start = silent mode; `o:` = `-o` takes an argument; `v`, `h` = flags
- `$OPTARG` — the argument to an option that requires one (e.g., the value after `-o`)
- `$OPTIND` — index of the next argument to process; `shift $((OPTIND - 1))` removes processed flags from `$@`
- After the shift, `$1`, `$2`, … are the remaining positional arguments

## getopts vs getopt

| | `getopts` (built-in) | `getopt` (external) |
|---|---|---|
| Availability | Every POSIX shell | GNU coreutils (Linux); BSD version differs |
| Long options | No | Yes (`--option`) |
| Portability | Universal | Platform-specific behaviour |
| Error handling | Built-in | Via `--` parsing |

Use `getopts` for portability and simplicity; see [[Argument Parsing Skeleton]] for long options.
