---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [text-processing, stream-editor, regex]
status: working
---

# sed

> **Area:** [[CLI Tools]]

Stream editor: applies editing commands to lines of text read from stdin or a file. The go-to tool for substitution, deletion, and line-range operations in shell pipelines.

> For complex text transformations, reach for [[awk]] or Python. `sed` is fastest for simple substitution and line operations.

---

## 1. Substitution

```bash
sed 's/old/new/'          # replace first occurrence per line
sed 's/old/new/g'         # replace all occurrences per line (global)
sed 's/old/new/I'         # case-insensitive (GNU sed; not POSIX)
sed 's/old/new/2'         # replace only the 2nd occurrence per line

# In-place editing (backup first)
sed -i.bak 's/foo/bar/g' file.txt    # modifies file.txt; saves original as file.txt.bak
sed -i '' 's/foo/bar/g' file.txt     # macOS / BSD: -i requires an argument (use '' for none)

# Delimiter can be any character — use a different one when the pattern contains /
sed 's|/old/path|/new/path|g' file.txt
sed 's,old,new,g' file.txt
```

## 2. Addresses (line ranges)

```bash
# Address types
sed '3s/old/new/'          # line 3 only
sed '2,5s/old/new/'        # lines 2 through 5
sed '2,$s/old/new/'        # line 2 to end of file
sed '/pattern/s/old/new/'  # only lines matching a regex
sed '/start/,/end/s/old/new/'    # between two patterns (inclusive)

# Negation
sed '/pattern/!s/old/new/'       # all lines NOT matching pattern
```

## 3. Deletion

```bash
sed '/pattern/d'           # delete lines matching pattern
sed '3d'                   # delete line 3
sed '3,7d'                 # delete lines 3-7
sed '/^$/d'                # delete blank lines
sed '/^#/d'                # delete comment lines
sed '/pattern/,/end/d'     # delete a range between two patterns
```

## 4. Insertion and appending

```bash
sed '3i\This line is inserted before line 3' file  # insert before
sed '3a\This line is appended after line 3'  file  # append after
sed '/pattern/a\New line after every match'  file
```

## 5. Print and line selection

```bash
sed -n '5p'                # print only line 5 (-n suppresses default output)
sed -n '5,10p'             # print lines 5-10
sed -n '/pattern/p'        # print only lines matching pattern
sed -n '/start/,/end/p'    # print a range between two patterns

# Count matches
sed -n '/pattern/p' file | wc -l
```

## 6. Multiple commands

```bash
sed -e 's/foo/bar/' -e 's/baz/qux/'   # multiple expressions
sed 's/foo/bar/; s/baz/qux/'          # semicolon-separated (GNU sed)

# Script file
sed -f script.sed file.txt
```

## 7. Useful patterns

```bash
# Strip trailing whitespace
sed 's/[[:space:]]*$//' file.txt

# Strip leading whitespace
sed 's/^[[:space:]]*//' file.txt

# Strip both
sed 's/^[[:space:]]*//; s/[[:space:]]*$//' file.txt

# Remove HTML tags (crude)
sed 's/<[^>]*>//g'

# Extract lines between two markers (exclusive)
sed -n '/START/,/END/{ /START/d; /END/d; p }' file.txt

# Print the Nth line
sed -n '10p' file.txt

# Delete trailing empty lines
sed -e '/^[[:space:]]*$/{ $d; N; /^\n$/D }' file.txt

# Double-space a file
sed 'G' file.txt
```

---

## Daily workflows

### "Replace a string across many files"
```bash
find . -name '*.conf' -exec sed -i.bak 's/old-hostname/new-hostname/g' {} +
```

### "Extract lines between two markers"
```bash
sed -n '/BEGIN CERTIFICATE/,/END CERTIFICATE/p' file.pem
```

### "Remove comment lines and blank lines from a config"
```bash
sed '/^[[:space:]]*#/d; /^[[:space:]]*$/d' config.conf
```

### "Preview in-place changes without modifying the file"
```bash
sed 's/old/new/g' file.txt   # output to stdout only; don't add -i
```

## Gotchas / Golden rules

1. **`-i` syntax differs between GNU sed and BSD/macOS sed** — GNU: `-i.bak`; BSD: `-i .bak` or `-i ''`. For portable scripts, write a backup to a temp file instead.
2. **`-n` suppresses all output by default** — you must explicitly `p` (print) what you want to see; forgetting `-n` when using `p` results in each match printing twice.
3. **Regex is POSIX BRE by default** — `+` and `?` are literal; use `\+` and `\?` (BRE) or add `-E` to use ERE where `+` and `?` work as expected.
4. **In-place editing still reads the whole file** — it is not a seek-and-replace at byte level; `sed -i` rewrites the entire file, which can be slow on large files and breaks hard links.
5. **Greedy matching in character classes** — `s/<[^>]*>//g` is safer than `s/<.*>//g` for stripping tags; the `.*` version is greedy and may match from the first `<` to the last `>` on a line.
