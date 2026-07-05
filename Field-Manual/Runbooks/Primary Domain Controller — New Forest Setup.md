---
type: runbook
area: "Windows Administration"
tags: [windows, active-directory, ad-ds, domain-controller, dns, new-forest]
status: working
---

# Primary Domain Controller — New Forest Setup

> **Area:** [[Windows Administration]]

Stand up the first domain controller in a brand-new Active Directory forest: static networking, the AD DS role, forest/domain promotion, DNS verification, a baseline OU structure, and the first System State backup.

> This covers a **new forest's first DC** only. Adding a DC to an existing domain, or promoting a replica DC, is a different flow (join with existing domain credentials, no DSRM new-forest parameters) and isn't covered here.

---

## When to use

Standing up a new AD forest from scratch — a new company, a lab environment, or an isolated environment that needs its own directory. Not for adding a second/replica DC to an existing domain.

## Prerequisites

- Windows Server (2019/2022+) installed, licensed, and patched
- A static IP already assigned to the NIC — do this before touching DNS, since this box becomes its own DNS server
- Hostname decided **before** promotion — renaming after promotion is another disruptive cycle
- Local Administrator access
- Decided in advance: forest root domain FQDN (e.g. `corp.example.com` — use a name you control, not a public TLD you don't own), NetBIOS name, and forest/domain functional level
- A DSRM (Directory Services Restore Mode) password chosen and stored securely — this is the "break glass" password for AD DS restore
- **A VM snapshot/checkpoint taken immediately before Step 4** — the cheapest rollback path for a from-scratch forest
- A plan for external time sync (public NTP, or the org's existing time source)

---

## Step 1 — Set a static IP and point DNS at itself

```powershell
New-NetIPAddress -InterfaceAlias 'Ethernet' -IPAddress 10.0.0.10 -PrefixLength 24 -DefaultGateway 10.0.0.1
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 127.0.0.1
# Once AD DS/DNS is installed, this server becomes its own DNS server.
```

*Verify:* `Get-NetIPAddress -InterfaceAlias 'Ethernet'` shows the static address; `Test-Connection <gateway>` succeeds.

---

## Step 2 — Rename the computer

```powershell
Rename-Computer -NewName 'DC01' -Restart
```

*Verify:* After reboot, `$env:COMPUTERNAME` returns `DC01`.

---

## Step 3 — Install the AD DS role

```powershell
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
```

*Verify:* `Get-WindowsFeature AD-Domain-Services` shows `Installed`.

---

## Step 4 — Promote to the first DC of a new forest

```powershell
Import-Module ADDSDeployment

$dsrm = Read-Host -AsSecureString 'DSRM password'

Install-ADDSForest `
    -DomainName 'corp.example.com' `
    -DomainNetbiosName 'CORP' `
    -ForestMode 'WinThreshold' `      # highest level widely available as of Server 2019/2022 — check
    -DomainMode 'WinThreshold' `      # `Install-ADDSForest -DomainName ... -WhatIf` for the current max on newer builds
    -InstallDns:$true `
    -SafeModeAdministratorPassword $dsrm `
    -NoRebootOnCompletion:$false `
    -Force:$true
```

Functional level, once raised, cannot be lowered without rebuilding the domain — pick the newest level every planned future DC will support. The server reboots automatically when this completes.

*Verify:* The server reboots and you can log on as `CORP\Administrator`.

---

## Step 5 — Confirm AD DS and DNS came up clean

```powershell
Get-Service NTDS, DNS, Netlogon, kdc | Select-Object Name, Status
dcdiag /v
Get-ADDomain
Get-ADForest
```

*Verify:* All four services show `Running`; `dcdiag` reports "passed test" for every test with no failures.

---

## Step 6 — Verify DNS is serving the AD zones and SRV records

```powershell
Resolve-DnsName -Name corp.example.com -Type A
Resolve-DnsName -Name _ldap._tcp.dc._msdcs.corp.example.com -Type SRV
dcdiag /test:dns /v
```

*Verify:* The SRV record resolves to `DC01.corp.example.com`; `dcdiag /test:dns` passes.

---

## Step 7 — Configure DNS forwarders for external resolution

```powershell
Add-DnsServerForwarder -IPAddress 1.1.1.1, 9.9.9.9
Get-DnsServerForwarder
```

*Verify:* `Resolve-DnsName www.example.com` (a public name) resolves through the DC.

---

## Step 8 — Sync the PDC emulator to an external time source

```powershell
w32tm /config /manualpeerlist:"time.cloudflare.com,0x8 time.windows.com,0x8" /syncfromflags:manual /reliable:yes /update
Restart-Service w32time
w32tm /query /status
w32tm /query /source
```

*Verify:* `w32tm /query /source` shows the configured NTP peer, not `Local CMOS Clock`.

*Why:* the PDC emulator is the authoritative time source for the whole domain — Kerberos allows only a 5-minute clock skew, and every other DC and domain member syncs from this one by default.

---

## Step 9 — Create the baseline OU structure

```powershell
$base = 'DC=corp,DC=example,DC=com'
'Tier0', 'Servers', 'Workstations', 'Users', 'Groups', 'Service Accounts' | ForEach-Object {
    New-ADOrganizationalUnit -Name $_ -Path $base -ProtectedFromAccidentalDeletion $true
}
Get-ADOrganizationalUnit -Filter * | Select-Object Name, DistinguishedName
```

*Verify:* Each OU appears in the output and in `dsa.msc`. `-ProtectedFromAccidentalDeletion` blocks casual removal via cmdlet or GUI.

---

## Step 10 — Enable the AD Recycle Bin

```powershell
Enable-ADOptionalFeature 'Recycle Bin Feature' -Scope ForestOrConfigurationSet -Target corp.example.com -Confirm:$false
```

*Verify:* `Get-ADOptionalFeature -Filter 'Name -eq "Recycle Bin Feature"'` shows `EnabledScopes` populated.

*Why now:* this cannot be disabled once enabled, so there's no cost to doing it on day one — and without it, recovering a deleted object later means an authoritative restore instead of a one-line `Restore-ADObject`.

---

## Step 11 — Take the first System State backup

```powershell
Install-WindowsFeature Windows-Server-Backup
wbadmin start systemstatebackup -backupTarget:E: -quiet
```

*Verify:* `wbadmin get versions` lists the backup.

*Why:* with a single DC, there is no replication partner yet — this backup is the only recovery path until a second DC exists.

---

## Rollback

- **Before Step 4 completes:** revert to the pre-promotion snapshot taken in Prerequisites. This is the cleanest option — a partially-promoted DC can leave AD DS in a state that `Uninstall-ADDSDomainController` doesn't cleanly resolve on a first-in-forest DC.
- **After Step 4 (forest now exists):** demoting the only DC in a forest destroys the domain — there is no undo that preserves objects.
  ```powershell
  Uninstall-ADDSDomainController -DemoteOperationMasterRole -RemoveApplicationPartitions -Force
  ```
  This returns the machine to a standalone server with the forest gone. Prefer restoring the VM snapshot and starting over from Step 3.
- **Steps 5–7 fail (DNS/dcdiag issues):** safe to fix in place — no destructive state has been created yet.

## Done when

- [ ] `Get-Service NTDS,DNS,Netlogon` all show `Running`
- [ ] `dcdiag /v` passes every test
- [ ] `Get-ADDomain` / `Get-ADForest` return the expected domain/forest names and functional levels
- [ ] `_ldap._tcp.dc._msdcs.<domain>` SRV record resolves
- [ ] External name resolution works through the DC's forwarders
- [ ] `w32tm /query /source` shows an external NTP peer, not the local CMOS clock
- [ ] Baseline OUs exist and are protected from accidental deletion
- [ ] AD Recycle Bin is enabled
- [ ] A verified System State backup exists

## See also

- [[windows-users]] — create the first real AD user/group accounts once the forest exists
- [[windows-events]] — Security log auditing, DCSync detection (Event ID 4662)
- [[powershell-cmdlets]] · [[powershell]]
- [[Windows OS Hardening]] — S3 Domain Controller section: Tier 0 isolation, Protected Users, RODCs, no Print Spooler on DCs. Apply before the DC touches production traffic.
- Adding a second DC for replication/redundancy is a different flow — not covered here.
