---
type: cheatsheet
area: "Linux Administration"
aliases: [users, permissions, chmod, chown]
tags: [linux, users, permissions, sudo, groups, pam]
status: working
---

# Users & Permissions

> **Area:** [[Linux Administration]]

User and group management, file permissions, sudo, and PAM — the access control layer of any Linux system.

---

## 1. User management

```bash
# Create users
useradd -m -s /bin/bash alice         # -m: create home, -s: shell
useradd -r -s /usr/sbin/nologin svc  # system account (no home, no login)
useradd -G wheel,docker alice         # add to supplementary groups at creation
adduser alice                         # interactive (Debian/Ubuntu); friendlier

# Modify users
usermod -aG docker alice              # append to group (-a is critical; without it replaces)
usermod -s /bin/zsh alice             # change shell
usermod -L alice                      # lock account (prefix ! in /etc/shadow)
usermod -U alice                      # unlock account
usermod -e 2025-12-31 alice           # set account expiry date

# Delete users
userdel alice                         # delete user (home directory preserved)
userdel -r alice                      # delete user and home directory

# Change password
passwd alice                          # interactive
echo 'alice:newpassword' | chpasswd   # scripted (avoid; password in process list)

# Expire password immediately (force reset on next login)
passwd -e alice
chage -d 0 alice                      # same via chage
chage -l alice                        # show password aging information
```

## 2. Group management

```bash
groupadd devteam                      # create a group
groupadd -g 1500 devteam              # with specific GID
groupdel devteam                      # delete group
gpasswd -a alice devteam              # add user to group
gpasswd -d alice devteam              # remove user from group
gpasswd -M alice,bob devteam          # set exact member list
newgrp docker                         # switch primary group in current session (opens subshell)

id alice                              # UID, GID, all groups
groups alice                          # groups the user belongs to
getent passwd alice                   # entry from /etc/passwd (works across LDAP/NIS too)
getent group docker                   # members of a group
```

## 3. File permissions

```bash
# Symbolic notation
chmod u+x script.sh          # add execute for owner
chmod g-w file.txt           # remove write for group
chmod o=r file.txt           # set other to read-only
chmod a+r file.txt           # add read for all (a = ugo)
chmod u+x,g-w file           # multiple changes

# Octal notation (easier to reason about for absolute permissions)
chmod 644 file.txt           # rw-r--r--  (owner rw, group r, other r)
chmod 755 script.sh          # rwxr-xr-x  (owner rwx, group+other rx)
chmod 600 private.key        # rw-------  (owner rw, no one else)
chmod 700 ~/.ssh             # rwx------
chmod 1777 /tmp              # rwxrwxrwt  (sticky bit: only owner can delete their own files)
chmod 2775 /shared           # rwxrwsr-x  (setgid: new files inherit group)
chmod 4755 /usr/bin/sudo     # rwsr-xr-x  (setuid: runs as owner, not caller)

# Recursive (apply to all files and subdirectories)
chmod -R 755 /var/www/html/
# Caution: recursive chmod on files and dirs together is usually wrong;
# dirs need x to be traversable, files should not have x
find /var/www -type d -exec chmod 755 {} +
find /var/www -type f -exec chmod 644 {} +

# Change ownership
chown alice file.txt
chown alice:webdev file.txt    # user and group
chown :webdev file.txt         # group only
chown -R alice:webdev /var/www/

# View permissions
ls -la /path/
stat file.txt
```

**Octal reference:**

| Octal | Binary | Meaning |
|---|---|---|
| 0 | 000 | --- |
| 1 | 001 | --x |
| 2 | 010 | -w- |
| 3 | 011 | -wx |
| 4 | 100 | r-- |
| 5 | 101 | r-x |
| 6 | 110 | rw- |
| 7 | 111 | rwx |

## 4. ACLs (extended permissions)

Standard ugo permissions can't express "give bob read access to alice's file without changing the group." ACLs solve this:

```bash
# View ACL
getfacl file.txt

# Set ACL
setfacl -m u:bob:r   file.txt     # give bob read access
setfacl -m g:ops:rw  file.txt     # give group ops read+write
setfacl -m o::---    file.txt     # revoke other access
setfacl -x u:bob     file.txt     # remove bob's ACL entry
setfacl -b           file.txt     # remove all ACL entries

# Default ACLs (inherited by new files in a directory)
setfacl -d -m u:bob:r /shared/dir/

# Copy ACL from one file to another
getfacl src.txt | setfacl --set-file=- dst.txt
```

## 5. sudo

```bash
# Run a command as root
sudo command

# Run as another user
sudo -u alice command

# Start a root shell
sudo -i          # login shell (full environment)
sudo -s          # shell with current environment

# Edit sudoers safely
visudo           # validates syntax before saving (always use this, not direct editor)

# sudoers rules (in /etc/sudoers or /etc/sudoers.d/<file>):
alice ALL=(ALL:ALL) ALL                       # alice can run anything as anyone
%wheel ALL=(ALL:ALL) NOPASSWD: ALL            # wheel group, no password
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl  # specific command, no password
Defaults timestamp_timeout=0                  # require password for every sudo invocation
Defaults logfile=/var/log/sudo.log            # log all sudo commands
```

## 6. Pluggable Authentication Modules (PAM)

PAM controls how authentication, account validation, session setup, and password changes work. Config lives in `/etc/pam.d/`.

```bash
# Test a PAM stack without logging in
su - alice              # tests pam_unix, pam_limits, pam_env, etc.

# Password quality (pam_pwquality)
# /etc/security/pwquality.conf (or inline in /etc/pam.d/passwd):
# minlen = 14
# dcredit = -1    # at least 1 digit
# ucredit = -1    # at least 1 uppercase
# lcredit = -1    # at least 1 lowercase
# ocredit = -1    # at least 1 special
# difok = 8       # min changed characters vs old password
# enforce_for_root = 1

# Login failures / account lockout (pam_faillock)
# /etc/security/faillock.conf:
# deny = 5         # lock after 5 failures
# unlock_time = 600  # locked for 10 minutes
# faillock --user alice --reset   # manually unlock

# Session limits (pam_limits) — /etc/security/limits.conf or limits.d/
# alice hard nproc  1024     # max processes
# @dev  hard nofile 65536    # max open files for group 'dev'
# *     soft core   0        # disable core dumps for all
```

---

## Daily workflows

### "Add a service account with no login"
```bash
useradd -r -M -s /usr/sbin/nologin myapp
```

### "Fix permissions on a web root"
```bash
chown -R www-data:www-data /var/www/site/
find /var/www/site -type d -exec chmod 755 {} +
find /var/www/site -type f -exec chmod 644 {} +
```

### "Grant a user sudo for specific commands"
```bash
echo 'deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart myapp' \
  > /etc/sudoers.d/deploy
chmod 440 /etc/sudoers.d/deploy
visudo -c   # validate
```

### "Check who has root or sudo access"
```bash
grep -E '^(root|[^:]+:[^:]*:0:)' /etc/passwd
grep -E '(sudo|wheel)' /etc/group
ls -la /etc/sudoers.d/
```

## Files & locations

| Path | What |
|---|---|
| `/etc/passwd` | User account info (username, UID, GID, home, shell) |
| `/etc/shadow` | Hashed passwords and aging info (root-readable only) |
| `/etc/group` | Group definitions |
| `/etc/gshadow` | Group passwords and admins |
| `/etc/sudoers` | Main sudoers file (edit via `visudo`) |
| `/etc/sudoers.d/` | Drop-in sudoers files |
| `/etc/pam.d/` | PAM configuration per service |
| `/etc/security/` | PAM module config files |

## Gotchas / Golden rules

1. **`usermod -G` without `-a` replaces all supplementary groups** — always use `usermod -aG group user`; omitting `-a` strips the user from every other group.
2. **Group membership changes don't take effect in existing sessions** — the user must log out and back in (or `newgrp`) for new group memberships to be visible.
3. **`chmod -R` gives the same permissions to directories and files** — files should not have the execute bit; use `find` with `-type f` and `-type d` separately.
4. **`visudo` is not optional** — a syntax error in `/etc/sudoers` locks all sudo access; always use `visudo`.
5. **setuid on scripts is silently ignored by the Linux kernel** — setuid only works on compiled binaries; setuid shell scripts don't run as the file owner.
