---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [json, data, filtering, scripting]
status: working
---

# jq

> **Area:** [[CLI Tools]]

Command-line JSON processor. Reads JSON from stdin or a file, applies a filter expression, and outputs the result. The go-to tool for wrangling API responses and config files in shell scripts.

> jq filters are programs, not XPath-style paths. The learning curve is the filter language.

---

## 1. Identity and basics

```bash
jq '.'          # pretty-print the input (identity filter)
jq -c '.'       # compact output (one line)
jq -r '.'       # raw output — strips quotes from string values; needed for shell variable assignment
jq -n '{"key": "value"}'   # null input: generate JSON from scratch without reading stdin
```

## 2. Field access

```bash
jq '.name'                  # top-level field
jq '.address.city'          # nested field
jq '.tags[0]'               # first array element
jq '.tags[-1]'              # last array element
jq '.tags[1:3]'             # slice (index 1 inclusive to 3 exclusive)
jq '.tags[]'                # iterate: output each element on its own line
jq '.foo?'                  # optional: suppress error if .foo does not exist
jq '.foo // "default"'      # alternative: use "default" if .foo is null or false
```

## 3. Constructing output

```bash
# Build a new object
jq '{id: .id, name: .name}'

# Build a new array
jq '[.results[].name]'

# String interpolation
jq '"User: \(.name) (\(.email))"'

# Concatenation (strings or arrays)
jq '.first + " " + .last'
jq '.a + .b'               # arrays: concatenation; objects: merge (right wins on key conflict)
```

## 4. Filtering arrays

```bash
# select: keep only elements matching a condition
jq '.[] | select(.status == "active")'
jq '.[] | select(.age > 30 and .role == "admin")'
jq '.[] | select(.name | startswith("A"))'

# map: transform every element
jq '[.[] | .name]'            # equivalent shorthand:
jq '[.[].name]'
jq 'map(.price * 1.2)'        # apply an expression to every element

# map with select (filter + transform in one)
jq '[.[] | select(.active) | .name]'
```

## 5. Useful builtins

```bash
jq 'length'                   # length of string / array / object / null (0)
jq 'keys'                     # sorted array of object keys
jq 'keys_unsorted'
jq 'values'                   # array of object values
jq 'has("field")'             # true/false: does key exist?
jq 'in({"a":1})'              # true if input key exists in the argument object
jq 'type'                     # "null" | "boolean" | "number" | "string" | "array" | "object"
jq 'to_entries'               # [{key:k, value:v}, …]  — useful for iterating key-value pairs
jq 'from_entries'             # [{key:k, value:v}, …] → object
jq 'with_entries(.value += 1)'  # shorthand for to_entries | map(...) | from_entries
jq 'sort_by(.age)'            # sort array of objects by a field
jq 'group_by(.status)'        # group array elements into sub-arrays by field value
jq 'unique_by(.id)'           # deduplicate by field
jq 'flatten'                  # recursively flatten nested arrays
jq 'any(. > 5)'               # true if any element satisfies the condition
jq 'all(. > 0)'               # true if all elements satisfy the condition
jq 'min_by(.score)'
jq 'max_by(.score)'
jq 'add'                      # sum of numbers / concatenation of strings or arrays / merge of objects
jq 'first'                    # first element
jq 'last'                     # last element (alias for .[-1])
jq 'limit(3; .[])'            # emit at most 3 outputs
jq 'indices("x")'             # positions of all occurrences of "x" in a string or array
jq 'split(",")'
jq 'join(",")'
jq 'ltrimstr("prefix")'
jq 'rtrimstr("suffix")'
jq 'ascii_downcase'
jq 'tostring'
jq 'tonumber'
jq 'env.HOME'                 # access environment variables
jq '@base64'                  # encode to base64 (also @uri, @html, @csv, @tsv, @sh)
jq '@base64d'                 # decode from base64
```

## 6. Piping and combining

```bash
# Pipe inside jq (different from the shell pipe)
jq '.results | map(select(.active)) | sort_by(.name) | .[0:5]'

# Multiple outputs from a single run (each on its own line)
jq '.[] | "\(.id): \(.name)"'

# Combine multiple filters with comma (outputs all results)
jq '.name, .email'

# Reduce: accumulate a value
jq 'reduce .[] as $item (0; . + $item.amount)'
```

## 7. Passing values in

```bash
# Pass a shell variable as a jq string
jq --arg name "$NAME" '.[] | select(.name == $name)'

# Pass a shell variable as a raw JSON value (number, bool, object)
jq --argjson limit 10 '.[] | select(.count > $limit)'

# Pass a file's contents as a variable
jq --slurpfile cfg config.json '. + $cfg[0]'

# Read multiple JSON files and process them together
jq -s '.[0].users + .[1].users | unique_by(.id)' users1.json users2.json
```

---

## Daily workflows

### "Extract a field from each object in an API array response"
```bash
curl -s https://api.example.com/users | jq -r '.[].email'
```

### "Filter a list to only active items, return just their names"
```bash
jq -r '[.[] | select(.active == true) | .name] | join(", ")' users.json
```

### "Pretty-print and inspect a deeply nested value"
```bash
cat response.json | jq '.data.nested.things[0]'
```

### "Transform an array into a lookup object (id → name)"
```bash
jq '[.[] | {(.id|tostring): .name}] | add' items.json
```

### "Extract a value for use in a shell script"
```bash
TOKEN=$(curl -s https://auth.example.com/token -d '...' | jq -r '.access_token')
```

## Gotchas / Golden rules

1. **`-r` (raw output) is required when the result goes into a shell variable** — without it, strings include the surrounding `"`, which breaks variable use.
2. **`jq '.'` is the fastest way to validate JSON** — exit code 0 = valid; non-zero = parse error.
3. **`select` returns nothing (not null) when the condition is false** — downstream filters in a pipe see no input for that element, which is the intended behaviour; don't try to handle it as null.
4. **`//` (alternative operator) triggers on both null and false** — `jq '.flag // "default"'` returns "default" when `.flag` is `false`, which is usually not what you want. Use `if . == null then "default" else . end` for null-only fallback.
5. **Large inputs with `--slurpfile` hold the entire file in memory** — for very large files, prefer streaming with `--stream`.
