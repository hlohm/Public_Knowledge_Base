---
type: snippet
area: Shells & Scripting
tags: [boilerplate, shell, scripting]
status: stable
---

# Bash Strict Mode Header

> **Area:** [[Shells & Scripting]]

**What & why.** The preamble that turns silent script failures into loud, early ones. Without
it, a script keeps running after a command fails, treats typo'd variables as empty strings, and
hides failures in the middle of a pipe. Start every bash script with this. Pairs with [[bash]].

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# -e            exit immediately if any command fails (non-zero)
# -u            error on use of an unset variable (catches typos)
# -o pipefail   a pipeline fails if ANY stage fails, not just the last
# IFS=$'\n\t'   split words only on newline/tab, not spaces — safer loops over filenames

# Fail with a message and a non-zero status
die() { echo "error: $*" >&2; exit 1; }

# Clean up on exit, however we exit (success, error, or Ctrl-C)
cleanup() { rm -rf "${tmpdir:-}"; }
trap cleanup EXIT

tmpdir="$(mktemp -d)"
# ... script body ...
```

## Customize
- **Drop `IFS=$'\n\t'`** if the script genuinely needs space-splitting (rare; usually a sign to
  quote properly instead).
- **`set -x`** temporarily for debugging — echoes each command as it runs.
- **`trap cleanup EXIT`** — extend `cleanup` to remove temp files, release locks, stop a
  spawned process. Use `trap '...' ERR` for error-only handling.
- For opt-in strictness on a risky section only, you can `set +e` / `set -e` around it.

## Use
- Save as the first lines of any new bash script; `chmod +x script.sh`.
- Lint it: `shellcheck script.sh` catches the bugs strict mode can't.

## Caveats
- `set -e` has well-known edge cases (e.g. it's suppressed for commands in `if`/`&&`/`||`
  conditions, and in some function-return situations). It's a strong default, not a guarantee —
  still check critical commands explicitly with `|| die "..."`.
