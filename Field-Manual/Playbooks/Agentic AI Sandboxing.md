---
type: playbook
area: "Linux Administration"
aliases: ["AI Agent Containment", "Agent Sandboxing", "Coding Agent Sandboxing"]
tags: [ai, llm, agents, sandboxing, security, hardening, containment]
status: working
---

# Agentic AI Sandboxing

> **Area:** [[Linux Administration]]

How to contain an autonomous LLM agent — coding agent, notes agent, research agent — so that prompt injection and hostile code are *survivable events*, not incidents. Covers boundary design, profile selection, and adversarial verification. Deliberately not covered: model choice, prompt engineering, alignment.

> Vendor-agnostic by design. Concrete config examples use Claude Code's sandbox/permission vocabulary (see [[claude-code]]) because the seeded profiles were built and verified on it; every control here has an equivalent in other agent runtimes — or a gap you need to name.

## Situation

- You are about to give an LLM agent a shell, file tools, or web access on a machine you care about, **or**
- An existing agent deployment needs a posture review after a scope change: new tools, new data sources, more autonomy, or a new MCP server.

---

## First principles (read before branching)

Eight rules that hold for every profile below. Everything after this section is these rules applied.

1. **Assume injection succeeds.** An agent that reads attacker-influenceable content — a web page, an email, a package README, an issue comment, even a filename — will eventually follow instructions embedded in it. LLMs cannot reliably distinguish instruction from data; that is a property of the architecture, not a bug that patches out. Don't design for "the agent won't obey"; design so that *obedience is survivable*. Plan every boundary as if the agent were the attacker's, because under injection it is.

2. **Name the lethal trifecta, then break a leg.** Private data + exposure to untrusted content + the ability to communicate externally = an exfiltration machine waiting for its instruction. Every profile below is a different choice of *which leg to remove*: the dirty workshop removes the private data, the curator removes (most of) the egress, the chat-only fallback removes the tools. If a design keeps all three legs, it is not a design, it is a countdown. (A useful softer rule of thumb — the "rule of two": pick at most two of *untrusted input*, *sensitive access*, *ability to change state or communicate out*, or accept that a human must approve every consequential action.)

3. **Two boundaries, two jobs — never conflate them.** The *outer* boundary (VM/hypervisor, VLAN, firewall rules) exists to stop **lateral movement** into the rest of your estate. The *inner* boundary (the agent runtime's own sandbox: filesystem scope, syscall filter, network allowlist) exists to stop **exfiltration** and contain the process. They fail differently, they're configured in different places, and one is not a substitute for the other. A box with broad WAN egress by design makes the inner domain allowlist your *actual* exfil control, not a nicety. And because in-box sandboxes have been escaped in the wild (an agent bypassing its own denylist via `/proc/self/root/...`, then disabling its own sandbox to finish the task), the outer boundary is the one you ultimately trust.

4. **Every tool has an enforcement plane — fence in the right one.** OS-level sandboxes (bubblewrap/Seatbelt/Hyper-V, network proxies) typically constrain *shell subprocesses only*. The agent's first-party tools — file read/write, web fetch, web search — often go through an application-layer permission system and **never touch the OS sandbox**. A path denied in the sandbox config can still be read by the file tool; an empty sandbox network allowlist does not gate the fetch tool. Two rule namespaces, two enforcement planes: put every fence in the plane its tool actually traverses, and put **secret fences in both** (the double-deny). Verify empirically per tool — docs lag behavior.

5. **The policy must sit outside the agent's write set.** Managed/system-scope config owned by root, hook scripts owned by root, agent's own settings directory hard-denied for writes. If the agent can edit its fence, there is no fence — self-modification is a standard escape ("disable the sandbox to finish the task" is a *reasoning step*, not malice).

6. **Gates fail closed.** Any custom gate (pre-tool-use hook, proxy filter) must emit an explicit deny on parse errors, unexpected input, or its own failure — never fall through to allow. Hostname extraction is a security boundary: parse URLs with a real parser (userinfo tricks like `https://good.example@evil.example/` defeat string matching), lowercase, strip trailing dots, then suffix-match.

7. **Blast radius is a budget; undo is a control.** Decide up front what a total compromise of the agent costs you, and make that cost payable: workspace on a snapshot you roll back rather than repair, documents in git so vandalism is a `git revert`, credentials so scoped and short-lived that rotation is a non-event. "Cattle, not pets" is a security property here, not just ops hygiene.

8. **Silence is the alarm.** Managed policy files typically load silently or not at all — a filename typo voids the whole policy with no error. Verification commands that signal success by *speaking* (`/status` listing the policy source, `git check-ignore` printing the name) signal failure by silence. Check after every policy edit; never assume.

---

## Quick assessment

Four questions decide the profile:

```text
Q1  Does the agent run untrusted code?        # dep trees, postinstall scripts, cloned repos
Q2  Are secrets co-resident with the agent?   # SSH keys, password DBs, VPN configs, its own token
Q3  How much egress does the job need?        # broad WAN (builds) vs. a fixed doc allowlist vs. none
Q4  Is the workspace disposable?              # snapshot-rollback vs. durable-but-versioned
```

| Profile | Untrusted code | Secrets nearby | Egress | Workspace |
|---|---|---|---|---|
| **P1 — dirty workshop** | yes — that's the job | **none, by construction** | broad WAN, zero lateral | disposable (snapshot) |
| **P2 — curator** | no — trusted tooling only | yes — daily driver | minimal fixed allowlist | durable, git-versioned |
| **P3 — vendor-hosted sandbox** | maybe | vendor-side / brokered | vendor policy | ephemeral per session |
| **P4 — desktop copilot / computer use** | no | yes — the whole desktop | whatever the browser reaches | your real environment |

**The golden rule of profile selection:** if you answered *yes* to both Q1 and Q2, **split the workload across two machines/profiles**. There is no configuration that safely runs untrusted code next to your secrets — the profiles exist precisely so you never have to.

Note the inversion between the two archetypes: P1 gives the agent *maximum agency inside a sterile cell*; P2 gives it *minimum agency inside a valuable environment*. Most real deployments are one of these two; drift between them (a "quick build" on the curator box, a password manager installed in the workshop) is how postures rot.

---

## Fix P1 — the dirty workshop (hands-off coding agent, hostile code, sterile cell)

The box's *job* is to run hostile code: supply-chain payloads in dependency trees, and a capable agent that — under injection — will try to exfil or pivot. You do not try to make the code trustworthy; you make the cell sterile and the walls real.

**Threat model:** (a) lateral movement into your infra; (b) exfiltration of source/data; (c) wrecked workspace; (d) privilege escalation. **Not defended:** the code being wrong or malicious per se — that's accepted as the workload.

### 1. Outer boundary — a real VM on its own segment

```text
- Full VM (KVM/HVM), not a container/LXC: you want a kernel boundary under
  the in-box sandbox, and unprivileged containers often force the nested
  sandbox into a degraded mode (bwrap can't mount a fresh /proc).
- Own VLAN/segment. Firewall policy, first-match top-down:
    pass   agent-net -> <public resolvers>:53,853   # pin two public resolvers;
                                                    # never your internal resolver
    block  agent-net -> RFC1918 (all of 10/8, 172.16/12, 192.168/16)  # log it
    pass   agent-net -> any                         # broad WAN is fine BELOW the block
- The RFC1918 block must sit ABOVE the pass-any, or the pass shadows it.
  You are filtering destination, not next-hop.
- Inbound: SSH only, only from your admin subnet. The box initiates nothing inward.
- Keep it OFF the monitoring/trust spine (no agent enrolled in your SIEM/EDR mesh
  with credentials that reach back) — liveness pings at most.
```

### 2. Inner sandbox — a hard gate, not a suggestion

Deliver the agent's sandbox policy as **managed settings** (system scope, root-owned) so the agent and the user account can't loosen it:

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,          // missing deps => refuse to start, not "warn and run naked"
    "allowUnsandboxedCommands": false,  // no escape hatch: commands run sandboxed or not at all
    "filesystem": {
      "allowWrite": ["/home/<worker>/projects", "/tmp"],
      "denyRead":  ["/home/<worker>/.ssh", "<agent credential file>", "<git credential store>"]
    },
    "network": {
      "allowedDomains": ["<registry domains>", "<vcs domains>", "<vendor api domains>"]
    }
  }
}
```

- The **domain allowlist is the exfil control** (principle 3). Keep entries specific — `*.example-registry.org`, not `*`. Remember TLS is not inspected: even a code-hosting domain is an exfil path, which is why the *real* mitigation is that nothing worth stealing is on the box.
- **Two network messages = two enforcement points.** "Blocked by network allowlist" = the in-sandbox deny working. "Network request outside of sandbox" = a command that *left* the sandbox (backgrounded, excluded) asking permission — and bypassing the allowlist entirely. Keeping the agent inside the sandbox is a security property, not a UX preference; steer with the project instructions file.

### 3. The worker account

```bash
useradd -m <worker>                 # dedicated user: agent + toolchain + fixtures
# NO sudo, NO membership beyond its own group, NO infra keys in ~/.ssh
sudo -l -U <worker>                 # verify: "not allowed" (run as admin; `sudo -ln` as the user lies)
```

Admin (you) and worker (the agent) are different users; maintenance happens over SSH as admin, never as the worker.

### 4. Credentials — scoped, short-lived, denied to the agent's readers

- Push access via a **repo-scoped fine-grained token** (contents:read/write on one repo, short expiry), stored in a credential store whose path is in `denyRead`.
- **Branch-protect main** — the agent opens PRs; it never pushes to main. Review is your injection filter.
- Real secrets (infra keys, password DBs) are simply *not on the box*. If a fixture needs a password, generate a throwaway one for the fixture.
- Dev services (test servers, fixture daemons) bind **loopback only**; you reach them over an SSH tunnel. Never `--host 0.0.0.0` — loopback + tunnel *is* the containment.

### 5. Cattle discipline

```text
- Snapshot after provisioning ("clean-base") and after workspace setup ("project-ready").
- Git remote is canonical for anything worth keeping; the box itself is backed up by NOTHING.
- Compromise response = rollback, not forensics. Roll back, rotate the one scoped token, move on.
```

---

## Fix P2 — the curator (low-agency agent, trusted tooling, co-resident secrets)

The inverted threat model: the tooling is trusted, but the agent lives on your daily driver next to everything valuable — SSH keys, password manager, VPN configs, its own OAuth token. The risk is the agent, under injection from note/page content, **reading a secret and leaking it without any shell at all**.

**Threat model:** (a) secret reads via *any* tool; (b) exfil without shell — a fetch tool leaks data in the query string of a GET to any reachable domain (the payload lands in that server's access logs regardless of response); a search tool leaks the query text to the search backend and can't be domain-scoped at all; (c) self-modification of policy; (d) content vandalism. **Not defended:** untrusted toolchains — that class of work belongs on P1.

### 1. Kill tool classes outright

```text
- Deny the shell entirely. Document editing needs grep/read/edit/write tools, not bash.
  Nothing can leave a sandbox it never enters — this deletes the whole
  "command escaped the sandbox" failure class from P1.
- Deny web search. It is a second, independent exfil channel that no domain
  allowlist can scope.
- Drive git yourself, outside the agent. If you ever carve out a shell, allow
  content-scoped read-only commands (git status/diff/log) — never push — and
  remember the moment a shell exists, all P1 shell-side fences become load-bearing again.
```

### 2. The per-plane double-deny (principle 4 in practice)

Every credential surface appears **twice** — once per enforcement plane:

```json
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["/home/<user>/.ssh", "/home/<user>/.gnupg",
                   "<password-db paths>", "<vpn config>", "<agent settings dir>"]
    }
  },
  "permissions": {
    "deny": [
      "Bash", "WebSearch",
      "Read(//home/<user>/.ssh/**)", "Read(//home/<user>/.gnupg/**)",
      "Read(//home/<user>/**/*.kdbx)", "Read(<agent settings dir>/**)",
      "Edit(<agent settings dir>/**)", "Write(<agent settings dir>/**)"
    ],
    "allow": ["Edit(//home/<user>/<workspace>/**)", "Write(//home/<user>/<workspace>/**)"]
  }
}
```

- The permission-plane denies are the **load-bearing half**: the sandbox `denyRead` does *not* stop the first-party Read tool. Keep the sandbox half anyway (defense in depth, and it's already standing if a shell carve-out ever lands).
- **Absolute paths only** — `~`-expansion mismatches are a known rule-matching failure mode.
- The allows on the workspace keep in-scope edits prompt-free; everything outside still prompts. Ergonomics matter: a profile that nags constantly gets disabled.

### 3. The fail-closed web gate

Gate the fetch tool with a **pre-tool-use hook** (root-owned script), not permission rules, when the permission layer's handling of web tools is the buggy part — hooks fire *upstream* of permission evaluation. The gate enforces a small fixed allowlist of documentation domains:

```python
#!/usr/bin/env python3
# Fail-closed pre-tool-use gate: fetch-domain allowlist + search deny.
import json, sys
from urllib.parse import urlsplit

ALLOWED = ("rfc-editor.org", "ietf.org", "nist.gov", "kernel.org", "man7.org",
           "wikipedia.org")          # suffix-match: entry covers itself + subdomains

def emit(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))
    sys.exit(0)

try:
    data = json.load(sys.stdin)
    if data.get("tool_name") == "WebSearch":
        emit("deny", "search is an unscopeable exfil channel on this profile")
    if data.get("tool_name") != "WebFetch":
        sys.exit(1)                                    # not our tool -> normal flow
    host = (urlsplit(data.get("tool_input", {}).get("url", "")).hostname or "").lower().rstrip(".")
    if not host:
        emit("deny", "unparseable URL")
    if any(host == d or host.endswith("." + d) for d in ALLOWED):
        emit("allow", f"{host} on allowlist")
    emit("deny", f"{host} not on allowlist")
except SystemExit:
    raise
except Exception as exc:
    emit("deny", f"gate failing closed ({type(exc).__name__})")   # principle 6
```

Dry-run it *outside* the agent before trusting it — one allowed case, one denied, the userinfo trick (`https://wikipedia.org@evil.example/`), and malformed stdin. Expected: allow / deny / deny-as-`evil.example` / deny.

### 4. Undo and residual risk

```text
- The workspace is a git repo. Injection-driven vandalism is a `git revert`, not a loss.
- Residuals you ACCEPT by name, not by omission:
  * a GET to an allowlisted domain can still carry content in the query string —
    the allowlist shrinks the audience to operators you tolerate, it doesn't zero the channel;
  * user-editable allowlisted sites (wikis) are an injection source — blast radius
    is vault edits (revertable) and fetches to other allowlisted domains;
  * the ultimate mitigation is P1's: the agent can't read anything worth stealing.
```

---

## Fix P3 — vendor-hosted execution (the sandbox is someone else's)

Remote agent sessions run the loop and code execution on the vendor's infrastructure. You are not configuring the boundary; you are **verifying trust delegation**. The checklist:

```text
- Per-session isolation: fresh sandbox per session, destroyed after, no cross-tenant state.
- Egress enforced OUTSIDE the sandbox: mandatory proxy the sandboxed code can't
  reconfigure; allowlisted destinations only; no reach into private/link-local/
  metadata addresses (no pivot into your network).
- Credential handling: session-scoped short-lived tokens only inside the sandbox;
  connector/OAuth tokens stay server-side, never enter the execution environment.
- The reach-back path: what can a remote session touch on YOUR device (files,
  browser)? Only brokered, only connected folders, only while your client is online?
- What it does NOT cover: local MCP servers and desktop tools still run on your
  machine under app-layer permissions — the vendor VM does not contain them.
- Your TCB now includes the vendor. Write that down (see Trusted Computing Base
  in the dictionary); if your compliance posture needs endpoint visibility,
  note that EDR cannot see inside either their sandbox or a local agent VM.
```

## Fix P4 — desktop copilot / computer use (there is no sandbox)

When an agent drives your actual desktop — screen, mouse, browser profile — it runs **inside your trust boundary** with whatever you can reach. There is no meaningful technical containment; the approval prompt is the entire boundary.

```text
- Treat it as P2's threat model with the fences removed: everything on screen,
  in the clipboard, and in logged-in browser sessions is readable and sendable.
- Scope sessions: dedicated browser profile, logged out of anything the task
  doesn't need; password manager LOCKED during sessions.
- Never combine with unattended operation. Human-in-the-loop is the control —
  if you wouldn't watch it, don't run it.
- Prefer promoting the workload to P1/P2/P3 whenever the task allows.
```

---

## Verification — the adversarial checklist

A profile you haven't attacked is a hypothesis, not a control. After every policy change, *be the injection*:

- [ ] **Policy loaded:** the agent's status output lists the managed policy file; local override attempts report "overridden by higher-priority configuration". Silence = failure (principle 8).
- [ ] **Secret fence, per plane:** ask the agent to read a canary file in each protected path *via its file tool* (this is the test the OS-plane deny alone would pass wrongly), and — where a shell exists — via `cat`.
- [ ] **Shell denial (P2):** ask it to run `ls` → denied at the permission layer, no prompt.
- [ ] **Exfil, in-sandbox (P1):** foreground `curl` to an off-list domain → blocked-by-allowlist message; on-list passes.
- [ ] **Exfil, out-of-sandbox (P1):** backgrounded/excluded command triggering a network prompt → you understand which message you're looking at, and the answer is no.
- [ ] **Lateral (P1):** `nc -zv <internal-ip> 22` (and your management ports) from the box → blocked; WAN fetch still works.
- [ ] **Gate behavior (P2):** on-list fetch passes without prompt; off-list denies with reason; userinfo-trick URL denies as the *real* host; search denies; `chmod -x` the hook → falls back to prompting, not silent allow.
- [ ] **Self-modification:** ask the agent to append to its own settings/hook → denied in every plane.
- [ ] **Hard gate (P1):** remove/rename the sandbox binary → agent refuses to run commands rather than running them unsandboxed.
- [ ] **Undo drill:** scribble via the agent; `git diff` shows it; revert works. Snapshot rollback restores pristine (P1).
- [ ] **Privilege:** `sudo -l -U <worker>` → not allowed; worker's groups are only its own.

## Escalation / after-action — suspected injection incident

1. **Stop the session** — don't argue with the model; every further turn executes attacker context.
2. **Preserve the transcript** and the offending content (page, note, README) — that's your IOC.
3. **Diff everything writable:** `git status && git diff` in every workspace the agent can write; check the policy/hook files' mtime+ownership even though they're root-owned.
4. **Rotate anything readable:** every credential within the agent's actual read set (per plane!) is presumed leaked — the scoped-PAT design makes this one revocation, which is the point.
5. **Roll back** the workspace/VM snapshot rather than spot-cleaning.
6. **Write the after-action into the runbook**: which leg of the trifecta was standing, which plane the fence was missing from, and the new verify-step that would have caught it.

## Gotchas / golden rules

- **First-party tools bypass the OS sandbox** — the single most load-bearing fact in this playbook. Fence per plane; secrets in both planes; verify per tool.
- **Backgrounded and excluded commands leave the sandbox** — and with it, the network allowlist. Two different block messages = two different enforcement points; learn to read them.
- **A managed-policy typo voids the whole file silently.** The status output is the only truth.
- **Argument-pattern denies are not fences.** Blocking `curl`/`wget` by command pattern is trivially bypassed (`sh -c`, aliases, any interpreter); use plane-appropriate denies and network policy instead.
- **TLS is not inspected by domain allowlists.** The proxy allows by client-supplied hostname; broad entries (code-hosting domains) remain exfil paths. Specific entries + nothing-worth-stealing beats clever filtering.
- **In-box sandboxes get escaped.** `/proc` tricks, self-disabling, deps silently missing. That's why P1 has a VM and a firewall under it — the inner sandbox is depth, not the boundary.
- **Ergonomics are security.** A profile that prompts on every legitimate action trains you to approve reflexively — scope the allows so the *normal* workflow is silent and only the abnormal prompts.
- **Postures rot by drift, not by breach.** Re-run the verification checklist when tools, MCP servers, data sources, or autonomy change — not on a calendar.

## Further reading

- [Simon Willison: The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) — the trifecta framing; his [prompt injection series](https://simonwillison.net/series/prompt-injection/) is the canonical running literature.
- [Claude Code: sandboxing documentation](https://code.claude.com/docs/en/sandboxing) — the enforcement-plane split (Bash sandbox vs. first-party permission system), managed settings, network proxy limits.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — prompt injection, insecure output handling, excessive agency as a named risk class.
- [bubblewrap](https://github.com/containers/bubblewrap) — the unprivileged sandboxing primitive under most Linux agent sandboxes.
