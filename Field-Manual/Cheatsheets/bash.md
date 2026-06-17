---
type: cheatsheet
area: Shells & Scripting
aliases: []
tags: [shell, scripting]
status: stable
---

# bash

> **Area:** [[Shells & Scripting]]

The default Linux shell, used both interactively and for scripting. This covers the everyday
interactive surface and the scripting constructs you reach for most. For the safe-script
preamble, see [[Bash Strict Mode Header]]; for portability, POSIX `sh` is the stricter subset.

> **Bashisms:** arrays, `[[ ]]`, `$( )` process substitution, and `local` are bash-only. If a
> script must run under `/bin/sh`, avoid them or set `#!/usr/bin/env bash` explicitly.

---

## 1. Interactive shortcuts

```bash
# Movement (Emacs mode, the default)
Ctrl-a / Ctrl-e      # start / end of line
Alt-b  / Alt-f       # back / forward one word
Ctrl-w / Alt-d       # delete word before / after cursor
Ctrl-u / Ctrl-k      # delete to start / end of line
Ctrl-y               # paste (yank) what you just cut
Ctrl-l               # clear screen (keeps the line)

# History
Ctrl-r               # reverse-search history (type to match, Ctrl-r again = older)
!!                   # last command            (sudo !! = rerun with sudo)
!$                   # last arg of last command
!abc                 # last command starting with "abc"
history              # numbered history; !123 reruns entry 123
```

---

## 2. Variables & expansion

```bash
name="value"             # no spaces around =
echo "$name"             # always quote expansions
echo "${name}_suffix"    # braces disambiguate

# Defaults & checks
echo "${VAR:-default}"   # use default if VAR unset/empty
echo "${VAR:=default}"   # ...and assign it
echo "${VAR:?error msg}" # error out if unset/empty (great in scripts)

# String ops
${#var}                  # length
${var#prefix}  ${var##*/}    # strip shortest / longest leading match  (##*/ = basename)
${var%suffix}  ${var%.*}     # strip shortest / longest trailing match (%.* = drop extension)
${var/old/new}  ${var//old/new}   # replace first / all
${var^^}  ${var,,}       # upper / lower case
```

---

## 3. Command substitution & arithmetic

```bash
now=$(date +%F)          # capture output  (prefer $(...) over backticks)
count=$(( 2 + 3 * 4 ))   # integer arithmetic
(( i++ ))                # arithmetic command (no $); true/false by result
files=$(ls *.txt | wc -l)
```

---

## 4. Tests & conditionals

```bash
# [[ ]] is the bash test — safer than [ ] (no word-splitting, supports && || =~)
if [[ -f "$file" ]]; then ... ; fi      # file exists & is regular
if [[ -d "$dir"  ]]; then ... ; fi      # directory
if [[ -z "$x" ]]; then ... ; fi         # empty string
if [[ -n "$x" ]]; then ... ; fi         # non-empty
if [[ "$a" == "$b" ]]; then ... ; fi    # string equality
if [[ "$n" -gt 5 ]]; then ... ; fi      # numeric: -eq -ne -lt -le -gt -ge
if [[ "$s" =~ ^[0-9]+$ ]]; then ... ; fi  # regex match

# Short-circuit
[[ -f "$f" ]] && echo "exists" || echo "missing"

case "$1" in
  start) echo starting ;;
  stop)  echo stopping ;;
  *)     echo "usage: $0 {start|stop}"; exit 1 ;;
esac
```

---

## 5. Loops

```bash
for f in *.log; do echo "$f"; done            # globs (no quotes around the glob)
for i in {1..5}; do echo "$i"; done           # brace range
for ((i=0; i<5; i++)); do echo "$i"; done     # C-style

while read -r line; do echo "$line"; done < file.txt   # read a file line by line
while IFS=, read -r a b c; do echo "$a/$b"; done < data.csv   # split on comma

until [[ -f /tmp/ready ]]; do sleep 1; done    # wait for a condition
```

`read -r` (raw) stops backslash mangling; set `IFS` to control splitting. Looping over
`$(ls)` is a classic bug — glob directly instead.

---

## 6. Functions & arguments

```bash
greet() {
  local name="${1:?need a name}"   # local keeps it out of the global scope
  echo "hello, $name"
}
greet "world"

# Positional args inside a function or script:
#   $0 script name   $1..$9 args   $# count   $@ all (quoted: each separate)
#   "$@"  → "a" "b"   |   "$*" → "a b" (joined)   |   $? last exit code
```

---

## 7. Redirection & pipes

```bash
cmd > out.txt            # stdout to file (truncate)
cmd >> out.txt           # append
cmd 2> err.txt           # stderr to file
cmd > out.txt 2>&1       # both to file (order matters: redirect stdout first)
cmd &> out.txt           # bash shorthand for both
cmd 2>/dev/null          # discard stderr
cmd | tee out.txt        # to screen AND file
cmd1 | cmd2              # pipe stdout of cmd1 into cmd2
cmd <<< "string"         # here-string (feed a string as stdin)
cmd <<'EOF'              # here-doc (quoted EOF = no expansion)
literal text
EOF
```

Pipe exit status: by default `$?` is the *last* command's. `set -o pipefail` makes a pipe fail
if *any* stage fails — see [[Bash Strict Mode Header]].

---

## 8. Globs & brace expansion

```bash
*.txt        # any .txt          ?           # single char        [abc] # one of a,b,c
**           # recursive (needs: shopt -s globstar)
{a,b,c}.txt  # → a.txt b.txt c.txt            mv file.{txt,bak}    # quick rename/backup
shopt -s nullglob   # unmatched glob expands to nothing, not the literal pattern
```

---

## Daily workflows

### "Run a command on every matching file"
```bash
for f in *.jpg; do convert "$f" "${f%.jpg}.png"; done
# or, for huge sets / spaces-safe:
find . -name '*.jpg' -print0 | xargs -0 -n1 -P4 process   # -P4 = 4 in parallel
```

### "Quick one-off backup of a file before editing"
```bash
cp config.yml{,.bak}      # brace expansion → cp config.yml config.yml.bak
```

### "Make a script safe from the first line"
See [[Bash Strict Mode Header]] — start every script with it.

---

## Files & locations

| Path | What |
| --- | --- |
| `~/.bashrc` | per-shell interactive config (aliases, functions, prompt) |
| `~/.bash_profile` / `~/.profile` | login-shell config |
| `~/.bash_history` | command history |
| `~/.inputrc` | readline key bindings |
| `/etc/bash.bashrc` | system-wide interactive config |

---

## Gotchas / Golden rules

1. **Always quote `"$var"`** — unquoted variables word-split and glob-expand. The single most
   common source of bash bugs.
2. **`[[ ]]` not `[ ]`** in bash — it's safer and more capable. Use `[ ]`/`test` only for POSIX `sh`.
3. **Don't parse `ls`.** Glob (`for f in *`) or use `find -print0 | xargs -0`.
4. **`set -euo pipefail`** at the top of every script — see [[Bash Strict Mode Header]].
5. **`$()` over backticks** — nestable and readable.

## Further reading
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/) · `man bash` ·
  [ShellCheck](https://www.shellcheck.net/) (lint your scripts)
