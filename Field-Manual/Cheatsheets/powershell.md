---
type: cheatsheet
area: "Windows Administration"
aliases: [pwsh, PS]
tags: [windows, powershell, scripting, administration]
status: working
---

# PowerShell

> **Area:** [[Windows Administration]]

PowerShell is an object-oriented shell and scripting language. Unlike Unix shells, commands output .NET objects — not text — so pipes pass structured data rather than strings. Runs on Windows, macOS, and Linux (PowerShell 7+).

> **PowerShell 5.1** ships with Windows (legacy, Windows-only). **PowerShell 7+** (`pwsh`) is the cross-platform successor. Prefer 7+ for new scripts; 5.1 for Group Policy and Windows-only modules.

---

## 1. Getting help and exploring

```powershell
Get-Help Get-Process                # help for a cmdlet
Get-Help Get-Process -Examples      # examples only
Get-Help Get-Process -Full          # full help (man page equivalent)
Update-Help                         # download latest help content

Get-Command -Name '*Service*'       # find cmdlets matching a pattern
Get-Command -Module ActiveDirectory # all cmdlets from a module
Get-Alias ls                        # what does 'ls' alias to?

Get-Member -InputObject $obj        # show all properties and methods of an object
$obj | Get-Member                   # same, pipeline form

# Discover properties of output
Get-Process | Get-Member
Get-Process | Select-Object -First 1 | Format-List *   # all properties of one process
```

## 2. Objects and the pipeline

The pipeline passes .NET objects, not text:

```powershell
Get-Process | Where-Object { $_.CPU -gt 10 }          # filter objects by property
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
Get-Process | Select-Object Name, Id, CPU              # project specific properties
Get-Process | Measure-Object CPU -Sum -Average         # aggregate

# Property access
$proc = Get-Process -Name explorer
$proc.Id
$proc.MainWindowTitle

# ForEach-Object
Get-Process | ForEach-Object { Write-Host "$($_.Name): $($_.WorkingSet64 / 1MB) MB" }

# Group-Object
Get-Process | Group-Object -Property Company | Sort-Object Count -Descending
```

## 3. Cmdlets and common patterns

```powershell
# Output formatting (terminal display — not for pipeline)
Get-Service | Format-Table Name, Status, StartType -AutoSize
Get-Process | Format-List *
Get-Process | Out-GridView    # interactive searchable grid (Windows only)

# Output to file
Get-Service | Export-Csv services.csv -NoTypeInformation
Get-Service | ConvertTo-Json | Out-File services.json

# Input
$csv = Import-Csv data.csv
$json = Get-Content data.json | ConvertFrom-Json

# Filtering
Get-Service | Where-Object Status -eq 'Running'
Get-ChildItem C:\Windows -Filter *.log -Recurse
Get-ChildItem | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }

# String operations
'hello world'.ToUpper()
'hello world' -replace 'world', 'PowerShell'
'a,b,c' -split ','
@('a','b','c') -join '-'
"Name: $($env:USERNAME)"      # string interpolation (double quotes only)
```

## 4. Variables, types, and arithmetic

```powershell
$x = 42
$s = "hello"
$arr = @(1, 2, 3)
$hash = @{Name="Alice"; Role="Admin"}   # hashtable
[int]$count = 0                          # typed variable

# Type coercion
[int]"42" + 1          # 43
[datetime]"2024-06-01"

# Arithmetic
5 / 2               # 2.5 (not integer division)
[math]::Floor(5/2)  # 2
[math]::Round(3.567, 2)  # 3.57

# Arrays
$arr = @(1, 2, 3, 4, 5)
$arr[0]             # first element
$arr[-1]            # last element
$arr[1..3]          # slice
$arr.Count
$arr += 6           # append (creates a new array)
$arr | Measure-Object -Sum

# Hashtables
$h = @{Key="Value"; Count=3}
$h['Key']
$h.Key
$h.Count            # note: this is the hashtable's .Count property (number of entries)
$h.GetEnumerator() | Sort-Object Name
```

## 5. Control flow

```powershell
# If / elseif / else
if ($x -gt 10) {
    Write-Host "big"
} elseif ($x -gt 5) {
    Write-Host "medium"
} else {
    Write-Host "small"
}

# Comparison operators: -eq -ne -lt -le -gt -ge -like -match -contains -in
# -like: wildcard (*,?); -match: regex; -contains: array contains element

# Switch
switch ($day) {
    "Monday"  { "Start of week" }
    "Friday"  { "End of week" }
    default   { "Midweek" }
}

# Loops
foreach ($item in $collection) { ... }
for ($i = 0; $i -lt 10; $i++) { ... }
while ($condition) { ... }
do { ... } while ($condition)
1..5 | ForEach-Object { $_ * 2 }

# Error handling
try {
    Get-Item C:\nonexistent -ErrorAction Stop
} catch [System.IO.FileNotFoundException] {
    Write-Error "Not found: $_"
} finally {
    Write-Host "Always runs"
}
```

## 6. Functions and scripts

```powershell
function Get-Greeting {
    param(
        [Parameter(Mandatory)]
        [string]$Name,
        [string]$Title = "Hello"
    )
    "$Title, $Name!"
}

Get-Greeting -Name "Alice"
Get-Greeting -Name "Bob" -Title "Greetings"

# Script parameters (at the top of a .ps1 file)
param(
    [Parameter(Mandatory)]
    [string]$Environment,
    [switch]$Verbose,
    [int]$Timeout = 30
)

# Approved verbs: Get, Set, New, Remove, Start, Stop, Invoke, Import, Export…
# Use: Get-Verb to list all approved verbs
```

## 7. Execution policy and modules

```powershell
Get-ExecutionPolicy                          # current policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser   # allow local scripts
# Policies: Restricted, AllSigned, RemoteSigned, Unrestricted, Bypass

# Modules
Get-Module -ListAvailable                    # all installed modules
Import-Module ActiveDirectory
Get-Module                                   # loaded modules

Install-Module PSReadLine -Scope CurrentUser  # PowerShell Gallery
Find-Module -Name 'Az.*'                     # search the gallery
Update-Module PSReadLine

# Profile
$PROFILE                                     # path to your profile script
New-Item -Path $PROFILE -Force               # create it if it doesn't exist
notepad $PROFILE                             # edit it
```

## 8. Remoting

```powershell
# PowerShell remoting (WinRM)
Enable-PSRemoting -Force                     # on the target (run as admin)
Enter-PSSession -ComputerName server01       # interactive remote session
Invoke-Command -ComputerName server01,server02 -ScriptBlock { Get-Service | Where Status -eq Stopped }

# Copy file to remote
Copy-Item C:\local\file.txt -Destination "\\server01\c$\remote\"
# Or via PSSession:
$s = New-PSSession -ComputerName server01
Copy-Item file.txt -ToSession $s -Destination C:\remote\
Remove-PSSession $s

# SSH remoting (PowerShell 7+ with OpenSSH)
Enter-PSSession -HostName server01 -UserName alice -SSHTransport
```

---

## Daily workflows

### "Find and restart a stopped service"
```powershell
Get-Service -Name 'Spooler' | Start-Service
Get-Service | Where-Object Status -eq 'Stopped' | Select-Object Name, DisplayName
```

### "Get the top 10 memory-consuming processes"
```powershell
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, Id, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,1)}}
```

### "Search event log for recent errors"
```powershell
Get-WinEvent -LogName System -MaxEvents 100 | Where-Object LevelDisplayName -eq 'Error'
```

### "Run a command on multiple servers"
```powershell
Invoke-Command -ComputerName server01,server02 -ScriptBlock {
    (Get-Service -Name wuauserv).Status
}
```

## Gotchas / Golden rules

1. **`$_` is the pipeline variable; outside a pipeline it's undefined** — `$_` means "current object" only inside `ForEach-Object`, `Where-Object`, `Select-Object` scriptblocks, and catch blocks.
2. **`-eq` is case-insensitive by default** — use `-ceq` for case-sensitive comparison.
3. **`$null` and empty string are different** — `if ($x)` is false for `$null`, `""`, `0`, and `@()`; use `if ($null -eq $x)` for explicit null checks.
4. **Single quotes are literal; double quotes interpolate** — `'$env:USERNAME'` is the literal string; `"$env:USERNAME"` expands the variable.
5. **`Format-*` breaks the pipeline for data processing** — `Format-Table` / `Format-List` produce formatting objects, not data; always apply formatting last or use `Select-Object` + `Export-Csv` if you need data further downstream.
