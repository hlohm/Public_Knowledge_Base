---
type: cheatsheet
area: "CLI Tools"
aliases: ["patch", "unified diff", "diffutils"]
tags: [text, files, patching]
status: working
---

# diff

> **Area:** [[CLI Tools]]

Compare files and directory trees, read unified diff output fluently, and apply changes with `patch`. Covers GNU diff/patch and the everyday `git diff` forms; deep git usage lives in [[git]].

---

## 1. Core syntax

```bash
diff old.txt new.txt      # order matters: OLD first, NEW second — "what turns old into new"
diff -u old.txt new.txt   # unified format — the one everything else (git, patch, review) speaks
diff -y old.txt new.txt   # side-by-side view; add -W 200 for wide terminals
diff -q old.txt new.txt   # just "differ or not" — no content; fast sanity check
diff <(cmd1) <(cmd2)      # compare command outputs directly (process substitution)
```

Exit codes: `0` = identical, `1` = files differ, `2` = trouble. **`1` is not an error** — mind this in scripts with `set -e`.

## 2. Useful flags

```bash
diff -u -w a b            # ignore all whitespace — cuts noise after reformatting
diff -u -b a b            # ignore changes in amount of whitespace (gentler than -w)
diff -u -i a b            # case-insensitive
diff -u -I '^#' a b       # ignore lines matching regex (comments, timestamps)
diff --color=always a b | less -R    # readable colored output in a pager
diff -u -N a b            # treat missing files as empty — needed so new files show up
```

## 3. Directory trees

```bash
diff -r dir1 dir2         # recursive compare; shows differing files and their diffs
diff -rq dir1 dir2        # names only — "which files differ / only exist on one side"
diff -ru dir1 dir2        # recursive unified diff — this is how you make a multi-file patch
diff -r -x '*.log' -x '.git' dir1 dir2   # exclude patterns (repeat -x per pattern)
```

## 4. Reading unified diff output

```diff
--- old.txt    2026-08-04          ← the "a" file (source)
+++ new.txt    2026-08-04          ← the "b" file (target)
@@ -12,5 +12,6 @@ optional context   ← hunk header
 unchanged context line
-removed from old
+added in new
```

- `@@ -12,5 +12,6 @@` — hunk starts at line 12 in the old file spanning 5 lines, line 12 in the new spanning 6.
- Leading space = context, `-` = only in old, `+` = only in new.
- A changed line appears as a `-`/`+` pair; there is no "modified" marker.
- `\ No newline at end of file` — literal note, not content; the file lacks a trailing newline.
- In `git diff`, `a/` and `b/` prefixes are the old and new versions of the same path.

## 5. patch — applying diffs

```bash
patch < fix.patch                 # apply in current dir; paths come from the patch headers
patch -p1 < fix.patch             # strip 1 leading path component (a/src/x.c → src/x.c) — the git default
patch -p0 < fix.patch             # keep paths as-is (plain diff output without a/ b/ prefixes)
patch --dry-run -p1 < fix.patch   # test first — always, on anything you care about
patch -R -p1 < fix.patch          # reverse: un-apply a previously applied patch
patch -b -p1 < fix.patch          # keep .orig backups of every changed file
```

Rejected hunks land in `<file>.rej` — fix those by hand. For git-generated patches, `git apply fix.patch` (or `git am` for `format-patch` mail) respects the index and is usually the better tool.

## 6. git diff essentials

```bash
git diff                  # working tree vs index — what you have NOT staged yet
git diff --staged         # index vs HEAD — what WILL be committed
git diff HEAD             # working tree vs HEAD — both of the above combined
git diff main..feature    # what feature adds on top of main
git diff --stat           # summary: files + change counts, no content
git diff --word-diff      # word-level — much better for prose and config lines
git diff -w               # ignore whitespace — see through re-indentation
git diff --name-only      # just the paths
git diff --no-index a b   # use git's differ on files OUTSIDE any repo (colors, word-diff)
```

More (log -p, format-patch, difftool): [[git]].

## 7. Related comparators

```bash
cmp file1 file2           # byte-level compare; first differing byte — right tool for binaries
comm -12 <(sort a) <(sort b)   # set operations on sorted lines: -12 = common to both
comm -23 <(sort a) <(sort b)   # lines only in a
nvim -d file1 file2       # interactive side-by-side with sync scrolling ([[nvim]]); do/dp to move changes
```

---

## Daily workflows

### "Make a patch, send it, apply it elsewhere"
```bash
diff -ruN original/ modified/ > change.patch   # -N so newly added files are included
# on the other machine, inside the tree to modify:
patch --dry-run -p1 < change.patch             # verify it applies cleanly
patch -p1 < change.patch
```

### "What changed in this config vs the packaged default?"
```bash
diff -u /usr/share/doc/pkg/config.example /etc/pkg/config
diff -u -I '^\s*#' -I '^\s*$' default.conf live.conf   # ignore comments and blank lines
```

### "Are these two directories in sync?"
```bash
diff -rq dir1 dir2        # quick verdict per file
# for large trees or remote sides, rsync's dry-run is faster: see [[rsync]]
rsync -avn --delete dir1/ dir2/
```

## Gotchas / Golden rules

1. **Argument order is meaning** — `diff old new` produces the changes that turn *old into new*. Swap them and your patch does the exact opposite.
2. **Exit code 1 just means "differ"** — under `set -e` a plain `diff` in a script aborts it. Use `diff ... || true` or check `$?` explicitly.
3. **`-p` level mismatches are the classic patch failure** — git-style patches (`a/`, `b/` prefixes) need `-p1`; plain `diff -ru dir1 dir2` output usually wants `-p0` or running from the right parent dir. `--dry-run` tells you before anything breaks.
4. **Forgotten `-N` silently drops new files** — `diff -ru` without `-N` only mentions "Only in dir2: newfile" instead of including its content in the patch.
5. **Whitespace/CRLF noise drowns real changes** — files edited on Windows show every line changed. `diff -u --strip-trailing-cr`, or `-w` when indentation churned. See [[wsl]] for the CRLF story.
