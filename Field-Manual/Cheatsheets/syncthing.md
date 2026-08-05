---
type: cheatsheet
area: Networking & Protocols
aliases: [stcli, "syncthing cli", stdiscosrv, strelaysrv]
tags: [sync, file-sync, p2p, networking, security]
status: working
---

# syncthing

> **Area:** [[Networking & Protocols]]

Continuous, multi-master file synchronisation over an encrypted peer-to-peer transport — no
central server, every node a peer. Covers device/folder management, the `syncthing cli`, the
**untrusted (receive-encrypted)** device model, connectivity (discovery/relays/ports), file
versioning (§8), the GUI, and running it as a service. Properly deployed it is a full data-management
plane, not just a copy tool: the mesh handles **replication** (device loss ≠ data loss) and
per-device **versioning** handles file-level history (§8) — but it is still **not backup**; a
point-in-time restore guarantee needs a real backup tool (use [[borgmatic]] for that).

> Config moved in **v1.27**: the database/config default shifted from `~/.config/syncthing` to
> `~/.local/state/syncthing` on Linux. Always resolve the real paths with `syncthing --paths`
> rather than assuming.

---

## 1. Run & identity

```bash
syncthing serve --no-browser            # run in foreground, don't pop a browser (service-friendly)
syncthing serve --home=/path/to/home    # use an explicit config/data home (or set STHOMEDIR=)
syncthing --paths                       # print every path this instance uses — config, db, certs
syncthing --version
syncthing generate --home=/path/to/home # create a FRESH config + device identity WITHOUT starting
```

The **device ID is the hash of the node's TLS certificate** (`cert.pem`). It is created on first
run (or by `syncthing generate`). Print it:

```bash
syncthing cli show system | grep -i myID   # local device ID (daemon must be running)
# GUI equivalent: Actions → Show ID
```

> **Never copy `cert.pem`/`key.pem` between hosts.** Two nodes with the same cert = the **same
> device ID on the mesh twice** → endless connection flapping. Each node gets its own identity.

---

## 2. The CLI (`syncthing cli`)

Talks to the running daemon over its REST API (uses the GUI API key automatically when run
locally). The fastest way to change config without the web UI:

```bash
syncthing cli show system                       # version, device ID, uptime, discovery state
syncthing cli show connections                  # who's connected, in/out bytes, address, type
syncthing cli config devices list               # configured remote devices
syncthing cli config folders list               # configured folders + their types
syncthing cli config dump-json | jq .           # the whole config as JSON (read-only view)
syncthing cli operations restart                # graceful restart (re-reads config)
```

GUI/security knobs live under `config gui`:

```bash
syncthing cli config gui insecure-skip-host-check set true   # accept non-localhost Host headers
syncthing cli config gui user set <gui-user>
syncthing cli config gui password set <gui-pass>             # hashed on write
syncthing cli config gui raw-address set 127.0.0.1:8384      # keep the GUI on loopback
```

---

## 3. Folders & sharing

```bash
# Add a remote device (paste its ID), then share folders with it via the GUI or:
syncthing cli config devices add --device-id <PEER-DEVICE-ID> --name <label>
syncthing cli config folders <folder-id> devices add --device-id <PEER-DEVICE-ID>
```

**Folder types** (`type` per folder):

| Type | Meaning |
| --- | --- |
| `sendreceive` | default — two-way sync |
| `sendonly` | local changes propagate out; incoming changes are *not* applied (flagged instead) |
| `receiveonly` | accept incoming only; local edits are reverted to match the cluster |
| `receiveencrypted` | **untrusted node** — stores only ciphertext; cannot be sent in plaintext (see §4) |

`.stignore` (at a folder root) excludes paths from sync; `.stfolder` is the marker that proves a
folder is mounted (its absence pauses the folder — a guard against syncing into an empty mount).

---

## 4. Untrusted devices (receive-encrypted)

The key feature for putting a node on hardware you don't trust: the remote stores **encrypted
blocks only** and never holds the plaintext or the key.

```text
On each TRUSTED sender, when sharing a folder to the untrusted device:
  Folder → Sharing → (tick the device) → Advanced → set an "Encryption Password".
  → that device is now untrusted for this folder; senders transmit ciphertext.

On the UNTRUSTED node:
  the incoming folder auto-creates as type `receiveencrypted`. Nothing to configure;
  the password is NEVER entered here.
```

- The encryption password is **per (folder, untrusted-device)** and lives on the **trusted
  senders** (store it in a password manager) — never on the untrusted node.
- A trusted peer can **restore** from the untrusted replica: it pulls the encrypted blocks and
  decrypts locally with its own password. The untrusted node alone can't read a byte.
- **Do not make an untrusted node an introducer** (§5) — it must not be able to add devices to
  your cluster.

---

## 5. Connectivity — discovery, relays, ports

```text
22000/tcp   sync data (direct connections)        ← open this for a publicly reachable node
22000/udp   sync data over QUIC
21027/udp   LOCAL discovery (LAN broadcast only)   ← useless across the internet; don't port-forward
8384/tcp    web GUI                                ← keep on 127.0.0.1; reach via SSH tunnel
```

- **Global discovery** (default public servers) maps device ID → current address, so nodes find
  each other without static IPs — survives a changing public IP.
- **Relays** carry traffic when no direct connection is possible (both peers NAT'd). Relayed
  traffic is still end-to-end encrypted but slower; a publicly reachable node (open `22000`)
  lets NAT'd peers connect directly instead.
- **Introducer**: a device marked *introducer* auto-shares its other known devices into your
  cluster. Convenient for a trusted hub; **never** enable it on a low-trust node.

```bash
syncthing cli show connections          # check whether a peer is "tcp-client"/"relay-client"/etc
```

---

## 6. GUI & config file

- GUI default bind is `127.0.0.1:8384`. To reach it from another machine, **SSH-tunnel** it
  (`ssh -L 8384:localhost:8384 <user>@<host>`) rather than binding it to a public interface.
- Off-loopback access trips a **"Host check error"** (anti-DNS-rebinding guard) because the
  browser's `Host:` header isn't in the allowlist → set `insecureSkipHostcheck` (§2). Safe only
  when the GUI is otherwise protected (loopback + tunnel + GUI password + HTTPS).
- **`config.xml` is rewritten on exit.** Editing it while the daemon runs gets clobbered — `stop
  the service first`, then edit, then start. Prefer the `syncthing cli` (live-safe).

---

## 7. Autostart per OS family

Run as the **regular user** (never root) and always with `--no-browser`.

### Linux (systemd)

Upstream packages ship two units — pick one, don't enable both:

```bash
# user service — starts at login (add lingering for boot-time start on headless boxes)
systemctl --user enable --now syncthing.service
sudo loginctl enable-linger <user>          # start user services at boot without a login session

# system service, one instance per user — starts at boot
sudo systemctl enable --now syncthing@<user>.service
```

See [[systemd]] for unit/override handling. No unit installed? `systemctl cat syncthing@` to check; get them from the package `syncthing` or upstream's `etc/linux-systemd/`.

### macOS (launchd)

```bash
brew services start syncthing               # Homebrew: installs + loads a LaunchAgent (login start)
```

Without Homebrew: put upstream's `syncthing.plist` (from `etc/macos-launchd/` in the release tarball) into `~/Library/LaunchAgents/`, edit the binary path, then:

```bash
launchctl load ~/Library/LaunchAgents/syncthing.plist
```

### Windows

No official service. In rough order of preference:

```text
1. "Syncthing Windows Setup" installer — offers login autostart (and optional service mode).
2. Startup-folder shortcut: shell:startup → shortcut to syncthing.exe serve --no-console --no-browser
3. Task Scheduler: trigger "At log on", action = syncthing.exe serve --no-console --no-browser
   (runs without a visible window; survives UAC oddities better than the startup folder)
4. True service (runs before login): wrap with NSSM — run as a dedicated non-admin account.
```

### BSD / others

`pkg install syncthing` ships an rc.d script: `sysrc syncthing_enable=YES && service syncthing start` (FreeBSD; runs as the `syncthing` user — adjust `syncthing_user` in `rc.conf` if syncing your own home). Android: the Syncthing app manages its own background start.

---

## 8. File versioning

Per-folder, per-device history of replaced/deleted files. The one semantic that decides where to
enable it: **versioning only captures changes arriving *from other devices*.** When a peer's
update would overwrite or delete a local file, the device stashes the old copy first. Local edits
are never versioned locally — they get versioned *on the peers* once they sync out.

> **Design pattern:** enable versioning on an **always-on hub node** that holds every folder.
> Every edit made anywhere else gets a version there within seconds (fs-watcher sync ≈ per-save
> granularity). That's a first line of recovery for fat-fingered or script/agent-mangled files —
> cheaper to restore from than a backup archive, but **no substitute for one** (Gotcha #7).

**Types** (per folder, set on the *versioning* device):

| Type | Behaviour | Key params |
| --- | --- | --- |
| Trash Can | keeps only deleted/replaced files | `cleanoutDays` (0 = keep forever) |
| Simple | last N versions per file | `keep` (count) |
| **Staggered** | thins versions over time: all within the 1st hour → hourly for a day → daily for 30 days → weekly until max age; auto-cleanup | `maxAge` (default 365 d) |
| External | runs your command per replaced file | `command` |

**Config** — GUI: Folder → Edit → File Versioning. CLI (live-safe):

```bash
syncthing cli config folders <folder-id> versioning type set staggered
syncthing cli config folders <folder-id> versioning params set --key maxAge --value 31536000   # seconds
syncthing cli config folders <folder-id> versioning fs-path set /path/elsewhere               # optional: move versions off-folder
```

**Where versions live & what they cost:**

- Default: `<folder>/.stversions/`, mirroring the folder tree; files carry a `~YYYYMMDD-HHMMSS`
  suffix (`note~20260716-141210.md`). `fs-path` relocates this (e.g. another disk).
- `.stversions` is **excluded from sync** — it grows disk only on the versioning device and never
  propagates to peers. Growth is full copies (no dedup), so it's trivial for text/documents but
  can bite on large churny binaries — scope versioning per folder accordingly.
- Cleanup runs on an interval (`cleanupIntervalS`, default 1 h) — staggered/trashcan enforce
  their retention then, not at write time.

**Restore:** GUI → Folder → Versions ("Restore Versions" browser, pick file + timestamp), or just
copy the file out of `.stversions` and strip the suffix.

---

## Daily workflows

### "Pair two of my own devices"
```bash
# On each: Actions → Show ID (or: syncthing cli show system | grep myID)
# On device A: add device B's ID; on device B: accept A. Then share a folder one way; accept it.
```

### "Add an always-on node on a host I don't trust"
```bash
# 1. fresh identity on the node (don't copy certs):  syncthing generate --home=<dir>
# 2. open 22000/tcp(+udp) on the node; keep 8384 on loopback
# 3. on each trusted sender: share the folder to the new device WITH an encryption password
# 4. the node receives it as receiveencrypted — ciphertext only
```

### "Figure out why two devices won't connect"
```bash
syncthing cli show connections          # are they connected at all? via relay or direct?
syncthing cli show system               # is discovery up? what's the announced address?
# then: confirm 22000 is actually reachable on the listening side (see [[nc]]); check both
# firewall layers if it's a cloud host (provider edge + host firewall — see [[iptables]]).
```

### "Recover a file someone (or something) mangled"
```bash
# On the versioning device (the hub, not the machine where the edit happened!):
# GUI: Folder → Versions → pick the file + timestamp → Restore
# or by hand: cp '<folder>/.stversions/path/note~20260716-141210.md' '<folder>/path/note.md'
# The restored file then syncs back out to every peer like any other change.
```

### "Move a node's data/config home"
```bash
syncthing cli operations restart        # or stop the service
# move the dir; set STHOMEDIR=/new/home (or --home=) in the unit; re-resolve with: syncthing --paths
```

---

## Files & locations

| Path | What |
| --- | --- |
| `~/.local/state/syncthing/` *(v1.27+)* or `~/.config/syncthing/` | config + database home (`syncthing --paths` is authoritative) |
| `…/config.xml` | the configuration (rewritten on exit — don't hand-edit live) |
| `…/cert.pem`, `…/key.pem` | **device identity** — the cert hash *is* the device ID; never copy between hosts |
| `…/https-cert.pem`, `…/https-key.pem` | GUI TLS cert |
| `…/index-*.db` / database dir | the sync database (large; node-local, not synced) |
| `<folder>/.stfolder` | folder marker; its absence pauses the folder |
| `<folder>/.stignore` | per-folder exclude patterns |
| `<folder>/.stversions/` | local version history (§8) — excluded from sync; **not a backup** |

---

## Gotchas / Golden rules

1. **Never copy `cert.pem` between hosts.** Same cert → duplicate device ID → mesh flapping. Each
   node gets a fresh identity (`syncthing generate`).
2. **Receive-encrypted is set on the *sender*, not the untrusted node.** The encryption password
   lives on the trusted peers; the untrusted node only ever holds ciphertext and never the key.
   Typing the password *into* the untrusted node defeats the entire point.
3. **Don't make a low-trust node an introducer.** It could inject arbitrary devices into your
   cluster — exactly the pivot you're avoiding.
4. **GUI stays on loopback.** Reach it by SSH tunnel; off-loopback needs `insecureSkipHostcheck`
   and is only safe with a GUI password + HTTPS behind that tunnel. Never bind it to a public IP.
5. **`config.xml` is rewritten on daemon exit.** Stop before hand-editing, or use `syncthing cli`.
6. **`21027/udp` is LAN-only.** It's broadcast local discovery; forwarding it to the internet
   does nothing. Internet reachability comes from `22000` + global discovery/relays.
7. **Versioning is not backup.** It's a strong *recovery layer* (§8) — per-save file history on a
   hub catches most day-to-day damage — but it lives on the same disk as the data, offers no
   point-in-time snapshot of a whole folder, and versions only what *arrived via sync*. Keep a
   real, separate backup.
8. **Versioning goes on the receiving device.** Enabling it on the machine where the edits happen
   protects nothing — local changes are only versioned on the *peers* they sync to (§8).
9. **Config path moved in v1.27.** `~/.config/syncthing` → `~/.local/state/syncthing`; resolve
   with `syncthing --paths` instead of guessing — bites you on upgrades and migrations.
