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
**untrusted (receive-encrypted)** device model, connectivity (discovery/relays/ports), the GUI,
and running it as a service. It is **not backup** — its versioning is convenience, not a restore
guarantee (use [[borgmatic]] for that).

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
| `<folder>/.stversions/` | local version history (if versioning is enabled) — **not a backup** |

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
7. **Versioning is not backup.** `.stversions/` and trash can are conveniences; a deletion or
   corruption can propagate to every peer. Keep a real, separate backup.
8. **Config path moved in v1.27.** `~/.config/syncthing` → `~/.local/state/syncthing`; resolve
   with `syncthing --paths` instead of guessing — bites you on upgrades and migrations.
