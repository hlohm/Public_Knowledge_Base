---
type: "term"
branch: "Graphics, Media & HCI"
aliases: ["Text-based User Interface", "Terminal User Interface"]
tags: [media]
status: "developed"
---

# TUI

> **Branch:** [[14 - Graphics, Media & HCI|Graphics, Media & HCI]]
> **Also known as:** Text-based User Interface, Terminal User Interface

A full-screen interactive interface drawn entirely with characters in a terminal — panes, menus, tables, and live updates rendered via cursor-addressing escape sequences rather than pixels (htop, vim, tmux, midnight commander).

**Context.** The sweet spot between a plain command line and a GUI: richer interaction than typed commands, but it still runs over SSH, inside tmux, on a headless box, with no display server or toolkit dependency — which is why ops and developer tooling keeps landing here. Classic implementation layer is curses/ncurses; the modern wave (Rust's ratatui, Go's Bubble Tea, Python's Textual) brought reactive, widget-based frameworks to the terminal. The constraint to respect: a good TUI degrades gracefully to a dumb 80×24 terminal, because that's what the emergency console will be.

## See also

- [[Shell]]
- [[CLI]]
- [[GUI]]
- [[Interface]]

## Often confused with

- [[CLI]] — a CLI is command-in, text-out, one exchange at a time; a TUI takes over the whole screen and stays interactive until you quit.

## Further reading

- [Wikipedia: Text-based user interface](https://en.wikipedia.org/wiki/Text-based_user_interface)
