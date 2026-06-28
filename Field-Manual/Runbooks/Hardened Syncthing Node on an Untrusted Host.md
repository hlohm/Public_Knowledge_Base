---
type: runbook
area: Linux Administration
tags: [syncthing, hardening, sandbox, firewall, untrusted, sync]
status: working
---

# Hardened Syncthing Node on an Untrusted Host

> **Area:** [[Linux Administration]]

Stand up an always-on [[syncthing]] node on a host you don't fully trust — a cloud free-tier
VPS, a colo box, anywhere the operator could read the disk — such that it improves cluster
connectivity and holds an off-site replica **without ever holding your plaintext**. The lever is
Syncthing's **untrusted (receive-encrypted)** device mode: concede the host, deny the data.

> Threat model is bounded on purpose: you cannot defend against the hypervisor/provider, and you
> don't try. You defend the network surface, the blast radius, cluster hygiene (exactly one device
> identity), and — for free — data-at-rest readability via receive-encryption.
>
> "Relay" here is loose: this is a reachable **encrypted replica** that helps NAT'd peers connect,
> **not** a Syncthing `strelaysrv` relay server. Debian/Ubuntu-family commands; adapt for others.

## When to use
- You want an off-site, always-reachable Syncthing node on hardware outside your trust boundary,
  and you want it to store ciphertext only.

## Prerequisites
- A fresh host with SSH key access and a sudo-capable user.
- An existing Syncthing cluster with at least one **trusted** node that holds the plaintext folders.
- Ability to edit the **provider's edge firewall** (security group / cloud firewall) *and* the
  **host firewall** — see [[iptables]]. On many cloud images both exist and **both** must allow a
  port (the classic "double firewall" trap).
- A password manager for the per-folder encryption passwords and the GUI password.

## Steps

### Phase 1 — host baseline & SSH
- [ ] **Patch, set hostname, enable unattended security upgrades, add swap if RAM is tight.**
  A small sync node can spike RAM during an index build; a swap file is cheap insurance.
  *Verify:* `swapon --show` lists the file; `systemctl is-enabled unattended-upgrades` → enabled.
- [ ] **Lock SSH down** via a drop-in (don't hand-edit the shipped `sshd_config`): keys-only,
  no root, no password/keyboard-interactive, optional custom port. See [[ssh]] / [[fail2ban]].
  ```bash
  printf '%s\n' 'PasswordAuthentication no' 'KbdInteractiveAuthentication no' \
    'PermitRootLogin no' 'PubkeyAuthentication yes' 'Port <ssh-port>' \
    | sudo tee /etc/ssh/sshd_config.d/10-hardening.conf
  sudo sshd -t
  ```
  *Verify:* `sshd -t` is silent (valid config).
- [ ] **If you changed the port on Ubuntu ≥22.10, disable socket activation** — `ssh.socket`
  owns the port and *silently ignores* `Port` in the config until you do.
  ```bash
  systemctl is-active ssh.socket && sudo systemctl disable --now ssh.socket
  sudo systemctl enable --now ssh.service
  sudo systemctl restart ssh.service          # restart, not reload, for a listen-port change
  ```
  *Verify:* `sudo ss -tlnp | grep sshd` shows the new port. **Keep the old session open** and prove
  a new one on the new port before closing anything.

### Phase 2 — firewall (both layers)
- [ ] **Open `22000/tcp` + `22000/udp`** (Syncthing) and your SSH port at the **provider edge**
  (security group / cloud firewall). Leave `8384` (GUI) and `21027/udp` closed.
- [ ] **Open the same on the host firewall** and **persist** it — see [[iptables]]. On images with
  a default `REJECT` rule, insert *above* it; on Ubuntu persist with `netfilter-persistent save`.
  *Verify:* from elsewhere, `nc -zv <host> 22000` succeeds and `nc -zv <host> 8384` is refused
  (see [[nc]]); the rules survive a reboot.

### Phase 3 — service user & filesystem layout
- [ ] **Create a dedicated non-login system user** and a proper data area — not in a human's home.
  ```bash
  sudo useradd --system --shell /usr/sbin/nologin --home-dir /var/lib/syncthing --create-home syncthing
  sudo chmod 0700 /var/lib/syncthing
  sudo install -d -o syncthing -g syncthing -m 0750 /srv/syncthing
  ```
  *Verify:* the user has no shell; `/srv/syncthing` is owned `syncthing:syncthing`.

### Phase 4 — install & sandbox
- [ ] **Install [[syncthing]]** from the project's own apt repo (current release, not the stale
  distro build), then write a **hardened systemd unit** running as the `syncthing` user. The
  sandbox directives and their meanings are in [[systemd.exec]]; the load-bearing ones here:
  ```ini
  [Service]
  User=syncthing
  Group=syncthing
  Environment=STHOMEDIR=/var/lib/syncthing
  ExecStart=/usr/bin/syncthing serve --no-browser --no-restart --home=/var/lib/syncthing
  Restart=on-failure
  SuccessExitStatus=3 4
  RestartForceExitStatus=3 4
  # sandbox (see [[systemd.exec]]):
  NoNewPrivileges=true
  ProtectSystem=strict
  ProtectHome=true
  ReadWritePaths=/var/lib/syncthing /srv/syncthing
  PrivateTmp=true
  PrivateDevices=true
  ProtectKernelTunables=true
  ProtectKernelModules=true
  ProtectControlGroups=true
  RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
  RestrictNamespaces=true
  LockPersonality=true
  SystemCallFilter=@system-service
  SystemCallErrorNumber=EPERM
  CapabilityBoundingSet=
  RemoveIPC=true
  UMask=0077
  ```
  ```bash
  sudo systemctl daemon-reload && sudo systemctl enable --now syncthing.service
  ```
  *Verify:* `systemctl status syncthing` is active; `systemd-analyze security syncthing.service`
  returns a low score — **expect ~1.5, the floor for a network-bound P2P daemon** (`PrivateNetwork`,
  `AF_INET`, `IPAddressDeny` are irreducible; the *green directive list* is the security, not the
  number). `SuccessExitStatus=3 4` keeps Syncthing's restart(3)/upgrade(4) exit codes sane.

### Phase 5 — identity & GUI
- [ ] **Confirm a fresh device identity** (first start generated its own `cert.pem` — you did
  **not** copy one in). Tunnel to the GUI, set a **password + HTTPS**, keep the bind on loopback.
  ```bash
  ssh -p <ssh-port> -L 8384:localhost:8384 <user>@<host>   # then browse http://localhost:8384
  ```
  *Verify:* the node's device ID differs from every other node; GUI is reachable only via the tunnel.

### Phase 6 — pair as an untrusted (receive-encrypted) device
- [ ] **On each trusted sender**, add this node and share each folder to it **with a per-folder
  encryption password** (Folder → Sharing → tick device → Advanced → Encryption Password). Store
  every password in your password manager — it lives on the senders, **never** on this node.
  *Verify:* on this node the folder auto-appears as type `receiveencrypted`; on disk the filenames
  and contents under `/srv/syncthing/<folder>` are opaque ciphertext.
- [ ] **Do not enable introducer** on this node, and only share folders you accept as off-site
  replicas. Let it converge to *Up to Date*.
  *Verify:* the GUI shows the folders **Up to Date** and the device as connected.

### Phase 7 — monitoring hook (provider-agnostic)
- [ ] **Wire it into whatever you already run**, dialling *outward* so you add no inbound surface:
  a push-based **liveness** ping (cron/timer → your dead-man's-switch), an **external reachability**
  probe of `<host>:22000` from a different vantage, and a host-metrics agent (dial-out) with a
  **disk-fill alert** — the one failure liveness/reachability miss on a finite sync volume.
  *Verify:* liveness, reachability, and the disk alert all report green; kill-test one to prove it buzzes.

## Rollback
- All additive until Phase 6. To unwind: stop/disable the service, remove this node's device ID
  from every peer (so the cluster forgets it), then wipe `/var/lib/syncthing` and `/srv/syncthing`.
- Cutover safety: never close the old SSH port/session until a new one on the new port is proven;
  open firewall ports *before* restarting the service, not after.

## Done when
- [ ] Syncthing runs as a dedicated sandboxed user under a proper FHS layout, with a **fresh**
  device identity (no copied cert).
- [ ] Only `22000` (and SSH) is reachable from the internet; the GUI is loopback-only.
- [ ] Every shared folder is `receiveencrypted` — the host holds **ciphertext only**.
- [ ] A trusted peer has been shown to **restore** from this node's encrypted copy (decrypts locally).
- [ ] Liveness + external reachability + disk-fill alerting are green, and a kill-test fired.

## Gotchas
1. **Never copy `cert.pem`** onto the new node — generate a fresh identity, or you put one device
   ID on the cluster twice (flapping). See [[syncthing]] §1.
2. **The encryption password lives on the trusted senders, never here.** Typing it into this node
   makes it able to decrypt — defeating the whole design.
3. **Two firewalls on cloud hosts.** The provider edge *and* the host firewall must both allow a
   port, and the host rules must be **persisted** or a reboot drops them ([[iptables]]).
4. **GUI off-loopback → "Host check error"** (anti-rebinding), not a TLS/HSTS error. Fix with
   `insecureSkipHostcheck`; only safe behind the tunnel + GUI password + HTTPS ([[syncthing]] §6).
5. **`systemd-analyze` ~1.5 is the floor** for a network daemon — don't chase a lower number by
   breaking networking; read [[systemd.exec]] for which directives are irreducible here.
6. **Custom SSH port needs `ssh.socket` disabled** on modern Ubuntu, and a `restart` (not `reload`)
   for the port to actually move.
