---
type: cheatsheet
area: "Networking & Protocols"
aliases: [ssh config, ~/.ssh/config, ssh-config]
tags: [remote, networking, crypto, config]
status: working
---

# ssh_config

> **Area:** [[Networking & Protocols]]

The client-side SSH configuration file — `Host`/`Match` blocks, the directives worth knowing,
connection multiplexing, and how to debug what actually gets applied. Split out of [[ssh]] as
the config file grew past "one example block." Server-side `sshd_config` is a different file
with different directives — see [[SSH Server Hardening]].

---

## 1. Files and precedence

```bash
~/.ssh/config              # per-user config, read first
/etc/ssh/ssh_config        # system-wide defaults, read second
```

**First match wins, per parameter** — not per block. If two `Host` blocks both match a
connection and both set `Port`, the *first* one in the file is used; a later block can still
supply a *different* parameter (like `User`) that the first block didn't set. This is the
opposite of most config formats (where later overrides earlier) and the single most common
source of "I changed it but nothing happened."

Consequence: put **specific hosts first, wildcards and `Host *` defaults last**.

```bash
chmod 600 ~/.ssh/config    # sshd/ssh itself will ignore a world/group-writable config
```

---

## 2. Host patterns

```sshconfig
Host myserver               # exact match — the alias you type: ssh myserver
Host *.internal              # glob — matches anything.internal
Host 10.0.*.*                 # globs work on IPs too
Host staging-* !staging-old  # multiple patterns; leading ! excludes a match
Host *                        # matches everything — use for global defaults, put LAST
```

`Host` is the pattern matched against what you typed on the command line, not the real
hostname — that's what `HostName` is for (§3).

---

## 3. Core directives

```sshconfig
Host myserver
    HostName 203.0.113.10        # the real address/DNS name to connect to
    User you                     # remote login name
    Port 2222                    # non-default port
    IdentityFile ~/.ssh/id_ed25519   # which key to offer
    IdentitiesOnly yes           # offer ONLY IdentityFile, not everything in the agent
```

`IdentitiesOnly yes` matters once you have more than one key loaded: without it, ssh offers
every key in the agent in turn, and a server with lenient logging or a low `MaxAuthTries` can
reject you before it ever tries the right one.

---

## 4. Jump hosts and proxies

```sshconfig
Host bastion
    HostName bastion.example.com
    User you

Host *.internal
    ProxyJump bastion            # hop through 'bastion' transparently

# Older/alternative form — spawns a command to pipe the connection through
Host oldstyle
    ProxyCommand ssh -W %h:%p bastion
```

`ProxyJump` (OpenSSH 7.3+) is the modern replacement for `ProxyCommand ... -W`; prefer it
unless you're stuck on an ancient client.

---

## 5. Connection keepalive and multiplexing

```sshconfig
Host *
    ServerAliveInterval 60       # ping the server every 60s so NAT/firewalls don't drop idle conns
    ServerAliveCountMax 3        # give up after 3 missed pings

    ControlMaster auto           # reuse one TCP connection for multiple sessions to the same host
    ControlPath ~/.ssh/sockets/%r@%h-%p   # the shared socket; mkdir ~/.ssh/sockets first
    ControlPersist 10m           # keep the master connection alive 10min after the last session closes
```

Multiplexing makes every `ssh`/`scp`/`rsync` to a host you're already connected to skip the
TCP+auth handshake — the difference is dramatic over high-latency links (VPNs, satellite,
distant regions). `%r`/`%h`/`%p` expand to remote user / host / port so each destination gets
its own socket.

```bash
# Inspect / tear down a multiplexed connection
ssh -O check myserver        # is the master running?
ssh -O exit myserver         # close it
```

---

## 6. Agent and forwarding

```sshconfig
Host *
    AddKeysToAgent yes           # ssh-add a key into the agent the first time it's used

Host trusted-jumpbox
    ForwardAgent yes             # let THAT host use your local agent's keys to hop further
```

**`ForwardAgent yes` is a trust decision, not a convenience toggle.** Anyone with root on the
forwarded-to host can use your agent (and thus your keys) for as long as you're connected —
scope it to specific `Host` blocks you actually trust, never `Host *`.

---

## 7. Host key checking

```sshconfig
Host *
    UserKnownHostsFile ~/.ssh/known_hosts
    StrictHostKeyChecking ask    # default: prompt on an unknown key (leave this alone)

Host ephemeral-ci-runner-*
    StrictHostKeyChecking no     # ONLY for genuinely disposable/ephemeral hosts
    UserKnownHostsFile /dev/null
```

Turning off strict host key checking removes MITM protection. It's occasionally reasonable for
throwaway CI runners or containers that get a fresh host key every boot — never for anything
that holds real data or credentials.

---

## 8. Match blocks (conditional config)

```sshconfig
# Only apply when NOT already inside a tmux/ssh session on this host
Match host myserver exec "test -z \"$TMUX\""
    RemoteCommand tmux new-session -A -s main

# Apply different settings based on the local network
Match host *.internal exec "ping -c1 -W1 10.0.0.1 >/dev/null 2>&1"
    ProxyJump none                # on the internal network already — skip the jump host
```

`Match` tests conditions (`host`, `user`, `exec`, `localuser`, ...) rather than just matching
the typed alias like `Host` does — use it when the right config depends on *where you are*, not
just *what you typed*.

---

## 9. Splitting the file

```sshconfig
# ~/.ssh/config
Include ~/.ssh/config.d/*.conf   # pull in per-project/per-client files; must come before use
Include ~/.ssh/config.d/work.conf

Host *
    AddKeysToAgent yes
```

`Include` lets you keep one file per client/project under `~/.ssh/config.d/` instead of one
sprawling file — handy when hosts are added/removed by a script or synced separately.

---

## 10. Debugging effective config

```bash
# The single most useful command here: shows the FINAL merged config for a host,
# exactly as ssh will apply it (all files, all Match/Host blocks resolved).
ssh -G myserver

ssh -vv myserver        # -v/-vv/-vvv: verbose connection log (which key/method was tried, why it failed)
```

`ssh -G` answers "why isn't my config taking effect" faster than reading the file by hand —
it shows the resolved value of every directive, so a shadowed `Port` or an unintended
`IdentitiesOnly` jumps out immediately.

---

## Daily workflows

### "New server, want to just type `ssh name`"
```sshconfig
Host name
    HostName 203.0.113.10
    User you
    IdentityFile ~/.ssh/id_ed25519
```

### "Everything behind a bastion, one line each"
```sshconfig
Host bastion
    HostName bastion.example.com
    User you

Host *.internal
    ProxyJump bastion
```

### "Confirm what ssh will actually do before connecting"
```bash
ssh -G myserver | grep -E '^(hostname|port|user|proxyjump|identityfile) '
```

### "Speed up repeated connections to the same host"
```sshconfig
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 10m
```
```bash
mkdir -p -m 700 ~/.ssh/sockets   # ControlPath needs the directory to exist first
```

---

## Files & locations

| Path | What |
| --- | --- |
| `~/.ssh/config` | per-user client config (read first) |
| `/etc/ssh/ssh_config` | system-wide client defaults (read second) |
| `~/.ssh/config.d/*.conf` | optional split-out files, pulled in via `Include` |
| `~/.ssh/sockets/` | `ControlMaster` sockets (create it, mode 700) |
| `~/.ssh/known_hosts` | host key fingerprints — see [[ssh]] §6 for troubleshooting |

---

## Gotchas / Golden rules

1. **First match wins, per parameter — not per block.** Specific `Host` entries go at the top,
   `Host *` defaults go at the bottom. A later block can still fill in a parameter the earlier
   match left unset.
2. **`chmod 600 ~/.ssh/config`.** A group/world-writable config file is silently ignored (or
   refused, depending on version) by ssh.
3. **`ssh -G host` before you debug by eye.** It shows the fully resolved config; reading
   `Host`/`Match` blocks by hand to predict precedence is error-prone.
4. **`IdentitiesOnly yes` once you have more than one key.** Otherwise ssh tries every agent
   key against every host, which can trip auth-attempt limits before the right key is offered.
5. **`ForwardAgent yes` is a trust decision.** Scope it to specific hosts, never `Host *`.
6. **`ControlPath`'s directory must exist before use** — ssh will not create
   `~/.ssh/sockets/` for you.

## Further reading
- [ssh_config(5)](https://man.openbsd.org/ssh_config)
