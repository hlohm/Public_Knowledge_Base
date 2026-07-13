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
tools built on it. Covers keys, the client config that saves the most typing, and the
forwarding tricks. Server-side hardening (`sshd_config`) lives under [[Linux Administration]].

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
| `~/.ssh/authorized_keys` | *(on the server)* keys allowed to log in as that user |
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

## Further reading
- [ssh(1)](https://man.openbsd.org/ssh) · [ssh_config(5)](https://man.openbsd.org/ssh_config) ·
  [sshd_config(5)](https://man.openbsd.org/sshd_config)
