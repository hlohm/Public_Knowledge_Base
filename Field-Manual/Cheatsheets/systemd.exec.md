---
type: cheatsheet
area: Linux Administration
aliases: [systemd-hardening, sandboxing, ProtectSystem, CapabilityBoundingSet, SystemCallFilter]
tags: [systemd, hardening, sandbox, capabilities, seccomp]
status: working
---

# systemd.exec

> **Area:** [[Linux Administration]]

The hardening / sandboxing directives a systemd unit applies to a process — capabilities,
seccomp syscall filtering, and namespace isolation — plus how to read them, test them, and
diagnose the denials they cause. The companion to [[systemd]] (which covers `systemctl` /
`journalctl` management) and the reference for the "tighten to taste" lines in
[[systemd Service and Timer]].

> Directives documented in `man systemd.exec`. The whole-system view is `man systemd.directives`.

---

## 1. The three layers (what actually denies your process)

A hardened unit stacks **three independent kernel mechanisms**. They are not one system, and
none of them is AppArmor/SELinux (those are a separate LSM layer with their own policy files,
orthogonal to everything here). Each fails with its own error, which is the whole game when
debugging — see §5.

```ini
# LAYER 1 — Linux capabilities: split "root" into ~40 separate privileges.
# CapabilityBoundingSet is a CEILING; a uid-0 process cannot exceed it even though it is root.
CapabilityBoundingSet=CAP_NET_RAW CAP_SYS_ADMIN   # the only caps this unit may ever hold
AmbientCapabilities=CAP_NET_BIND_SERVICE          # caps GRANTED to a non-root (User=) process
NoNewPrivileges=yes                               # block regaining privs via setuid/file caps

# LAYER 2 — seccomp: allow-list which syscalls the process may make AT ALL.
SystemCallFilter=@system-service @mount           # predefined sets; a blocked call is refused
SystemCallErrorNumber=EPERM                        # return EPERM instead of killing with SIGSYS
SystemCallArchitectures=native                     # forbid foreign-arch syscall ABIs

# LAYER 3 — namespaces / filesystem & device isolation: change what the process can SEE.
ProtectSystem=strict                               # whole FS read-only except ReadWritePaths
ProtectHome=true                                   # /home, /root, /run/user hidden
PrivateTmp=true                                    # private /tmp, unshared with the host
PrivateDevices=yes                                 # stripped /dev: no physical block devices
ReadWritePaths=/var/lib/myapp                      # the carve-outs ProtectSystem=strict allows
```

**Why the distinction matters:** a missing *capability* and a blocked *syscall* and a
*read-only mount* all stop your process, but they are fixed by three different directives and
they announce themselves with different errnos. Identify the layer first, then reach for the
right knob.

---

## 2. Capabilities (Layer 1)

```bash
# What caps does the unit actually grant right now? (the LOADED, in-memory value)
systemctl show <unit> -p CapabilityBoundingSet -p AmbientCapabilities -p User

# Decode a cap name / number
capsh --decode=0x...            # bitmask -> names
man capabilities                # the full list with what each one bypasses
```

Key facts:

- **Root + bounding set = effective caps.** For a `User=`-less (root) unit, the bounding set
  *is* the effective capability set. Tighten the bounding set and you take privileges away from
  root itself.
- **`AmbientCapabilities` is for non-root units.** It hands specific caps to a `User=nobody`
  style process. A root unit ignores it — don't add it expecting it to "boost" root.
- **Bounding-set lines UNION across drop-ins (OR).** A drop-in `CapabilityBoundingSet=CAP_X`
  *adds* `CAP_X` to whatever the vendor unit already set — it does not replace it. This is what
  makes additive `/etc` drop-ins work (see §4).
- **`~` inverts.** `CapabilityBoundingSet=~CAP_SYS_ADMIN` means "everything *except* SYS_ADMIN".

The two DAC-bypass caps that bite most often:

| Cap | Bypasses | You need it when… |
| --- | --- | --- |
| `CAP_DAC_OVERRIDE` | read/write/execute permission checks | writing where file perms would say no |
| `CAP_DAC_READ_SEARCH` | read + directory-traverse checks | reading/walking where perms would say no |
| `CAP_FOWNER` | owner-gated ops (chmod, utime on files you don't own) | rarely — narrower than it looks |

---

## 3. seccomp (Layer 2)

```bash
# Is the unit filtering syscalls, and how does it surface a block?
systemctl show <unit> -p SystemCallFilter -p SystemCallErrorNumber -p SystemCallArchitectures

# List what a predefined set contains
systemd-analyze syscall-filter @system-service    # members of a @group
systemd-analyze syscall-filter                     # all groups
```

Key facts:

- **Allow-list semantics by default.** `SystemCallFilter=@system-service @mount` permits *only*
  those groups; everything else is blocked. A leading `~` flips it to a deny-list.
- **Allow-list lines UNION across drop-ins.** Add the one missing syscall in a drop-in without
  restating the vendor's whole set: `SystemCallFilter=@…` accumulates.
- **`SystemCallErrorNumber` changes the symptom.** With it unset, a blocked call **kills the
  process with SIGSYS** ("Bad system call"). Set to `EPERM`, the call instead *returns* EPERM —
  which disguises a seccomp block as a permission error. This single line is why seccomp and
  capability failures get confused (see §5).
- **ioctl can't be filtered by request.** seccomp filters by syscall number, not ioctl command,
  so an ioctl-driven operation (like a btrfs subvolume op) is never blocked by the filter
  itself — only the *helper* syscalls around it can be.

---

## 4. Namespace & filesystem isolation (Layer 3)

```bash
# What's hidden / read-only for this unit?
systemctl show <unit> -p ProtectSystem -p ProtectHome -p PrivateDevices \
  -p ReadWritePaths -p PrivateTmp -p RestrictAddressFamilies
```

The high-impact ones:

| Directive | Effect | Common reason to relax it |
| --- | --- | --- |
| `ProtectSystem=strict` | entire FS read-only | add `ReadWritePaths=` for the dirs it must write |
| `ProtectHome=true` | `/home`, `/root` invisible | a tool that legitimately reads a home dir |
| `PrivateDevices=yes` | no physical `/dev` block devices | **filesystem tooling** (btrfs/LVM/ZFS) needs `=no` |
| `PrivateTmp=yes` | private `/tmp` & `/var/tmp` | IPC via a well-known `/tmp` socket |
| `RestrictAddressFamilies=` | allowed socket families | needs `AF_NETLINK` for many admin tools |
| `ProtectKernelModules=yes` | can't load modules | a hook that must `modprobe` on demand |

`PrivateDevices=no` is the classic gotcha for any unit that snapshots a filesystem: the
snapshot/volume tooling needs to see the real block devices, which the private `/dev` strips.

---

## 5. Diagnosing a sandbox denial (the method)

The errno tells you which layer. Read it first — it saves the guessing.

| Symptom | errno | Most likely layer | First knob to try |
| --- | --- | --- | --- |
| `Permission denied` | EACCES (13) | **DAC** check failed | `CAP_DAC_OVERRIDE` / `CAP_DAC_READ_SEARCH` (or real file perms) |
| `Operation not permitted` | EPERM (1) | capability **or** seccomp* | the privileged op's cap (e.g. `CAP_SYS_ADMIN`); or a `SystemCallFilter` addition |
| Killed, `Bad system call` | SIGSYS | **seccomp**, default action | add the syscall to `SystemCallFilter` |
| `Read-only file system` | EROFS (30) | namespace isolation | `ReadWritePaths=` / relax `ProtectSystem` |

\* EPERM is ambiguous: it covers both "missing capability for a privileged operation" **and**
"seccomp-blocked syscall *when the unit sets `SystemCallErrorNumber=EPERM`*". Disambiguate with
the clean-room test below.

**The discriminator that cracks the ambiguous cases:** if the unit sets
`SystemCallErrorNumber=EPERM`, then a `Permission denied` (EACCES) string is **not** your
seccomp filter — seccomp would have said `Operation not permitted` (EPERM). EACCES therefore
points at a real DAC check, i.e. a missing `CAP_DAC_*`, not the syscall filter.

### Procedure

- [ ] **Read the errno, not just the word.** Map the exact string via the table above. EACCES
      and EPERM are different errors that print almost-identical English.
- [ ] **Dump the loaded sandbox** for the failing unit:
      ```bash
      systemctl show <unit> \
        -p CapabilityBoundingSet -p AmbientCapabilities -p User \
        -p SystemCallFilter -p SystemCallErrorNumber \
        -p ProtectSystem -p ProtectHome -p PrivateDevices -p ReadWritePaths
      ```
- [ ] **Get the exposure breakdown** — scores every setting, flags the dangerous-vs-safe ones:
      ```bash
      systemd-analyze security <unit>
      ```
- [ ] **Reproduce in a clean room.** Run the failing command under `systemd-run` with the *same*
      sandbox, then toggle ONE directive. This isolates the responsible layer:
      ```bash
      # Reproduce under the unit's exact effective sandbox (expect the same failure)
      sudo systemd-run --pty --collect --wait \
        -p CapabilityBoundingSet='<the vendor set> CAP_SYS_ADMIN' \
        -p PrivateDevices=no \
        -p SystemCallFilter='@system-service @mount' \
        -p SystemCallErrorNumber=EPERM \
        -- /usr/bin/yourtool …
      ```
- [ ] **Toggle one layer at a time.** Drop `SystemCallFilter` → if it now works, it was seccomp.
      Add a `CAP_*` → if it works, it was capabilities. Set `PrivateDevices=no` → if it works,
      it was device isolation.
      > **Footgun:** `-p CapabilityBoundingSet=CAP_X` *alone* sets the ceiling to ONLY `CAP_X`,
      > silently stripping every other root cap (including `CAP_DAC_OVERRIDE`). A "no-sandbox"
      > control built this way is **not** clean — it's still cap-restricted. To test the true
      > baseline, run the bare command with full root and no `systemd-run` at all.
- [ ] **Pin the exact syscall (if seccomp is suspected)** with strace *outside* the sandbox —
      where it succeeds — to see which call the filter would block:
      ```bash
      sudo strace -f -e trace=openat2,clone3,fsopen,move_mount yourtool … 2>&1 | grep -v ENOENT
      ```
- [ ] **Apply the minimal fix as an `/etc` drop-in** (§6), `daemon-reload`, and verify with a
      real run — not just `systemctl show`.

---

## 6. Drop-in mechanics (making a fix durable)

```bash
# Create / edit an additive drop-in (never edit the vendor unit)
sudo systemctl edit <unit>            # opens /etc/systemd/system/<unit>.d/override.conf
sudoedit /etc/systemd/system/<unit>.service.d/10-capabilities.conf   # or a named drop-in

# After ANY unit/drop-in change — load it into the running manager
sudo systemctl daemon-reload

# Confirm the merged result, then run for real
systemctl show <unit> -p CapabilityBoundingSet
sudo systemctl start <unit> && journalctl -fu <unit>
```

Rules that matter:

- **`/etc`, never the vendor file.** A drop-in under `/etc/systemd/system/<unit>.d/` survives
  package upgrades; an `edit --full` or an edit to `/usr/lib/systemd/system/<unit>` gets
  re-shipped and clobbered on the next update. (Especially true on rolling distros.)
- **File presence ≠ active config.** A drop-in on disk does nothing until a `daemon-reload`
  pulls it into the running manager. `systemctl show` reports the *loaded* value, so it can
  look correct while the last *run* still used the old, unreloaded config. After editing →
  `daemon-reload` → run to verify.
- **Additive directives union; assignment directives replace.** `CapabilityBoundingSet=` and
  allow-list `SystemCallFilter=` accumulate across drop-ins (good — add just what's missing).
  Scalar directives like `ProtectSystem=` are last-write-wins.
- **Empty value = reset.** `SystemCallFilter=` (nothing after the `=`) clears the inherited
  list before your next line, when you genuinely need to start over rather than add.

---

## 7. Daily workflows

### "Permission denied" from a hardened unit
```bash
systemctl show <unit> -p CapabilityBoundingSet -p SystemCallErrorNumber   # EACCES? cap, not seccomp
systemd-analyze security <unit>                                            # what's stripped
# EACCES -> DAC check -> add CAP_DAC_OVERRIDE in an /etc drop-in:
printf '[Service]\nCapabilityBoundingSet=CAP_DAC_OVERRIDE\n' \
  | sudo tee /etc/systemd/system/<unit>.d/30-dac.conf
sudo systemctl daemon-reload && sudo systemctl start <unit>
```

### Filesystem tool fails only inside the unit
```bash
# btrfs/LVM/ZFS snapshot hooks: the private /dev hides the block devices
sudo systemctl edit <unit>     # add:  [Service]\nPrivateDevices=no
sudo systemctl daemon-reload
```

### Audit a unit's exposure before trusting it
```bash
systemd-analyze security <unit>          # 0.0 (perfect) … 10.0 (exposed); per-setting reasons
systemd-analyze verify /etc/systemd/system/<unit>.service   # lint the unit file
```

### Harden a unit from scratch
```bash
# Start strict, run it, loosen only what breaks (read the journal each round)
# ProtectSystem=strict + ReadWritePaths=<dirs> + NoNewPrivileges=yes is the high-value core.
systemd-analyze security <unit>          # re-check the score after each loosening
```

---

## 8. Files & locations

| Path | Purpose |
| --- | --- |
| `/usr/lib/systemd/system/<unit>` | vendor unit — **don't edit**; gets re-shipped |
| `/etc/systemd/system/<unit>.d/*.conf` | your additive drop-ins — the durable place to fix |
| `/etc/systemd/system/<unit>` | full local override of the vendor unit (heavier hammer) |
| `man systemd.exec` | every sandboxing directive, authoritative |
| `man capabilities` | the capability list + what each one bypasses |

---

## Gotchas / Golden rules

1. **Read the errno, not the word.** `Permission denied` (EACCES) and `Operation not permitted`
   (EPERM) are *different* failures pointing at *different* layers. The string is the first clue.
2. **A `CapabilityBoundingSet=X` test strips every other cap.** Your "control" run is only clean
   if it's bare root with no `systemd-run` sandbox at all. Otherwise you're testing a different
   restriction than you think.
3. **`SystemCallErrorNumber=EPERM` disguises seccomp as a permission error.** If a unit sets it,
   an EACCES string rules seccomp *out* (seccomp would emit EPERM).
4. **Drop-in on disk ≠ active.** No `daemon-reload`, no effect. `systemctl show` tells you about
   *now*, not about the last run — verify with an actual run.
5. **`/etc` drop-ins survive upgrades; vendor-unit edits don't.** Make the fix additive and put
   it under `/etc/systemd/system/<unit>.d/`.
6. **Filesystem tooling needs `PrivateDevices=no`.** btrfs/LVM/ZFS snapshot hooks can't see the
   block devices through a private `/dev`. (A btrfs subvolume *snapshot create* additionally
   needs `CAP_SYS_ADMIN` **and** `CAP_DAC_OVERRIDE` — `CAP_FOWNER` is *not* required.)
7. **`systemd-analyze security` before you trust a unit.** It scores exposure and explains every
   setting — the fastest way to see what a unit can and can't do.

## Further reading
- [systemd.exec(5)](https://www.freedesktop.org/software/systemd/man/systemd.exec.html) ·
  [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html) ·
  [systemd-analyze(1)](https://www.freedesktop.org/software/systemd/man/systemd-analyze.html)
