---
type: cheatsheet
area: "Windows Administration"
aliases: [Event Viewer, event logs, Get-WinEvent]
tags: [windows, events, logs, security, monitoring]
status: working
---

# Windows Event Logs

> **Area:** [[Windows Administration]]

Querying, filtering, and forwarding Windows event logs via PowerShell (`Get-WinEvent`) and the Event Viewer UI. The authoritative source for Windows system, security, and application diagnostics.

---

## 1. Key event logs

| Log name | What's in it |
|---|---|
| `System` | Hardware, drivers, kernel, service failures |
| `Application` | Application errors and informational events |
| `Security` | Logon/logoff, object access, policy changes, privilege use |
| `Microsoft-Windows-PowerShell/Operational` | PowerShell script block logging |
| `Microsoft-Windows-TaskScheduler/Operational` | Task creation, runs, failures |
| `Microsoft-Windows-Windows Defender/Operational` | Defender detections and scans |
| `Microsoft-Windows-Sysmon/Operational` | Sysmon process/network/file events (if Sysmon installed) |
| `Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational` | RDP connections |
| `Setup` | Windows Update and component installations |

```powershell
Get-WinEvent -ListLog *              # list all logs on the system
Get-WinEvent -ListLog 'Security'    # show metadata for one log
```

## 2. Get-WinEvent basics

```powershell
# Read from a named log
Get-WinEvent -LogName System -MaxEvents 100
Get-WinEvent -LogName Security -MaxEvents 50

# Newest first (default is chronological)
Get-WinEvent -LogName System -MaxEvents 100 | Sort-Object TimeCreated -Descending

# From a saved .evtx file
Get-WinEvent -Path C:\Logs\Security.evtx

# Filter by level
Get-WinEvent -LogName System | Where-Object { $_.LevelDisplayName -in 'Error', 'Critical' }
```

## 3. Efficient filtering with FilterHashtable

`FilterHashtable` passes filters to the Windows Event Log API — much faster than piping to `Where-Object` because the filtering happens in the kernel before records are returned:

```powershell
# By log name + event ID + time range
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4625                          # failed logon
    StartTime = (Get-Date).AddHours(-24)
}

# Multiple event IDs
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = @(4624, 4625, 4634, 4647)    # logon success, failure, logoff types
}

# By level (1=Critical 2=Error 3=Warning 4=Information 5=Verbose)
Get-WinEvent -FilterHashtable @{ LogName = 'System'; Level = 2 }

# Provider + event ID
Get-WinEvent -FilterHashtable @{
    ProviderName = 'Microsoft-Windows-Security-Auditing'
    Id = 4688    # process creation
    StartTime = (Get-Date).AddDays(-1)
}
```

## 4. Security events reference

| Event ID | What it means |
|---|---|
| **4624** | Successful logon |
| **4625** | Failed logon (Failure Reason shows why) |
| **4634** | Logoff |
| **4648** | Logon using explicit credentials (RunAs) |
| **4672** | Special privileges assigned (effectively: admin logon) |
| **4688** | Process creation (requires auditing enabled) |
| **4698** | Scheduled task created |
| **4700** | Scheduled task enabled |
| **4702** | Scheduled task updated |
| **4720** | User account created |
| **4722** | User account enabled |
| **4724** | Password reset attempt |
| **4726** | User account deleted |
| **4732** | User added to security-enabled local group |
| **4740** | User account locked out |
| **4768** | Kerberos TGT requested |
| **4769** | Kerberos service ticket requested |
| **4771** | Kerberos pre-authentication failed |
| **7045** | New service installed |
| **1102** | Audit log cleared (Security) |
| **4719** | System audit policy changed |

## 5. Practical queries

```powershell
# Failed logons in the last 24 hours with source IP
Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4625; StartTime=(Get-Date).AddDays(-1) } |
    ForEach-Object {
        $xml = [xml]$_.ToXml()
        [PSCustomObject]@{
            Time        = $_.TimeCreated
            User        = $xml.Event.EventData.Data | Where-Object Name -eq 'TargetUserName' | Select-Object -Expand '#text'
            SourceIP    = $xml.Event.EventData.Data | Where-Object Name -eq 'IpAddress'     | Select-Object -Expand '#text'
            FailureCode = $xml.Event.EventData.Data | Where-Object Name -eq 'SubStatus'     | Select-Object -Expand '#text'
        }
    } | Group-Object SourceIP | Sort-Object Count -Desc

# Locked-out accounts
Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4740 } | Select-Object -First 20 |
    ForEach-Object { "$($_.TimeCreated) - $($_.Properties[0].Value)" }

# New services installed (attacker persistence)
Get-WinEvent -FilterHashtable @{ LogName='System'; Id=7045 } | Select-Object -First 20

# PowerShell script block logging (ID 4104)
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-PowerShell/Operational'
    Id = 4104
} | Select-Object TimeCreated, Message | Format-List
```

## 6. Event log administration

```powershell
# Clear a log (requires admin)
Clear-EventLog -LogName Application
wevtutil cl Security   # wevtutil: lower-level log utility

# Export a log to .evtx
wevtutil epl Security C:\backup\Security.evtx

# Check log size and retention settings
Get-WinEvent -ListLog System | Select-Object LogName, MaximumSizeInBytes, IsEnabled
wevtutil gl System     # full log config

# Set log size (32 MB in bytes)
wevtutil sl System /ms:33554432
```

## 7. Windows Event Forwarding (WEF) — collecting to a central host

```powershell
# On the collector server (run as admin):
wecutil qc /q                       # quick configure the collector service

# On source computers (via GPO or command):
winrm quickconfig -q               # enable WinRM
# Then create a subscription in Event Viewer: Subscriptions → Create Subscription
# Or via wecutil:
wecutil cs \\collector\subscriptions\mysub.xml

# Verify subscriptions
wecutil es                          # list subscriptions
wecutil gs MySub                    # subscription details
wecutil gr MySub                    # subscription runtime status
```

---

## Daily workflows

### "Find failed logons from the last hour"
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625;StartTime=(Get-Date).AddHours(-1)} |
    Measure-Object | Select-Object -Expand Count
```

### "Check if the security log was cleared"
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=1102} | Select-Object TimeCreated, Message
```

### "Find processes launched by a suspicious user"
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4688;StartTime=(Get-Date).AddDays(-1)} |
    Where-Object { $_.Message -match 'suspicioususer' }
```

## Gotchas / Golden rules

1. **`Get-EventLog` is deprecated** — it only reads classic logs and is slow; use `Get-WinEvent` for everything.
2. **Security log requires admin** — `Get-WinEvent -LogName Security` fails without elevation; always run as admin for security log queries.
3. **`FilterHashtable` is orders of magnitude faster than `Where-Object`** — for large logs with thousands of events, always filter at the API level.
4. **Event IDs are not globally unique** — the same ID means different things in different logs; always specify `LogName` or `ProviderName` alongside `Id`.
5. **The Security log wraps by default at 128 MB** — increase the maximum size on domain controllers and high-value servers; events lost to log wrapping are gone permanently.
