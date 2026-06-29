---
type: cheatsheet
area: "Shells & Scripting"
aliases: [POSIX sh, /bin/sh]
tags: [shell, posix, scripting, portability]
status: working
---

# sh (POSIX)

> **Area:** [[Shells & Scripting]]

The POSIX shell — the portable baseline. Write to `sh` when your script must run on any Unix: minimal containers (Alpine/BusyBox), BSD systems, macOS `/bin/sh` (which is `dash`, not bash), or CI environments where bash is not guaranteed. See [[bash]] for Linux-specific scripting.

> **`#!/bin/sh` does not mean bash.** On Ubuntu, `/bin/sh` is `dash` — a strict POSIX shell. Features like `[[ ]]`, `local`, arrays (`${arr[@]}`), `$(( ))` with `**`, and `echo -e` may not work. If in doubt, use `shellcheck --shell=sh` to validate.

---

## 1. What POSIX sh includes

These work in any `sh`-compliant shell:

```sh
# Variables
VAR="value"
echo "$VAR"         # always double-quote variable expansions
echo "${VAR:-default}"    # default if unset or empty
echo "${VAR:=default}"    # assign default if unset or empty
echo "${VAR:?error msg}"  # error and exit if unset or empty
echo "${VAR:+other}"      # use 'other' if VAR is set (opposite of :-)

# Arithmetic (POSIX arithmetic expansion)
N=$((N + 1))
M=$(( (A + B) * 2 ))

# String operations
echo "${VAR#prefix}"      # remove shortest prefix match
echo "${VAR##prefix*}"    # remove longest prefix match
echo "${VAR%suffix}"      # remove shortest suffix match
echo "${VAR%%*suffix}"    # remove longest suffix match

# Conditionals
[ -f /etc/passwd ]        # file exists and is regular
[ -d /etc ]               # directory exists
[ -z "$VAR" ]             # string is empty
[ -n "$VAR" ]             # string is non-empty
[ "$A" = "$B" ]           # string equality (= not ==)
[ "$A" != "$B" ]
[ "$N" -eq 42 ]           # numeric equality (-eq -ne -lt -le -gt -ge)

# if/elif/else
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "OS: $ID"
elif [ -f /etc/issue ]; then
    echo "Unknown OS"
fi

# case
case "$OSTYPE" in
    linux*)   echo "Linux" ;;
    darwin*)  echo "macOS" ;;
    *)        echo "Other" ;;
esac

# Loops
for f in /etc/*.conf; do
    echo "$f"
done

while IFS= read -r line; do   # read a file line by line
    echo "$line"
done < /etc/passwd

# Functions
greet() {
    printf '%s\n' "Hello, $1"
}
greet "World"
```

## 2. What sh does NOT include

```sh
# These are bash/zsh extensions — do not use in sh scripts:
[[ $VAR == pattern ]]      # use [ ] instead
local var=value            # local is not POSIX (works in dash as an extension but not specified)
echo -e "line\nnew"        # -e is not POSIX; use printf instead
source file.sh             # use: . file.sh
arrays: arr=(); ${arr[@]}  # no arrays in POSIX sh
$'\n' string literals       # not POSIX; use printf
process substitution <()   # bash/zsh only
```

## 3. POSIX-safe idioms

```sh
# Print with newlines safely
printf '%s\n' "Hello, World"
printf 'Count: %d\n' 42

# Source a file
. /etc/profile

# Check exit status
command && echo "success" || echo "failed"
if command; then echo "success"; fi

# Temporary directory
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Integer division (no bc needed)
result=$((A / B))
remainder=$((A % B))

# Read user input
printf 'Enter name: '
read -r name
echo "Hello, $name"

# Avoid word splitting: always quote variables
cp "$src" "$dst"          # correct
cp $src $dst              # breaks on filenames with spaces
```

## 4. Portability checklist

| Feature | POSIX sh | bash | Notes |
|---|---|---|---|
| `[[ ]]` | ✗ | ✓ | Use `[ ]` for portability |
| `local` | ✗* | ✓ | *Works in dash/ksh as extension |
| `$'...'` | ✗ | ✓ | Use `printf` |
| Arrays `${arr[@]}` | ✗ | ✓ | No arrays in POSIX sh |
| `source` | ✗ | ✓ | Use `.` (dot) |
| `echo -e` | ✗* | ✓ | *System-dependent; use `printf` |
| `$((... **  ...))` | ✗ | ✓ | `**` not in POSIX arithmetic |
| Brace expansion `{a,b}` | ✗ | ✓ | Not in POSIX sh |
| `read -d` | ✗ | ✓ | Use `read -r` only |

```sh
# Validate your script
shellcheck --shell=sh script.sh
```

---

## Gotchas / Golden rules

1. **`/bin/sh` is not bash on most modern systems** — Ubuntu/Debian use `dash`; macOS 12+ uses `zsh`-derived; Alpine uses `busybox ash`. Test on the actual target.
2. **`[ ]` tests need spaces around every token** — `[-f file]` is a syntax error; `[ -f file ]` is correct.
3. **`=` not `==` for string comparison in `[ ]`** — `[ "$a" == "$b" ]` is bash-ism; `[ "$a" = "$b" ]` is POSIX.
4. **Always quote `$VAR` in `[ ]`** — `[ $VAR = "x" ]` fails if `$VAR` is empty (becomes `[ = "x" ]`); `[ "$VAR" = "x" ]` is safe.
5. **Use `printf` instead of `echo` for portable output** — `echo` behaviour with flags and escape sequences varies by implementation; `printf '%s\n'` is always predictable.
