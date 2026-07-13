---
type: runbook
area: "Linux Administration"
tags: [ssh, sshd, hardening, security, fail2ban, linux]
status: working
---

# SSH Server Hardening

> **Area:** [[Linux Administration]]

Lock down an SSH server: disable password auth, restrict algorithms, tighten daemon options, and add brute-force protection. Covers `sshd_config`, authorized keys, and fail2ban.

> **Client-side SSH** (key generation, `~/.ssh/config`, agent, tunnels) is in [[ssh]].

---

## When to use

Any time you expose port 22 (or any SSH port) to a network — especially the public internet. Run this on every new server before opening firewall access.

---

## Prerequisites

- Root or `sudo` access on the target host
- At least one working **non-root** user account with a configured `authorized_keys` — set this up and verify login **before** disabling password auth
- A second SSH session open as a safety net throughout

---

## Step 1 — Set up key-based authentication first

```bash
# On the client machine: generate a key if you don't have one
ssh-keygen -t ed25519 -C "you@example.com"

# Copy public key to the server
ssh-copy-id -i ~/.ssh/id_ed25519.pub <user>@<host>

# Or manually:
# cat ~/.ssh/id_ed25519.pub  → append to ~/.ssh/authorized_keys on the server

# Verify key-based login works BEFORE continuing
ssh -i ~/.ssh/id_ed25519 <user>@<host>
```

*Verify:* You are logged in without a password prompt before continuing to Step 2.

---

## Step 2 — Harden sshd_config

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak   # always back up first
sudo nano /etc/ssh/sshd_config
```

Apply the following settings (add or change as needed):

```
# ── Authentication ─────────────────────────────────────────────────────────────
PermitRootLogin no                   # never allow direct root login
PasswordAuthentication no            # keys only
PermitEmptyPasswords no
ChallengeResponseAuthentication no   # disable PAM challenge-response
UsePAM yes                           # keep PAM for account/session management

# ── Protocol and algorithms ────────────────────────────────────────────────────
Protocol 2                           # SSHv1 is not supported by modern OpenSSH anyway
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# ── Access control ─────────────────────────────────────────────────────────────
AllowUsers <user>                    # whitelist; OR use AllowGroups sshusers
# AllowGroups sshusers              # alternative: add users to this group
MaxAuthTries 3                       # lock out after 3 failed attempts per connection
MaxSessions 5

# ── Timeouts ───────────────────────────────────────────────────────────────────
LoginGraceTime 30                    # seconds to authenticate before disconnect
ClientAliveInterval 300              # send keepalive every 5 minutes
ClientAliveCountMax 2                # disconnect after 2 missed keepalives

# ── Port (optional) ────────────────────────────────────────────────────────────
# Port 2222                          # security by obscurity; reduces noise but not security
                                     # if you change this, update firewall and fail2ban

# ── Miscellaneous ──────────────────────────────────────────────────────────────
X11Forwarding no
AllowAgentForwarding no              # set to yes if you need agent forwarding
AllowTcpForwarding no                # set to yes if you need tunnels
PrintMotd no
Banner /etc/ssh/banner               # optional legal/warning banner
```

*Verify config is valid before reloading:*

```bash
sudo sshd -t                         # test config; exits 0 if valid
```

*Verify:* `sshd -t` exits without errors.

---

## Step 3 — Reload sshd

```bash
# Reload (preferred — no connection disruption)
sudo systemctl reload sshd

# Or restart if reload is not available
sudo systemctl restart sshd

sudo systemctl status sshd           # confirm it is running
```

*Verify:* **In your second, still-open session:** confirm you can still execute commands. Then open a **third** connection to confirm login still works with your key.

---

## Step 4 — Harden authorized_keys (per user)

```bash
# ~/.ssh/ and authorized_keys permissions are enforced by sshd:
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Review what keys are authorized
cat ~/.ssh/authorized_keys

# Restrict a key to a specific command (e.g., for backup)
# In authorized_keys, prepend restrictions before the key:
# command="/usr/local/bin/backup.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAA...

# Set expiry on a key (OpenSSH 8.2+)
# expiry-time="20261231",no-port-forwarding ssh-ed25519 AAAA...
```

---

## Step 5 — Install and configure fail2ban

fail2ban watches auth logs and bans IPs that exceed failed login thresholds.

```bash
# Install
sudo apt install fail2ban          # Debian/Ubuntu
sudo dnf install fail2ban          # RHEL/Rocky
sudo pacman -S fail2ban            # Arch

# Create a local override (never edit /etc/fail2ban/jail.conf directly)
sudo tee /etc/fail2ban/jail.d/sshd.conf <<'EOF'
[sshd]
enabled   = true
port      = ssh
filter    = sshd
backend   = systemd
maxretry  = 3
findtime  = 600
bantime   = 3600
ignoreip  = 127.0.0.1/8 ::1
EOF

# If you changed the SSH port:
# port = 2222

# Enable and start
sudo systemctl enable --now fail2ban

# Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd

# View current bans
sudo fail2ban-client status sshd | grep 'Banned IP'

# Manually unban an IP
sudo fail2ban-client set sshd unbanip <ip-address>
```

*Verify:* `fail2ban-client status sshd` shows `Currently banned: 0` and the jail is active.

---

## Step 6 — (Optional) Restrict with firewall

```bash
# iptables: allow SSH only from specific source networks
sudo iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j DROP

# nftables
sudo nft add rule inet filter input tcp dport 22 ip saddr 10.0.0.0/8 accept
sudo nft add rule inet filter input tcp dport 22 drop

# ufw (Debian/Ubuntu)
sudo ufw allow from 10.0.0.0/8 to any port 22
sudo ufw deny 22
```

See [[iptables]] or [[linux-networking]] for firewall basics.

---

## Done when

- [ ] Key-based login verified working for your user
- [ ] `PasswordAuthentication no` confirmed: `ssh -o PasswordAuthentication=yes <user>@<host>` fails with "Permission denied (publickey)"
- [ ] `PermitRootLogin no` confirmed: `ssh root@<host>` fails
- [ ] `sshd -t` passes
- [ ] `systemctl status sshd` is active
- [ ] `fail2ban-client status sshd` shows jail active

---

## Rollback

If you are locked out:

1. Use the cloud provider's console / out-of-band access (IPMI, serial, recovery mode)
2. Restore the backup: `sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config`
3. `sudo systemctl restart sshd`

If fail2ban banned your own IP:

```bash
sudo fail2ban-client set sshd unbanip <your-ip>
```

---

## See also

- [[ssh]] — client-side: key generation, `~/.ssh/config`, agent, tunnels, port forwarding
- [[SSH Key Management]] — provisioning, rotation, offboarding, compromise response, fleet audit
- [[linux-users]] — PAM, password policy, sudo hardening
- [[Hardened Golden Base Image for a Single-Purpose Host]] — broader system hardening including SSH
- [[Unix OS Hardening]] — full playbook covering SSH as one component
