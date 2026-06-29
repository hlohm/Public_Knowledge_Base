---
type: cheatsheet
area: "Windows Administration"
aliases: [Windows Subsystem for Linux, WSL2]
tags: [windows, wsl, linux, interop]
status: working
---

# WSL

> **Area:** [[Windows Administration]]

Windows Subsystem for Linux. Runs a real Linux kernel in a lightweight VM (WSL2) with full system-call compatibility. Lets you use Linux tools, shells, and development environments natively on Windows.

---

## 1. Installation and management

```powershell
# Install WSL with default distro (Ubuntu)
wsl --install

# Install a specific distro
wsl --install -d Debian
wsl --install -d Arch

# List available distros
wsl --list --online                  # distros available to install
wsl --list --verbose                 # installed distros: name, state, WSL version
wsl -l -v                            # shorthand

# Set default distro
wsl --set-default Ubuntu

# Set WSL version for a distro
wsl --set-version Ubuntu 2           # convert to WSL2
wsl --set-default-version 2          # all future installs use WSL2

# Launch a distro
wsl                                  # open default distro in current directory
wsl -d Debian                        # open a specific distro
wsl -d Ubuntu -u root               # as a specific user

# Terminate / restart
wsl --terminate Ubuntu               # stop a specific distro
wsl --shutdown                       # shut down all distros and the WSL2 VM

# Update the WSL kernel
wsl --update
wsl --version                        # WSL and kernel version info
```

## 2. Filesystem interop

```bash
# From Linux: access Windows drives
ls /mnt/c/Users/<user>/Desktop/
cd /mnt/c/Users/<user>/Documents/

# Run a Windows executable from Linux
/mnt/c/Windows/System32/notepad.exe
cmd.exe /c "dir C:\\"
explorer.exe .                       # open current directory in Windows Explorer
```

```powershell
# From PowerShell: access Linux filesystem
\\wsl$\Ubuntu\home\alice\            # UNC path to WSL filesystem
dir \\wsl$\Ubuntu\etc\

# Open a Linux path in Explorer
explorer.exe \\wsl$\Ubuntu\home\alice
```

## 3. Command interop

```powershell
# Run Linux commands from PowerShell/cmd
wsl ls -la ~/
wsl grep -r 'TODO' /home/alice/src/
wsl --exec python3 script.py

# Pipeline between Windows and Linux (string output)
Get-Process | wsl awk '{print $1}' | Select-Object -First 5
dir C:\Logs | wsl grep -c 'error'
```

```bash
# Run Windows commands from Linux
powershell.exe Get-Date
cmd.exe /c dir
ipconfig.exe | grep -i 'IPv4'
clip.exe < myfile.txt               # copy file content to Windows clipboard
```

## 4. WSL configuration

```ini
# Global config: %USERPROFILE%\.wslconfig  (Windows side)
[wsl2]
memory=4GB                  # max RAM for the WSL2 VM
processors=4                # max CPU cores
swap=2GB                    # swap size (set 0 to disable)
localhostForwarding=true    # forward WSL2 ports to localhost

# Distro config: /etc/wsl.conf  (Linux side, inside each distro)
[boot]
systemd=true                # enable systemd (WSL2 only; Ubuntu 22.04+, Debian 12+)

[automount]
enabled=true
root=/mnt/
options="metadata"          # enable Linux file metadata on Windows drives

[network]
generateResolvConf=true     # auto-generate /etc/resolv.conf
generateHosts=true          # auto-generate /etc/hosts

[user]
default=alice               # default user when launching this distro
```

After editing `.wslconfig`, restart WSL:
```powershell
wsl --shutdown
wsl
```

After editing `/etc/wsl.conf`, terminate the distro:
```powershell
wsl --terminate Ubuntu
wsl -d Ubuntu
```

## 5. Networking

```powershell
# WSL2 uses a virtual NAT adapter
# Find WSL2 IP from Windows
(Get-NetAdapter -Name "vEthernet (WSL)").InterfaceIndex
# Or from Linux: ip addr show eth0

# Access WSL2 services from Windows via localhost (localhostForwarding=true)
# A server on :3000 in WSL2 is accessible at localhost:3000 in Windows

# Access Windows services from WSL2
cat /etc/resolv.conf | grep nameserver   # this IP is the Windows host
# Windows host is typically 172.x.x.1 (the gateway in ip route)
```

## 6. Systemd in WSL2 (Ubuntu 22.04+, Debian 12+)

```bash
# Enable in /etc/wsl.conf:
# [boot]
# systemd=true

# After restarting the distro:
systemctl status                    # should work
systemctl start nginx
systemctl enable docker
journalctl -f
```

## 7. Export and import distros

```powershell
# Backup a distro to a tar file
wsl --export Ubuntu ubuntu-backup.tar

# Restore / import a distro
wsl --import Ubuntu-Restored C:\WSL\Ubuntu-Restored ubuntu-backup.tar
wsl --import Ubuntu-Restored C:\WSL\Ubuntu-Restored ubuntu-backup.tar --version 2

# Unregister (delete) a distro
wsl --unregister Ubuntu            # WARNING: deletes all data in the distro
```

---

## Daily workflows

### "Launch a Linux shell quickly from PowerShell"
```powershell
wsl
```

### "Run a one-off Linux command from cmd"
```cmd
wsl grep -r "error" /var/log/ | head -20
```

### "Port-forward a WSL2 service to the host network (for other machines)"
```powershell
# WSL2 is NAT'd; Windows localhost forwards work, but other machines on the LAN can't reach WSL2 directly
# Workaround: netsh portproxy
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=(wsl hostname -I).Split()[0]
# Remove:
netsh interface portproxy delete v4tov4 listenport=3000 listenaddress=0.0.0.0
```

## Gotchas / Golden rules

1. **Keep project files in the Linux filesystem (`~/`), not `/mnt/c/`** — I/O on the Windows filesystem from Linux is 10–20× slower via the 9P protocol; `git clone`, `npm install`, and builds should happen in `~/` not `C:\`.
2. **`wsl --shutdown` is required for `.wslconfig` changes to take effect** — the WSL2 VM is shared across all distros; restarting just one distro does not restart the VM.
3. **WSL2 IP address changes on every boot** — if you hardcode the WSL2 IP (e.g., for a firewall rule), it breaks after shutdown; use `localhost` forwarding instead.
4. **Permissions on `/mnt/c/` files are always 777** — Windows NTFS doesn't map to Unix permissions; adding `options=metadata` to `[automount]` in `/etc/wsl.conf` allows setting proper permissions.
5. **Systemd requires WSL2 and a supported distro version** — WSL1 does not support systemd; older Ubuntu (20.04 and earlier) needs `ubuntu-wsl2-systemd-script` or manual setup.
