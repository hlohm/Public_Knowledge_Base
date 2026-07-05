---
type: cheatsheet
area: "Windows Administration"
aliases: [local users, net user, ADUC, Active Directory Users and Computers, user management]
tags: [windows, users, groups, active-directory, administration]
status: working
---

# Windows User & Group Management

> **Area:** [[Windows Administration]]

Creating, querying, and modifying local and Active Directory users and groups via PowerShell, plus the legacy `net.exe` equivalents. Standing up the domain controller itself is covered in [[Primary Domain Controller — New Forest Setup]].

---

## 1. Local users — PowerShell

```powershell
New-LocalUser -Name 'alice' -FullName 'Alice Smith' -Description 'Local admin' `
    -Password (ConvertTo-SecureString 'P@ssw0rd!' -AsPlainText -Force) -AccountNeverExpires
Get-LocalUser                                    # list all local accounts
Get-LocalUser -Name 'alice' | Format-List *       # full detail on one account
Set-LocalUser -Name 'alice' -PasswordNeverExpires $false -Description 'Updated'
Rename-LocalUser -Name 'alice' -NewName 'asmith'
Disable-LocalUser -Name 'alice'                  # keep the account, block logon
Enable-LocalUser -Name 'alice'
Remove-LocalUser -Name 'alice'
```

## 2. Local groups — PowerShell

```powershell
New-LocalGroup -Name 'Deployers' -Description 'Can run deployment scripts'
Get-LocalGroup
Get-LocalGroupMember -Group 'Administrators'
Add-LocalGroupMember -Group 'Administrators' -Member 'alice'
Remove-LocalGroupMember -Group 'Administrators' -Member 'alice'
```

## 3. Local users/groups — net.exe (legacy, still useful for scripting old images)

```cmd
net user                                    # list local accounts
net user alice                              # detail on one account
net user alice P@ssw0rd! /add               # create
net user alice /active:no                   # disable
net user alice /delete
net localgroup Administrators alice /add
net localgroup Administrators alice /delete
```

## 4. AD users — query & create

```powershell
Import-Module ActiveDirectory                # RSAT / installed automatically on a DC

Get-ADUser -Filter *                                          # every user (careful in large domains)
Get-ADUser -Identity alice -Properties *                       # all attributes for one user
Get-ADUser -Filter "Name -like '*smith*'"                     # wildcard search
Get-ADUser -Filter "Enabled -eq `$false"                      # disabled accounts

New-ADUser -Name 'Alice Smith' -SamAccountName 'alice' `
    -UserPrincipalName 'alice@corp.example.com' `
    -Path 'OU=Users,OU=Corp,DC=corp,DC=example,DC=com' `
    -AccountPassword (ConvertTo-SecureString 'P@ssw0rd!' -AsPlainText -Force) `
    -Enabled $true -ChangePasswordAtLogon $true
```

## 5. AD users — modify, disable, unlock, reset password

```powershell
Set-ADUser -Identity alice -Title 'Sysadmin' -Department 'IT' -EmailAddress 'alice@corp.example.com'
Set-ADAccountPassword -Identity alice -Reset `
    -NewPassword (ConvertTo-SecureString 'N3wP@ssw0rd!' -AsPlainText -Force)
Unlock-ADAccount -Identity alice
Disable-ADAccount -Identity alice             # offboarding: disable before delete
Enable-ADAccount -Identity alice
Move-ADObject -Identity 'CN=Alice Smith,OU=Users,DC=corp,DC=example,DC=com' `
    -TargetPath 'OU=Disabled Users,DC=corp,DC=example,DC=com'
Remove-ADUser -Identity alice -Confirm:$false

# Fleet-wide status checks
Search-ADAccount -LockedOut                   # everyone currently locked out
Search-ADAccount -AccountExpired
Search-ADAccount -PasswordNeverExpires -UsersOnly
```

## 6. AD groups

```powershell
New-ADGroup -Name 'IT-Admins' -GroupScope Global -GroupCategory Security `
    -Path 'OU=Groups,DC=corp,DC=example,DC=com'
Add-ADGroupMember -Identity 'IT-Admins' -Members alice, bob
Remove-ADGroupMember -Identity 'IT-Admins' -Members alice -Confirm:$false
Get-ADGroupMember -Identity 'IT-Admins'                       # direct members
Get-ADPrincipalGroupMembership -Identity alice                # every group alice belongs to (incl. nested)
```

## 7. AD organizational units (OUs)

```powershell
New-ADOrganizationalUnit -Name 'Servers' -Path 'DC=corp,DC=example,DC=com' `
    -ProtectedFromAccidentalDeletion $true
Get-ADOrganizationalUnit -Filter * | Select-Object Name, DistinguishedName
Set-ADOrganizationalUnit -Identity 'OU=Servers,DC=corp,DC=example,DC=com' -Description 'Member servers'
```

## 8. Bulk operations from CSV

```powershell
# users.csv columns: Name,SamAccountName,OU,Password
Import-Csv .\users.csv | ForEach-Object {
    New-ADUser -Name $_.Name -SamAccountName $_.SamAccountName `
        -UserPrincipalName "$($_.SamAccountName)@corp.example.com" `
        -Path $_.OU `
        -AccountPassword (ConvertTo-SecureString $_.Password -AsPlainText -Force) `
        -Enabled $true -ChangePasswordAtLogon $true
}
```

## 9. Password & lockout policy

```powershell
Get-ADDefaultDomainPasswordPolicy                              # domain-wide baseline
Set-ADDefaultDomainPasswordPolicy -Identity corp.example.com `
    -LockoutThreshold 5 -LockoutDuration '00:30:00' -LockoutObservationWindow '00:30:00'
Get-ADFineGrainedPasswordPolicy -Filter *                       # per-OU/group overrides (2008+ domain mode)
```

---

## Daily workflows

### "Onboard a new starter"
```powershell
New-ADUser -Name 'Bob Jones' -SamAccountName 'bjones' -UserPrincipalName 'bjones@corp.example.com' `
    -Path 'OU=Users,DC=corp,DC=example,DC=com' `
    -AccountPassword (ConvertTo-SecureString 'TempP@ss1!' -AsPlainText -Force) `
    -Enabled $true -ChangePasswordAtLogon $true
Add-ADGroupMember -Identity 'IT-Admins' -Members bjones
```

### "Find and unlock a locked-out account"
```powershell
Search-ADAccount -LockedOut | Select-Object Name, SamAccountName
Unlock-ADAccount -Identity bjones
```

### "Offboard a leaver"
```powershell
Disable-ADAccount -Identity bjones
Get-ADPrincipalGroupMembership -Identity bjones | ForEach-Object { Remove-ADGroupMember -Identity $_ -Members bjones -Confirm:$false }
Move-ADObject -Identity (Get-ADUser bjones).DistinguishedName -TargetPath 'OU=Disabled Users,DC=corp,DC=example,DC=com'
```

## Gotchas / Golden rules

1. **`SamAccountName` is capped at 20 characters and must be unique domain-wide** — `New-ADUser` errors on collision; older GUI tools silently truncate instead, so a name that "worked" in ADUC can still fail from PowerShell.
2. **Local and AD cmdlets look alike but come from different modules** — `Microsoft.PowerShell.LocalAccounts` vs `ActiveDirectory`. Running an AD cmdlet without domain connectivity fails with "Unable to find a default server" — you need RSAT installed and a reachable DC.
3. **`New-ADUser -Enabled $true` still needs a password that meets complexity** — a weak password with `-Enabled $true` throws and can leave a half-created, disabled account behind; check with `Get-ADUser` after any bulk import.
4. **`Search-ADAccount -LockedOut` only reflects the DC it queries** — in multi-DC domains lockout status can lag until replication catches up; query the PDC emulator for the authoritative answer.
5. **Deleting a user does not clean up their SID from ACLs and group memberships elsewhere** — orphaned SIDs accumulate as "Account Unknown" entries; remove group membership before deletion when precision matters, or budget time later to clean up stale ACEs.

## See also

- [[powershell-cmdlets]] — general admin cmdlet reference (registry, network, disks)
- [[windows-services]] · [[windows-events]]
- [[Primary Domain Controller — New Forest Setup]] — stand up the DC these cmdlets talk to
