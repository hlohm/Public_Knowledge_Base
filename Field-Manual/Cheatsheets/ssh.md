---
type: cheatsheet
area: Networking & Protocols
aliases: [scp, sftp]
tags: [remote, networking, crypto]
status: stable
---

# ssh

> **Area:** [[Networking & Protocols]]

Remote shell over an encrypted channel — plus the file-transfer (`scp`/`sftp`) and tunnelling
tools built on it. Covers keys, the client config that saves the most typing, the forwarding
tricks, and per-key `authorized_keys` options. Server-side hardening (`sshd_config`) lives
under [[Linux Administration]] → [[SSH Server Hardening]].

---

## 1. Connecting

```bash
ssh user@host                       # basic connection
ssh -p 2222 user@host               # non-default port
ssh -i ~/.ssh/id_ed25519 user@host  # specific identity (key) file
ssh user@host 'uptime'              # run one command and exit
ssh -v user@host                    # verbose — the go-to for debugging auth/connection
ssh -J jump@bastion user@target     # hop through a jump host (ProxyJump)
```

---

## 2. Keys

```bash
# Generate a modern key (Ed25519 preferred; comment helps you identify it later)
ssh-keygen -t ed25519 -C "you@host"

# Copy your public key to a server (appends to its authorized_keys)
ssh-copy-id user@host
# manual equivalent:
cat ~/.ssh/id_ed25519.pub | ssh user@host 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'

# Load a key into the agent (so you type the passphrase once per session)
eval "$(ssh-agent)"        # start an agent if needed
ssh-add ~/.ssh/id_ed25519
ssh-add -l                 # list loaded keys

# Fingerprint of a key (for verifying you're adding the right one)
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

Private key stays on your machine (`chmod 600`); only the `.pub` goes on servers. Passphrase-
protect private keys — the agent means you only type it once.

---

## 3. Client config (`~/.ssh/config`)

The biggest typing-saver. Define a host once, then `ssh myserver`:

```sshconfig
Host myserver
    HostName 203.0.113.10        # or a DNS name
    User you
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
```

Then: `ssh myserver`, `scp file myserver:`, `rsync ... myserver:` all use it. For jump hosts,
multiplexing, `Match` blocks, and debugging what config actually applies, see [[ssh_config]].

---

## 4. File transfer (scp / sftp / rsync)

```bash
# scp — simple copy over ssh (trailing : means "remote home")
scp file.txt user@host:/path/         # local → remote
scp user@host:/path/file.txt .        # remote → local
scp -r dir/ user@host:/path/          # recursive
scp -P 2222 file user@host:           # NOTE capital -P for port (lowercase in ssh)

# sftp — interactive file session
sftp user@host
#   sftp> put localfile      get remotefile      ls / lcd / cd      bye

# rsync over ssh — the better choice for anything nontrivial (resumable, incremental)
rsync -avz file user@host:/path/                # archive, verbose, compress
rsync -avz --dry-run dir/ user@host:/path/      # preview first
rsync -avz -e 'ssh -p 2222' dir/ user@host:/p/  # custom ssh options
```

A **trailing slash on the source** (`dir/`) copies the *contents*; without it copies the dir
itself. The classic rsync footgun.

---

## 5. Tunnels & forwarding

```bash
# Local forward: reach a remote-only service via a local port
#   "localhost:8080 on my machine → host's localhost:80"
ssh -L 8080:localhost:80 user@host
# e.g. browse a DB admin UI bound to the server's loopback:
ssh -L 5433:localhost:5432 user@dbhost     # then connect to localhost:5433

# Remote forward: expose a local service on the remote side
ssh -R 9000:localhost:3000 user@host

# Dynamic forward: a local SOCKS proxy through the server
ssh -D 1080 user@host                      # point your browser's SOCKS proxy at localhost:1080

# Add -N (no shell) -f (background) for tunnel-only sessions:
ssh -fN -L 8080:localhost:80 user@host
```

---

## 6. Troubleshooting

```bash
ssh -v user@host             # verbose; -vv / -vvv for more (read which auth method fails)
ssh-keygen -lf ~/.ssh/id_ed25519.pub    # confirm which key you're offering

# "REMOTE HOST IDENTIFICATION HAS CHANGED" — host key changed (reinstall? or MITM)
ssh-keygen -R host           # remove the stale known_hosts entry, then reconnect & verify

# Permission denied (publickey):
#   - is the key in the agent?           ssh-add -l
#   - right key for this host?           check ~/.ssh/config IdentityFile
#   - server perms: ~/.ssh = 700, authorized_keys = 600, home not group-writable
```

---

## 7. `authorized_keys` options (server side, per key)

Options are prepended to a key line, **comma-separated with no spaces** (spaces only inside
quotes). They restrict what *that one key* can do — the finest-grained control SSH offers:

```text
restrict,command="/usr/local/bin/backup.sh",from="203.0.113.7" ssh-ed25519 AAAA... backup@nas
└─ options ────────────────────────────────────────────────────┘ └─ the key ─────┘ └ comment ┘
```

| Option | Effect |
| --- | --- |
| `restrict` | **deny everything** — pty, all forwarding, agent, X11, user-rc — then re-enable pieces explicitly. Future-proof: options added to OpenSSH later are denied too. Prefer this over stacking `no-*` |
| `command="cmd"` | force this command, ignoring whatever the client asked for. The client's request lands in `$SSH_ORIGINAL_COMMAND` (dispatch wrappers for rsync/borg check it) |
| `from="pat,pat"` | accept the key only from matching source hosts — hostnames, IPs, CIDR, `!` negation: `from="10.0.0.0/8,!10.0.0.99"` |
| `expiry-time="YYYYMMDD[HHMM]"` | key stops working after this timestamp *(OpenSSH 8.2+)* |
| `permitopen="host:port"` | limit local forwards (`-L`) to this destination only (repeatable) |
| `permitlisten="[host:]port"` | limit remote forwards (`-R`) to this listen spec only |
| `pty`, `port-forwarding`, `agent-forwarding`, `X11-forwarding`, `user-rc` | re-enable one capability after `restrict` |
| `no-pty`, `no-port-forwarding`, `no-agent-forwarding`, `no-X11-forwarding`, `no-user-rc` | piecemeal denies (the pre-`restrict` style — still common in the wild) |
| `environment="VAR=val"` | set an env var — inert unless `PermitUserEnvironment yes` in `sshd_config` |
| `cert-authority` | this line is a **CA public key**: any user cert it signed is accepted (see [[SSH Key Management]]) |
| `principals="a,b"` | with `cert-authority`: only certs carrying one of these principals |
| `tunnel="n"` | bind this key to tun device *n* (layer-3 VPN mode) |
| `no-touch-required` / `verify-required` | FIDO (`*-sk`) keys: skip the touch / additionally require PIN |

Recipes:

```text
# Backup-only key: forced command, locked to one source IP, nothing else allowed
restrict,command="/usr/local/bin/backup.sh",from="203.0.113.7" ssh-ed25519 AAAA... backup

# Tunnel-only key: may open ONE forward, gets no shell/pty
restrict,port-forwarding,permitopen="127.0.0.1:5432" ssh-ed25519 AAAA... db-tunnel

# Contractor key that self-destructs at year end
expiry-time="20261231",restrict,pty ssh-ed25519 AAAA... contractor
```

- **`command=` is not a shell jail by itself** — combine with `restrict`, or the client can still
  request forwards/agent and pivot.
- One key per line; test in a **second session** before closing your working one. Applying these
  fleet-wide is [[SSH Key Management]]; the daemon-side counterpart is [[SSH Server Hardening]] §4.

---

## 8. Escape sequences, agent hygiene & key extras

`~` at the **start of a line** in a live session is the escape character:

```text
~.    kill a hung session (the one everyone needs)
~^Z   suspend ssh into the local shell
~#    list forwarded connections
~C    command line — add/remove -L/-R/-D forwards live (OpenSSH ≥ 9.2: needs
      "EnableEscapeCommandline yes" in ssh_config; disabled by default)
~~    send a literal ~
```

Agent hygiene — `ssh -A` (agent forwarding) lets **root on the remote host use your agent** to
authenticate anywhere your keys reach. Prefer `-J`/`ProxyJump` (keys never leave your machine);
if you must forward, constrain it:

```bash
ssh-add -c ~/.ssh/id_ed25519    # confirm locally on every use of the key
ssh-add -t 1h ~/.ssh/id_ed25519 # auto-expire from the agent
ssh-add -D                      # flush all loaded keys
```

`ssh-keygen` beyond generate:

```bash
ssh-keygen -p -f ~/.ssh/id_ed25519        # change/set the passphrase (in place)
ssh-keygen -y -f ~/.ssh/id_ed25519        # re-derive the .pub from a private key
ssh-keygen -t ed25519-sk                  # FIDO2 hardware-backed key (touch to sign)
ssh-keyscan -t ed25519 host >> ~/.ssh/known_hosts   # pre-pin a host key (verify fingerprint!)
ssh-keygen -lf <(ssh-keyscan host 2>/dev/null)      # show a remote host's fingerprints
```

---

## Daily workflows

### "Passwordless login to a new server"
```bash
ssh-keygen -t ed25519 -C "you@host"   # if you don't have a key yet
ssh-copy-id user@host                 # push the public key
ssh user@host                         # now key-based
```

### "Reach a service bound to a server's localhost"
```bash
ssh -fN -L 8080:localhost:80 user@host   # then open http://localhost:8080
```

### "Copy a directory efficiently and resumably"
```bash
rsync -avz --partial --progress dir/ user@host:/dest/
```

---

## Files & locations

| Path | What |
| --- | --- |
| `~/.ssh/config` | client config (Host blocks) — see [[ssh_config]] |
| `~/.ssh/id_ed25519` / `.pub` | your private / public key |
| `~/.ssh/known_hosts` | fingerprints of servers you've connected to |
| `~/.ssh/authorized_keys` | *(on the server)* keys allowed to log in as that user — per-key options in §7 |
| `/etc/ssh/sshd_config` | *(on the server)* daemon config — see [[Linux Administration]] |

---

## Gotchas / Golden rules

1. **`scp` uses `-P` for port; `ssh` uses `-p`.** Mixing them up is a rite of passage.
2. **Trailing slash matters in `rsync`** — `dir/` copies contents, `dir` copies the directory.
3. **Verify host keys on first connect**, and treat a "host key changed" warning as
   potentially hostile until you know why.
4. **Use `~/.ssh/config`** — it removes nearly all the repetitive `-p`/`-i`/`user@` typing and
   documents your hosts.
5. **Ed25519 keys, passphrase-protected, loaded into the agent.** Never copy a private key onto
   a server.
6. **Single-purpose keys get `restrict` + `command=` + `from=`.** `command=` alone is not a
   jail — without `restrict`, the client can still open forwards. (§7)
7. **Avoid `ssh -A`.** Forwarded agents are usable by root on the remote host; `ProxyJump`
   gives the same reach without exposing your keys.

## Further reading
- [ssh(1)](https://man.openbsd.org/ssh) · [ssh_config(5)](https://man.openbsd.org/ssh_config) ·
  [sshd_config(5)](https://man.openbsd.org/sshd_config)
