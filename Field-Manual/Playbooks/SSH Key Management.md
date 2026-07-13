---
type: playbook
area: "Linux Administration"
aliases: [ssh key rotation, authorized_keys audit, key revocation]
tags: [ssh, keys, access-control, rotation, offboarding, incident, audit]
status: working
---

# SSH Key Management

> **Area:** [[Linux Administration]]

The lifecycle of SSH keys across a fleet — provisioning, rotation, revocation, compromise
response, and the audit that catches the drift that builds up over time. Key generation and
client-side care lives in [[ssh]]; locking down the daemon is [[SSH Server Hardening]]. This is
the "who has access, and does that still make sense" layer that sits above both.

---

## Situation

- A new user or service needs SSH access to one or more hosts
- A user is leaving, or a service is being decommissioned — access must be pulled everywhere, now
- A key has been in use past its expected lifetime, or policy requires periodic rotation
- A private key may have leaked (stolen laptop, key committed to a repo, shared insecurely)
- Periodic review: who can log in where, and with what key

---

## Quick assessment

```bash
# What keys does THIS host trust, and for which user?
for f in /home/*/.ssh/authorized_keys /root/.ssh/authorized_keys; do
  [ -f "$f" ] && echo "== $f ==" && grep -c '^ssh-\|^ecdsa-' "$f"
done

# Fingerprint + comment for every key in a file — identifies WHO each key belongs to
ssh-keygen -lf ~/.ssh/authorized_keys

# What's loaded in YOUR agent right now
ssh-add -l

# Flag unrestricted keys (no forced command, no source restriction) — the highest-risk ones
grep -L 'command=' /home/*/.ssh/authorized_keys 2>/dev/null
```

---

## Decision branches

| Situation | Go to |
|---|---|
| New user/service needs access | Fix A — Provision a new key |
| Key nearing/past rotation policy age | Fix B — Rotate a key |
| User leaving / service decommissioned | Fix C — Revoke access (offboarding) |
| Private key may have leaked | Fix D — Suspected compromise |
| Fleet grew organically, unclear who has access where | Fix E — Audit across a fleet |
| Per-host `authorized_keys` no longer scales | Fix F — Move to a CA-signed cert model |
| Automation/service needs a key with no interactive shell | Fix G — Restricted service-account keys |

---

## Fix A — Provision a new key

```bash
# Generate on the CLIENT side — private keys never travel
ssh-keygen -t ed25519 -C "alice@laptop-2026"
# Ed25519 unless a legacy target forces RSA; if so, at least 4096 bits:
# ssh-keygen -t rsa -b 4096 -C "alice@laptop-2026"

# Push the public key to each host that needs it
ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@host1
ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@host2

# Verify BEFORE walking away — a failed copy leaves someone locked out later
ssh -i ~/.ssh/id_ed25519 alice@host1 'whoami'
```

*Record it*: host, user, fingerprint (`ssh-keygen -lf`), and date in whatever inventory you use
for access — a compromise or offboarding later depends on that record existing.

---

## Fix B — Rotate a key

Add the new key **alongside** the old one, verify it works, and only then remove the old key —
never delete-then-generate, which risks a lockout window with no way back in.

```bash
# 1. Generate the replacement (never reuse a passphrase or the old key material)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new -C "alice@laptop-$(date +%Y%m)"

# 2. Append the NEW public key to authorized_keys on every host (old key still present)
ssh-copy-id -i ~/.ssh/id_ed25519_new.pub alice@host1

# 3. Verify the new key logs in
ssh -i ~/.ssh/id_ed25519_new alice@host1 'whoami'

# 4. Only now, remove the old key's line (see Fix C for the precise removal method)
#    and retire the old key material on the client
mv ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.retired-$(date +%Y%m%d)
mv ~/.ssh/id_ed25519_new ~/.ssh/id_ed25519
```

---

## Fix C — Revoke access (offboarding)

```bash
# Find the exact line by FINGERPRINT, not by eyeballing base64 — collisions in a long file are easy to miss
ssh host1 "ssh-keygen -lf ~/.ssh/authorized_keys" | grep '<fingerprint>'

# Remove that line, per host, per user account they had access to
ssh host1 "sed -i '/<unique-comment-or-substring>/d' ~/.ssh/authorized_keys"

# Loop it across a known fleet
for host in host1 host2 host3; do
  ssh "$host" "sed -i '/<unique-comment-or-substring>/d' /home/alice/.ssh/authorized_keys"
done

# Kill any session the key already established — removing the line does not drop an open connection
ssh host1 "pkill -u alice"

# If root/shared accounts were reachable with a personal key, rotate THOSE too — a shared
# account's key is not "theirs" to revoke individually, it must be replaced fleet-wide
```

*Verify:* `ssh -i <their-key> user@host` now fails with `Permission denied (publickey)` on
every host that was in scope.

---

## Fix D — Suspected compromise

Treat as an incident, not routine rotation — revoke first, investigate second.

```bash
# 1. Revoke everywhere immediately (Fix C's loop, or the KRL path in Fix F if certs are in use)

# 2. Check auth logs on every reachable host for THIS key's fingerprint — was it used after the leak?
sudo grep 'Accepted publickey' /var/log/auth.log | grep '<fingerprint>'
sudo journalctl -u sshd --since '<date the leak may have occurred>' | grep 'Accepted publickey'

# 3. If it WAS used and you don't recognize the session: treat every host it reached as
#    potentially compromised — that's now a separate, broader incident, not a key problem

# 4. Rotate with fresh key material — never re-passphrase and reuse a leaked private key
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new -C "you@host-$(date +%Y%m%d)"
```

---

## Fix E — Audit across a fleet

```bash
# Collect every authorized_keys file across the fleet (run this WHILE you still have access —
# it's also your evidence trail if access later needs reconstructing)
for host in $(cat hosts.txt); do
  echo "== $host =="
  ssh "$host" '
    for f in /home/*/.ssh/authorized_keys /root/.ssh/authorized_keys; do
      [ -f "$f" ] && echo "-- $f --" && ssh-keygen -lf "$f"
    done
  '
done > fleet-keys-audit.txt

# Flag the risky patterns:
grep -B1 '^ssh-' /root/.ssh/authorized_keys 2>/dev/null   # any personal key with root access at all
sort -u fleet-keys-audit.txt | uniq -c | sort -rn          # same key reused across many hosts/users
```

Cross-reference the fingerprints against a source of truth — a spreadsheet, an IdP group, a
CMDB, anything — of who is *supposed* to have access. Anything present in the audit but absent
from that list is an orphan: someone who left, a service that was decommissioned, or a key that
was never tracked in the first place. Every orphan found here is exactly the gap Fix F closes.

---

## Fix F — Move to a CA-signed cert model

Once per-host `authorized_keys` files stop scaling (many hosts, frequent joiners/leavers), sign
short-lived certificates from one CA instead of distributing individual public keys.

```bash
# ONE-TIME: generate a CA key pair — keep the PRIVATE half offline/in a vault; it signs everyone's access
ssh-keygen -t ed25519 -f ssh_user_ca -C "ssh-user-ca"

# Sign a user's public key into a certificate — this is what you hand out, not the raw key
ssh-keygen -s ssh_user_ca -I "alice-2026-07" -n alice -V +52w -z 1 alice_id_ed25519.pub
#   -I  identity string, shows up in sshd logs
#   -n  principal(s) allowed to present this cert
#   -V  validity window — expiry replaces most manual revocation
#   -z  serial number — needed to revoke by serial before expiry (below)

# Server side: trust the CA instead of maintaining individual authorized_keys entries
echo 'TrustedUserCAKeys /etc/ssh/ssh_user_ca.pub' | sudo tee -a /etc/ssh/sshd_config
sudo sshd -t && sudo systemctl reload sshd
```

**Revoking before expiry** (the compromise/offboarding case, without waiting out `-V`):

```bash
# Add a serial to a revocation list
ssh-keygen -k -f revoked_keys -s ssh_user_ca.pub -z 1

# Point sshd at it
echo 'RevokedKeys /etc/ssh/revoked_keys' | sudo tee -a /etc/ssh/sshd_config
sudo sshd -t && sudo systemctl reload sshd
```

This turns Fix B/C into "issue or expire a certificate" instead of "edit `authorized_keys` on
every host" — the main win at fleet scale. `TrustedUserCAKeys` and `RevokedKeys` are separate
`sshd_config` directives; see [[SSH Server Hardening]] for applying/reloading config generally.

---

## Fix G — Restricted service-account keys

An automation key should never be a general-purpose login key. Restrict it at the
`authorized_keys` line, per [[SSH Server Hardening]] §4, tailored to the one thing it does:

```
command="/usr/local/bin/backup.sh",no-agent-forwarding,no-X11-forwarding,no-port-forwarding,no-pty,from="10.0.0.0/8" ssh-ed25519 AAAA...C3NzaC1lZDI1NTE5AAAA backup-svc@host
```

- `command="..."` — the ONLY thing this key can run, regardless of what the client requests
- `from="<cidr>"` — reject the key outright from any source address outside that range
- `no-pty` — no interactive shell, ever
- `no-agent-forwarding` / `no-X11-forwarding` / `no-port-forwarding` — closes lateral-movement paths a backup or CI key has no business having

Generate it with Fix A's steps, then edit the `authorized_keys` line by hand to add the
restrictions before distributing it — a service key with no restrictions is functionally a
second admin login.

---

## Prevent recurrence

- **Keep an inventory** — host, user, fingerprint, purpose, date issued — for every key. Without
  it, Fix C and Fix E are guesswork.
- **Prefer certs over raw keys at fleet scale** (Fix F) — expiry (`-V`) removes the "forgot to
  rotate" failure mode entirely for the common case.
- **Restrict service keys at issue time** (Fix G), not after an incident.
- **Run the Fix E audit on a schedule** (cron, CI, whatever already runs unattended) — an audit
  you only run during an incident finds the orphan a year too late.
- **Offboarding checklist includes SSH access explicitly** — it's easy to remove someone from an
  IdP/directory and forget the keys already deployed to individual hosts outside it.

## See also

- [[ssh]] — key generation, agent, client-side basics
- [[ssh_config]] — client config, `IdentitiesOnly`, agent-forwarding trust boundary
- [[SSH Server Hardening]] — `sshd_config` lockdown, `authorized_keys` restrictions, fail2ban
- [[linux-users]] — account lifecycle / offboarding on the OS side
