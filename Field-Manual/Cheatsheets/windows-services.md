---
type: cheatsheet
area: "Windows Administration"
aliases: [services, scheduled tasks, Task Scheduler]
tags: [windows, services, scheduled-tasks, administration]
status: working
---

# Windows Services & Scheduled Tasks

> **Area:** [[Windows Administration]]

Managing Windows services (start/stop/config) and scheduled tasks (creation, management, troubleshooting) via PowerShell and the `sc` command.

---

## 1. Services — PowerShell

```powershell
# List services
Get-Service                                      # all services
Get-Service -Name 'Spooler'                      # by name
Get-Service | Where-Object Status -eq 'Stopped'  # only stopped services
Get-Service | Where-Object { $_.StartType -eq 'Automatic' -and $_.Status -eq 'Stopped' }

# Control
Start-Service -Name 'Spooler'
Stop-Service  -Name 'Spooler'
Restart-Service -Name 'Spooler'
Suspend-Service -Name 'Spooler'   # pause (not all services support this)
Resume-Service  -Name 'Spooler'

# Configuration
Set-Service -Name 'Spooler' -StartupType Automatic    # Manual | Automatic | Disabled | AutomaticDelayedStart
Set-Service -Name 'Spooler' -Description "Print Spooler Service"
Set-Service -Name 'Spooler' -Credential (Get-Credential)  # change service account

# Wait for stop/start
Start-Service 'Spooler' -PassThru | Wait-Service -Status 'Running'
```

## 2. Services — sc.exe (legacy / lower-level)

```cmd
sc query                            # list all services
sc query "Spooler"                  # query one service
sc start "Spooler"
sc stop  "Spooler"
sc config "Spooler" start= auto     # change start type (note: space after =)
sc config "Spooler" start= demand   # manual
sc config "Spooler" start= disabled
sc failure "Spooler" reset= 86400 actions= restart/5000/restart/5000/restart/5000
                                    # restart on failure: after 1 day reset, restart 3 times with 5s delay
sc delete "MyService"               # delete a service
```

## 3. Service accounts and LAPS

```powershell
# Check what account a service runs under
Get-WmiObject -Class Win32_Service -Filter 'Name="Spooler"' | Select Name, StartName

# Configure a group Managed Service Account (gMSA) for a service
# (Domain-joined; AD must have a KDS root key)
Set-Service -Name 'MyService' -Credential (New-Object PSCredential("DOMAIN\MyServiceAccount$", (New-Object SecureString)))
```

## 4. Scheduled tasks — PowerShell

```powershell
# List tasks
Get-ScheduledTask                               # all tasks
Get-ScheduledTask -TaskPath '\MyApp\'           # tasks in a folder
Get-ScheduledTask | Where-Object State -eq 'Ready'
Get-ScheduledTaskInfo -TaskName 'MyTask'        # last run time, result, next run

# Create a task
$action  = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NonInteractive -File C:\Scripts\backup.ps1'
$trigger = New-ScheduledTaskTrigger -Daily -At '03:00'
$settings= New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 2) -RestartCount 2 -RestartInterval (New-TimeSpan -Minutes 5)
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest

Register-ScheduledTask -TaskName 'DailyBackup' -TaskPath '\MyApp\' `
    -Action $action -Trigger $trigger -Settings $settings -Principal $principal

# Run a task now (regardless of trigger)
Start-ScheduledTask -TaskName 'DailyBackup' -TaskPath '\MyApp\'

# Enable / disable
Enable-ScheduledTask  -TaskName 'DailyBackup'
Disable-ScheduledTask -TaskName 'DailyBackup'

# Remove a task
Unregister-ScheduledTask -TaskName 'DailyBackup' -Confirm:$false

# Run as a specific user
$principal = New-ScheduledTaskPrincipal -UserId 'DOMAIN\serviceaccount' -LogonType Password
# Note: LogonType Password requires storing credentials in Task Scheduler — prefer gMSA or SYSTEM

# Export and import task definitions
Export-ScheduledTask -TaskName 'DailyBackup' | Out-File backup-task.xml
Register-ScheduledTask -Xml (Get-Content backup-task.xml | Out-String) -TaskName 'DailyBackup'
```

## 5. Common task triggers

```powershell
New-ScheduledTaskTrigger -Daily -At '02:30'
New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Wednesday,Friday -At '08:00'
New-ScheduledTaskTrigger -AtStartup                         # on system boot
New-ScheduledTaskTrigger -AtLogOn                           # on any user logon
New-ScheduledTaskTrigger -AtLogOn -User 'alice'             # on specific user logon
New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 15) -At '00:00' -RepetitionDuration (New-TimeSpan -Hours 24)
                                                             # every 15 min for 24h
```

## 6. Troubleshooting

```powershell
# Last run result (0 = success; see Task Scheduler error codes)
(Get-ScheduledTaskInfo -TaskName 'DailyBackup').LastTaskResult
# 0x0 = success; 0x1 = error; 0x41300 = task hasn't run yet; 0x80070002 = file not found

# Event log for task scheduler
Get-WinEvent -LogName 'Microsoft-Windows-TaskScheduler/Operational' -MaxEvents 50 |
    Where-Object { $_.Message -match 'DailyBackup' }

# Service event log
Get-EventLog -LogName System -Source 'Service Control Manager' -Newest 20

# Check service dependencies
Get-Service 'Spooler' | Select-Object -ExpandProperty DependentServices
Get-Service 'Spooler' | Select-Object -ExpandProperty ServicesDependedOn
```

---

## Daily workflows

### "Why didn't my scheduled task run?"
```powershell
Get-ScheduledTaskInfo 'DailyBackup'   # LastRunTime, LastTaskResult, NextRunTime
Get-WinEvent -LogName 'Microsoft-Windows-TaskScheduler/Operational' |
    Where-Object Message -match 'DailyBackup' | Select-Object -First 10
```

### "Restart a service that crash-loops"
```powershell
sc failure "MyService" reset= 86400 actions= restart/5000/restart/5000/restart/5000
Get-Service 'MyService' | Restart-Service
```

### "Create a task that runs every hour as SYSTEM"
```powershell
Register-ScheduledTask -TaskName 'HourlyCleanup' -TaskPath '\Ops\' `
  -Action (New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-File C:\Scripts\cleanup.ps1') `
  -Trigger (New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 1) -At '00:00' -RepetitionDuration ([TimeSpan]::MaxValue)) `
  -Principal (New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest)
```

## Gotchas / Golden rules

1. **Task Scheduler uses the account's stored credentials** — if the service account password changes, every task running under that account must be updated; use gMSA or SYSTEM to avoid this.
2. **`LastTaskResult 0x41301` means the task is currently running** — not an error; check if it's stuck (past its expected duration).
3. **`sc config` needs a space after `=`** — `sc config Spooler start= auto` (with space) works; `sc config Spooler start=auto` fails silently.
4. **Services set to Automatic may not start if dependencies fail** — check DependentServices; use Automatic (Delayed Start) for services that don't need to be ready at boot.
5. **Task Scheduler action paths must be absolute** — relative paths are resolved from `C:\Windows\System32`; always use full paths in `-Execute` and `-Argument`.
