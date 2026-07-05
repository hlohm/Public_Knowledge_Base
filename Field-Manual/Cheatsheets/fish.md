---
type: cheatsheet
area: "Shells & Scripting"
aliases: []
tags: [shell, fish, interactive, scripting, autosuggestions]
status: working
---

# fish

> **Area:** [[Shells & Scripting]]

The Friendly Interactive SHell. Not POSIX-compatible — it has its own clean syntax, outstanding tab completion, and autosuggestions out of the box. Designed for interactive use first; scripting second.

> **Critical difference:** fish is not `/bin/sh`. You cannot run `#!/bin/fish` scripts from cron or most CI systems. Fish is an excellent interactive shell; use [[sh]] or [[bash]] for scripts that must be portable.

---

## 1. Key features out of the box

- **Autosuggestions** — as you type, fish suggests completions based on history and file paths (right arrow to accept)
- **Tab completion** — works for commands, subcommands, flags, files, and man pages without configuration
- **Syntax highlighting** — valid commands in blue, invalid in red, as you type
- **History** — fully searchable, shared across sessions, no duplicates
- **Web-based configuration** — `fish_config` opens a browser-based UI

---

## 2. Syntax differences from bash

```fish
# Variables: set instead of VAR=value
set myvar "hello"
set -x EXPORTED_VAR "world"     # export (-x)
set -e EXPORTED_VAR             # erase (unset)

# Strings: single quotes are literal; double quotes interpolate
set name "Alice"
echo "Hello, $name"             # Hello, Alice
echo 'Hello, $name'             # Hello, $name (literal)

# No [ ] — use the 'test' builtin or 'if' directly
if test -f /etc/passwd
    echo "file exists"
end

if [ -f /etc/passwd ]           # also works (test aliased to [)
    echo "exists"
end

# if / else
if test $status -eq 0
    echo "success"
else
    echo "failure"
end

# switch (case)
switch $lang
    case python
        echo "Python"
    case "java*"
        echo "Java variant"
    case '*'
        echo "other"
end

# Loops
for item in a b c
    echo $item
end

for f in *.txt
    echo $f
end

while true
    sleep 1
end

# Functions
function greet
    echo "Hello, $argv[1]"
end
greet "World"

# $argv is the argument list (1-indexed); $argv[1] is the first argument
# No $1, $2 — always use $argv
```

## 3. Functions

```fish
# Basic definition
function greet
    echo "Hello, $argv[1]"
end
greet World                        # Hello, World

# Named arguments instead of $argv[1], $argv[2]
function greet --argument-names name greeting
    echo "$greeting, $name"
end
greet Alice "Good morning"

# Description (shown in tab completion and `functions`)
function greet --description 'Say hello to someone'
    echo "Hello, $argv[1]"
end

# --wraps: inherit another command's completions
function gco --wraps 'git checkout'
    git checkout $argv
end

# Local variables — always scope with -l inside a function
function counter
    set -l count 0
    set count (math $count + 1)
    echo $count
end
```

### Introspection and persistence

```fish
functions                 # list all defined functions
functions greet           # print the source of one function
functions -e greet        # erase a function (session only)
functions -c greet greet2 # copy to a new name

funced greet               # open a function in $EDITOR for interactive editing
funcsave greet              # save the current definition to ~/.config/fish/functions/greet.fish
```

### Autoloading

Fish loads functions **lazily** — a function doesn't need to be defined in `config.fish`; drop it in `~/.config/fish/functions/<name>.fish` and fish loads it on first call:

```fish
# ~/.config/fish/functions/greet.fish
function greet
    echo "Hello, $argv[1]"
end
```

`funcsave` writes exactly this file for you — that's the normal workflow: prototype with `function`/`funced`, persist with `funcsave`.

### Event handlers

```fish
# Run a function when a variable changes
function on_editor_change --on-variable EDITOR
    echo "EDITOR is now $EDITOR"
end

# Run a function when a signal is received
function on_sigint --on-signal SIGINT
    echo "Caught Ctrl+C"
end

# Run a function after every command
function after_command --on-event fish_postexec
    echo "Ran: $argv"
end
```

## 4. Abbreviations (instant expand)

Abbreviations are like aliases but they expand immediately in the command line (you see what you're actually running):

```fish
abbr -a gs 'git status'
abbr -a gp 'git push'
abbr -a ll 'ls -lah'

abbr --list          # show all abbreviations
abbr -e gs           # erase an abbreviation
```

Stored in `~/.config/fish/config.fish`.

## 5. Key bindings

| Key | Action |
|---|---|
| `Tab` | Complete / show completions |
| `→` | Accept autosuggestion (or move right) |
| `Alt+→` | Accept one word of autosuggestion |
| `Ctrl+R` | Search history (interactive) |
| `Ctrl+F` | Forward one character |
| `Ctrl+B` | Backward one character |
| `Alt+F` / `Alt+B` | Forward / backward one word |
| `Ctrl+A` / `Ctrl+E` | Beginning / end of line |
| `Alt+L` | List directory (like `ls`) |
| `Ctrl+C` | Cancel current command |

## 6. Configuration

```fish
# ~/.config/fish/config.fish — sourced on every interactive session
set -x PATH $HOME/.local/bin $PATH
set -x EDITOR nvim

# Theme
set fish_greeting ""              # suppress default greeting

# Prompt: set with fish_config, or manually:
function fish_prompt
    echo -n (prompt_pwd) " > "
end

# Starship cross-shell prompt
starship init fish | source

# fzf integration
fzf --fish | source

# Conditional (for systems without a tool)
if type -q zoxide
    zoxide init fish | source
end
```

```fish
# Universal variables (persist across sessions without config file change)
set -U fish_color_command blue
set -U MY_TOKEN "abc123"
```

## 7. Completions

Fish generates completions from man pages automatically. To write a custom completion:

```fish
# ~/.config/fish/completions/myapp.fish
complete -c myapp -s h -l help -d 'Show help'
complete -c myapp -s o -l output -r -d 'Output file'
complete -c myapp -l dry-run -d 'Dry run'
complete -c myapp -n '__fish_no_arguments' -a '(ls *.conf)' -d 'Config file'
```

## 8. Scripts

Fish scripts have `.fish` extension and use fish syntax, not bash:

```fish
#!/usr/bin/env fish
# my-script.fish

argparse 'h/help' 'n/name=' -- $argv
or return

if set -q _flag_help
    echo "Usage: my-script [-n name]"
    return
end

set name (set -q _flag_name; and echo $_flag_name; or echo "World")
echo "Hello, $name"
```

`argparse` is fish's built-in argument parsing — much cleaner than `getopts`.

---

## Daily workflows

### "Quickly navigate to a recent directory"
```fish
# fish remembers recent directories automatically
prevd      # go to previous directory
nextd      # go to next directory
dirh       # list directory history
cdh        # interactive directory history picker
```

### "Accept an autosuggestion word-by-word"
```
type "git pus"  → fish suggests "git push origin main"
Alt+→           → accept "git push" one word at a time
```

### "Define a persistent abbreviation"
```fish
abbr -a dc 'docker compose'
```

### "Run a one-off bash command from fish"
```fish
bash -c 'echo $BASH_VERSION'
/bin/bash script.sh
```

### "Turn a one-off command into a permanent function"
```fish
function weather --description 'Show weather for a city'
    curl -s "wttr.in/$argv[1]"
end
funcsave weather        # persists to ~/.config/fish/functions/weather.fish
```

## Gotchas / Golden rules

1. **`$argv` not `$@` or `$1`** — fish uses `$argv` for arguments (1-indexed); `$argv[1]` is the first, `$argv[-1]` is the last.
2. **No semicolons between statements — use newlines or `;`** — `echo a; echo b` works; `echo a && echo b` does not (use `and`/`or` keywords instead).
3. **`and` / `or` are statements, not operators** — `and echo "yes"` runs if the previous command succeeded; use them on their own lines or after `;`.
4. **Universal variables persist forever** — `set -U VAR val` survives reboots; unlike environment variables which are per-session. Erase them explicitly with `set -Ue VAR`.
5. **Don't use fish as a shebang for scripts that run outside fish** — cron, systemd, and most CI runners run scripts under `/bin/sh`; a `#!/usr/bin/env fish` script will fail if fish is not installed system-wide.
6. **Functions don't run in a subshell — variables leak unless scoped** — `set count 0` inside a function changes the global (or outer) `$count` if one exists; always `set -l` for a variable that should stay local to the function.
7. **`return` sets an exit status, not a value** — fish functions have no return-value mechanism like other languages; to "return" data, `echo` it and capture with command substitution: `set result (myfunc)`.
8. **Editing a function in memory (`function`/`funced`) doesn't persist it** — it's gone when the shell exits unless you `funcsave` it, or define it in `~/.config/fish/functions/<name>.fish` directly.
