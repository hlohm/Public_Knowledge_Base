---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [text-processing, data, columns, scripting]
status: working
---

# awk

> **Area:** [[CLI Tools]]

Pattern-scanning and text-processing language. Reads records (lines by default), splits each into fields, and executes actions for records matching patterns. The right tool when you need columns, arithmetic, or aggregation in a shell pipeline.

> When it gets to more than 20 lines of awk, switch to Python. awk's strength is concise one-liners.

---

## 1. Core model

```
awk 'pattern { action }' file
```

- Input is split into **records** (lines) by `RS` (record separator, default `\n`)
- Each record is split into **fields** by `FS` (field separator, default whitespace)
- `$0` = whole record; `$1`, `$2`, … = fields; `NF` = number of fields; `NR` = record number

```bash
awk '{ print $1 }' file.txt          # print first field of every line
awk '{ print $NF }' file.txt         # print last field
awk '{ print NR, $0 }' file.txt      # line number + line
awk 'NR==5 { print }' file.txt       # print line 5 only
awk '/pattern/ { print }' file.txt   # print lines matching regex
awk '!/pattern/ { print }' file.txt  # print lines NOT matching
```

## 2. Field separator

```bash
awk -F: '{ print $1 }' /etc/passwd       # colon-delimited: usernames
awk -F',' '{ print $2 }' data.csv        # CSV: second column
awk -F'\t' '{ print $3 }' data.tsv       # TSV: third column
awk 'BEGIN { FS="," } { print $2 }' file # set FS in BEGIN block

# Multiple separators (ERE)
awk -F'[,;]' '{ print $1, $2 }' file
```

## 3. BEGIN and END blocks

```bash
# BEGIN: runs once before any input is read (setup, print headers)
# END: runs once after all input is consumed (totals, summaries)

awk 'BEGIN { print "Name\tSize" }
     { print $1, $2 }
     END { print NR, "records" }' file.txt
```

## 4. Built-in variables

```bash
FS    # field separator (default: whitespace)
RS    # record separator (default: newline)
OFS   # output field separator (default: space)
ORS   # output record separator (default: newline)
NR    # current record number (total across all files)
FNR   # record number within the current file
NF    # number of fields in the current record
FILENAME # name of the current input file
```

```bash
awk 'BEGIN { OFS="," } { print $1,$2,$3 }' file  # comma-separated output
```

## 5. Arithmetic and variables

```bash
awk '{ sum += $3 } END { print sum }' data.txt         # sum a column
awk '{ sum += $3; n++ } END { print sum/n }' data.txt  # average
awk '{ if ($3 > max) max=$3 } END { print max }' data.txt  # maximum

# Count occurrences of values in a field
awk '{ count[$1]++ } END { for (k in count) print k, count[k] }' file

# Total by group
awk -F, '{ total[$1] += $3 } END { for (k in total) print k, total[k] }' data.csv
```

## 6. String operations

```bash
awk '{ print length($0) }' file           # line length
awk '{ print substr($0, 5, 10) }' file   # substring: start=5, length=10
awk '{ print index($0, "foo") }' file    # position of substring (0 = not found)
awk '{ gsub(/old/, "new"); print }' file # global substitution (modifies $0)
awk '{ sub(/old/, "new"); print }' file  # first substitution only
awk '{ print toupper($0) }' file
awk '{ print tolower($0) }' file
awk '{ split($2, parts, ":"); print parts[1] }' file  # split field into array
```

## 7. Conditionals and loops

```bash
awk '{ if ($3 > 100) print $1, "HIGH"; else print $1, "LOW" }' file

awk '{ for (i=1; i<=NF; i++) printf "%s ", $i; printf "\n" }' file  # reprint all fields

awk '/START/,/END/ { print }' file   # range pattern: print lines between START and END
```

---

## Daily workflows

### "Extract and reformat columns from whitespace-delimited output"
```bash
ps aux | awk 'NR>1 { printf "%-10s %s\n", $1, $11 }'
```

### "Sum a column in a CSV"
```bash
awk -F, '{ sum += $4 } END { print sum }' sales.csv
```

### "Count occurrences of each unique value in a log field"
```bash
awk '{ count[$9]++ } END { for (s in count) print count[s], s }' access.log | sort -rn
```

### "Print lines where a field exceeds a threshold"
```bash
awk '$5 > 1000 { print NR, $0 }' data.txt
```

### "Reorder and rejoin fields"
```bash
awk -F: 'BEGIN { OFS="," } { print $3,$1,$5 }' /etc/passwd
```

## Gotchas / Golden rules

1. **`$0` is the whole line; modifying `$1` rebuilds `$0` with `OFS` as the separator** — if you reassign `$1 = toupper($1)`, the whole line is rebuilt using OFS instead of the original spacing.
2. **Uninitialized variables are 0 (numeric) or "" (string)** — `count[$key]++` works without declaring `count`; it silently starts at 0.
3. **Array iteration order is undefined** — `for (k in array)` does not iterate in insertion order; pipe to `sort` if order matters.
4. **`print a, b` uses OFS; `print a b` concatenates with no separator** — the comma is significant: `print $1, $2` outputs `$1 OFS $2`; `print $1 $2` outputs them joined.
5. **`gsub` returns the number of substitutions, not the result** — it modifies the target in place; to operate on a copy, use a variable: `s=$0; gsub(/x/,"y",s); print s`.
