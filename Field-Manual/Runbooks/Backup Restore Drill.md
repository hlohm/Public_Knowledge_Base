---
type: runbook
area: Backup & Recovery
tags: [backup, drill]
status: stable
---

# Backup Restore Drill

> **Area:** [[Backup & Recovery]]

Periodically prove you can actually restore from backup — *before* you need to. A backup you
have never restored is not a backup. This drill restores to scratch space and verifies, so it
never touches live data. Uses [[borgmatic]]; adapt the commands if you use another tool.

## When to use
- On a schedule (monthly is a reasonable default), and after any change to backup config,
  retention, or the storage target.

## Prerequisites
- The repo passphrase / key is available (test that you can reach it, not just that it exists).
- Enough free space in the scratch location for the paths you'll extract.
- Read access to the repo; no `sudo` needed for read-only borg actions in most setups.

## Steps

1. **Confirm backups are current and the repo is reachable.**
   ```bash
   borgmatic repo-list | tail -5
   borgmatic repo-info
   ```
   *Verify:* the newest archive is as recent as you expect, and `repo-info` returns without an
   auth/lock error.

2. **Pick the archive to restore from.**
   ```bash
   borgmatic repo-list
   ```
   *Verify:* note an archive name (or use `latest`).

3. **Extract to scratch space — never to the original location.**
   ```bash
   borgmatic extract --archive <name> --path etc/nginx --destination /tmp/restore-drill
   ```
   *Verify:* `ls -R /tmp/restore-drill` shows the expected tree; the command exits 0.

4. **Compare the restored copy against the live copy.**
   ```bash
   diff -r /etc/nginx /tmp/restore-drill/etc/nginx
   ```
   *Verify:* differences are only ones you can explain (live changes since the backup). No
   surprising corruption or truncation.

5. **Run a deep integrity check while you're here.**
   ```bash
   sudo borgmatic check --only data        # slow: reads & re-hashes every chunk
   ```
   *Verify:* completes without error.

6. **Confirm the key/passphrase path works end-to-end** (not just that files exist):
   ```bash
   borgmatic info --archive <name>         # forces a decrypt of archive metadata
   ```
   *Verify:* archive details print — proving the key + passphrase actually open the repo.

## Rollback
- Nothing to roll back: the drill only reads the repo and writes to `/tmp/restore-drill`.
- Clean up afterwards: `rm -rf /tmp/restore-drill`.

## Done when
- A known file was restored to scratch and matched (or differed only explainably) against live,
- `check --only data` passed,
- and you confirmed the key/passphrase open the repo. Record the date so the next drill is due
  on schedule.
