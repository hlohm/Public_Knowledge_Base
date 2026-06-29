---
type: playbook
area: "Linux Administration"
tags: [hardening, security, unix, linux, bsd, kernel, firewall, ssh, audit, mac, apparmor, selinux]
status: working
---

# Unix OS Hardening

> **Area:** [[Linux Administration]]

A decision-tree hardening reference for any Unix-like system — Linux (all major families), FreeBSD, OpenBSD, and macOS — across server, VM, cloud, container host, appliance, workstation, laptop, and embedded deployments. Pick your threat model, identify your profile, follow the branches. Every section is independent; apply any subset and the rest still holds.

> Hardening is not one-time. A system's role changes; new CVEs land; review the applicable sections again whenever either happens.

## Situation

- You are deploying a new system and need to harden it from the start, **or**
- An existing system needs a posture review, gap-fill, or uplift to a new threat model.

## Quick assessment (first 3 commands)

```bash
cat /etc/os-release && uname -r                                # OS family, version, running kernel
systemd-detect-virt 2>/dev/null || hostnamectl status          # bare metal / VM type / container
ss -tlnp                                                       # current listening surface — the first thing to shrink
```

Then audit what's running:

```bash
systemctl list-units --type=service --state=running --no-pager # Linux with systemd
service -e                                                     # BSDs / OpenRC
```

---

## Threat model

Select the highest tier that applies; each tier inherits all controls from lower tiers.

| Tier | Adversary | Typical context |
|---|---|---|
| **TM0** | Automated scanners, credential stuffers, commodity ransomware | Any internet-facing host |
| **TM1** | Targeted attacker with commodity tools; opportunistic lateral movement | Public servers, VPS, edge nodes |
| **TM2** | Motivated adversary with custom tools; kernel exploits; insider risk | Sensitive infrastructure, production backends |
| **TM3** | State-level; hardware implants; firmware attacks; supply-chain | Critical infrastructure, high-value secrets stores |

**If in doubt, start at TM1.** TM2+ introduces friction that breaks operational workflows if applied without understanding the tradeoffs.

**Provider trust ceiling:** on any hosted VM the **hypervisor operator is inside your TCB.** FDE protects disk-at-rest on a stolen or decommissioned drive; it does not protect you from the host operator. Name this boundary; don't pretend it isn't there.

---

## System profile

| Code | Form factor |
|---|---|
| **S1** | Internet-facing server (SSH, web, mail, VPN, DNS) |
| **S2** | Internal server (DB, CI/CD, monitoring, directory services) |
| **S3** | VM guest / cloud instance |
| **S4** | Container host |
| **S5** | Workstation / desktop |
| **S6** | Laptop |
| **S7** | Network appliance / router / firewall |
| **S8** | Embedded / IoT |

---

## Decision branches

Sections: **A** Baseline · **B** Boot/Firmware · **C** FDE · **D** Kernel · **E** Auth & Access · **F** Network & Firewall · **G** Services & Isolation · **H** MAC · **I** Audit & Logging · **J** File Integrity · **K** Vuln Management · **L** Advanced Kernel · **M** Verified Boot

| Profile | TM0 minimum | + TM1 | + TM2 | + TM3 |
|---|---|---|---|---|
| S1 internet server | A D E F G H | + I J K | + L | + M |
| S2 internal server | A D E F G | + H I J K | + L | + M |
| S3 VM / cloud | A D E F G H I | + J K | + L | — |
| S4 container host | A D E F G H J | + I K | + L | — |
| S5 workstation | A D E F G | + H C I | + B L | + B (TPM) |
| S6 laptop | A C D E F G | + H I | + B L | + B M |
| S7 appliance | A D E F G | + I | + L M | + M |
| S8 embedded | A D F | + E | + B | + B M |

---

## Fix A — Universal Baseline

Applies to **every** Unix system at every tier.

**Minimal install** — fewer packages = fewer CVEs = a smaller surface to reason about:

```bash
apt-mark showmanual | sort          # Debian/Ubuntu: what was manually installed
rpm -qa --qf '%{name}\n' | sort    # RHEL family
pkg info | awk '{print $1}'         # FreeBSD
```

**Core dump policy** — setuid core dumps can contain secrets:

```bash
# /etc/security/limits.d/10-coredumps.conf
* hard core 0
```

```
# /etc/sysctl.d/10-coredumps.conf
fs.suid_dumpable = 0
kernel.core_uses_pid = 1
```

**umask** — 022 leaks read access; tighten for anything server-shaped:

```bash
# /etc/profile.d/umask.sh  (or equivalent login config)
umask 027   # 027: no world-read; 022 only if shared-account workstation semantics are needed
```

**Root account:**

```bash
passwd -l root      # Linux: lock the password slot
pw lock root        # FreeBSD
```

**Clock sync** — TLS validity, audit timestamps, and tokens all depend on accurate time; do this before anything else:

```bash
apt install chrony && systemctl enable --now chrony    # Debian/Ubuntu
dnf install chrony && systemctl enable --now chronyd   # RHEL family
pkg install chrony && sysrc chronyd_enable=YES && service chronyd start  # FreeBSD
chronyc tracking                                       # verify
```

---

## Fix B — Firmware & Boot

Primarily for **bare metal** (S1 physical, S5, S6, S7, S8). VM guests skip UEFI/GRUB steps; the hypervisor controls boot integrity.

**BIOS/UEFI password** — prevents changing boot order or entering setup from a running OS.

**Boot order** — primary disk first; USB/PXE as fallback (not removed entirely, so recovery is still possible with physical access).

**GRUB password** — prevents single-user mode or kernel parameter injection without authentication:

```bash
grub-mkpasswd-pbkdf2                    # generate hash (interactive)

# /etc/grub.d/40_custom
set superusers="<admin>"
password_pbkdf2 <admin> grub.pbkdf2.sha512.<hash>

sudo update-grub                        # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL
```

**UEFI Secure Boot:**

```bash
mokutil --sb-state        # is Secure Boot active and enforcing?
bootctl status            # systemd-boot: shows Secure Boot + TPM state
```

**TPM-backed measured boot (TM2+)** — seals the disk key to the measured boot chain; unlocks automatically only when the boot sequence is bit-for-bit identical:

```bash
systemd-cryptenroll --tpm2-device=list                         # confirm TPM is visible
sudo systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=0+7 /dev/<luks-dev>
# PCR 7 = Secure Boot state; PCR 0 = firmware; combine as needed
```

**IPMI / BMC (bare metal servers):**

- Change BMC default credentials immediately — the BMC is a full computer with network access and physical control over the host.
- Bind IPMI/BMC to a dedicated out-of-band management network; never expose it to the internet or the data-plane VLAN.
- Apply BMC firmware updates; the BMC has its own CVE stream.

---

## Fix C — Full-Disk Encryption

Mandatory for **S6 (laptop)**; recommended for **S5** and any host with sensitive data-at-rest. On a VPS: protects disk-at-rest against a decommissioned or stolen drive, **not** against the hypervisor operator.

**LUKS2 + dm-crypt (Linux)** — set up at install time; retrofitting an active root partition is non-trivial:

```bash
sudo cryptsetup luksDump /dev/<dev>            # inspect existing LUKS header

# Enroll TPM2 to an existing LUKS device (after Fix B)
sudo systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=0+7 /dev/<luks-dev>

# Always add a recovery key slot and store it offline
sudo systemd-cryptenroll --recovery-key /dev/<luks-dev>
```

**Encrypted swap** — a hibernate image contains RAM contents; the swap partition must be encrypted:

```bash
# /etc/crypttab
swap /dev/<swap-dev> /dev/urandom swap,cipher=aes-xts-plain64,size=256
```

**Headless server network unlock (dropbear-in-initramfs)** — prompts for passphrase over SSH before root mounts; removes physical presence requirement:

```bash
apt install dropbear-initramfs
# /etc/dropbear/initramfs/authorized_keys  → paste your public key
# /etc/dropbear/initramfs/dropbear.conf    → set DROPBEAR_OPTIONS with static IP
update-initramfs -u
```

**ZFS native encryption (FreeBSD / Linux):**

```bash
zfs create -o encryption=aes-256-gcm -o keylocation=prompt -o keyformat=passphrase pool/data
zfs load-key pool/data && zfs mount pool/data   # at boot
```

**macOS FileVault:**

```bash
fdesetup status
fdesetup enable     # stores a recovery key; copy it offline before closing the dialog
```

*Verify:* `cryptsetup status /dev/mapper/<name>` shows the cipher and key size; recovery key stored in offline secret store; reboot unlocks correctly.

---

## Fix D — Kernel Hardening

The single most broadly applicable section — apply on **every** Linux system.

**sysctl drop-in** — `/etc/sysctl.d/99-hardening.conf`:

```
# Network: prevent spoofing, redirects, and recon
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_rfc1337 = 1                    # TIME_WAIT assassination protection
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv6.conf.all.accept_ra = 0             # remove if using SLAAC
net.ipv6.conf.default.accept_ra = 0

# Disable IP forwarding unless this host IS a router / container host with routing
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Memory: maximize ASLR entropy
kernel.randomize_va_space = 2

# Info leaks: restrict /proc and kernel symbol addresses
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.perf_event_paranoid = 3              # disables perf for unprivileged users entirely

# ptrace: restrict to parent-only (2) or disable entirely (3)
# 1 is the default on most distros and is too weak for TM1+
kernel.yama.ptrace_scope = 2

# eBPF: major kernel attack surface — disable unprivileged access
kernel.unprivileged_bpf_disabled = 1
net.core.bpf_jit_harden = 2

# Core dumps from setuid processes
fs.suid_dumpable = 0
```

```bash
sudo sysctl --system    # apply without reboot; confirm with: sysctl kernel.kptr_restrict
```

**Module blacklist** — `/etc/modprobe.d/99-blacklist-unused.conf`:

```
# Rare filesystems — common exploit payload delivery path
install cramfs /bin/false
install freevxfs /bin/false
install jffs2 /bin/false
install hfs /bin/false
install hfsplus /bin/false
install udf /bin/false

# Unusual network protocols — each is an attack surface you probably don't need
install dccp /bin/false
install sctp /bin/false
install rds /bin/false
install tipc /bin/false
install n-hdlc /bin/false
install ax25 /bin/false
install netrom /bin/false
install x25 /bin/false
install rose /bin/false
install decnet /bin/false
install atm /bin/false

# Bluetooth (remove these lines if Bluetooth is needed)
install bluetooth /bin/false
install btusb /bin/false

# Firewire / Thunderbolt DMA (physical-access attack vector; remove if you use TB peripherals)
install firewire-core /bin/false
install firewire-ohci /bin/false
```

**Kernel lockdown (Linux 5.4+)** — prevents modifying a running kernel even as root; only meaningful when Secure Boot is enforcing:

```bash
cat /sys/kernel/security/lockdown    # check support

# Set via kernel command line in GRUB or systemd-boot:
# lockdown=integrity        prevents loading unsigned modules, writing /dev/mem
# lockdown=confidentiality  also prevents reading /dev/mem, unencrypted hibernate
```

**FreeBSD** — `/etc/sysctl.conf`:

```
security.bsd.see_other_uids=0          # users cannot see other users' processes
security.bsd.see_other_gids=0
security.bsd.hardlink_check_uid=1      # prevent hardlink-based privilege escalation
security.bsd.hardlink_check_gid=1
security.bsd.unprivileged_proc_debug=0
kern.randompid=1
kern.sugid_coredump=0
net.inet.ip.redirect=0
net.inet.ip.sourceroute=0
net.inet.tcp.blackhole=2               # silently drop to closed ports (limits port-scan signal)
net.inet.udp.blackhole=1
net.inet6.ip6.redirect=0
```

**OpenBSD** — `/etc/sysctl.conf`:

```
kern.securelevel=1   # prevents /dev/mem access and unsigned module loading after boot
                     # level 2: also prevents raw disk writes and immutable-flag changes
```

---

## Fix E — Authentication & Access Control

**SSH hardening** — `/etc/ssh/sshd_config.d/10-hardening.conf`:

```
PermitRootLogin no
AuthenticationMethods publickey
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
X11Forwarding no
AllowAgentForwarding no      # re-enable only on designated jump hosts
AllowTcpForwarding no        # re-enable only where tunneling is explicitly needed
GatewayPorts no
LoginGraceTime 30
MaxAuthTries 3
MaxSessions 2
ClientAliveInterval 300
ClientAliveCountMax 2
LogLevel VERBOSE             # records key fingerprints; needed to detect key-based brute force
AllowUsers <user>            # explicit allowlist — omitting this means any valid account can attempt

# Modern algorithms only (verify your OpenSSH version supports these before deploying)
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256
```

```bash
sudo sshd -t    # validate config before reloading; a broken config locks you out
```

**Preferred posture — no public SSH.** Admin via WireGuard VPN; provider console = out-of-band break-glass. This removes the entire access plane from the public internet. See [[ssh]] and [[fail2ban]] if public SSH is unavoidable.

**PAM — password quality** — `/etc/security/pwquality.conf`:

```
minlen = 14
dcredit = -1      # require at least 1 digit
ucredit = -1      # require at least 1 uppercase
ocredit = -1      # require at least 1 special character
lcredit = -1      # require at least 1 lowercase
maxrepeat = 3
gecoscheck = 1    # reject passwords containing the account name
dictcheck = 1
enforcing = 1
```

**PAM — account lockout** — `/etc/security/faillock.conf`:

```
deny = 5
unlock_time = 900
even_deny_root = true
root_unlock_time = 60
```

**sudo hardening** — `/etc/sudoers.d/99-hardening` (edit with `visudo -f`):

```
Defaults env_reset
Defaults mail_badpass
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Defaults logfile=/var/log/sudo.log
Defaults use_pty           # prevents sudo from being used in backgrounded non-interactive scripts
# Defaults log_input,log_output    # TM2+: full session recording; requires sudoreplay
```

**User account audit:**

```bash
# Accounts with empty or locked-but-loginable passwords
sudo awk -F: '($2 == "" || $2 == "!!") {print $1}' /etc/shadow

# UID 0 accounts other than root
awk -F: '($3 == 0) {print $1}' /etc/passwd

# SUID/SGID binaries — review anything not traceable to a known package
sudo find / -perm /6000 -type f 2>/dev/null | sort

# World-writable directories outside expected temp paths
sudo find / -xdev -type d -perm -0002 2>/dev/null | grep -v '/tmp\|/var/tmp\|/proc\|/sys'
```

**Login defaults** — `/etc/login.defs`:

```
PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_WARN_AGE   14
LOGIN_RETRIES   3
LOGIN_TIMEOUT   60
UMASK           027
```

---

## Fix F — Network & Firewall

Default-deny on **both** ingress and egress. Run both the provider/cloud security group AND a host-level firewall — they are different trust boundaries with different failure modes.

**nftables (modern Linux)** — `/etc/nftables.conf`:

```nft
#!/usr/sbin/nft -f
flush ruleset

table inet filter {
    chain input {
        type filter hook input priority filter; policy drop;

        ct state invalid drop
        ct state established,related accept

        iif lo accept

        ip protocol icmp icmp type { echo-request, destination-unreachable, time-exceeded } accept
        ip6 nexthdr icmpv6 icmpv6 type { echo-request, destination-unreachable, nd-neighbor-solicit, nd-neighbor-advert, nd-router-advert } accept

        tcp dport <service-port> accept       # add only what this host actually serves
        tcp dport <ssh-port> accept           # restrict source IP with: ip saddr <mgmt-ip>

        # log prefix "[nft-drop] " drop       # uncomment for TM1+ to log rejected inbound
    }

    chain forward {
        type filter hook forward priority filter; policy drop;
    }

    chain output {
        type filter hook output priority filter; policy drop;

        ct state established,related accept
        oif lo accept

        # Permit only what this host legitimately originates
        tcp dport { 53, 80, 443 } accept
        udp dport { 53, 123 } accept          # DNS, NTP
        # tcp dport <workload-upstream-port> accept
    }
}
```

See [[iptables]] for the equivalent iptables command reference.

**pf (FreeBSD / OpenBSD)** — `/etc/pf.conf`:

```pf
ext_if = "em0"

set block-policy drop
set skip on lo

block all

pass in quick on $ext_if proto tcp to ($ext_if) port <service-port> keep state
pass in quick on $ext_if proto tcp to ($ext_if) port <ssh-port> keep state

pass out quick on $ext_if proto { tcp udp } to any port { 53 80 443 123 } keep state

pass in quick on $ext_if proto icmp icmp-type echoreq
pass out quick on $ext_if proto icmp keep state
```

```bash
pfctl -nf /etc/pf.conf    # syntax check without loading
pfctl -f /etc/pf.conf     # load
pfctl -e                  # enable
```

**Service binding** — every daemon that doesn't need to be public should bind to `127.0.0.1` or a specific interface:

```bash
ss -tlnp | grep '0.0.0.0'    # anything here that shouldn't be public is misconfiguration
```

**IPv6** — disable if genuinely unused rather than leaving it unguarded:

```
# add to /etc/sysctl.d/99-hardening.conf
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

**Disable unnecessary network services:**

```bash
sudo systemctl disable --now avahi-daemon cups bluetooth ModemManager nfs-server rpcbind
ss -tlnp && ss -ulnp    # confirm the surface shrank
```

*Verify:* from an external host, `nmap -Pn <host>` or `nc -zv <host> <port>` (see [[nc]]) shows only the intended ports; rules persist after a reboot.

---

## Fix G — Services & Process Isolation

**Inventory and remove unnecessary services:**

```bash
systemctl list-units --type=service --state=running --no-pager
# For each service not required by this host's role:
sudo systemctl disable --now <svc>
sudo systemctl mask <svc>      # mask prevents it from being started even as a dependency
```

**Dedicated service accounts** — every daemon runs as its own unprivileged system user:

```bash
sudo useradd --system --no-create-home --shell /sbin/nologin <svc-user>
```

**systemd unit sandboxing** — additive drop-in at `/etc/systemd/system/<unit>.d/hardening.conf`; survives package upgrades (never use `systemctl edit --full` on rolling/transactional distros — it creates a full override that gets clobbered on upgrade). See [[systemd.exec]] for directive meanings:

```ini
[Service]
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/<svc>       # only what this unit must write; narrow aggressively
PrivateTmp=true
PrivateDevices=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
RestrictNamespaces=true
LockPersonality=true
MemoryDenyWriteExecute=true         # drop for JVM, V8, LuaJIT, or any JIT-compiling runtime
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM
CapabilityBoundingSet=              # empty = no capabilities; add back only what's documented as needed
UMask=0077
```

```bash
sudo systemctl daemon-reload
sudo systemd-analyze security <unit>    # green directive list is the goal; the score is secondary
```

A network-bound daemon floors around 1.5 on the score — that is not a regression; breaking `AF_INET` to chase a lower number is. See [[systemd.exec]] § Gotchas.

**Resource limits** — prevent a runaway process from consuming the host:

```ini
[Service]
LimitNOFILE=1024
LimitNPROC=256
MemoryMax=512M
CPUQuota=50%
```

**FreeBSD jails** — a stronger isolation boundary than Linux namespaces for long-running services:

```bash
# /etc/jail.conf
<jail-name> {
    host.hostname = "<jail-name>";
    ip4.addr = <jail-ip>;
    path = "/jails/<jail-name>";
    exec.start = "/bin/sh /etc/rc";
    exec.stop = "/bin/sh /etc/rc.shutdown";
    devfs_ruleset = 4;
    mount.devfs;
}
```

```bash
sysrc jail_enable=YES
service jail start <jail-name>
```

---

## Fix H — Mandatory Access Control

Never disable your distro's default MAC to "make something work" — that something is usually the workload you most want confined.

**AppArmor (Debian / Ubuntu — on by default):**

```bash
sudo aa-status                                    # confirm profiles loaded and enforcing
sudo aa-status | grep "complain mode"             # complain-mode profiles are not enforcing

# Generate a profile for a custom binary
sudo aa-genprof /path/to/binary                   # run under aa-genprof, approve/deny calls interactively

# Reload after editing a profile
sudo apparmor_parser -r /etc/apparmor.d/<profile>
```

**SELinux (RHEL / CentOS / Fedora — enforcing by default):**

```bash
getenforce          # must return "Enforcing" on a production system
sestatus

# NEVER set SELINUX=disabled in /etc/selinux/config — it disables all kernel labeling
# NEVER run setenforce 0 on production — it is not "temporary", it's off until reboot

# Diagnose a denial without disabling
sudo ausearch -m avc -ts recent | audit2why

# Generate a targeted policy module for a specific denial; review before loading
sudo ausearch -m avc -ts recent | audit2allow -M <module-name>
sudo semodule -i <module-name>.pp
```

**OpenBSD — pledge / unveil (per-process, compile-time API):**

`pledge()` restricts the syscalls a process may invoke; `unveil()` restricts filesystem access to named paths. Both are irrevocable once set — a compromised process cannot widen its own sandbox. Base system binaries use them; you inherit the protection automatically. When writing software for OpenBSD, use both.

```bash
doas sysctl kern.proc.pledge.<pid>    # inspect a running process's current pledges
```

**FreeBSD Capsicum:**

Base system binaries use Capsicum by default. It is a per-binary API applied at compile time; as an operator you primarily inherit it rather than configure it. Third-party ports vary.

---

## Fix I — Audit & Logging

**auditd ruleset** — `/etc/audit/rules.d/99-hardening.rules`:

```
-b 8192          # event buffer; increase if auditd reports "backlog limit exceeded"
-f 1             # failure mode: 1=printk, 2=kernel panic (TM2+ only — very disruptive)

# Identity and credential files
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/sudoers -p wa -k sudoers
-w /etc/sudoers.d/ -p wa -k sudoers
-w /etc/ssh/sshd_config -p wa -k sshd_config

# Privilege escalation executables
-a always,exit -F path=/usr/bin/sudo -F perm=x -F auid>=1000 -F auid!=4294967295 -k priv_esc
-a always,exit -F path=/usr/bin/su -F perm=x -F auid>=1000 -F auid!=4294967295 -k priv_esc
-a always,exit -F path=/usr/bin/passwd -F perm=x -F auid>=1000 -k priv_esc

# User and group modification
-a always,exit -F path=/usr/sbin/useradd -F perm=x -k user_mod
-a always,exit -F path=/usr/sbin/userdel -F perm=x -k user_mod
-a always,exit -F path=/usr/sbin/usermod -F perm=x -k user_mod
-a always,exit -F path=/usr/sbin/groupadd -F perm=x -k user_mod

# Kernel module loading
-w /sbin/insmod -p x -k module_load
-w /sbin/rmmod -p x -k module_load
-w /sbin/modprobe -p x -k module_load
-a always,exit -F arch=b64 -S init_module,finit_module -S delete_module -k module_load

# Network configuration changes
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k network_cfg
-w /etc/hosts -p wa -k network_cfg
-w /etc/network/ -p wa -k network_cfg

# Login / session tracking
-w /var/log/wtmp -p wa -k logins
-w /var/log/btmp -p wa -k logins
-w /var/log/lastlog -p wa -k logins

# Time tampering
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time_change
-w /etc/localtime -p wa -k time_change

# Filesystem mounts by unprivileged users
-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts

# Make ruleset immutable — must reboot to change audit config after this
# Only enable once the ruleset is stable
# -e 2
```

```bash
sudo augenrules --check && sudo augenrules --load
sudo systemctl enable --now auditd
```

**Remote log shipping** — a local log that an attacker can clear is evidence, not integrity:

```bash
# rsyslog TCP forwarding — /etc/rsyslog.d/99-remote.conf
*.* @@<log-server>:514     # @@ = TCP; @ = UDP; use TLS (omrelp + imtls) for TM1+

# journald remote forwarding
# /etc/systemd/journal-upload.conf
[Upload]
URL=http://<log-server>:19532
```

*Verify:* write a test entry (`logger "hardening-test"`); confirm it appears on the remote log server within seconds.

---

## Fix J — File Integrity Monitoring

**AIDE** — run after all hardening steps, against the known-good state:

```bash
sudo apt install aide       # or: dnf install aide
sudo aideinit               # builds the baseline database
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

sudo aide --check           # compare current state to baseline; every diff is a finding
```

Schedule `aide --check` as a daily systemd timer or cron job; route output to the remote log server.

**Immutable flags** — for files that must not change during normal operation:

```bash
sudo chattr +i /etc/passwd /etc/shadow /etc/group /etc/gshadow
# To make a legitimate change: chattr -i; change; chattr +i; audit why it was necessary
```

---

## Fix K — Vulnerability Management

**Unattended security updates:**

```bash
# Debian/Ubuntu
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
# /etc/apt/apt.conf.d/50unattended-upgrades: confirm the security origin is present and uncommented

# RHEL family
sudo dnf install dnf-automatic
# /etc/dnf/automatic.conf: apply_updates = yes  upgrade_type = security
sudo systemctl enable --now dnf-automatic-install.timer
```

**Per-distro CVE scanning:**

```bash
sudo debsecan --suite <release> --format report   # Debian: packages with published CVEs
arch-audit -u                                      # Arch: against the Arch Security Tracker
sudo rpm -Va | grep -v "^..........  c "           # RHEL: verify package file checksums
pkg audit -F                                       # FreeBSD: against VuXML database
```

**Lynis** — comprehensive host audit; aim for a hardening index >80 before marking stable:

```bash
sudo lynis audit system
```

**OpenSCAP with CIS / STIG profiles (RHEL / Ubuntu):**

```bash
sudo oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results scan-results.xml \
  /usr/share/xml/scap/ssg/content/ssg-<distro>-ds.xml
```

---

## Fix L — Advanced Kernel Controls (TM2+)

Additional controls that meaningfully reduce the kernel attack surface at the cost of slightly constraining the OS environment.

```
# /etc/sysctl.d/99-hardening-l2.conf

# userfaultfd: useful for exploits that spray kernel objects from userspace
vm.unprivileged_userfaultfd = 0

# Disable magic SysRq entirely on servers
kernel.sysrq = 0

# Restrict perf to root (redundant if perf_event_paranoid=3 from Fix D, belt-and-suspenders)
kernel.perf_event_max_sample_rate = 1
```

**Kernel compile-time hardening** (relevant if building custom kernels):

- `CONFIG_STACKPROTECTOR_STRONG` — canary on every function with a stack buffer
- `CONFIG_FORTIFY_SOURCE` — bounds-check string/memory operations at compile time
- `CONFIG_INIT_ON_ALLOC_DEFAULT_ON` — zero-initialize heap allocations (closes many info-leak windows)
- `CONFIG_INIT_ON_FREE_DEFAULT_ON` — zero-initialize on free (prevents use-after-free data leaks)
- `CONFIG_RANDOMIZE_BASE` (KASLR) — randomize kernel load address

The **linux-hardened** kernel (Arch) and **HardenedBSD** include many of these by default.

---

## Fix M — Verified / Measured Boot (TM2+, TM3)

The chain: UEFI firmware verifies bootloader signature → bootloader verifies kernel → kernel verifies initrd → TPM PCR measurements recorded at each step. Any modification causes the TPM to refuse to release the sealed disk key, requiring manual intervention.

**dm-verity — read-only, integrity-verified root:**

```bash
sudo veritysetup status /dev/mapper/root    # check if running on a dm-verity root
```

Used by default in: Fedora CoreOS, Flatcar Container Linux, openSUSE MicroOS, ChromeOS, Android. For TM2+ servers, strongly prefer an immutable-distro base over a mutable one.

**Remote attestation (TPM2 + Keylime or similar):** the server proves its boot-chain measurements to an external verifier before being trusted with secrets. Out of scope for most deployments; relevant for TM3 and regulated environments.

---

## OS Family Addenda

### Debian / Ubuntu

- **AppArmor** is the default MAC; confirm enforcing (`aa-status`). Never disable.
- **unattended-upgrades** with the security origin (see Fix K).
- **needrestart** — detects services using outdated shared libraries after an upgrade; avoids post-patch "rebooted the kernel but the service still loads the old libssl" trap.
- **Ubuntu ≥ 22.10 SSH socket activation:** `ssh.socket` owns the port; a `Port` directive in `sshd_config` is silently ignored until `ssh.socket` is disabled. Disable the socket, then `restart` (not `reload`) ssh to pick up the new port.
  ```bash
  sudo systemctl disable --now ssh.socket
  sudo systemctl enable --now ssh
  ```
- **snap confinement:** snaps run in an AppArmor + seccomp sandbox by default; keep snapd updated separately (`snap refresh`).

### RHEL / CentOS Stream / Rocky / AlmaLinux / Fedora

- **SELinux** is the MAC; must stay in `enforcing` mode. Targeted policy is the correct default. Fix denials with `audit2allow` + targeted policy modules, not by relaxing enforcement.
- **FIPS 140 mode** — enables only NIST-approved algorithms system-wide; required for some compliance frameworks:
  ```bash
  sudo fips-mode-setup --enable
  sudo reboot
  fips-mode-setup --check
  ```
- **firewalld** — zone-based nftables front-end; set the default zone to `drop` or `block`:
  ```bash
  sudo firewall-cmd --set-default-zone=drop
  sudo firewall-cmd --permanent --add-port=<port>/tcp --zone=<zone>
  sudo firewall-cmd --reload
  ```
- **`rpm -Va`** — verifies every installed package file against the RPM database checksums; the output format `S5T` = size/hash/mtime changed; anything in `/etc` that isn't a config file (`c`) is suspicious.
- **OpenSCAP with STIG or CIS profiles** available via the `scap-security-guide` package.

### Arch Linux

- **No MAC by default.** AppArmor is available and `linux-hardened` kernel includes it; install and enforce for TM1+.
- **arch-audit** — cross-references installed packages against the Arch Linux Security Tracker:
  ```bash
  sudo pacman -S arch-audit
  arch-audit -u    # only show packages with known vulnerabilities
  ```
- **Partial upgrades are unsupported** — always `pacman -Syu` (full system sync), never `pacman -Sy <package>` alone; the latter produces a partial upgrade state that causes subtle, hard-to-diagnose failures.
- **AUR:** each package is a PKGBUILD you can read; treat it as third-party code and review it before building. AUR packages bypass package signing.
- **linux-hardened kernel:** includes upstream KSPP hardening patches plus additional controls; direct drop-in replacement for `linux`.

### Alpine Linux

- **No systemd:** uses OpenRC + BusyBox. Systemd unit sandboxing (Fix G) does not apply; use chroot, containers, or OCI runtimes for service isolation.
- **musl libc:** glibc-linked binaries do not run without a compatibility shim; source all packages from Alpine repos.
- **Minimal by default** — the attack surface is already small; keep it that way by installing nothing beyond the role.
- **`apk audit`** — checks installed file checksums against the package database.
- Best used as a container base image, where its minimalism directly reduces the image CVE count.

### NixOS

Hardening as code — the entire security posture is in `configuration.nix`, version-controlled and atomically rollbackable:

```nix
security.protectKernelImage = true;
security.lockKernelModules = true;
security.allowUserNamespaces = false;      # remove only if containers require user namespaces
security.unprivilegedUsernsClone = false;

boot.kernel.sysctl = {
  "kernel.kptr_restrict" = 2;
  "kernel.dmesg_restrict" = 1;
  "kernel.yama.ptrace_scope" = 2;
  "kernel.unprivileged_bpf_disabled" = 1;
  "net.core.bpf_jit_harden" = 2;
  "net.ipv4.conf.all.rp_filter" = 1;
  # ... the full Fix D block belongs here
};

networking.firewall.enable = true;
networking.firewall.allowedTCPPorts = [ <port> ];
networking.firewall.rejectPackets = true;   # REJECT vs DROP: REJECT fails faster; DROP is stealthier

services.openssh.settings.PermitRootLogin = "no";
services.openssh.settings.PasswordAuthentication = false;
```

- **Immutable `/nix/store`** — system binaries are read-only by construction; there is no equivalent to a system-binary replacement attack via the package manager.
- **Generations** — `nixos-rebuild switch` is atomic; boot into the previous generation if the new config is broken.

### openSUSE MicroOS / Leap / Tumbleweed

- **MicroOS:** transactional-update (atomic, read-only root); changes take effect after reboot with automatic rollback if the new snapshot fails to boot. Ideal for TM2 servers.
- **Btrfs + snapper:** automatic snapshot on every package operation; `snapper rollback` to revert.
- **AppArmor** (Leap/Tumbleweed) or **SELinux** (MicroOS option).

### FreeBSD

- **pf** — see Fix F; the most capable BSDs firewall and the origin of the design.
- **Jails** — the correct isolation primitive for multi-tenant FreeBSD servers; each jail has its own filesystem root, users, network stack, and process table.
- **ZFS boot environments** — `pkg upgrade` creates a new BE before modifying the system; boot from the prior BE if the upgrade breaks anything.
- **HardenedBSD** — a FreeBSD fork with PIE, RELRO, SafeStack, higher-entropy ASLR, and non-executable stack/heap by default. Consider for TM2+.
- **`pkg audit -F`** — fetches the VuXML database and checks installed ports for known CVEs.

### OpenBSD

- **Most secure mainstream OS by default.** Focus here is on config correctness, not control addition — the controls are already there.
- **`securelevel`** — set to 1 for servers (see Fix D); prevents root from loading unsigned modules or accessing `/dev/mem` after boot.
- **`doas`** instead of `sudo` — simpler, smaller, auditable; `/etc/doas.conf` for one-shot privilege grants.
- **`pledge()` / `unveil()`** — base system binaries use both; you inherit them. Any custom software you deploy on OpenBSD should use them.
- **W⊕X enforced kernel-wide** — no mapping can be simultaneously writable and executable; this eliminates the entire class of classic shellcode injection attacks.
- **`syspatch`** for base system security patches (binary patches, apply immediately); `pkg_add -u` for ports.

### macOS (Darwin)

- **SIP (System Integrity Protection)** — never disable. It protects `/System`, `/usr`, `/bin`, `/sbin`, and the boot process against modification by root.
- **FileVault 2** — mandatory for S6 (laptop); recommended for S5. Store the recovery key offline before closing the dialog.
- **Gatekeeper + XProtect + MRT** — kept up to date by silent background updates; do not disable.
- **Hardened Runtime** — prevents code injection into signed applications; enforced for all App Store apps.
- **Application Firewall** — enable in System Settings → Network → Firewall; enable stealth mode (don't respond to ICMP on closed ports).
- **MDM for fleet deployments** — enforce configuration via MDM (Jamf, Kandji, Mosyle) rather than scripts; profiles survive re-enrollment; scripts do not.
- **Audit** — macOS ships OpenBSM; `praudit /dev/auditpipe` for a live event stream; `/etc/security/audit_control` configures audit classes.

---

## Form Factor Addenda

### S1 — Internet-facing server

Fix A + D + E + F + G + H + I are the non-negotiable minimum; add J and K for TM1+.

- **No public SSH** is strongly preferred. If unavoidable: non-standard port, `AllowUsers`, `MaxAuthTries 3`, [[fail2ban]], geo-restrict at the edge firewall.
- **Egress constraint is mandatory** — a single-purpose internet-facing server has a defined egress profile (workload upstreams + NTP + DNS + ACME); block everything else. Exfiltration and C2 both require unrestricted egress.
- Double-firewall (provider security group + host nftables/pf); both must persist a reboot.
- See [[Hardened Golden Base Image for a Single-Purpose Host]] for the full reproducible-image build pattern, and [[Hardened Syncthing Node on an Untrusted Host]] for an end-to-end concrete example.

### S2 — Internal server

- Lower internet exposure; the primary risk model is lateral movement from a compromised peer or insider.
- Host firewall (Fix F): restrict inbound to the management subnet and the specific source IPs that legitimately reach this server. Default-deny on both directions still applies.
- MAC (Fix H) is especially important in co-located environments — a breach on one service should not move to another service sharing the host.
- No internet-routable IPs on service interfaces; management on a dedicated VLAN.

### S3 — VM guest / cloud instance

- Accept the hypervisor in the TCB; don't build controls that assume the host operator is untrusted.
- **Cloud metadata service** (`169.254.169.254`): restrict access from unprivileged processes; use IMDSv2 on AWS (requires PUT token, not just GET). Exposed to SSRF if reachable from a web workload.
  ```bash
  # Block metadata service from all non-root processes
  sudo nft add rule inet filter output ip daddr 169.254.169.254 skuid != 0 drop
  ```
- Cloud security group = outer firewall; host nftables/pf = inner firewall. Run both — they fail differently.
- Snapshots can contain secrets in memory and swap; understand your provider's snapshot isolation model before taking one of a running instance.

### S4 — Container host

- **Host kernel hardening (Fix D) is critical** — all containers share the kernel; a kernel exploit in one container affects the entire host.
- **Rootless containers** (Podman, rootless Docker): container root maps to an unprivileged host UID; prefer for all non-privileged workloads.
- **Never `--privileged`** — it removes all namespace isolation and grants full host access. Use specific `--cap-add` with the minimum capability instead.
- **Seccomp profiles:** Docker and Podman apply a default profile; never use `--security-opt seccomp=unconfined`.
- **AppArmor / SELinux container profiles:** `docker-default` AppArmor profile is applied automatically; on RHEL, `container_t` / `container_file_t` SELinux labels constrain containers to their expected access patterns.
- **`--read-only`:** mount the container filesystem read-only; attach writable tmpfs only for ephemeral state.
- **gVisor (`runsc`):** OCI-compatible container runtime with a user-space kernel intercept; strong isolation for untrusted workloads at the cost of syscall overhead.

### S5 — Workstation / Desktop

- FDE (Fix C) recommended; mandatory if the machine ever leaves a physically secured space.
- **Screen lock on idle and lid close:**
  ```bash
  gsettings set org.gnome.desktop.screensaver lock-enabled true
  gsettings set org.gnome.desktop.session idle-delay 300
  ```
- **USB / Thunderbolt control** — `usbguard` to whitelist known-good devices:
  ```bash
  sudo apt install usbguard
  sudo usbguard generate-policy > /etc/usbguard/rules.conf   # baseline from currently-connected devices
  sudo systemctl enable --now usbguard
  ```
- **Application sandboxing:** Flatpak apps run in a Bubblewrap sandbox by default; `firejail` for system-installed browsers and document viewers.
- Host firewall (Fix F) still applies; inbound default-deny; outbound is less constrained than a server but should be audited.

### S6 — Laptop

Everything in S5, plus:

- **FDE is mandatory** — a laptop is a high-probability theft target; without FDE the disk is fully readable from any live OS in under two minutes.
- **TPM2-sealed key (Fix B + C):** disk unlocks automatically when the boot chain is unmodified; PIN or passphrase required if the measurement changes (BIOS update, kernel change, Secure Boot toggle). Belt-and-suspenders: `systemd-cryptenroll --tpm2-device=auto --tpm2-with-pin`.
- **Encrypted swap / no unencrypted hibernate** — suspend-to-disk leaks RAM; either disable hibernate or ensure swap is on the LUKS volume.
- **MAC address randomization** — prevents cross-network tracking:
  ```bash
  nmcli connection modify <conn> wifi.cloned-mac-address random
  nmcli connection modify <conn> 802-3-ethernet.cloned-mac-address random
  ```
- **Always-on VPN on untrusted networks** — enforce DNS through the VPN tunnel; split-tunnel only when the local network is explicitly trusted.
- **BIOS password (Fix B) is required** — without it, physical access allows changing boot order and booting from USB, bypassing FDE.

### S7 — Network Appliance / Router / Firewall

- **Management plane isolation** — SSH or console only on a dedicated out-of-band management interface or VLAN; no management on the data-plane interfaces.
- **Control plane protection** — rate-limit traffic destined for the CPU (routing protocol hellos, SSH, ICMP); prevent CPU exhaustion from a sustained DoS:
  ```bash
  # Linux-based appliance: limit new SSH connections
  sudo nft add rule inet filter input tcp dport 22 ct state new limit rate 10/minute accept
  ```
- **Routing protocol authentication:** BGP with TCP-AO (preferred) or MD5; OSPF with SHA-256; unauthenticated routing protocol sessions are a BGP hijack waiting to happen.
- **uRPF (Unicast Reverse Path Forwarding):** drop packets arriving on an interface where the source address is not reachable back via that interface — the primary defense against IP spoofing on the data plane.
  ```
  net.ipv4.conf.all.rp_filter = 1    # strict mode; use loose (2) only if asymmetric routing
  ```
- **Disable CDP/LLDP on external-facing interfaces** — they advertise platform and topology details to adjacent devices.
- **Automated configuration backup** — off-device, version-controlled; a network device that loses its config is an immediate outage.

### S8 — Embedded / IoT

- **Assume unpatched in the field.** Design the attack surface at build time; post-deployment patching is rare and often impossible.
- **Verified/signed firmware** via the platform's secure boot chain (TrustZone on ARM, eFuse-based secure boot on Broadcom/Qualcomm SoCs).
- **No default credentials** — the defining failure mode of embedded security. Randomize per-device; derive from hardware ID + manufacturing salt; provision at the factory, never at first boot from a shared secret.
- **Read-only rootfs** — `overlayfs` for ephemeral writes; `dm-verity` for integrity verification:
  ```bash
  mount | grep ' on / '    # root should show ro (read-only)
  ```
- **Disable debug interfaces at production build time** — JTAG, UART console, USB debug mode. Each is a backdoor that bypasses all software controls.
- **Minimal kernel config** — build only the drivers, filesystems, and protocol modules the device actually uses; everything else is attack surface.
- **Hardware security enclave (TPM, SE, eSE)** — store keys in hardware; they should never be extractable as plaintext by software.

---

## Validation

Run these after hardening; anything unexpected from the established baseline is a finding.

```bash
# Listening services — only intended ports and interfaces
ss -tlnp && ss -ulnp

# SUID/SGID binaries — review anything not traceable to a known package
sudo find / -perm /6000 -type f 2>/dev/null | sort

# World-writable directories outside expected temp paths
sudo find / -xdev -type d -perm -0002 2>/dev/null | grep -v '/tmp\|/var/tmp\|/proc\|/sys'

# Empty or unusable password slots
sudo awk -F: '($2 == "" || $2 == "!!") {print $1}' /etc/shadow

# UID 0 accounts other than root
awk -F: '($3 == 0) {print $1}' /etc/passwd

# Firewall — default-deny is active
sudo nft list ruleset        # Linux nftables
sudo pfctl -sr               # BSD pf

# Kernel sysctl — confirm critical values survived reboot
sudo sysctl kernel.kptr_restrict kernel.dmesg_restrict kernel.yama.ptrace_scope \
           net.ipv4.conf.all.rp_filter net.ipv4.ip_forward \
           kernel.unprivileged_bpf_disabled

# SSH config validation
sudo sshd -t && echo "sshd config valid"

# systemd unit sandbox scores (run for each workload service)
systemd-analyze security <unit>

# Lynis comprehensive audit
sudo lynis audit system
```

*External reachability check from a separate host (see [[nc]]):*

```bash
nmap -Pn -sT -p 1-65535 <host>    # only configured ports should respond
```

---

## Escalation / After-action

**Establish the baseline immediately after hardening is complete:**

```bash
sudo aide --init
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

**Document this run** — record which sections were applied, which were consciously skipped, and why. The threat model you chose is context that won't be obvious from the configuration alone.

**Maintenance rhythm:**

| Frequency | Action |
|---|---|
| Daily | Confirm unattended security updates are running; confirm log ship to remote is live |
| Weekly | `arch-audit -u` / `debsecan` / `pkg audit -F` for newly-published CVEs |
| Monthly | Re-audit listening services, user accounts, sudo grants, and SUID list for drift |
| Quarterly | Re-run Lynis; compare hardening index to the previous baseline; address regressions |
| On role change | Re-run the decision table — a server's profile and threat model change when its role does |
| After kernel / major OS update | Verify sysctl values and module blacklist survived; re-run `systemd-analyze security` for sandboxed units |

**If you find an unexpected change:** treat it as a potential incident until proven benign. Run `sudo aide --check`, pull the relevant `auditd` log window, cross-reference with the remote log server, and check `last` / `lastb` for authentication anomalies.

---

## See also

- **[[Hardened Golden Base Image for a Single-Purpose Host]]** — the reproducible-image build pattern for internet-facing single-purpose servers; the full workflow for applying this playbook at image-build time
- **[[Hardened Syncthing Node on an Untrusted Host]]** — this playbook applied end-to-end to a concrete workload
- [[systemd.exec]] (unit sandbox directives reference) · [[ssh]] (client configuration) · [[fail2ban]] · [[iptables]] · [[btrfs]] · [[nc]] (reachability testing) · [[syncthing]]
