---
type: playbook
area: "Windows Administration"
tags: [hardening, security, windows, bitlocker, defender, gpo, audit, lsass, ntlm, smb, wdac, credential-guard]
status: working
---

# Windows OS Hardening

> **Area:** [[Windows Administration]]

A decision-tree hardening reference for Windows — client (10/11) and server (2016/2019/2022) — across internet-facing servers, domain infrastructure, VMs, workstations, laptops, and privileged access machines. Pick your threat model and system profile; follow the Fix sections that apply.

> Three Windows-specific threat axes dominate every engagement: **credential theft** (LSASS dumping, hash extraction), **lateral movement** (Pass-the-Hash, NTLM relay, SMB exploitation), and **execution** (malicious scripts, macro abuse, LOLBin chaining). The Fix sections address all three; the decision table gates which depth is proportionate.

## Situation

- You are deploying or re-imaging a Windows host and need to harden it from baseline, **or**
- An existing system needs a posture review or uplift to a new threat model.

## Quick assessment (first 3 commands)

```powershell
# OS version, patch level, VM or bare metal
Get-ComputerInfo | Select-Object OsName, OsVersion, OsBuildNumber, CsHyperVisorPresent

# Current listening surface — the first thing to shrink
Get-NetTCPConnection -State Listen |
    Select-Object LocalAddress, LocalPort,
        @{n='Process';e={(Get-Process -Id $_.OwningProcess -EA SilentlyContinue).Name}} |
    Sort-Object LocalPort

# Installed roles and features (Server) / enabled optional features (Client)
Get-WindowsFeature | Where-Object Installed | Select-Object Name, DisplayName  # Server
Get-WindowsOptionalFeature -Online | Where-Object State -eq Enabled | Select-Object FeatureName  # Client
```

---

## Threat model

Same four tiers as [[Unix OS Hardening]]; inherit all lower-tier controls.

| Tier | Adversary | Typical context |
|---|---|---|
| **TM0** | Automated scanners, commodity ransomware, credential stuffers | Any internet-facing host |
| **TM1** | Targeted attacker; commodity tools; opportunistic lateral movement | Domain members, internet-exposed servers |
| **TM2** | Motivated adversary; custom tools; credential dumping; insider risk | Sensitive servers, production workstations |
| **TM3** | State-level; firmware/supply-chain attacks; advanced persistence | Domain Controllers, privileged infrastructure |

**Provider trust ceiling on VMs / Azure:** the hypervisor operator is in the TCB. BitLocker protects data-at-rest on a decommissioned or stolen disk; it does not protect against the platform operator.

---

## System profile

| Code | Form factor |
|---|---|
| **S1** | Internet-facing server (IIS, ADFS, RDP Gateway, DNS) |
| **S2** | Internal member server (file, SQL, CI/CD, app) |
| **S3** | Domain Controller |
| **S4** | Azure VM / cloud instance |
| **S5** | Workstation (domain-joined) |
| **S6** | Laptop |
| **S7** | Privileged Access Workstation (PAW) |
| **S8** | Standalone / workgroup machine |

---

## Decision branches

Sections: **A** Baseline · **B** Firmware & Boot · **C** BitLocker · **D** OS & Protocol · **E** Auth & Access · **F** Firewall · **G** Services & Features · **H** Defender & ASR · **I** Audit & Logging · **J** Application Control · **K** Vuln Management · **L** Advanced Controls · **M** Measured Boot

| Profile | TM0 minimum | + TM1 | + TM2 | + TM3 |
|---|---|---|---|---|
| S1 internet server | A D E F G H | + I J K | + L | + B M |
| S2 internal server | A D E F G | + H I J K | + L | + B M |
| S3 Domain Controller | A D E F G H I | + J K | + L M | + B M |
| S4 Azure VM / cloud | A D E F G H I | + J K | + L | — |
| S5 workstation | A D E F G H | + I J K | + C L | + B M |
| S6 laptop | A C D E F G H | + I J K | + B L | + B M |
| S7 PAW | A B C D E F G H I J K L | + M | + M | + M |
| S8 standalone | A D E F G | + H I | + C L | + B M |

---

## Fix A — Universal Baseline

Applies to **every** Windows system at every tier.

**Windows Update — enable automatic security updates:**

```powershell
# Verify update service is running
Get-Service wuauserv | Select-Object Status, StartType

# Check pending updates
Get-WindowsUpdate  # requires PSWindowsUpdate module: Install-Module PSWindowsUpdate
```

For domain members, configure Windows Update via GPO: Computer Configuration → Administrative Templates → Windows Components → Windows Update.

**Remove unneeded roles and features:**

```powershell
# Server: uninstall unused roles immediately after install
Get-WindowsFeature | Where-Object Installed | Select-Object Name

# Example: remove IIS if this is not a web server
Uninstall-WindowsFeature -Name Web-Server -IncludeManagementTools

# Client: disable unused optional features
Get-WindowsOptionalFeature -Online | Where-Object State -eq Enabled |
    Where-Object FeatureName -like "TelnetClient" |
    Disable-WindowsOptionalFeature -Online -NoRestart
```

**Built-in accounts:**

```powershell
# Rename the built-in Administrator account (makes it harder to target by name)
Rename-LocalUser -Name Administrator -NewName <admin-alias>

# Disable the built-in Guest account (should be disabled by default; confirm)
Disable-LocalUser -Name Guest

# Disable the built-in Administrator account where a named admin account exists
Disable-LocalUser -Name Administrator
```

**AutoPlay / AutoRun** — a persistent malware delivery vector:

```powershell
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
  -Name NoDriveTypeAutoRun -Type DWord -Value 255    # 255 = disable on all drive types
```

**Screen lock / idle timeout:**

```powershell
# GPO: Computer Configuration → Windows Settings → Security Settings → Local Policies → Security Options
# "Interactive logon: Machine inactivity limit" → 900 seconds (15 min)
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" `
  -Name InactivityTimeoutSecs -Type DWord -Value 900
```

---

## Fix B — Firmware & Boot

Primarily for **bare metal** (S5, S6, S7) and physical servers (S1, S2, S3). VMs inherit the hypervisor's boot security model.

**UEFI Secure Boot** — verify it is active and enforcing:

```powershell
Confirm-SecureBootUEFI      # returns True if active; throws if BIOS/legacy boot
(Get-CimInstance -Class Win32_BIOS).SecureBootState  # alternative check
```

**TPM 2.0** — prerequisite for BitLocker + Credential Guard + Measured Boot:

```powershell
Get-Tpm | Select-Object TpmPresent, TpmReady, TpmEnabled, TpmActivated, ManufacturerId
# TpmPresent and TpmReady must both be True before proceeding
```

**BIOS/UEFI password** — prevents changing boot order or loading a different OS.

**GRUB equivalent — Windows Boot Manager** — use BitLocker PIN (Fix C) to require pre-boot authentication; this is the Windows mechanism for preventing tampered-boot attacks.

**Windows Boot Manager integrity** — Secure Boot + HVCI (Fix L) together form the Windows equivalent of a GRUB password + verified boot combination.

---

## Fix C — BitLocker FDE

Mandatory for **S6 (laptop)**; strongly recommended for all physical hosts with sensitive data. On Azure / Hyper-V: protects data-at-rest against decommissioned or stolen disks, **not** against the platform operator.

**Enable BitLocker with TPM + PIN** (most secure pre-boot posture):

```powershell
# Verify prerequisites
Get-Tpm
Confirm-SecureBootUEFI

# Enable BitLocker on the OS drive with TPM + PIN
Enable-BitLocker -MountPoint "C:" `
  -EncryptionMethod XtsAes256 `
  -TpmAndPinProtector `
  -Pin (ConvertTo-SecureString "<pin>" -AsPlainText -Force)

# Add a recovery key protector and back up to AD (domain-joined) or Azure AD
Add-BitLockerKeyProtector -MountPoint "C:" -RecoveryPasswordProtector
# Back up the recovery key to AD:
$keyProtector = (Get-BitLockerVolume -MountPoint "C:").KeyProtector |
    Where-Object KeyProtectorType -eq "RecoveryPassword"
Backup-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId $keyProtector.KeyProtectorId
```

**BitLocker Network Unlock (headless servers)** — unlocks automatically when the server boots on the trusted management network; requires a WDS server with the Network Unlock role:

```powershell
# On the server being protected
Add-BitLockerKeyProtector -MountPoint "C:" -NetworkUnlockProtector
```

**Check BitLocker status:**

```powershell
Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, EncryptionMethod, EncryptionPercentage, ProtectionStatus
# ProtectionStatus must be "On"; VolumeStatus must be "FullyEncrypted"
```

**Encrypt all data volumes**, not just the OS drive:

```powershell
Get-Volume | Where-Object DriveLetter -ne $null | ForEach-Object {
    Enable-BitLocker -MountPoint "$($_.DriveLetter):" -EncryptionMethod XtsAes256 -RecoveryPasswordProtector
}
```

*Verify:* a reboot prompts for the PIN (or unlocks via TPM if configured TPM-only); `Get-BitLockerVolume` shows `FullyEncrypted` and `ProtectionStatus: On`.

---

## Fix D — OS & Protocol Hardening

The most Windows-specific section; apply on **every** Windows system. These controls close the attack vectors most commonly exploited in the wild: SMB/NTLM exploitation, credential caching in memory, and legacy protocol abuse.

**Disable SMBv1** — EternalBlue (MS17-010) and virtually every ransomware campaign since 2017 use it; there is no legitimate reason to keep it enabled:

```powershell
Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force    # server (receiving) component
Set-SmbClientConfiguration -EnableSMB1Protocol $false -Force    # client (initiating) component

# Also remove the Windows feature (belt + suspenders)
Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart   # Client
Uninstall-WindowsFeature -Name FS-SMB1    # Server with roles

# Verify
Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol
```

**Enable SMB signing** — prevents SMB relay attacks where an attacker intercepts and forwards authenticated SMB sessions:

```powershell
Set-SmbServerConfiguration -RequireSecuritySignature $true -Force
Set-SmbClientConfiguration -RequireSecuritySignature $true -Force
```

**NTLM level — refuse LM and NTLMv1:**

```powershell
# LmCompatibilityLevel 5: send NTLMv2 only; refuse LM + NTLM responses from clients
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" `
  -Name LmCompatibilityLevel -Type DWord -Value 5
```

**WDigest — disable plaintext credential caching in memory** (the primary target of Mimikatz `sekurlsa::wdigest`):

```powershell
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" `
  -Name UseLogonCredential -Type DWord -Value 0
```

**LSA Protection (RunAsPPL)** — makes `lsass.exe` a Protected Process Light; prevents code injection and memory reads even from admin-level processes:

```powershell
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" `
  -Name RunAsPPL -Type DWord -Value 1
# Value 2 = UEFI-locked (requires firmware to undo — stronger, harder to reverse)
# Requires reboot; verify with: Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" | Select-Object RunAsPPL
```

**Disable LLMNR** — Link-Local Multicast Name Resolution; primary vector for Responder/NTLM relay attacks on local networks:

```powershell
# Via registry
New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" -Force | Out-Null
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" `
  -Name EnableMulticast -Type DWord -Value 0
```

GPO path: Computer Configuration → Administrative Templates → Network → DNS Client → Turn off Multicast Name Resolution = Enabled.

**Disable NetBIOS over TCP/IP** — eliminates another NTLM relay capture vector (port 137/138):

```powershell
$interfaces = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces"
foreach ($iface in $interfaces) {
    Set-ItemProperty -Path $iface.PSPath -Name NetbiosOptions -Type DWord -Value 2
    # 0=default (DHCP), 1=enable, 2=disable
}
```

**Disable legacy TLS/SSL** — SSLv3, TLS 1.0, TLS 1.1 are broken; require TLS 1.2+ for all SCHANNEL consumers (IIS, RDP, WinRM, LDAP):

```powershell
function Disable-SChannelProtocol {
    param([string]$Protocol)
    foreach ($role in @("Server", "Client")) {
        $path = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\$Protocol\$role"
        New-Item -Path $path -Force | Out-Null
        Set-ItemProperty -Path $path -Name Enabled -Value 0
        Set-ItemProperty -Path $path -Name DisabledByDefault -Value 1
    }
}
Disable-SChannelProtocol "SSL 2.0"
Disable-SChannelProtocol "SSL 3.0"
Disable-SChannelProtocol "TLS 1.0"
Disable-SChannelProtocol "TLS 1.1"
# On hosts where TLS 1.2/1.3 are confirmed working; do NOT disable before verifying
```

**PowerShell hardening** — enable logging before restricting execution; blindly blocking PowerShell without logging is worse than leaving it open (attackers fall back to cmd.exe, which you can't see):

```powershell
# Module logging (log all module activity)
$mlPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging"
New-Item -Path $mlPath -Force | Out-Null
Set-ItemProperty -Path $mlPath -Name EnableModuleLogging -Value 1
New-ItemProperty -Path $mlPath -Name ModuleNames -PropertyType MultiString -Value "*" -Force

# Script block logging (log all script block content, including deobfuscated form)
$sblPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
New-Item -Path $sblPath -Force | Out-Null
Set-ItemProperty -Path $sblPath -Name EnableScriptBlockLogging -Value 1

# Transcription (full session transcript to a central share)
$txPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription"
New-Item -Path $txPath -Force | Out-Null
Set-ItemProperty -Path $txPath -Name EnableTranscripting -Value 1
Set-ItemProperty -Path $txPath -Name OutputDirectory -Value "\\<log-server>\pstranscripts$"
Set-ItemProperty -Path $txPath -Name EnableInvocationHeader -Value 1
```

**Exploit protection (system-wide defaults):**

```powershell
# DEP: Data Execution Prevention (should already be on; confirm)
Set-ProcessMitigation -System -Enable DEP

# ASLR: force-randomize image base addresses
Set-ProcessMitigation -System -Enable ForceRelocateImages, BottomUp, HighEntropy

# SEHOP: Structured Exception Handler Overwrite Protection
Set-ProcessMitigation -System -Enable SEHOP

# CFG: Control Flow Guard
Set-ProcessMitigation -System -Enable CFG

# Export current settings
Get-ProcessMitigation -System | ConvertTo-Json | Out-File exploitprot-baseline.json
```

**Disable Print Spooler if printing is not needed** (PrintNightmare, SpoolFool, and several other privilege escalation CVEs):

```powershell
Stop-Service -Name Spooler -Force
Set-Service -Name Spooler -StartupType Disabled
```

On Domain Controllers and servers that do not serve as print servers, the Print Spooler must be disabled — no exception.

---

## Fix E — Authentication & Access Control

**Password and lockout policy** (GPO: Computer Configuration → Windows Settings → Security Settings → Account Policies):

| Setting | Recommended value |
|---|---|
| Minimum password length | 14 characters |
| Password complexity | Enabled |
| Maximum password age | 90 days |
| Enforce password history | 24 passwords |
| Account lockout threshold | 5 invalid attempts |
| Account lockout duration | 15 minutes |
| Reset lockout counter after | 15 minutes |

```powershell
# Local policy (non-domain) via net accounts
net accounts /minpwlen:14 /maxpwage:90 /minpwage:1 /uniquepw:24
net accounts /lockoutthreshold:5 /lockoutduration:15 /lockoutwindow:15
```

**UAC — prompt for credentials on secure desktop:**

```powershell
$uacPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
Set-ItemProperty -Path $uacPath -Name EnableLUA                     -Value 1  # must never be 0
Set-ItemProperty -Path $uacPath -Name ConsentPromptBehaviorAdmin    -Value 1  # prompt for creds (not just consent)
Set-ItemProperty -Path $uacPath -Name ConsentPromptBehaviorUser     -Value 0  # auto-deny elevation for standard users
Set-ItemProperty -Path $uacPath -Name PromptOnSecureDesktop         -Value 1  # use isolated secure desktop (prevents shatter attacks)
```

**RDP — Network Level Authentication mandatory:**

```powershell
# Require NLA before the session is established (prevents pre-auth exploitation of the RDP stack)
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" `
  -Name UserAuthentication -Value 1

# Restrict RDP source IPs via Windows Firewall rule (Fix F); do not leave RDP open to 0.0.0.0/0
# Preferred: no public RDP at all; admin via VPN + internal RDP, or RD Gateway with MFA
```

**Restrict WinRM** — Windows Remote Management is a lateral movement path when left open:

```powershell
# Confirm WinRM listener is bound to a specific interface, not 0.0.0.0
Get-WSManInstance winrm/config/listener -Enumerate

# Restrict via firewall rule to management subnet only
New-NetFirewallRule -DisplayName "WinRM HTTPS mgmt only" `
  -Direction Inbound -Protocol TCP -LocalPort 5986 `
  -RemoteAddress <mgmt-subnet> -Action Allow
New-NetFirewallRule -DisplayName "Block WinRM HTTP" `
  -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Block
```

**LAPS (Local Administrator Password Solution)** — randomizes the local administrator password per machine, stored in AD or Azure AD; eliminates Pass-the-Hash lateral movement via shared local admin credentials:

```powershell
# Modern Windows LAPS (built-in from Windows Server 2022 / Windows 11 22H2+)
# Enable via GPO: Computer Configuration → Administrative Templates → System → LAPS

# Legacy LAPS (older systems — deploy via MSI + GPO)
# https://www.microsoft.com/en-us/download/details.aspx?id=46899

# Verify LAPS is working
Get-LapsADPassword -Identity <hostname> -AsPlainText   # modern LAPS
Get-ADComputer <hostname> -Properties ms-Mcs-AdmPwd    # legacy LAPS
```

**Protected Users security group (domain-joined TM1+)** — membership removes NTLM authentication, RC4/DES Kerberos, unconstrained delegation, and credential caching for that account. Apply to all privileged accounts:

```powershell
Add-ADGroupMember -Identity "Protected Users" -Members "<admin-account>"
# Test on a non-critical account first — it removes fallback mechanisms and can break legacy auth
```

**Audit local administrators** — every unexpected member is a persistence mechanism:

```powershell
Get-LocalGroupMember -Group Administrators
# Domain: Get-ADGroupMember -Identity "Domain Admins" -Recursive
```

**Accounts with no password required:**

```powershell
Get-LocalUser | Where-Object { $_.PasswordRequired -eq $false -and $_.Enabled -eq $true }
```

---

## Fix F — Network & Firewall

**Enable Windows Defender Firewall on all three profiles** and set default-deny inbound:

```powershell
Set-NetFirewallProfile -Profile Domain, Public, Private `
  -Enabled True `
  -DefaultInboundAction Block `
  -NotifyOnListen False

# Servers: also default-deny outbound; permit only what the role requires
Set-NetFirewallProfile -Profile Domain, Public, Private -DefaultOutboundAction Block
```

**Define workload-specific inbound rules** (replace any that currently allow `Any` source):

```powershell
# Example: allow HTTPS from anywhere, RDP only from management subnet
New-NetFirewallRule -DisplayName "Allow HTTPS inbound" `
  -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow

New-NetFirewallRule -DisplayName "Allow RDP from mgmt" `
  -Direction Inbound -Protocol TCP -LocalPort 3389 `
  -RemoteAddress <mgmt-subnet> -Action Allow
```

**Block SMB inbound from untrusted networks** — SMB (445) should never be reachable from the internet or from segments that do not need file share access:

```powershell
New-NetFirewallRule -DisplayName "Block SMB from untrusted" `
  -Direction Inbound -Protocol TCP -LocalPort 445 `
  -RemoteAddress <untrusted-range> -Action Block
```

**Outbound rules for servers** (permit only what the role legitimately originates):

```powershell
# DNS, NTP, HTTP/HTTPS
New-NetFirewallRule -DisplayName "Allow DNS out" -Direction Outbound -Protocol UDP -RemotePort 53 -Action Allow
New-NetFirewallRule -DisplayName "Allow NTP out" -Direction Outbound -Protocol UDP -RemotePort 123 -Action Allow
New-NetFirewallRule -DisplayName "Allow HTTPS out" -Direction Outbound -Protocol TCP -RemotePort 443 -Action Allow
New-NetFirewallRule -DisplayName "Allow HTTP out" -Direction Outbound -Protocol TCP -RemotePort 80 -Action Allow
```

**Verify firewall state:**

```powershell
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction
Get-NetFirewallRule | Where-Object Enabled -eq True | Select-Object DisplayName, Direction, Action, Profile | Sort-Object Direction
```

---

## Fix G — Services & Features

**Disable unnecessary services** — each running service is attack surface and a potential lateral movement pivot:

```powershell
$servicesToDisable = @(
    "RemoteRegistry",       # remote registry reads are a recon/persistence path
    "Telnet",               # plaintext remote access — if present, remove it
    "FTP",                  # plaintext file transfer — use SFTP/FTPS
    "SNMP",                 # v1/v2c are unauthenticated; disable if not monitoring via SNMP
    "WMPNetworkSvc",        # Windows Media Player network sharing
    "XblAuthManager",       # Xbox Live auth — irrelevant on servers
    "XboxNetApiSvc"         # Xbox networking — irrelevant on servers
)
foreach ($svc in $servicesToDisable) {
    if (Get-Service -Name $svc -ErrorAction SilentlyContinue) {
        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
        Set-Service -Name $svc -StartupType Disabled
    }
}
```

**Disable Remote Registry** explicitly — it allows registry reads/writes over the network even for accounts that have no SMB share access:

```powershell
Set-Service -Name RemoteRegistry -StartupType Disabled
Stop-Service -Name RemoteRegistry -Force
```

**Review all services running as SYSTEM or LocalService** — any third-party service with elevated rights is a privilege escalation target:

```powershell
Get-WmiObject Win32_Service |
    Where-Object { $_.StartName -in @("LocalSystem", "NT AUTHORITY\LocalService") -and $_.State -eq "Running" } |
    Select-Object Name, DisplayName, StartName, PathName |
    Sort-Object StartName
```

**Remove Windows features not needed on the role:**

```powershell
# IIS (if this is not a web server)
Uninstall-WindowsFeature -Name Web-Server -IncludeManagementTools

# Legacy SMB/CIFS features
Uninstall-WindowsFeature -Name FS-SMB1

# Telnet server and client
Disable-WindowsOptionalFeature -Online -FeatureName TelnetServer -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName TelnetClient -NoRestart

# TFTP client
Disable-WindowsOptionalFeature -Online -FeatureName TFTP -NoRestart

# Windows Media Player (on servers)
Disable-WindowsOptionalFeature -Online -FeatureName WindowsMediaPlayer -NoRestart
```

---

## Fix H — Defender & Attack Surface Reduction

**Verify Defender AV is running with real-time protection and Tamper Protection:**

```powershell
Get-MpComputerStatus | Select-Object `
  AMRunningMode, RealTimeProtectionEnabled, TamperProtectionSource, `
  IoavProtectionEnabled, BehaviorMonitorEnabled, `
  AntispywareSignatureLastUpdated, AntivirusSignatureLastUpdated
# TamperProtectionSource should be "ATP" (Intune/Defender for Endpoint) or "Signatures"
# AMRunningMode should be "Normal" or "Passive" (not "EDR Block Mode" unless intentional)
```

**Configure Defender protection levels:**

```powershell
Set-MpPreference -MAPSReporting Advanced                       # cloud-delivered protection
Set-MpPreference -SubmitSamplesConsent SendSafeSamples
Set-MpPreference -PUAProtection Enabled                        # block potentially unwanted apps
Set-MpPreference -DisableRealtimeMonitoring $false             # ensure it's on
Set-MpPreference -EnableNetworkProtection Enabled              # block malicious domains/IPs
```

**Controlled Folder Access (ransomware protection)** — blocks untrusted processes from modifying protected directories:

```powershell
Set-MpPreference -EnableControlledFolderAccess Enabled
# Default protected: Desktop, Documents, Pictures, Videos, Music, Favorites
# Add custom paths:
Add-MpPreference -ControlledFolderAccessProtectedFolders "D:\CriticalData"
# Add trusted apps if they get blocked:
Add-MpPreference -ControlledFolderAccessAllowedApplications "C:\Program Files\<app>\<app>.exe"
```

**Attack Surface Reduction rules** — kernel-enforced behavioral blocks; start in Audit mode (2), validate, then switch to Block (1):

```powershell
$asrRules = @{
    "D4F940AB-401B-4EFC-AADC-AD5F3C50688A" = 1   # Block Office apps from creating child processes
    "3B576869-A4EC-4529-8536-B80A7769E899" = 1   # Block Office from creating executable content
    "75668C1F-73B5-4CF0-BB93-3ECF5CB7CC84" = 1   # Block Office apps from injecting into processes
    "92E97FA1-2EDF-4476-BDD6-9DD0B4DDDC7B" = 1   # Block Win32 API calls from Office macros
    "D3E037E1-3EB8-44C8-A917-57927947596D" = 1   # Block JS/VBScript from launching downloads
    "5BEB7EFE-FD9A-4556-801D-275E5FFC04CC" = 1   # Block potentially obfuscated scripts
    "BE9BA2D9-53EA-4CDC-84E5-9B1EEEE46550" = 1   # Block executable content from email / webmail
    "9E6C4E1F-7D60-472F-BA1A-A39EF669E4B0" = 1   # Block credential stealing from lsass.exe
    "D1E49AAC-8F56-4280-B9BA-993A6D77406C" = 1   # Block process creation from PSExec/WMI
    "B2B3F03D-6A65-4F7B-A9C7-1C7EF74A9BA4" = 1   # Block untrusted/unsigned processes from USB
    "7674BA52-37EB-4A4F-A9A1-F0F9A1619A2C" = 1   # Block Adobe Reader from creating child processes
    "E6DB77E5-3DF2-4CF1-B95A-636979351E5B" = 1   # Block persistence via WMI event subscription
    "C1DB55AB-C21A-4637-BB3F-A12568109D35" = 1   # Advanced ransomware protection
    "56A863A9-875E-4185-98A7-B882C64B5CE5" = 1   # Block abuse of vulnerable signed drivers
}
foreach ($rule in $asrRules.GetEnumerator()) {
    Add-MpPreference -AttackSurfaceReductionRules_Ids $rule.Key `
                     -AttackSurfaceReductionRules_Actions $rule.Value
}
# Verify
Get-MpPreference | Select-Object -ExpandProperty AttackSurfaceReductionRules_Ids
```

*If ASR rules break a legitimate application:* identify the blocked event (Event ID 1121 in Microsoft-Windows-Windows Defender/Operational), then add an exclusion scoped to the specific executable — not a blanket rule disable.

---

## Fix I — Audit & Logging

**Advanced Audit Policy** — the granular successor to the legacy basic policy; set via `auditpol.exe` or GPO (Computer Configuration → Windows Settings → Security Settings → Advanced Audit Policy Configuration):

```cmd
rem Account Logon
auditpol /set /subcategory:"Credential Validation" /success:enable /failure:enable
auditpol /set /subcategory:"Kerberos Authentication Service" /success:enable /failure:enable
auditpol /set /subcategory:"Kerberos Service Ticket Operations" /success:enable /failure:enable

rem Account Management
auditpol /set /subcategory:"Computer Account Management" /success:enable /failure:enable
auditpol /set /subcategory:"Security Group Management" /success:enable /failure:enable
auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable

rem Logon/Logoff
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Logoff" /success:enable
auditpol /set /subcategory:"Account Lockout" /failure:enable
auditpol /set /subcategory:"Special Logon" /success:enable

rem Privilege Use
auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable

rem Policy Change
auditpol /set /subcategory:"Audit Policy Change" /success:enable /failure:enable
auditpol /set /subcategory:"Authentication Policy Change" /success:enable

rem System
auditpol /set /subcategory:"Security State Change" /success:enable
auditpol /set /subcategory:"Security System Extension" /success:enable
auditpol /set /subcategory:"System Integrity" /success:enable /failure:enable

rem Detailed Tracking — process creation with command line is critical for detecting attacks
auditpol /set /subcategory:"Process Creation" /success:enable

rem DS Access (Domain Controllers only)
auditpol /set /subcategory:"Directory Service Changes" /success:enable
auditpol /set /subcategory:"Directory Service Access" /success:enable /failure:enable
```

Enable command-line logging for process creation events (Event ID 4688):

```powershell
# GPO: Computer Configuration → Administrative Templates → System → Audit Process Creation
# → Include command line in process creation events = Enabled
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit" `
  -Name ProcessCreationIncludeCmdLine_Enabled -Type DWord -Value 1
```

**Security event log sizing** — the default 64 MB log is far too small for any production system:

```powershell
wevtutil sl Security /ms:1073741824   # 1 GB — minimum for production
wevtutil sl System /ms:104857600      # 100 MB
wevtutil sl Application /ms:104857600

# Verify
wevtutil gl Security | Select-String maxSize
```

**Key Event IDs to monitor** (forward all to SIEM; alert on these specifically):

| Event ID | Meaning | Priority |
|---|---|---|
| 4624 | Successful logon | Medium |
| 4625 | Failed logon | High (threshold alert) |
| 4648 | Explicit credential logon (`runas`) | High |
| 4672 | Special privileges assigned (admin logon) | High |
| 4688 | Process created (with command line) | Medium |
| 4697 | Service installed | Critical |
| 4698 | Scheduled task created | Critical |
| 4719 | Audit policy changed | Critical |
| 4720 | User account created | High |
| 4728 / 4732 / 4756 | User added to privileged group | Critical |
| 4776 | NTLM credential validation | Medium |
| 5140 | Network share accessed | Medium |
| 7045 | Service installed (System log) | Critical |

**Windows Event Forwarding (WEF)** — ship logs to a Windows Event Collector without a third-party agent:

```powershell
# On the collector:
wecutil qc /quiet                       # configure the collector service
wevtutil gl ForwardedEvents             # verify the ForwardedEvents log exists

# On sources: configure via GPO
# Computer Configuration → Administrative Templates → Windows Components → Event Forwarding
# → Configure target Subscription Manager = Server=http://<collector>:5985/wsman/SubscriptionManager/WEC
```

**Sysmon** — Microsoft Sysinternals; provides process creation (with hash), network connections, driver loads, registry changes, DNS queries, and more — far richer than the native audit log:

```powershell
# Install (download sysmon.exe from Microsoft Sysinternals)
sysmon.exe -accepteula -i sysmon-config.xml

# Update configuration without reinstalling
sysmon.exe -c sysmon-config.xml

# Check status
sysmon.exe -s

# Events land in: Applications and Services Logs → Microsoft → Windows → Sysmon → Operational
```

Use the SwiftOnSecurity or Olaf Hartong `sysmon-modular` config as a baseline; both are widely tested and freely available.

---

## Fix J — Application Control

**AppLocker (TM1, Windows 10/11 Enterprise or Server):**

AppLocker is per-user and enforced by a service; easier to configure than WDAC but weaker (can be bypassed by a local admin who can stop the service):

```powershell
# Generate default rules: Admins can run anything; Users restricted to Windows + Program Files
Get-AppLockerPolicy -Local -Xml | Out-File current-policy.xml

# Key rule: block execution from user-writable locations
# GPO: Computer Configuration → Windows Settings → Security Settings → Application Control Policies → AppLocker
# Create Executable Rules → Deny → path: %USERPROFILE%\* and %TEMP%\*

# Enable enforcement
Set-AppLockerPolicy -XmlPolicy policy.xml -Merge
Set-Service -Name AppIDSvc -StartupType Automatic
Start-Service -Name AppIDSvc
```

**Windows Defender Application Control (WDAC) — TM1/TM2 preferred:** kernel-enforced; a local admin cannot bypass it by stopping a service:

```powershell
# Generate a policy in Audit mode from a known-good reference machine
New-CIPolicy -Level Publisher -Fallback Hash -FilePath C:\BaselinePolicy.xml -UserPEs

# Allow Microsoft code + WHQL-signed drivers as a starting point
New-CIPolicy -Level Publisher -Fallback Hash -FilePath C:\AllowMicrosoft.xml `
  -MultiplePolicyFormat

# Merge policies
Merge-CIPolicy -PolicyPaths C:\BaselinePolicy.xml, C:\AllowMicrosoft.xml `
               -OutputFilePath C:\FinalPolicy.xml

# Audit mode: deploy and review 3006 events before enforcing
# Remove the option ID 3 (Audit Mode) from XML to switch to enforcement

# Convert to binary and deploy
ConvertFrom-CIPolicy -XmlFilePath C:\FinalPolicy.xml -BinaryFilePath C:\SIPolicy.p7b
Copy-Item C:\SIPolicy.p7b C:\Windows\System32\CodeIntegrity\SIPolicy.p7b
```

WDAC + Constrained Language Mode for PowerShell: when WDAC is active, PowerShell automatically runs in Constrained Language Mode for any script not allowed by the policy — no separate configuration needed.

---

## Fix K — Vulnerability Management

**Windows Update — ensure automatic security updates:**

```powershell
# Check update history
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20

# Force check for updates immediately
(New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()
```

**Microsoft Security Compliance Toolkit (MSCT)** — Microsoft's official hardening baselines for every Windows version, in GPO-importable format:

```
# Download: https://www.microsoft.com/en-us/download/details.aspx?id=55319
# Import the GPO backup for your version into Group Policy Management
# Compare local policy against the baseline using Policy Analyzer (included in MSCT)
```

**CIS Benchmarks** — independently maintained, widely used in compliance frameworks; available at cisecurity.org. Level 1 = recommended for most; Level 2 = defense-in-depth (high-friction, may break workflows).

**Vulnerability scanning with built-in tools:**

```powershell
# Check for missing updates
Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate -MicrosoftUpdate

# Verify no obvious misconfigurations
# Microsoft Baseline Security Analyzer has been retired; use MSCT Policy Analyzer or
# Invoke-PolicyAnalyzer (from the MSCT package) for GPO comparison
```

**Third-party patching** — Windows Update only patches Microsoft software; use a separate tool (WSUS + third-party catalogue, or a unified patch management solution) to patch Adobe, Java, Chrome, and other common exploit targets.

---

## Fix L — Advanced Controls (TM2+)

**Virtualization-Based Security (VBS)** — prerequisite for Credential Guard and HVCI; isolates a hypervisor-protected memory region even from kernel-mode code:

```powershell
# Check VBS status
Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus, SecurityServicesRunning, SecurityServicesConfigured
# VirtualizationBasedSecurityStatus 2 = running
# SecurityServicesRunning {1} = Credential Guard, {2} = HVCI
```

**Enable VBS + Credential Guard** — protects NTLM hashes and Kerberos tickets in an isolated VBS enclave; eliminates Pass-the-Hash and Pass-the-Ticket for accounts whose credentials are cached there:

```powershell
# Via registry (requires reboot; no UEFI lock — can be reversed)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v RequirePlatformSecurityFeatures /t REG_DWORD /d 1 /f  # Secure Boot
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LsaCfgFlags /t REG_DWORD /d 1 /f
# LsaCfgFlags: 0=disabled, 1=enabled (no UEFI lock), 2=enabled with UEFI lock (irrevocable without firmware)
```

Credential Guard requires: Windows 10/11 Enterprise or Server 2016+, UEFI Secure Boot, TPM 1.2+ (TPM 2.0 recommended), 64-bit CPU with virtualization extensions (VT-x/AMD-V), IOMMU (VT-d/AMD-Vi).

**HVCI (Hypervisor-Protected Code Integrity)** — the kernel itself cannot load unsigned drivers; eliminates a major driver-signing bypass attack class:

```powershell
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v Enabled /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v Locked /t REG_DWORD /d 0 /f
# Locked=1: UEFI lock — cannot be disabled without changing firmware; very strong but irreversible
```

Verify HVCI compatibility first — some older or unusual drivers are incompatible:

```powershell
# Driver compatibility check
dism /Online /Get-Drivers | Out-File drivers.txt
# Review for unsigned drivers; HVCI will block them
```

**Windows Defender Application Guard** — opens untrusted browser tabs and Office documents in a hardware-isolated Hyper-V container; the host is unaffected even if the container is fully compromised. Available on Windows 10/11 Enterprise:

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Windows-Defender-ApplicationGuard -NoRestart
```

**Just Enough Administration (JEA)** — restrict PowerShell remoting to specific cmdlets per role; a service desk operator gets only the commands they need, not a full shell:

```powershell
# Create a role capability file
New-PSRoleCapabilityFile -Path "C:\JEAConfig\Helpdesk.psrc" `
  -VisibleCmdlets "Get-Service", "Restart-Service" `
  -VisibleFunctions "Get-EventLog"

# Create a session configuration
New-PSSessionConfigurationFile -Path "C:\JEAConfig\Helpdesk.pssc" `
  -SessionType RestrictedRemoteServer `
  -RoleDefinitions @{ "DOMAIN\Helpdesk" = @{ RoleCapabilities = "Helpdesk" } }

Register-PSSessionConfiguration -Path "C:\JEAConfig\Helpdesk.pssc" -Name "Helpdesk" -Force
```

---

## Fix M — Measured Boot + Secure Boot Chain (TM3)

Windows Measured Boot records PCR measurements in the TPM at every boot step; a remote attestation service (Microsoft Attestation, or Azure Attestation for cloud) can verify the measurements before the machine is trusted with secrets.

```powershell
# Check boot integrity measurement log
Get-TpmSupportedFeature | Select-String Measured
Get-TpmMeasuredLog     # requires Windows 11 / Server 2022

# Verify Secure Boot is enforcing
Confirm-SecureBootUEFI

# UEFI Secure Boot + HVCI with Locked=1 (Fix L) is the Windows equivalent of dm-verity — 
# any modification to the measured boot chain requires physical firmware access to undo
```

**Early Launch Anti-Malware (ELAM)** — Windows Defender registers as an ELAM driver, which loads before any third-party drivers and can block unsigned or malicious drivers from loading at boot. Enabled by default when Defender is active; do not disable.

---

## OS Version Addenda

### Windows 11

- **TPM 2.0 and Secure Boot are hardware requirements** — VBS is enabled by default on new installs (not upgrades).
- **HVCI (Memory Integrity) is on by default** in Windows 11 22H2+ on compatible hardware; verify it stays on after driver installs.
- **Modern LAPS** is built in (22H2+); no separate MSI needed.
- **Smart App Control** (pre-WDAC for consumer; available until turned off and then irreversible) — enable it on new installs before any third-party software is installed.
- **Phishing protection** in Windows Security; enable "Warn me about malicious apps and sites."

### Windows 10

- VBS and HVCI are available but not on by default — enable explicitly (Fix L).
- LAPS requires the legacy MSI deployment.
- Windows Hello for Business and Smart App Control are not available (11 features).
- Apply the MSCT Windows 10 security baseline; confirm compatibility with your enterprise apps before deploying.

### Windows Server 2022

- **TLS 1.3 enabled by default** — the cleanest starting point for protocol hardening (Fix D).
- **SMB Direct compression** and **SMB over QUIC** are new; scope firewall rules accordingly.
- MSCT 2022 baseline is available; apply it before workload configuration.
- **Windows Admin Center** as management tool: prefer it over opening RDP broadly; it tunnels through HTTPS (443).

### Windows Server 2019

- TLS 1.0/1.1 still enabled by default; explicitly disable (Fix D).
- Windows Defender AV is included and enabled by default; do not uninstall it to install a third-party AV unless the replacement product is deployed first.
- MSCT Server 2019 Member Server and Domain Controller baselines available.

### Windows Server 2016

- Older defaults; requires more manual hardening on top of the MSCT baseline.
- SMBv1 may be installed; verify and remove.
- Credential Guard requires explicit enablement.
- Consider upgrading to 2022 rather than hardening a 2016 baseline for new deployments.

---

## Form Factor Addenda

### S1 — Internet-facing server

Fix A + D + E + F + G + H are the non-negotiable minimum; add I, J, K for TM1+.

- **No public RDP.** Admin via RD Gateway + MFA, or VPN + internal RDP. RDP on port 3389 directly exposed to the internet will be attacked within minutes.
- **IIS hardening** if running IIS: disable directory browsing, server version headers (`removeServerHeader` in `applicationHost.config`), unnecessary HTTP verbs (TRACE, PROPFIND), and WebDAV if unused.
- **ADFS / RD Gateway / WAP:** these are credential-handling roles exposed to the internet — apply Fix L (Credential Guard) and monitor authentication events (4624/4625/4648) aggressively.
- Egress filtering (Fix F — outbound default-deny) is essential: ransomware and C2 both require arbitrary outbound connectivity.

### S2 — Internal member server

- Host firewall (Fix F): restrict inbound to the management VLAN and the subnets that legitimately reach this server's specific service ports.
- **Service accounts:** use Group Managed Service Accounts (gMSA) instead of named user accounts with static passwords — the password rotates automatically and is never directly readable:
  ```powershell
  New-ADServiceAccount -Name <svc-gMSA> -DNSHostName <svc-gMSA>.<domain> `
    -PrincipalsAllowedToRetrieveManagedPassword "<server-hostname>$"
  Install-ADServiceAccount -Identity <svc-gMSA>
  ```
- **File servers:** enable VSS shadow copies for ransomware recovery; configure File Server Resource Manager (FSRM) file screening to block known ransomware extension patterns.

### S3 — Domain Controller

The most critical server in any Active Directory environment; a compromised DC means the entire domain is compromised.

- **Tier 0 isolation:** DCs must not be used for anything other than DC functions — no web browsing, no installing unapproved software, no workloads. If an admin needs to do non-DC work, they use a different machine.
- **Domain Admin accounts must only log on to DCs** — logging a domain admin onto a workstation caches its credential there; a compromised workstation then has domain admin.
- **Enable AD Recycle Bin:**
  ```powershell
  Enable-ADOptionalFeature "Recycle Bin Feature" -Scope ForestOrConfigurationSet `
    -Target <forest-FQDN>
  ```
- **Audit replication:** unexpected replication activity (especially DCSync) is an attack indicator.
  ```powershell
  Get-ADReplicationFailure -Target <dc-hostname> -Scope Server
  # Monitor Event ID 4662 with GUID for DCSync: 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2
  ```
- **No Print Spooler on DCs** (Fix D — this is mandatory for DCs, not optional).
- **RODCs (Read-Only DCs) for remote sites** — limits credential exposure at sites with weaker physical security.
- **Protected Users** for all tier-0 accounts; Authentication Policy Silos for strict logon restrictions.

### S4 — Azure VM / Cloud Instance

- Accept the platform in the TCB; do not design controls that depend on excluding Microsoft Azure from trust.
- **Azure Defender for Servers / Microsoft Defender for Cloud:** enable; it adds behavioral detection, just-in-time VM access, file integrity monitoring, and adaptive application controls.
- **Just-in-time (JIT) VM access:** RDP/SSH ports are closed by default; opened only on-demand for a specific IP and time window via Azure portal or API.
- **Azure AD / Entra ID join:** prefer Azure AD joined over domain joined for cloud-native workloads — simpler credential chain, no dependency on on-prem DC reachability.
- **Managed identities** instead of stored credentials for Azure service access; eliminates a class of credential theft.
- **Instance metadata endpoint** (169.254.169.254) — restrict access from unprivileged processes; contains the managed identity token.
  ```powershell
  New-NetFirewallRule -DisplayName "Block IMDS from non-SYSTEM" `
    -Direction Outbound -RemoteAddress 169.254.169.254 -Action Block
  # Then add an allow rule for the SYSTEM account / the agent that legitimately needs it
  ```

### S5 — Workstation (domain-joined)

- **Remove local admin rights from standard users** — this is the single most effective lateral movement prevention. Users who need occasional elevation use LAPS-managed local admin + UAC prompts. IT uses domain accounts with local admin rights deployed via GPO scoped to the machine type.
- **LAPS is mandatory** — shared local administrator passwords across a fleet mean a single workstation compromise yields lateral movement to every machine sharing that password.
- **AppLocker or WDAC (Fix J):** block execution from `%USERPROFILE%`, `%TEMP%`, and any network share that is not explicitly trusted. This blocks the majority of commodity malware drop-and-execute paths.
- **Office macro policy** (GPO: User Configuration → Administrative Templates → Microsoft Office → Security Settings):
  - Block all macros except those digitally signed by a trusted publisher.
  - Disable macros in documents from the internet (Protected View → do not allow macros to run).
- **Browser isolation:** enable Microsoft Defender Application Guard for Edge (Fix L) for browsing untrusted sites.
- **Screen lock:** enforce via GPO (Fix A); 15 minutes idle maximum; logon screen must not display last username.

### S6 — Laptop

Everything in S5, plus:

- **BitLocker with TPM + PIN is mandatory** (Fix C) — a lost or stolen laptop without FDE is a full data breach.
- **BitLocker recovery key escrow** to Azure AD (for Azure AD-joined) or AD (for domain-joined) before the device leaves the office.
- **Always-On VPN:** when off-site, all traffic routes through the corporate tunnel; split-tunnel with DNS-over-VPN at minimum.
- **Mobile Device Management (MDM/Intune):** enforce compliance policy (encryption status, patch level, Defender health); mark non-compliant devices as unable to access corporate resources via Conditional Access.
- **Remote wipe capability via Intune:** ensure it is configured and that someone knows how to trigger it before a device is reported lost.

### S7 — Privileged Access Workstation (PAW)

A PAW is a dedicated machine used exclusively for privileged administrative tasks. Its entire purpose is to break the credential exposure path.

- **Physical: dedicated hardware**, never a VM on a shared host; a compromised hypervisor could read the PAW's memory.
- **No internet browsing, no email, no productivity apps** — if an admin needs to do routine work, they use a separate standard workstation. Any task that exposes the PAW to untrusted content defeats its purpose.
- **BitLocker + TPM + PIN** (Fix C).
- **WDAC in enforcement mode** (Fix J) — application allowlisting; only approved admin tools can execute.
- **Credential Guard + HVCI** (Fix L) — enabled; no exceptions.
- **No local administrator accounts except LAPS-managed** — even the PAW's own admin account is rotated.
- **Outbound firewall:** permit only connectivity to domain controllers, management targets, and Windows Update. Block all other outbound.
- **Never log domain admin credentials on non-PAW machines** — doing so once makes the PAW's protections irrelevant for that session.
- See the Microsoft PAW guidance (Privileged Access / Enterprise Access Model) for the full tiered-access model.

### S8 — Standalone / workgroup machine

- No domain; local policy only (`secpol.msc` or `gpedit.msc` if available).
- Apply local password and lockout policy (Fix E — `net accounts`).
- Windows Defender AV and Firewall; no enterprise tools available but the same principles apply.
- BitLocker (Fix C) if the data warrants it; Microsoft account or USB key for recovery key escrow.
- Keep patched; standalone machines often fall behind without WSUS/Intune enforcement.

---

## Validation

```powershell
# SMBv1 must be false on both server and client components
Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol
Get-SmbClientConfiguration | Select-Object EnableSMB1Protocol

# NTLM level must be 5
(Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa").LmCompatibilityLevel

# WDigest must be 0 (disabled)
(Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest").UseLogonCredential

# LSA Protection (RunAsPPL) must be 1 or 2
(Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa").RunAsPPL

# Windows Firewall — all profiles enabled, inbound blocked
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction

# BitLocker — OS volume must be FullyEncrypted and ProtectionStatus On
Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, EncryptionMethod, ProtectionStatus

# Defender — real-time protection on, Tamper Protection on, signatures current
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, TamperProtectionSource, `
  AntispywareSignatureLastUpdated, AntivirusSignatureLastUpdated

# VBS / Credential Guard / HVCI (TM2+)
Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus, SecurityServicesRunning

# Local Administrators group — only expected members
Get-LocalGroupMember -Group Administrators

# Accounts with no password required
Get-LocalUser | Where-Object { $_.PasswordRequired -eq $false -and $_.Enabled -eq $true }

# Listening services — only expected ports
Get-NetTCPConnection -State Listen |
    Select-Object LocalAddress, LocalPort,
        @{n='Process';e={(Get-Process -Id $_.OwningProcess -EA SilentlyContinue).Name}} |
    Sort-Object LocalPort

# Print Spooler — must be disabled on DCs and non-print servers
Get-Service Spooler | Select-Object Status, StartType

# Audit policy — confirm key categories are enabled
auditpol /get /category:"Logon/Logoff","Account Logon","Account Management","Privilege Use","Detailed Tracking"
```

---

## Escalation / After-action

**Apply the MSCT security baseline** as an authoritative comparison point:

```powershell
# Download Policy Analyzer (included in MSCT) and compare your current GPO against the baseline
# For domain-joined: import the MSCT GPO backup into a test OU first; validate before fleet rollout
```

**Document this run** — record which sections were applied, which were consciously skipped, and the reasoning. The threat model and profile selected are context that is not derivable from the resulting configuration.

**Maintenance rhythm:**

| Frequency | Action |
|---|---|
| Daily | Confirm Defender signatures updated; WEF / Sysmon log forwarding active |
| Weekly | Review failed logon trends (Event 4625); check for new local admin accounts |
| Monthly | Verify Windows Update / WSUS compliance; audit privileged group membership |
| Quarterly | Re-run Policy Analyzer vs MSCT baseline; compare Lynis-equivalent score; review ASR block events |
| After OS / major update | Verify sysctl-equivalent settings survived (UAC, NTLM level, WDigest, RunAsPPL); re-run VBS/HVCI compatibility check |
| On role change | Re-evaluate which Fix sections apply — a file server becoming a DC is a completely different profile |

**If Credential Guard prevents something that was previously working:** this is the correct behavior — it stopped a credential exposure. Investigate what the application was doing with credentials; do not disable Credential Guard to make it work again.

**If an ASR rule blocks a legitimate application:** identify the Event ID 1121 entry (Microsoft-Windows-Windows Defender/Operational log); add an exclusion scoped to the specific executable path only, not a blanket rule audit.

---

## See also

- [[Unix OS Hardening]] — the parallel playbook for Linux, BSDs, and macOS
- Microsoft Security Compliance Toolkit — downloadable GPO baselines for every Windows version
- CIS Benchmarks for Windows (Level 1 / Level 2)
- Microsoft PAW / Enterprise Access Model documentation (privileged access architecture)
