---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [fuzzy-finder, interactive, search, shell]
status: working
---

# fzf

> **Area:** [[CLI Tools]]

Interactive fuzzy finder. Takes a list of items on stdin, lets you narrow the list by typing, and outputs the selected item. The universal interactive picker for files, history, processes, and anything else you can list.

> fzf is most powerful via its shell integration (Ctrl+R, Ctrl+T, Alt+C) — install it once and it enhances your shell permanently.

---

## 1. Basic usage

```bash
# Pick a file interactively from the current directory tree
fzf

# Pipe any list into fzf
cat /etc/passwd | fzf
ls /usr/bin | fzf
git branch | fzf

# Pass a selected item to another command
vim $(fzf)
cd $(find . -type d | fzf)
```

## 2. Key bindings in the picker

| Key | Action |
|---|---|
| Type | Narrow the list (fuzzy match) |
| `↑` / `↓` or `Ctrl+P` / `Ctrl+N` | Navigate |
| `Enter` | Confirm selection |
| `Esc` / `Ctrl+C` | Cancel |
| `Tab` | Multi-select (with `--multi`) |
| `Shift+Tab` | Deselect |

## 3. Shell integration (the must-have setup)

Source the fzf shell integration in your shell rc file:

```bash
# bash (~/.bashrc)
eval "$(fzf --bash)"

# zsh (~/.zshrc)
eval "$(fzf --zsh)"

# fish (~/.config/fish/config.fish)
fzf --fish | source
```

After sourcing, you get:

| Shortcut | What it does |
|---|---|
| `Ctrl+T` | Paste a selected file path into the command line |
| `Ctrl+R` | Fuzzy-search shell history |
| `Alt+C` | `cd` into a selected directory |

These three bindings alone are worth the install.

## 4. Flags

```bash
fzf --multi             # allow selecting multiple items (Tab to select, Enter to confirm)
fzf -m                  # shorthand for --multi

fzf --query 'init'      # pre-fill the search query
fzf -q 'init'

fzf --height 40%        # use only 40% of the terminal height (less disorienting)
fzf --reverse           # list from top, prompt at top (less tail-up scrolling)

fzf --header 'Pick a file'   # display a header line above the list

fzf --no-sort           # preserve the original order of the list (e.g., for history)
```

## 5. Preview window

The `--preview` flag runs a command for the currently highlighted item and shows its output:

```bash
# Preview file contents with bat (or cat)
fzf --preview 'bat --color=always {}' --preview-window '~3'

# Preview file with cat (no bat)
fzf --preview 'cat {}'

# Preview a directory
find . -type d | fzf --preview 'ls -la {}'

# Preview git log for a branch
git branch | fzf --preview 'git log --oneline --graph --color=always {}'
```

## 6. Integration patterns

```bash
# Fuzzy kill: interactively select a process to kill
kill $(ps aux | fzf --header-lines=1 | awk '{print $2}')

# Fuzzy git checkout
git checkout $(git branch -a | fzf)

# Fuzzy SSH: pick a host from ~/.ssh/config
ssh $(grep '^Host' ~/.ssh/config | awk '{print $2}' | fzf)

# Fuzzy open recent files in vim (using git history)
vim $(git log --oneline --name-only | grep -v '^[0-9a-f]' | sort -u | fzf)

# Pass multiple selections to a command
rg -l 'TODO' | fzf --multi | xargs nvim

# Fuzzy environment variable selector
printenv | fzf | cut -d= -f1
```

## 7. Configuration

```bash
# ~/.fzf.bash / ~/.fzf.zsh — or set FZF_DEFAULT_OPTS in your shell rc:
export FZF_DEFAULT_OPTS='--height 40% --reverse --border --inline-info'

# Default command: use fd or rg for faster, gitignore-aware listing
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
```

---

## Daily workflows

### "Jump to a project directory"
```bash
cd $(find ~/projects -maxdepth 2 -type d | fzf)
```

### "Search and open a file in your editor"
```bash
nvim $(rg -l '' | fzf --preview 'bat --color=always {}')
```

### "Fuzzy-find a command in history and run it"
```bash
# Ctrl+R with shell integration does this automatically
# Or manually:
eval $(history | fzf --no-sort | sed 's/^[[:space:]]*[0-9]*[[:space:]]*//')
```

## Gotchas / Golden rules

1. **`$(fzf)` exits with non-zero when the user cancels** — wrap in a check if the downstream command must not run on empty: `file=$(fzf) && vim "$file"`.
2. **`--multi` outputs one selected item per line** — pipe to `xargs` or use a while-read loop to process each selection.
3. **`FZF_DEFAULT_COMMAND` affects only Ctrl+T, not bare `fzf`** — `fzf` with no input still uses `find .` internally; set the command explicitly or pipe your own list.
4. **The preview command runs for every highlighted item** — keep it fast; avoid expensive operations. Use `bat` caching or `head -100` to limit output.
