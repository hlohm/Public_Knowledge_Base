---
type: "term"
branch: "Security"
domain: "Identity and Access Management"
aliases: ["ForceCommand", "Command Restriction"]
tags: ["iam"]
status: "developed"
---

# Forced Command

> **Domain:** [[04 - Identity and Access Management|Identity and Access Management]]
> **Also known as:** ForceCommand, Command Restriction

An [[SSH]] restriction that pins a key to a single server-side command: `command="…"` in `authorized_keys` (per key) or `ForceCommand` in `sshd_config` (per match block). Whatever the client asks to run, the server runs only the pinned command — the client's request is merely exposed to it as an environment variable.

**Context.** This is [[Least Privilege]] for automation keys: a backup key that can only run `borg serve --append-only`, a Git key that can only run the transport commands, a [[Deploy Key]] that can only trigger one script. Usually combined with `no-port-forwarding,no-pty,…` so the key is useless for anything else. The operational gotcha: such a key can't open an interactive shell, so a naive connectivity test that happens to authenticate with it "fails" confusingly — an agent offering the restricted key first can make a plain `ssh host` land in the forced command instead of a login, and testing basic reachability may require excluding the key (e.g. disabling pubkey auth for the probe). A compromised client still holds append/write rights within the pinned command — restriction is containment, not immunity.

## See also

- [[SSH]]
- [[Least Privilege]]
- [[Deploy Key]]
- [[Service Account]]
- [[Immutable Backup]]

## Further reading

- [OpenSSH manual: sshd — AUTHORIZED_KEYS FILE FORMAT](https://man.openbsd.org/sshd#AUTHORIZED_KEYS_FILE_FORMAT)
