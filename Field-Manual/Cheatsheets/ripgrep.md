---
type: cheatsheet
area: "CLI Tools"
aliases: [rg]
tags: [search, grep, regex, files]
status: working
---

# ripgrep

> **Area:** [[CLI Tools]]

Fast recursive text search. A modern replacement for `grep -r` — faster, respects `.gitignore`, skips binary files by default, and uses Rust regex. The daily driver for "find me where X is in this codebase."

> `rg` is the command. `ripgrep` is the package name.

---

## 1. Basic search

```bash
rg 'pattern'               # search current directory recursively
rg 'pattern' /path/to/dir  # search a specific directory
rg 'pattern' file.txt      # search a single file

rg -i 'pattern'            # case-insensitive
rg -F 'literal.string'     # fixed string (no regex — dots and brackets are literal)
rg -w 'word'               # whole-word match only
rg -x 'exact whole line'   # match entire lines only
```

## 2. Output control

```bash
rg -l 'pattern'            # list matching filenames only (no line content)
rg -c 'pattern'            # count matches per file
rg -n 'pattern'            # show line numbers (default in rg)
rg --no-line-number 'pat'  # suppress line numbers
rg -o 'pattern'            # print only the matching portion of each line
rg -m 5 'pattern'          # stop after 5 matches per file
rg -q 'pattern'            # quiet: exit 0 if any match, no output (for use in conditions)
rg --stats 'pattern'       # print search statistics after results
```

## 3. File type filtering

```bash
rg -t py 'import'          # only Python files
rg -t js -t ts 'require'   # JS and TypeScript files
rg -T py 'pattern'         # exclude Python files
rg --type-list             # show all known type names and their file patterns

rg -g '*.conf' 'pattern'   # glob filter: only .conf files
rg -g '!*.log' 'pattern'   # exclude .log files
```

## 4. Context lines

```bash
rg -A 3 'pattern'          # 3 lines after each match
rg -B 3 'pattern'          # 3 lines before each match
rg -C 3 'pattern'          # 3 lines before and after (context)
```

## 5. Regex

rg uses Rust regex (RE2-compatible, no backtracking — fast and predictable):

```bash
rg '\bword\b'              # word boundary
rg '^\s*#'                 # lines starting with optional whitespace then #
rg 'foo.*bar'              # foo followed by anything followed by bar
rg '\d{4}-\d{2}-\d{2}'    # date pattern YYYY-MM-DD
rg '(?i)error'             # inline case-insensitive flag
rg '(err|warn|crit)'       # alternation
rg -U 'foo\nbar'           # -U: multiline mode (. matches newline)
rg -P 'pattern'            # PCRE2 mode (enables lookaheads, backrefs — slower)
```

## 6. Replacement

```bash
rg 'pattern' -r 'replacement'    # print with substitution applied (does not modify files)
rg '(\w+)@(\w+)' -r '$2@$1'      # capture group references
# To actually modify files, pipe to sed -i or use your editor's project-wide find-replace
```

## 7. Paths and ignores

```bash
rg 'pattern' --hidden          # include hidden files (dotfiles)
rg 'pattern' --no-ignore       # ignore .gitignore and .rgignore rules
rg 'pattern' -u                # one -u: don't ignore hidden files
rg 'pattern' -uu               # two -u: also ignore binary-file filtering
rg 'pattern' -uuu              # three -u: effectively behaves like grep -r

rg 'pattern' --glob '!node_modules'   # exclude a directory
```

Create a `.rgignore` or `.ignore` file in a project root to exclude paths permanently for `rg` (same format as `.gitignore`).

---

## Daily workflows

### "Find all usages of a function in a codebase"
```bash
rg 'connect_to_db\(' -t py
```

### "Find TODO/FIXME comments across a project"
```bash
rg 'TODO|FIXME|HACK' --type-not=markdown
```

### "Check if a string appears anywhere in the repo"
```bash
rg -l '<secret-value>'
```

### "Count how many times each log level appears"
```bash
rg -co '(ERROR|WARN|INFO)' /var/log/app.log | sort | uniq -c | sort -rn
```

### "Find and display function definition with context"
```bash
rg -A 10 '^def process_batch' src/
```

## Gotchas / Golden rules

1. **`.gitignore` is respected automatically** — if you are not finding a file you expect, check if it is ignored; use `--no-ignore` to bypass.
2. **`-F` disables regex** — when searching for literal dots, brackets, or other metacharacters, always use `-F` to avoid surprises.
3. **`rg -l` + `xargs` is the fast "operate on all matching files" pattern** — `rg -l 'pattern' | xargs sed -i 's/pattern/replacement/g'`.
4. **`-r` does not modify files** — it is a display transform only; use your editor or `sed -i` for actual file modification.
5. **Binary files are skipped by default** — if you need to search inside binary files, add `-a` (treat as text), but the output may be garbled.
