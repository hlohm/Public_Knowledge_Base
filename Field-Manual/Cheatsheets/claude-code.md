---
type: cheatsheet
area: "CLI Tools"
aliases: [claude, claude code, claude cli]
tags: [ai, claude, cli, llm, tools]
status: stable
---

# claude-code

> **Area:** [[CLI Tools]]

Claude Code is Anthropic's official CLI for Claude — an interactive coding agent that can read, write, and execute code in your project, run shell commands, search the web, and maintain memory across sessions. Runs in your terminal against the current working directory.

---

## 1. Invocation

```sh
# Start an interactive session in the current directory
claude

# Start with an initial prompt (goes straight to work)
claude "explain the architecture of this repo"

# Continue the last conversation
claude --continue
claude -c

# Non-interactive: print the response and exit (scriptable)
claude --print "summarize CHANGELOG.md in 3 bullets"
claude -p "what does this script do?" < script.sh

# Specify a model
claude --model claude-opus-4-8
claude --model claude-haiku-4-5-20251001

# Output format for scripting
claude -p "list TODOs" --output-format json
claude -p "list TODOs" --output-format stream-json   # streaming

# Limit agentic turns (prevents runaway loops)
claude --max-turns 5 "refactor the auth module"

# Resume a specific prior conversation by session ID
claude --resume <session-id>
```

## 2. Slash commands

Typed at the prompt during an interactive session:

| Command | What it does |
|---|---|
| `/help` | Show available commands and keyboard shortcuts |
| `/clear` | Clear conversation history and start fresh |
| `/compact` | Summarise the conversation to free context window space |
| `/cost` | Show token usage and cost for the current session |
| `/model` | Switch model mid-session |
| `/fast` | Toggle Fast mode (Opus with faster output) |
| `/init` | Analyse the repo and create or update `CLAUDE.md` |
| `/memory` | View and manage persistent memory files |
| `/review` | Review the current branch diff (see also: `ultra` variant below) |
| `/exit` | End the session (also: `Ctrl+D`) |

### /code-review

```
/code-review ultra            # multi-agent cloud review of current branch
/code-review ultra <PR#>      # review a specific GitHub PR number
```

## 3. Keyboard shortcuts

| Key | Action |
|---|---|
| `Enter` | Submit message |
| `Shift+Enter` | Insert newline without submitting |
| `Escape` | Cancel the current tool call or generation |
| `Ctrl+C` | Interrupt (cancel running command) |
| `Ctrl+D` | Exit the session |
| `↑` | Recall previous message from history |

## 4. Shell passthrough

Prefix a command with `!` to run it in your shell and inject the output into the conversation:

```
! git log --oneline -10
! cat /etc/os-release
! npm test 2>&1 | tail -20
```

This is useful for feeding command output to Claude without copy-pasting, and for running commands that require interactive login (e.g., `! gcloud auth login`).

## 5. CLAUDE.md — project instructions

Claude Code reads `CLAUDE.md` from the repo root (and any parent directories up to `~/`) at the start of every session. Use it to:

- Tell Claude about the project architecture, build commands, and test commands
- Define conventions (naming, style, commit format)
- Set hard rules ("never commit to main directly", "no real secrets")
- Add tool-specific context that isn't obvious from the code

```sh
# Let Claude generate an initial CLAUDE.md from the repo
claude
> /init

# CLAUDE.md locations (all are loaded, deeper = higher priority)
~/.claude/CLAUDE.md          # global (all projects)
~/projects/CLAUDE.md         # parent directory
~/projects/myrepo/CLAUDE.md  # project root  ← most common
```

Inline `@filename` in CLAUDE.md to import another file's contents into context:
```markdown
@docs/architecture.md
@CONTRIBUTING.md
```

## 6. Settings

```sh
# Per-user settings
~/.claude/settings.json

# Per-project settings (checked into the repo)
.claude/settings.json

# Per-project local overrides (gitignored)
.claude/settings.local.json
```

Key settings fields:

```json
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "allow": ["Bash(git:*)", "Read", "Edit"],
    "deny":  ["Bash(rm -rf:*)"]
  },
  "env": {
    "ANTHROPIC_API_KEY": "sk-..."
  }
}
```

Permission strings follow the pattern `ToolName(matcher)`. Globs are supported.

## 7. MCP servers

Model Context Protocol servers extend Claude Code with additional tools (databases, APIs, services). Configure in settings:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my-org/mcp-server"],
      "env": { "API_KEY": "<key>" }
    }
  }
}
```

```sh
# Or pass on the command line
claude --mcp-server "name:/path/to/server"

# Check which MCP tools are loaded
> /tools
```

## 8. Hooks

Hooks are shell commands that run automatically on Claude Code events. Defined in `settings.json` under `"hooks"`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "echo 'About to run Bash'" }]
      }
    ],
    "PostToolUse": [...],
    "Stop": [...],
    "Notification": [...]
  }
}
```

Hook events:

| Event | Fires when |
|---|---|
| `PreToolUse` | Before any tool call — can block it by exiting non-zero |
| `PostToolUse` | After a tool call completes |
| `PreCompact` | Before conversation compaction |
| `Stop` | When Claude finishes a response turn |
| `Notification` | When Claude sends a notification |

A `PreToolUse` hook that exits with a non-zero code blocks the tool call and feeds the stdout/stderr back to Claude as an error message. Use this to enforce policies (block `git push --force`, require test runs, etc.).

## 9. Memory

Claude Code maintains a file-based memory system at `~/.claude/projects/<path>/memory/`. Memories persist across sessions and load automatically.

```sh
# View current memories
> /memory

# Ask Claude to remember something explicitly
> remember that we always use conventional commits in this repo
```

Memory files are plain Markdown with frontmatter (`type`, `description`). You can edit or delete them directly.

## 10. Non-interactive / scripting patterns

```sh
# Use in a pipeline
cat error.log | claude -p "summarise the root cause in one paragraph"

# Batch file review
for f in src/**/*.ts; do
    claude -p "does this file have any obvious security issues? file: $f" < "$f"
done

# Output JSON for further processing
claude -p "list all TODO comments in this file" --output-format json < main.py | jq '.[]'

# Use a specific model for cost control
claude --model claude-haiku-4-5-20251001 -p "add a docstring to each function" < utils.py
```

---

## Files & locations

| Path | Purpose |
|---|---|
| `~/.claude/settings.json` | Global user settings |
| `~/.claude/CLAUDE.md` | Global instructions (all projects) |
| `~/.claude/projects/*/memory/` | Persistent memory, per project |
| `.claude/settings.json` | Project-level settings (commit this) |
| `.claude/settings.local.json` | Local overrides (gitignore this) |
| `CLAUDE.md` | Project instructions (commit this) |

## Gotchas / Golden rules

1. **`CLAUDE.md` is public if committed** — treat it like code: no secrets, tokens, internal hostnames, or NDA material. It's read at session start, so keep it terse; long files waste context.
2. **`Escape` cancels the current tool call, not the whole session** — if Claude is mid-way through a chain of file edits, `Escape` stops the next tool but keeps the conversation going so you can redirect.
3. **Non-interactive mode (`-p`) does not load `CLAUDE.md` by default** — pass `--system-prompt` or pipe the file in if you need it.
4. **Hooks block on non-zero exit** — a misconfigured `PreToolUse` hook that always exits 1 will prevent Claude from using that tool at all; test hooks carefully.
5. **`/compact` does not lose your work** — it summarises conversation history but keeps the full file state; safe to run when the context window is filling up.
