---
type: cheatsheet
area: CLI Tools
aliases: []
tags: [terminal, multiplexer]
status: working
---

# tmux

> **Area:** [[CLI Tools]]

Terminal multiplexer: persistent sessions that survive disconnects, plus split panes and
multiple windows in one terminal. Pairs naturally with [[ssh]] (keep a session alive on a
remote host) and [[nvim]].

> The prefix is `Ctrl-b` by default (`C-b`); press it, release, then the key. Examples below
> assume the default prefix — remapped to `C-a` by many configs (see §6).

---

## 1. Sessions

```bash
tmux                       # start a new session
tmux new -s work           # ...named "work"
tmux ls                    # list sessions
tmux attach -t work        # re-attach (e.g. after an ssh drop)
tmux attach                # attach to the most recent session
tmux new -s work -d        # create detached (for scripting — see §5)
tmux kill-session -t work
tmux rename-session -t work project   # or: prefix, $ (from inside)
```

| keys | action |
| --- | --- |
| `C-b d` | detach (session keeps running in the background) |
| `C-b s` | interactive session picker |
| `C-b $` | rename the current session |
| `C-b (` / `C-b )` | switch to previous / next session |

---

## 2. Windows

```bash
tmux new -s work -n editor   # name the first window on creation
```

| keys | action |
| --- | --- |
| `C-b c` | new window |
| `C-b ,` | rename current window |
| `C-b n` / `C-b p` | next / previous window |
| `C-b 0`–`9` | jump to window by number |
| `C-b w` | interactive window picker |
| `C-b &` | kill current window (asks to confirm) |
| `C-b f` | find window by name |

---

## 3. Panes

```bash
tmux split-window -h    # same as C-b %  (vertical split, side by side)
tmux split-window -v    # same as C-b "  (horizontal split, stacked)
```

| keys | action |
| --- | --- |
| `C-b "` | split horizontally (new pane below) |
| `C-b %` | split vertically (new pane to the side) |
| `C-b <arrow>` | move between panes |
| `C-b o` | cycle to the next pane |
| `C-b ;` | toggle to the last active pane |
| `C-b z` | zoom the current pane full-screen (toggle) |
| `C-b x` | kill current pane (asks to confirm) |
| `C-b {` / `C-b }` | swap pane with previous / next |
| `C-b space` | cycle through preset layouts |

**Resizing** — hold the prefix and repeat, or use the resize-specific bindings:

```
C-b Ctrl-<arrow>     resize by 1 cell (hold, repeats without re-pressing prefix each time)
C-b Alt-<arrow>       resize by 5 cells
```

Layouts worth knowing by name (`C-b space` cycles these): `even-horizontal`,
`even-vertical`, `main-horizontal` (one big pane on top), `main-vertical` (one big pane on the
side), `tiled`.

---

## 4. Copy mode (scrollback and clipboard)

```
C-b [          enter copy mode (also triggered by scrolling in most configs)
  <arrows> / hjkl     move the cursor (vi-style if configured — see §6)
  Ctrl-b / Ctrl-f     page up / page down
  g / G               top / bottom of scrollback
  space               start a selection
  Enter               copy selection and exit copy mode
  q                   exit copy mode without copying
C-b ]          paste the most recent copy-mode selection
```

```bash
tmux show-buffer            # print the current paste buffer
tmux list-buffers           # show all copied buffers
tmux save-buffer file.txt   # dump the paste buffer to a file
```

By default, copy mode's clipboard is **internal to tmux** — `C-b ]` pastes it back inside
tmux, but it does *not* reach the OS clipboard unless you configure it (see `set-clipboard` and
the vi-mode bindings in §6). On most modern terminals with `set -g set-clipboard on`, a copy-mode
selection also lands on the system clipboard for free.

---

## 5. Scripting sessions (project setup)

Build a whole layout non-interactively — useful for "start my dev environment" scripts:

```bash
#!/usr/bin/env bash
SESSION=myproject

tmux new-session -d -s "$SESSION" -n editor
tmux send-keys -t "$SESSION:editor" 'nvim .' C-m

tmux new-window -t "$SESSION" -n server
tmux send-keys -t "$SESSION:server" 'npm run dev' C-m

tmux split-window -h -t "$SESSION:server"
tmux send-keys -t "$SESSION:server.1" 'npm test -- --watch' C-m

tmux select-window -t "$SESSION:editor"
tmux attach -t "$SESSION"
```

`send-keys ... C-m` types the command and presses Enter (`C-m` = carriage return) — without it
the text sits in the prompt unexecuted. Target panes as `session:window.pane`.

---

## 6. A minimal `~/.tmux.conf`

```tmux
# Remap prefix to Ctrl-a (closer to hand, matches screen's default)
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Mouse: click to select pane/window, drag to resize, scroll to scroll
set -g mouse on

# Start window/pane numbering at 1 (0 is an awkward reach)
set -g base-index 1
setw -g pane-base-index 1

# vi-style keys in copy mode
setw -g mode-keys vi

# Send copy-mode selections to the system clipboard too
set -g set-clipboard on

# Saner splits: keep the current pane's working directory
bind '"' split-window -v -c '#{pane_current_path}'
bind %   split-window -h -c '#{pane_current_path}'

# Bigger scrollback (default is only 2000 lines)
set -g history-limit 10000

# Reload config without restarting tmux
bind r source-file ~/.tmux.conf \; display 'Config reloaded'
```

```bash
tmux source-file ~/.tmux.conf   # apply after editing, or use the `bind r` above
```

---

## Daily workflows

### "Reconnect after an SSH drop with everything intact"
```bash
tmux new -s work    # first time — do your work
# connection drops...
ssh host
tmux attach -t work # everything is exactly as you left it
```

### "Set up a 3-pane dev layout every time"
```bash
tmux new -s dev -d
tmux split-window -h -t dev
tmux split-window -v -t dev
tmux attach -t dev
```

### "Check if a session is already running before starting a new one"
```bash
tmux attach -t work 2>/dev/null || tmux new -s work
```

### "Kill every tmux session at once"
```bash
tmux kill-server
```

---

## Files & locations

| Path | What |
| --- | --- |
| `~/.tmux.conf` | user config, read on tmux start (`bind r` above reloads without restart) |
| `/etc/tmux.conf` | system-wide config, read before the user config |

---

## Gotchas / Golden rules

1. **Copy mode's buffer isn't the OS clipboard by default.** `C-b ]` pastes inside tmux only —
   set `set-clipboard on` (§6) to bridge it to the system clipboard.
2. **`C-b d` detaches, it does not kill.** The session and everything running in it (long
   builds, `nvim` with unsaved buffers) keeps going in the background — `attach` picks it back up.
3. **`send-keys` needs an explicit `C-m`/`Enter`** to actually execute a typed command; without
   it the text just sits in the prompt.
4. **Panes default to the shell's original working directory, not the current pane's** — add
   `-c '#{pane_current_path}'` to split bindings (§6) if you want new panes/windows to inherit
   where you already are.
5. **Nested tmux (tmux inside an ssh session that's itself inside tmux) needs `C-b C-b`** (or a
   remapped outer prefix) to send the prefix to the inner session instead of the outer one.

## Further reading
- [tmux(1)](https://man7.org/linux/man-pages/man1/tmux.1.html) · `man tmux`
