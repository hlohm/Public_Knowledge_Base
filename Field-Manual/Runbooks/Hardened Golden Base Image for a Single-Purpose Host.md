---
type: runbook
area: Linux Administration
tags: [hardening, golden-image, baseline, appliance, provisioning, firewall, sandbox, immutable]
status: draft
---

# Hardened Golden Base Image for a Single-Purpose Host

> **Area:** [[Linux Administration]]

Build a hardened, reproducible **base image** for a single-purpose, internet-facing host — a mail
relay, reverse proxy, VPN endpoint, sync node — that you can clone and bring up **fast** and
**trust**. The method separates three things people tend to conflate: the **immutable hardened
base** (baked once), the **per-instance identity** (injected at first boot), and the **living
workload config** (deployed on top from a source of truth). Get those layers right and "spin up an
appliance in minutes" stops being a slogan.

> Threat model is bounded on purpose. On a VPS the **hypervisor/provider is in your TCB** — they can
> read guest RAM and disk, and you do **not** try to defend against them. You harden against the
> internet and co-tenants: reduce attack surface, shrink blast radius, constrain egress, and make
> data-at-rest unreadable to a stray disk. Full-disk encryption on a VPS buys disk-at-rest and
> clean-decommission protection, **not** protection against the host. State that boundary out loud —
> it's what keeps "an appliance I trust" an honest claim rather than a comforting one.
>
> Debian/Ubuntu-family commands below. Notes flag where an immutable/transactional base (e.g.
> openSUSE MicroOS), a declarative base (NixOS), a BSD (FreeBSD), or a musl base (Alpine) diverge.

## When to use
- You need a repeatable, **pre-trusted** base for one or more single-purpose internet-facing hosts,
  and you want each spin-up to be reproducible rather than hand-built — including standing up a
  second, identical node for redundancy.

## Prerequisites
- A provider that gives you: **console / break-glass** access, **settable PTR/rDNS**, the ability to
  **clone via snapshot or upload a custom image** (qcow2/raw), and ideally **cloud-init**.
- Edit access to **both** the provider's **edge firewall** *and* the **host firewall** — the classic
  "double firewall" trap where both must allow a port. See [[iptables]].
- A secret store (password manager, or `age`/SOPS, or a secrets manager) **plus** a way to inject
  secrets **at provision time** — never baked into the image, never committed to git.
- A trusted machine to author config as source of truth (a git repo), and a deploy path (rsync/pull)
  to the instances. The image is the floor; this is the furniture.
- A decision on your **OS base** and **provisioning model** — that's Phase 0.

## Steps

### Phase 0 — decide the base and the provisioning model (two orthogonal axes)
- [ ] **Pick the OS base by which hardening lever you keep, not by which is "most minimal."** If your
  main lever is systemd unit sandboxing, favour a glibc+systemd base.
  - **Debian-minimal** — low-risk default: lean by subtraction, full systemd sandboxing, every
    server package first-class.
  - **Immutable / transactional** (e.g. openSUSE MicroOS) — read-only root, atomic updates with
    automatic snapshot **rollback**; keeps systemd; leans container-native, so the workload often
    runs as a container.
  - **Declarative** (NixOS) — the whole machine is one reproducible config with atomic
    generations/rollback; superb for identical nodes, but a paradigm commitment — adopt fleet-wide,
    not for one box.
  - **BSD** (FreeBSD) — unified base, `pf`, jails, ZFS boot environments (atomic rollback); diverges
    from a Linux fleet and provider images are often ISO-install only.
  - **musl** (Alpine) — leanest, but trades systemd sandboxing for OpenRC and adds a small
    compatibility tail; pick only for a container-host role.
  *Verify:* you can state why the base fits your fleet **and** your skills, not just its size.
- [ ] **Pick the provisioning model: pre-baked image, not boot-time config.** "Up in a minute and
  trusted" forces the heavy lifting (packages + hardening) **into the image**; cloud-init then does
  only per-instance injection. Boot-time `apt install` can't hit a minute and widens the trust
  surface (you're now trusting mirrors and run-time success on every boot).
  *Verify:* the build work lives in the image; first boot does injection only. (Reality check:
  literal sub-minute spin-up is a provider-**API** property. Console/panel-driven providers give you
  *reproducible and pre-trusted*, not instant — calibrate the budget to your provider.)

### Phase 1 — build the base (on a throwaway "builder" instance)
- [ ] **Minimal install:** no GUI, minimal package set, remove unused services; **no compilers or dev
  tooling** in the final image. Smallest install = smallest attack surface.
- [ ] **Patch fully and set time sync** (chrony) — accurate time underpins TLS, audit, token, and
  any signature validity downstream.
- [ ] **Updates policy:** enable unattended **security** upgrades for the living host (you can't wait
  for a manual image rebuild on a critical CVE), and plan **periodic image rebuilds** so the golden
  base doesn't rot. Transactional/declarative bases do this atomically with rollback.
  *Verify:* package set is minimal; `timedatectl` shows synced; `systemctl is-enabled` on the
  unattended-upgrade unit → enabled.

### Phase 2 — access plane (SSH / break-glass)
- [ ] **Lock SSH via a drop-in** (don't hand-edit the shipped `sshd_config`): keys-only, no root, no
  password/keyboard-interactive, optional custom port. See [[ssh]] / [[fail2ban]].
  ```bash
  printf '%s\n' 'PasswordAuthentication no' 'KbdInteractiveAuthentication no' \
    'PermitRootLogin no' 'PubkeyAuthentication yes' 'Port <ssh-port>' \
    | sudo tee /etc/ssh/sshd_config.d/10-hardening.conf
  sudo sshd -t
  ```
  *Verify:* `sshd -t` is silent.
- [ ] **Modern-Ubuntu socket-activation caveat:** on Ubuntu ≥22.10, `ssh.socket` owns the port and
  silently ignores `Port` until disabled; then `restart` (not `reload`) to move the listener.
  *Verify:* `ss -tlnp | grep sshd` shows the intended port.
- [ ] **Strongest posture (recommended): no public SSH at all.** Admin over a VPN (e.g. WireGuard),
  with the **provider console as the out-of-band break-glass** — the equivalent of a bastion gate on
  a separate auth plane. Keep `fail2ban` only if you leave public SSH exposed.
  *Verify:* prove a new admin session (new port / over the VPN) **before** closing the old one;
  confirm the provider console reaches a login independently of SSH.

### Phase 3 — firewall: both layers, ingress + egress, default-deny
- [ ] **Provider edge firewall:** default-deny; allow only the workload's ports and your admin path.
- [ ] **Host firewall** (nftables / [[iptables]]): the same default-deny, and **persist it** (a reboot
  must not drop the rules). Where a default `REJECT` rule exists, insert allows *above* it.
- [ ] **Constrain egress too.** A single-purpose host needs only a handful of outbound destinations
  (its workload ports, ACME on 443, DNS, NTP); deny the rest to blunt exfiltration and C2.
  *Verify:* from outside, only the intended ports answer (see [[nc]]); rules survive a reboot;
  an outbound test to an unrelated host/port is blocked.

### Phase 4 — kernel & sysctl hardening
- [ ] **Drop in sysctl hardening** under `/etc/sysctl.d/`: network protections (reverse-path filter,
  no ICMP redirects, no source routing, SYN cookies); info-leak limits (`kptr_restrict`,
  `dmesg_restrict`, `yama.ptrace_scope`); BPF hardening; and **blacklist unused filesystem and
  network protocol modules**.
  *Verify:* `sysctl <key>` returns the intended values after a reboot; blacklisted modules fail to
  load.

### Phase 5 — mandatory access control + per-service sandboxing
- [ ] **Leave the distro's MAC enforcing** (AppArmor on Debian/Ubuntu, SELinux elsewhere) — don't
  disable the default to "make it work."
- [ ] **Sandbox each workload daemon with a systemd drop-in** — the single highest-leverage control.
  Use **additive** `/etc/systemd/system/<unit>.d/` drop-ins; never `systemctl edit --full` on a
  rolling/transactional distro (full overrides get clobbered on upgrade). Directive meanings live in
  [[systemd.exec]]; the load-bearing set:
  ```ini
  [Service]
  NoNewPrivileges=true
  ProtectSystem=strict
  ProtectHome=true
  ReadWritePaths=/var/lib/<svc>            # only what it must write
  PrivateTmp=true
  PrivateDevices=true
  ProtectKernelTunables=true
  ProtectKernelModules=true
  ProtectControlGroups=true
  RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
  RestrictNamespaces=true
  LockPersonality=true
  MemoryDenyWriteExecute=true              # drop if the workload JITs
  SystemCallFilter=@system-service
  SystemCallErrorNumber=EPERM
  CapabilityBoundingSet=                   # add back only what's needed, e.g. CAP_NET_BIND_SERVICE
  UMask=0077
  ```
  *Verify:* `systemd-analyze security <unit>` shows a **green directive list** — the list is the
  security, not the score. A network-bound daemon floors around ~1.5 (`AF_INET` is irreducible);
  don't break networking chasing a lower number.

### Phase 6 — secrets & per-instance identity (the golden-image footguns)
- [ ] **The image is secret-free.** Inject every secret at provision via cloud-init pulling from your
  encrypted store (`age`/SOPS or a secrets manager). Nothing sensitive is baked into the image or
  committed to git.
- [ ] **Regenerate per-host identity on first boot:** SSH **host keys** and **machine-id**. A cloned
  image that ships fixed host keys puts one identity on every instance — the host-level twin of
  copying a node's TLS identity across a cluster. cloud-init regenerates these; make it explicit.
  ```bash
  # first-boot (one-shot): force-fresh host identity on a clone
  sudo rm -f /etc/ssh/ssh_host_* /etc/machine-id
  sudo systemd-machine-id-setup
  sudo dpkg-reconfigure openssh-server   # regenerates host keys (Debian/Ubuntu)
  ```
  *Verify:* two instances from the same image have **different** SSH host-key fingerprints and
  machine-ids; `git log -p` and the image contain **no** secret material.

### Phase 7 — at-rest & filesystem
- [ ] **Mount hardening:** `noexec,nosuid,nodev` on `/tmp`, `/var/tmp`, `/dev/shm` (and `/home` where
  it applies).
- [ ] **Consider full-disk encryption for key material**, with the threat-model caveat from the top:
  it protects a stolen/decommissioned disk, not against the hypervisor. For a headless VPS, unlock
  over the network via dropbear-in-initramfs.
  *Verify:* `mount` shows the hardened options; if FDE is used, a reboot unlocks as designed.

### Phase 8 — observability (dial outward)
- [ ] **Wire monitoring that dials *outward*** so you add no inbound surface: a log/agent forwarding
  to your SIEM, host metrics with a **disk-fill alert**, and an **external reachability** probe of
  the workload port from a different vantage. Add `auditd` with a sane ruleset for the host audit
  trail.
  *Verify:* logs land in the SIEM; the agent and disk alert are green; an external probe sees the
  workload port; **kill-test** one alert to prove it fires.

### Phase 9 — capture the golden image & define cloning
- [ ] **Produce the reusable image** from the hardened builder: a provider **offline snapshot →
  import** to a new server, or **export → convert → upload**. Mind the format trap — a compressed
  snapshot often won't re-import as-is; convert to **qcow2** (raw expands to the full disk size).
- [ ] **Layer the living config separately.** The image is the hardened, package-complete, secret-free
  **floor**, rebuilt periodically. The workload's mutable config (the part that changes as you
  operate) is deployed on top from a **version-controlled source of truth** — author on a trusted box,
  push to instances. See [[git]]. This is what makes a redundant second node *identical by
  construction* rather than by hand.
  *Verify:* a fresh instance from `image + cloud-init + config deploy` comes up correct and identical
  to its siblings, within your spin-up budget.

## Rollback
- The builder is **throwaway** — if a phase goes wrong, discard it and rebuild from these notes; only
  the captured image and the config repo are kept.
- **Additive-safe sequencing:** open firewall ports *before* starting the workload; prove a new SSH /
  VPN path *before* closing the old; keep the **provider console** as the always-available
  break-glass so you can never firewall or SSH yourself out.
- On a transactional or declarative base, roll back to the **previous generation/snapshot** atomically.

## Done when
- [ ] A fresh instance comes up from `image + cloud-init` within your time budget, with a **unique**
  host identity and **no baked secrets**.
- [ ] Only the intended ports answer from the internet; **egress is constrained**; **both** firewall
  layers persist a reboot.
- [ ] Each workload daemon runs **sandboxed** (green directive list); MAC is enforcing; sysctls applied.
- [ ] Logs reach your SIEM; external reachability and disk-fill alerts are green; a kill-test fired.
- [ ] You can **rebuild the whole thing from version-controlled sources** (image recipe + config) with
  no hand-steps — and you've named the trust boundary (the provider is in the TCB) out loud.

## Gotchas
1. **Host-key / machine-id footgun.** A cloned image shares host identity unless first-boot
   regenerates it — the host-level version of copying a cluster member's certificate. Always Phase 6.
2. **Secret-free image, always.** Anything baked into the image or committed to git is *published* the
   moment that image is shared or that commit is pushed. Inject at provision, never before.
3. **Two firewalls.** Edge *and* host must both allow a port, the host rules must **persist**, and
   don't forget **egress** — inbound-only filtering leaves exfiltration wide open.
4. **"Spin up in a minute" is a pre-baking property** (and a provider-API one), not something you get
   by configuring at boot. Bake the base; inject the difference; calibrate the budget to the provider.
5. **The `systemd-analyze` number is not the goal** — the *green directive list* is. A network daemon
   floors around ~1.5; breaking networking to chase a lower score is a regression. See [[systemd.exec]].
6. **Never `systemctl edit --full`** on a rolling/transactional distro — additive `/etc` drop-ins
   survive package upgrades; full overrides get silently clobbered.
7. **The trust ceiling is the hypervisor.** Guest hardening stops the internet and co-tenants, not the
   host operator; FDE is disk-at-rest only. Keep the appliance's "trust" claim honest by saying so.
8. **Image rot vs immutability.** A frozen golden image drifts out of date; pair unattended *security*
   upgrades on the living host with periodic image rebuilds — or use a transactional/declarative base
   where update-and-rollback is atomic.

## See also
- **[[Hardened Syncthing Node on an Untrusted Host]]** — this baseline applied end-to-end to one
  workload (sandboxed service, double firewall, dial-out monitoring, bounded threat model).
- [[systemd.exec]] (sandbox directives) · [[ssh]] / [[fail2ban]] (access plane) · [[iptables]] /
  [[nc]] (firewall + reachability checks) · [[git]] (config source of truth).
