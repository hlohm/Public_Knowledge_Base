---
type: cheatsheet
area: "Shells & Scripting"
aliases: []
tags: [shell, zsh, interactive, completion, scripting]
status: working
---

# zsh

> **Area:** [[Shells & Scripting]]

Bash-compatible interactive shell with superior completion, history, globbing, and theming. Default shell on macOS since Catalina (10.15). Common with Oh My Zsh / Prezto / Starship for a curated interactive experience.

> **Scripting:** zsh scripts are not portable across shells. Use [[sh]] or [[bash]] for portable scripts; use zsh for your interactive shell and for personal scripts that only run on your machines.

---

## 1. Shell options (setopt)

```zsh
# Interactive settings to add to ~/.zshrc:
setopt AUTO_CD              # type a directory name to cd into it
setopt CORRECT              # suggest corrections for mistyped commands
setopt HIST_IGNORE_DUPS     # don't add duplicate commands to history
setopt HIST_IGNORE_SPACE    # commands starting with space are not saved to history
setopt SHARE_HISTORY        # share history across terminal sessions immediately
setopt EXTENDED_GLOB        # enable extended globbing (**, negation, etc.)
setopt NOMATCH              # error when glob matches nothing (don't pass literal glob)
setopt INTERACTIVE_COMMENTS # allow # comments in interactive sessions
setopt NO_BEEP              # suppress beep on error

unsetopt CASE_GLOB          # case-insensitive globbing (useful on macOS)
```

## 2. Completion system

```zsh
# Enable the completion system
autoload -Uz compinit
compinit

# Completion menu (tab → show menu; tab again → navigate)
zstyle ':completion:*' menu select

# Case-insensitive, partial-word completion
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'

# Group completions by category
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%B%d%b'

# Complete hidden files
zstyle ':completion:*' file-patterns '*:all-files'

# In interactive use:
# Tab          → complete / open menu
# Tab Tab      → enter menu navigation
# Shift+Tab    → move backwards in menu
# Ctrl+R       → fuzzy history search (or use fzf integration)
```

## 3. History

```zsh
HISTFILE=~/.zsh_history
HISTSIZE=50000
SAVEHIST=50000

# History search
Ctrl+R          # incremental reverse search (or: use fzf -- see [[fzf]])
history         # list all history (number, command)
history -D      # list with elapsed time
fc -l -20       # last 20 commands (fc = fix command)
!! 		    # repeat last command
!-2             # second-to-last command
!ssh            # last command starting with 'ssh'
!?nginx         # last command containing 'nginx'
^old^new        # repeat last command, replacing 'old' with 'new'
```

## 4. Extended globbing

```zsh
# Enable: setopt EXTENDED_GLOB

ls **/*.py          # recursive glob: all .py files in any subdirectory
ls **/*.py~test*    # all .py files NOT starting with test (~ = negate)
ls *.py(.)          # only regular files (not dirs)
ls *(/)             # only directories
ls *(x)             # only executable files
ls *(.Lm+10)        # regular files larger than 10 MB
ls *(.mh-24)        # regular files modified in the last 24 hours
ls *(Om)            # sort by modification time (oldest first)
ls *(.oc)           # sort by size (smallest first)

# Brace expansion (same as bash)
echo {a,b,c}.txt
echo file{1..5}.txt
```

## 5. Parameter expansion

```zsh
# zsh adds to POSIX parameter expansion:
echo ${(U)var}            # uppercase
echo ${(L)var}            # lowercase
echo ${(C)var}            # capitalize first letter
echo ${(l:10::0:)var}     # left-pad to width 10 with zeros
echo ${(r:10:)var}        # right-pad to width 10
echo ${(j:,:)array}       # join array elements with comma
echo ${(s:,:)string}      # split string on comma into array
echo ${#array}            # array length
echo ${array[2,5]}        # slice: elements 2 through 5 (1-indexed)
echo ${(o)array}          # sorted array
echo ${(u)array}          # unique elements
```

## 6. Key bindings

```zsh
bindkey -e                # emacs key bindings (default for most users)
bindkey -v                # vi mode

# Common Emacs-mode bindings (when bindkey -e):
# Ctrl+A   beginning of line
# Ctrl+E   end of line
# Ctrl+W   delete word backward
# Alt+F    move word forward
# Alt+B    move word backward
# Ctrl+K   kill to end of line
# Ctrl+U   kill to beginning of line
# Ctrl+R   history search
# Ctrl+L   clear screen

# Add custom binding
bindkey '^[[1;5C' forward-word    # Ctrl+Right → move word forward
bindkey '^[[1;5D' backward-word   # Ctrl+Left  → move word backward
```

## 7. ~/.zshrc essentials

```zsh
# Minimal recommended ~/.zshrc

# History
HISTFILE=~/.zsh_history
HISTSIZE=50000
SAVEHIST=50000
setopt SHARE_HISTORY HIST_IGNORE_DUPS HIST_IGNORE_SPACE

# Completion
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# Prompt (simple; replace with Starship or Oh My Zsh for more)
autoload -Uz promptinit && promptinit
prompt walters    # built-in theme: PS1 with user@host path %

# Or use Starship (cross-shell, fast):
# eval "$(starship init zsh)"

# fzf integration
# eval "$(fzf --zsh)"    # Ctrl+T, Ctrl+R, Alt+C

# Aliases
alias ll='ls -lah'
alias gs='git status'

# PATH
export PATH="$HOME/.local/bin:$PATH"
```

---

## Daily workflows

### "Navigate to a directory without typing cd"
```zsh
# setopt AUTO_CD is set
~                 # goes to $HOME
/etc              # cd /etc
projects/myapp    # cd ./projects/myapp (if it's a directory)
```

### "Find and run a past command"
```zsh
# Ctrl+R to search, or:
history | grep 'docker run'
!123              # run command number 123 from history
```

### "List only .py files modified today"
```zsh
setopt EXTENDED_GLOB
ls **/*.py(.mh-24)
```

## Gotchas / Golden rules

1. **`~/.zshrc` is not sourced for non-interactive shells** — scripts should not rely on your `.zshrc` settings; they start with a minimal environment.
2. **`setopt EXTENDED_GLOB` changes `#`, `~`, `^` meanings** — `#` becomes a glob quantifier, which breaks some patterns that expect `#` to be literal; be aware when mixing extended glob with scripts.
3. **Arrays are 1-indexed in zsh** — unlike bash (0-indexed); `$array[1]` is the first element.
4. **`/bin/sh` on macOS is NOT zsh** — it is `sh` (derived from `dash`/`bash` depending on the version); `#!/bin/sh` scripts run under sh, not zsh.
5. **`compinit` should only be called once** — calling it multiple times (e.g., in both `.zshrc` and a plugin) causes slowdowns; if using a plugin manager, let it call `compinit`.
