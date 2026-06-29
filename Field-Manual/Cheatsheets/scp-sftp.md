---
type: cheatsheet
area: "Networking & Protocols"
aliases: [scp, sftp, ftp]
tags: [file-transfer, ssh, scp, sftp, networking]
status: working
---

# (S)FTP / SCP

> **Area:** [[Networking & Protocols]]

File transfer over SSH and FTP. SCP and SFTP ride on the [[ssh]] transport; FTP is legacy-only and should not be used for anything sensitive.

> **Prefer SFTP over SCP for new work.** `scp` copies files; `sftp` is a full file-transfer session (browse, rename, delete). The underlying SSH auth and host-key verification is identical for both.

---

## 1. SCP — copy files over SSH

Syntax mirrors `cp`: `scp [options] source destination`

```bash
# Copy a local file to a remote host
scp /local/file.txt user@host:/remote/path/

# Copy a file from remote to local
scp user@host:/remote/file.txt /local/path/

# Copy between two remote hosts (routed through your machine)
scp user1@host1:/path/file user2@host2:/path/

# Copy a directory (recursive)
scp -r /local/dir/ user@host:/remote/dir/

# Specify a port
scp -P 2222 file.txt user@host:/path/

# Use a specific SSH key
scp -i ~/.ssh/deploy_key file.txt user@host:/path/

# Verbose (shows SSH handshake debug output — useful when it hangs)
scp -v file.txt user@host:/path/

# Preserve timestamps and permissions
scp -p file.txt user@host:/path/

# Compress during transfer (useful on slow links; skip on fast LAN)
scp -C largefile.tar user@host:/path/

# Limit bandwidth (KB/s)
scp -l 5000 bigfile.tar user@host:/path/
```

**Remote path syntax:**
```bash
scp user@host:file.txt .        # relative to home directory
scp user@host:~/file.txt .      # explicit home
scp user@host:/abs/path .       # absolute path
```

## 2. SFTP — interactive session

```bash
sftp user@host               # open an interactive session
sftp -P 2222 user@host       # custom port
sftp -i ~/.ssh/key user@host # specific key
sftp -b batch.txt user@host  # non-interactive: run commands from a file
```

**Interactive SFTP commands:**
```
ls / lls          remote / local listing
pwd / lpwd        remote / local working directory
cd / lcd          change remote / local directory
get remote [local]          download a file
get -r remote_dir           download a directory (recursive)
put local [remote]          upload a file
put -r local_dir            upload a directory
mget *.log                  download multiple files (glob)
mput *.conf                 upload multiple files (glob)
rm remote_file              delete remote file
rmdir remote_dir            delete remote directory
mkdir remote_dir            create remote directory
rename old new              rename a remote file
chmod 644 remote_file       change remote permissions
df -h                       remote filesystem disk usage
bye / exit                  end the session
```

## 3. Non-interactive SFTP (batch / scripts)

```bash
# Run commands from a here-doc
sftp user@host <<'EOF'
  cd /remote/path
  put local-file.txt
  get remote-file.txt
  bye
EOF

# Run commands from a file
cat > sftp-batch.txt <<'EOF'
put deployment.tar.gz /var/www/
chmod 644 /var/www/deployment.tar.gz
bye
EOF
sftp -b sftp-batch.txt deploy@webserver
```

## 4. rsync over SSH (often better than scp for large transfers)

For large or repeated transfers, [[rsync]] with SSH is faster and resumable:

```bash
rsync -avz -e ssh /local/dir/ user@host:/remote/dir/
rsync -avzP user@host:/remote/dir/ /local/dir/    # -P = --progress + --partial (resumable)
```

## 5. FTP (legacy)

FTP sends credentials in cleartext. Only use it when forced to by a third party (legacy provider, ISP FTP upload endpoint), never for internal infrastructure.

```bash
ftp ftp.example.com     # open interactive FTP session

# Interactive FTP commands (same pattern as SFTP but older syntax):
open ftp.example.com
user alice              # enter username
ls
cd /pub
get file.txt
mget *.txt              # download multiple files
put upload.txt
mput *.csv              # upload multiple files
binary                  # switch to binary mode before transferring non-text files
ascii                   # switch to ASCII mode (default)
passive                 # toggle passive mode (use when behind NAT)
bye
```

**Scripted FTP (no password in history):**
```bash
# .netrc approach — credentials in file, read by ftp/curl automatically
# ~/.netrc (mode 600):
# machine ftp.example.com login alice password <password>
ftp ftp.example.com <<'EOF'
binary
get file.txt
bye
EOF
```

---

## Daily workflows

### "Upload a file to a server"
```bash
scp /local/file.tar.gz deploy@server:/var/www/releases/
```

### "Download a log file quickly"
```bash
scp -C user@host:/var/log/app/app.log /tmp/
```

### "Upload an entire directory preserving structure"
```bash
rsync -avz /local/dist/ user@host:/var/www/site/
```

### "Interactive session to browse and fetch files"
```bash
sftp user@host
# Then: ls, cd, get file.txt, bye
```

## Files & locations

| Path | What |
|---|---|
| `~/.ssh/config` | SSH config: host aliases, identity files, ports — applies to both scp and sftp |
| `~/.netrc` | Credentials for ftp/curl (chmod 600) |

## Gotchas / Golden rules

1. **`scp` does not show progress by default** — add `-v` to see what it's doing if it appears to hang; add `-C` for compression on slow links.
2. **SFTP uses a different protocol than FTP** — the name is confusing; SFTP (SSH File Transfer Protocol) has nothing in common with FTP except the file-transfer purpose.
3. **`scp` with a colon in a filename requires `./` prefix** — `scp user@host:file:with:colons.txt` will confuse scp's parser; use `scp user@host:./file:with:colons.txt`.
4. **FTP passive mode is usually required behind NAT** — active mode requires the server to connect back to the client, which fails through most firewalls; `passive` or `pasv` in the session, or `ftp -p` flag.
5. **Binary mode for binary files** — FTP defaults to ASCII mode which corrupts non-text files on transfer (it translates line endings); always type `binary` before transferring archives, images, or executables.
