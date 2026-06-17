---
type: cheatsheet
area: CLI Tools
aliases: []
tags: [terminal, multiplexer]
status: stub
---

# tmux

> **Area:** [[CLI Tools]]

Terminal multiplexer: persistent sessions that survive disconnects, plus split panes and
multiple windows in one terminal. Pairs naturally with [[ssh]] (keep a session alive on a
remote host) and [[nvim]].

> **Status: stub.** Scope and the essentials are here; promote to `working`/`stable` as the
> daily commands get filled in and verified. See [[How to Extend]].

The prefix is `Ctrl-b` by default (`C-b`); press it, release, then the key.

## Essentials

```bash
tmux                       # start a new session
tmux new -s work           # ...named "work"
tmux ls                    # list sessions
tmux attach -t work        # re-attach (e.g. after an ssh drop)
tmux kill-session -t work
```

| keys | action |
| --- | --- |
| `C-b d` | detach (session keeps running in the background) |
| `C-b c` | new window |
| `C-b n` / `C-b p` | next / previous window |
| `C-b "` / `C-b %` | split pane horizontally / vertically |
| `C-b <arrow>` | move between panes |
| `C-b z` | zoom the current pane (toggle) |
| `C-b [` | enter copy/scroll mode (`q` to exit) |

## To fill in
- pane resizing & layouts
- copy-mode key bindings and clipboard integration
- a minimal `~/.tmux.conf` (prefix remap, mouse on, sane splits)
- scripting sessions for project setup

## Further reading
- [tmux(1)](https://man7.org/linux/man-pages/man1/tmux.1.html) · `man tmux`
