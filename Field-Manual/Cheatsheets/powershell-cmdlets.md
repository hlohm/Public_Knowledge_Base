---
type: cheatsheet
area: "Windows Administration"
aliases: [cmdlet reference, CIM, WMI, Get-CimInstance]
tags: [windows, powershell, cmdlets, administration, networking, registry]
status: working
---

# PowerShell Cmdlets

> **Area:** [[Windows Administration]]

The cmdlets reached for most often in day-to-day Windows administration: system info, filesystem, registry, networking, storage, and permissions. For the *language* (pipeline, objects, control flow, functions) see [[powershell]]; for services/tasks, event logs, and users see [[windows-services]], [[windows-events]], and [[windows-users]].

---

## 1. System & process info

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, OsVersion, CsSystemType   # OS/hardware summary in one call
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, LastBootUpTime  # CIM: modern WMI, WSMan-based
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10           # top CPU consumers
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5  # live perf counters
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location  # what launches at logon
```

## 2. Filesystem

```powershell
Get-ChildItem -Path C:\Data -Recurse -File | Measure-Object -Property Length -Sum   # total size of a tree
Get-ChildItem -Recurse | Sort-Object Length -Descending | Select-Object -First 10 FullName, Length  # biggest files
New-Item -ItemType Directory -Path C:\Data\New -Force        # mkdir -p equivalent, no error if it exists
Copy-Item C:\src -Destination C:\dst -Recurse
Move-Item C:\old.txt -Destination C:\archive\
Remove-Item C:\temp\* -Recurse -Force -Confirm:$false
Test-Path C:\Data\file.txt                                    # existence check — use before destructive ops
Get-FileHash C:\file.iso -Algorithm SHA256                    # integrity verification
```

## 3. Registry

```powershell
Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'  # registry is just another PSDrive
Get-ChildItem -Path 'HKLM:\SOFTWARE' | Select-Object -First 10 Name
New-ItemProperty -Path 'HKLM:\SOFTWARE\MyApp' -Name 'Version' -Value '1.0' -PropertyType String
Set-ItemProperty -Path 'HKLM:\SOFTWARE\MyApp' -Name 'Version' -Value '1.1'
Remove-ItemProperty -Path 'HKLM:\SOFTWARE\MyApp' -Name 'Version'
reg query "HKLM\SOFTWARE\MyApp"          # reg.exe: works remotely with \\host, the PS provider doesn't
reg export "HKLM\SOFTWARE\MyApp" backup.reg
```

## 4. Networking

```powershell
Get-NetIPAddress -AddressFamily IPv4                          # replaces ipconfig for scripting
Get-NetAdapter | Where-Object Status -eq 'Up'
New-NetIPAddress -InterfaceAlias 'Ethernet' -IPAddress 10.0.0.10 -PrefixLength 24 -DefaultGateway 10.0.0.1
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 10.0.0.1, 10.0.0.2
Test-NetConnection -ComputerName example.com -Port 443         # TCP port check (ICMP-only without -Port)
Get-NetTCPConnection -State Listen                              # what's listening (replaces netstat -an)
Resolve-DnsName example.com -Type A
New-NetFirewallRule -DisplayName 'Allow 8443' -Direction Inbound -LocalPort 8443 -Protocol TCP -Action Allow
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object DisplayName, Action
```

## 5. Storage & disks

```powershell
Get-Disk                                                        # physical disks
Get-Volume                                                      # volumes with free/used space
Get-PSDrive -PSProvider FileSystem                              # drive letters, like df
Get-Partition -DiskNumber 0
Resize-Partition -DiskNumber 0 -PartitionNumber 2 `
    -Size (Get-PartitionSupportedSize -DiskNumber 0 -PartitionNumber 2).SizeMax
New-Partition -DiskNumber 1 -UseMaximumSize -AssignDriveLetter |
    Format-Volume -FileSystem NTFS -NewFileSystemLabel 'Data'
```

## 6. Security & permissions

```powershell
Get-Acl C:\Data\Secret | Format-List                            # current ACL
$acl = Get-Acl C:\Data\Secret
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule('DOMAIN\alice', 'Modify', 'Allow')
$acl.SetAccessRule($rule)
Set-Acl C:\Data\Secret $acl
icacls C:\Data\Secret /grant 'DOMAIN\alice:(M)'                 # icacls: quicker for scripting/remote work
icacls C:\Data\Secret /inheritance:r                            # break inheritance
whoami /groups                                                  # current user's group memberships
whoami /priv                                                    # current user's enabled privileges
```

## 7. Software & patch inventory

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10   # installed patches
Get-Package | Select-Object Name, Version                       # installed software (provider-dependent)
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' |
    Select-Object DisplayName, DisplayVersion | Where-Object DisplayName   # fast software inventory
# Get-CimInstance Win32_Product also lists software but triggers an MSI repair per package — see Gotchas.
```

## 8. Date, time & locale

```powershell
Get-Date
Get-TimeZone
Set-TimeZone -Id 'UTC'
w32tm /query /status                                            # NTP sync status
w32tm /resync                                                   # force resync
Get-WinSystemLocale
```

## 9. Computer identity & power state

```powershell
Rename-Computer -NewName 'HOST02' -Restart                      # needs a restart to take effect
Add-Computer -DomainName corp.example.com -Credential (Get-Credential) -Restart   # domain-join
Restart-Computer -ComputerName server01 -Force
Stop-Computer -ComputerName server01
```

---

## Daily workflows

### "What's eating disk space on C:"
```powershell
Get-PSDrive C
Get-ChildItem C:\ -Recurse -File -ErrorAction SilentlyContinue |
    Sort-Object Length -Descending | Select-Object -First 20 FullName, @{N='MB'; E={[math]::Round($_.Length/1MB,1)}}
```

### "Check if a remote host is reachable on a specific port"
```powershell
Test-NetConnection -ComputerName example.com -Port 443 -InformationLevel Detailed
```

### "Join a new server to the domain"
```powershell
Rename-Computer -NewName 'APP01' -Restart
# after reboot:
Add-Computer -DomainName corp.example.com -Credential (Get-Credential) -Restart
```

### "Audit who has access to a sensitive folder"
```powershell
(Get-Acl C:\Data\Secret).Access | Select-Object IdentityReference, FileSystemRights, AccessControlType
```

## Gotchas / Golden rules

1. **`Get-CimInstance` vs `Get-WmiObject`** — CIM uses WSMan (works through WinRM-permitting firewalls, works cross-platform with PS7); WMI is DCOM-based and deprecated. Prefer CIM for anything new.
2. **`Get-CimInstance Win32_Product` triggers an MSI repair/reconfigure for every installed package it enumerates** — never run it routinely on production; query the registry `Uninstall` keys instead (§7).
3. **`Test-NetConnection` without `-Port` only does an ICMP ping** — a host that blocks ICMP but allows the port you actually care about will look "down" unless you specify `-Port`.
4. **The registry PSDrives (`HKLM:`, `HKCU:`) are local-only** — `Get-ItemProperty` doesn't reach a remote host; use `reg.exe \\host` or `Invoke-Command` for remote registry work.
5. **`Rename-Computer` and `Add-Computer` both require a restart to fully apply** — chaining them without a reboot in between can leave the machine in an inconsistent identity state; reboot after each.

## See also

- [[powershell]] — language, pipeline, objects, functions, remoting
- [[windows-services]] — `Get-Service`, scheduled tasks
- [[windows-events]] — `Get-WinEvent`, security event IDs
- [[windows-users]] — local and AD user/group management
- [[winget]] — package install/upgrade
