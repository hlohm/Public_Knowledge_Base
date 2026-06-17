---
type: cheatsheet
area: CLI Tools
aliases: [neovim, vim]
tags: [editor]
status: stable
---

# nvim

> **Area:** [[CLI Tools]]

A quick reference for working in nvim. The first half is **pure vim** — applies anywhere you
have vi/vim/nvim. The second half documents a **kickstart-style config**: leader bindings,
plugins, indicators. Adjust the config-specific parts to your own setup. Leader is `<space>`.
Most discovery happens through `<leader>sk` (search keymaps) and which-key — start a chord and
pause to see what's available.

---

## Modes

| Mode | Enter from normal | Indicator |
| --- | --- | --- |
| normal | `<Esc>` from anywhere | (none — `showmode = false` in this config) |
| insert | `i`, `a`, `o`, etc. | none visible; cursor changes shape |
| visual (char) | `v` | shown by selection |
| visual (line) | `V` | shown by selection |
| visual (block) | `<C-v>` | shown by selection |
| command | `:` | cmdline at bottom |
| terminal | inside a `:terminal` buffer | `TERMINAL` in statusline |

Exit to normal mode is `<Esc>` everywhere — except terminal mode, where this config maps
`<Esc><Esc>` (default would be `<C-\><C-n>`).

## Motions

Cursor movement. Counts compose with motions: `5j` moves down 5 lines, `3w` jumps 3 words.

### Within a line

| key | motion |
| --- | --- |
| `h` `j` `k` `l` | left / down / up / right |
| `w` / `W` | forward to start of next word / WORD (whitespace-delimited) |
| `b` / `B` | back to start of previous word / WORD |
| `e` | forward to end of word |
| `0` / `^` / `$` | start of line / first non-blank / end of line |
| `g_` | last non-blank character on line |
| `f<c>` / `F<c>` | forward / backward to next/previous `<c>` |
| `t<c>` / `T<c>` | forward to just before / backward to just after `<c>` |
| `;` / `,` | repeat / reverse last `f` `t` `F` `T` |
| `%` | jump to matching bracket / paren / brace |

### Across lines

| key | motion |
| --- | --- |
| `gg` / `G` | top / bottom of buffer |
| `<n>G` or `<n>gg` | go to line `<n>` |
| `(` `)` | previous / next sentence |
| `{` `}` | previous / next paragraph (empty line) |
| `[[` `]]` | previous / next section start |
| `gj` `gk` | down / up by *visual* line (when wrap is on) |

### Within the window

| key | motion |
| --- | --- |
| `H` `M` `L` | top / middle / bottom of window |
| `<C-d>` / `<C-u>` | scroll down / up half a screen |
| `<C-f>` / `<C-b>` | scroll forward / backward a full screen |
| `zz` `zt` `zb` | center / top / bottom the cursor in the window |

## Operators & text objects

Vim's grammar: `<count><operator><motion-or-text-object>`. `d2w` deletes 2 words forward.
`ci"` changes inside the quotes around the cursor.

### Operators

| key | operator |
| --- | --- |
| `d` / `c` / `y` | delete / change / yank |
| `p` / `P` | paste after / before |
| `>` / `<` / `=` | indent right / left / auto-indent |
| `gu` / `gU` / `g~` | lowercase / uppercase / toggle case |
| `gc` | toggle comment (built in to 0.10+) |

Double an operator to act on the whole line: `dd`, `yy`, `cc`, `>>`, `gcc`.

### Text objects

Used after operators. Pattern: `i<x>` for *inside* `<x>`, `a<x>` for *around* `<x>` (includes
delimiters / surrounding whitespace).

| key | text object |
| --- | --- |
| `w` / `W` | word / WORD |
| `s` / `p` | sentence / paragraph |
| `"` `'` `` ` `` | matching quotes |
| `(` `)` or `b` | matching parens |
| `[` `]` | matching square brackets |
| `{` `}` or `B` | matching braces |
| `<` `>` | matching angle brackets |
| `t` | XML / HTML tag |

So: `ciw` change inner word, `da"` delete around double-quotes (including the quotes), `yip`
yank inner paragraph. mini.ai extends this with next/previous variants (see *Text objects
(mini.ai)* below).

## Entering insert mode

| key | enters insert mode at... |
| --- | --- |
| `i` / `a` | cursor / after cursor |
| `I` / `A` | first non-blank / end of line |
| `o` / `O` | new line below / above |
| `s` / `S` | cursor (delete char first) / line (delete line first) |
| `C` | cursor (delete to end of line first) |

## Visual mode

Select first, then act: `d` deletes selection, `y` yanks it, etc.

| key | action |
| --- | --- |
| `v` / `V` / `<C-v>` | char-wise / line-wise / block-wise selection |
| `o` | move to other end of selection |
| `gv` | re-select last visual selection |
| `<` `>` | indent left / right (this config keeps the selection — easier multi-indent) |

## Search (within buffer)

| key | action |
| --- | --- |
| `/<pattern>` / `?<pattern>` | search forward / backward |
| `n` / `N` | next / previous match |
| `*` / `#` | search forward / backward for word under cursor |
| `<Esc>` | clear search highlight (custom mapping) |

Case-insensitive unless the pattern contains uppercase (`smartcase`); live preview while
typing (`incsearch`). Project-wide search across files: `<leader>sg` (telescope live grep) —
see *Searching (telescope)* below.

## Edits, undo, repeat

| key | action |
| --- | --- |
| `x` / `X` | delete char under / before cursor |
| `r<c>` / `R` | replace one char / enter replace mode |
| `~` | toggle case of char under cursor |
| `J` / `gJ` | join line below (with / without space) |
| `u` / `<C-r>` | undo / redo |
| `.` | repeat last change |

`.` is one of vim's most powerful commands — `dw` then `.` deletes the next word too; `dw`
then `5.` deletes the next five.

## Marks & jumps

`m<x>` sets mark `<x>`; `'<x>` jumps to the line, `` `<x> `` jumps to the exact column.

| key | action |
| --- | --- |
| `m<a-z>` / `m<A-Z>` | set buffer-local / global mark |
| `'<x>` / `` `<x> `` | jump to line / exact position of mark |
| `''` / ``` `` ``` | jump to line / position before last jump |
| `<C-o>` / `<C-i>` | back / forward through the jumplist |
| `g;` / `g,` | back / forward in the changelist |

`<C-o>` after a goto-definition lands you back exactly where you came from — worth muscle memory.

## Registers & macros

Default register is `"`; named registers are `a`–`z`.

| key | action |
| --- | --- |
| `"<x>y` / `"<x>p` | yank into / paste from register `<x>` |
| `:reg` | view all register contents |
| `q<x>` … `q` | start / stop recording a macro into register `<x>` |
| `@<x>` / `@@` | play macro `<x>` / replay last macro |
| `<n>@<x>` | play macro `<x>` `<n>` times |

System clipboard: with `clipboard = 'unnamedplus'`, yanks/pastes use the system clipboard
automatically — no need for `"+y` / `"+p`. The `"+` register stays available for explicit use.

## Ex commands

### Files

| command | action |
| --- | --- |
| `:w` / `:w <name>` | write / save as |
| `:q` / `:q!` | quit / quit without saving |
| `:wq` or `:x` | save and quit |
| `:e <file>` / `:e!` | open file / reload current, discarding changes |

### Substitution

| command | action |
| --- | --- |
| `:s/old/new/` | replace first match on current line |
| `:s/old/new/g` | replace all on current line |
| `:%s/old/new/g` | replace all in buffer |
| `:%s/old/new/gc` | confirm each replacement |

Live preview appears in a split (`inccommand = 'split'`) as you type.

### Windows / splits / tabs / buffers

| command | action |
| --- | --- |
| `:sp <file>` / `:vsp <file>` | horizontal / vertical split |
| `<C-w><c>` | window command prefix (e.g. `<C-w>=` to balance splits) |
| `:tabnew <file>` / `gt` / `gT` | new tab / next / previous tab |
| `:bn` / `:bp` / `:bd` / `:ls` | next / previous / delete / list buffers |

This config remaps split focus to `<C-h/j/k/l>` (no `<C-w>` prefix) — see *Windows & buffers*
below.

---

## Config-specific (kickstart-style)

> Everything below assumes a kickstart-based config. Bindings will differ in yours — use
> `<leader>sk` to discover what's actually mapped.

### Visual indicators

**Sign column** (kept always-visible via `signcolumn = 'yes'`) holds git change indicators and
LSP diagnostic markers. Git signs compare against the index (your last commit): `+` added, `~`
modified, `_` deleted below, `‾` deleted above. LSP diagnostics show severity letters
(`E` `W` `I` `H`) or nerd-font icons.

**listchars** (`vim.o.list = true`): `»` tab, `·` trailing space, `␣` non-breaking space.

**Cursor:** current line highlighted (`cursorline`); yanked region briefly flashes
(`vim.hl.on_yank()`).

**Numbers:** absolute on; uncomment `vim.o.relativenumber = true` if `10j`/`5k` jumping is in
the muscle memory.

### Searching (telescope, `<leader>s*`)

| keys | action |
| --- | --- |
| `<leader>sf` | search [f]iles in cwd |
| `<leader>sg` | search by live [g]rep |
| `<leader>sw` | search current [w]ord under cursor |
| `<leader>s.` | search recent files |
| `<leader>s/` | live grep in open buffers only |
| `<leader>/` | fuzzy find within current buffer |
| `<leader>sk` | search [k]eymaps — discovery escape hatch |
| `<leader>sh` / `<leader>sd` / `<leader>sc` | search help tags / diagnostics / commands |
| `<leader>sr` | [r]esume last picker |
| `<leader>sn` | search neovim config files |
| `<leader><leader>` | find existing buffers |

Inside a picker, `<C-/>` (insert) or `?` (normal) shows its keymaps.

### Windows & buffers

| keys | action |
| --- | --- |
| `<C-h>` / `<C-l>` / `<C-j>` / `<C-k>` | focus left / right / lower / upper split |
| `<leader><leader>` | jump to an existing buffer |

Splits open right and below (`splitright`, `splitbelow`).

### LSP (when a server is attached)

The `gr*` prefix is the LSP action group — press `gr` and pause for the which-key menu.

| keys | action |
| --- | --- |
| `grd` / `grD` | goto definition / declaration |
| `grr` / `gri` / `grt` | references / implementation / type definition |
| `grn` / `gra` | rename (across files) / code action |
| `gO` / `gW` | document outline / workspace symbols |
| `<C-t>` | jump back from a goto |
| `[d` / `]d` | previous / next diagnostic |
| `<leader>q` | diagnostics → quickfix list |
| `<leader>th` | toggle inlay hints |
| `<leader>f` | format buffer (conform.nvim, or LSP fallback) |

`:checkhealth vim.lsp` tells you what's running.

### Completion (blink.cmp, insert mode)

| keys | action |
| --- | --- |
| `<C-n>` / `<C-p>` | next / previous candidate |
| `<C-y>` / `<C-e>` | accept / close the menu |
| `<C-space>` | open menu, or open docs for current item |
| `<C-b>` / `<C-f>` | scroll the docs panel |
| `<C-k>` | toggle signature help |
| `<Tab>` / `<S-Tab>` | snippet placeholder navigation |

### Text objects (mini.ai)

| pattern | meaning |
| --- | --- |
| `va)` / `vi)` | select around / inside `)` |
| `ci'` | change inside `'` |
| `aa` / `ii` | around / inside the *next* match |

### Surround (mini.surround)

| keys | action |
| --- | --- |
| `sa{motion}{char}` | add — `saiw)` wraps inner word in parens |
| `sd{char}` | delete — `sd'` removes surrounding quotes |
| `sr{old}{new}` | replace — `sr)'` swaps parens for quotes |
| `sf{char}` / `sF{char}` | find right / left |

Append `n` / `l` for next / previous match.

### Comments

`gc` is the comment operator (built in to 0.10+): `gcc` toggles the line, `gc{motion}` over a
motion (`gcap` a paragraph), `gc` in visual over the selection. Syntax is per-filetype via
`commentstring`.

### File tree (neo-tree)

`\` opens neo-tree and reveals the current file (and closes it when focused). Inside: `<CR>`/`o`
open, `a` add (trailing `/` for a dir), `d` delete, `r` rename, `c` copy, `m` move, `H` toggle
hidden, `?` full keymap, `q` close.

### Terminal

`:term` opens a terminal buffer; `<Esc><Esc>` exits terminal mode (custom mapping).

---

## Discovery — finding what isn't on this sheet

- `<leader>sk` — fuzzy search every defined keymap with its description
- `<leader>sh` — fuzzy search `:help` tags
- `<leader>sc` — fuzzy search available commands
- press `<leader>` and pause — which-key shows what's available at any prefix
- `:checkhealth` — full system report when something misbehaves
- `:Mason` — manage installed LSPs / formatters / linters
- `:Tutor` — interactive vim refresher

## Further reading
- [Neovim docs](https://neovim.io/doc/) · [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim) · `:Tutor`
