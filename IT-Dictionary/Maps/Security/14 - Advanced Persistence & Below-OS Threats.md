---
type: "reference"
tags: [reference, security]
---

# Advanced Persistence & Below-OS Threats

> The deeper an implant sits, the earlier it runs and the less of the system is left above it to notice. This map walks the execution stack from user mode down to the hardware root of trust, then the identity-layer equivalents. Most of these are not ways *in* — they assume an existing privileged foothold and are about staying in, invisibly. Ghost (unlinked) terms are deliberate: each is a stub waiting to be written.

## The unifying idea

Whoever controls a lower layer controls everything above it, because each layer trusts the one that loaded it. "Advanced" persistence comes in three shapes: run **earlier** than the defences (boot and firmware), run **beneath** them (hypervisor), or forge **trust** inside a running system (identity). See [[Persistence]], [[Attack Surface]], [[Chain of Trust]], [[Defense in Depth]].

## Layer 1 — Pre-boot: bootkits & firmware

The earliest code wins. Disk-level implants survive an OS reinstall; firmware-level implants survive disk replacement.

- [[Bootkit]] — malware that runs before the OS loads (ATT&CK T1542.003).
- [[UEFI]] — the modern firmware interface; a small OS in its own right.
- [[EFI System Partition]] — the FAT partition holding signed boot loaders (the new MBR). *(ghost)*
- [[Boot Loader]] — the stage UEFI hands off to. *(ghost)*
- [[MBR]] — legacy Master Boot Record, home of first-generation bootkits. *(ghost)*
- [[SPI Flash]] — the chip the firmware lives on; deepest persistence. *(ghost)*
- [[Option ROM]] — firmware on peripherals (NIC, GPU), another implant home. *(ghost)*
- Existing anchors: [[Firmware]], [[Rootkit]].

## Layer 2 — Kernel & hypervisor

- [[Protection Ring]] — Ring 0 / Ring 3, and the security extension to "Ring -1/-2/-3".
- [[DKOM]] — hiding by editing live kernel data structures.
- [[BYOVD]] — riding a signed-but-vulnerable driver into the kernel.
- [[Driver Signature Enforcement]] — the control BYOVD sidesteps. *(ghost)*
- [[SMM]] — System Management Mode, firmware's invisible "Ring -2". *(ghost)*
- [[Intel ME]] — the management engine, conceptual "Ring -3". *(ghost)*
- [[Blue Pill]] — the classic hypervisor-rootkit idea: demote the live OS to a guest. *(ghost)*
- Existing anchors: [[Kernel]], [[Hypervisor]].

## Layer 3 — The defensive inversion (the defender owns Ring -1)

Modern Windows puts the hypervisor to *defensive* use, occupying the below-OS slot before an attacker can.

- [[VBS]] — an isolated secure world hosted by the hypervisor.
- [[HVCI]] — kernel code-integrity enforced from inside that secure world.
- [[Credential Guard]] — credential secrets isolated out of reach of [[Pass-the-Hash]].
- [[Secure Boot]] — verify each boot stage's signature.
- [[Measured Boot]] — record what ran so tampering is detectable.
- [[TPM]] — the hardware root of trust holding the measurements.
- [[Remote Attestation]] — prove boot integrity to a server. *(ghost)*
- [[Boot Guard]] — Intel's hardware-verified firmware boot. *(ghost)*
- Existing anchor: [[Chain of Trust]].

## Layer 4 — Identity & cloud persistence

The logical-trust branch: forge credentials and tokens inside systems that are working exactly as designed.

- [[Golden Ticket]] — forge any Kerberos TGT from the `krbtgt` key.
- [[Silver Ticket]] — forge one service ticket from a service account's key. *(ghost)*
- [[DCSync]] — ask a DC to replicate password hashes to you.
- [[Skeleton Key]] — patch a DC's LSASS to accept a master password. *(ghost)*
- [[Golden SAML]] — forge SAML assertions from a stolen IdP signing key.
- Existing anchors: [[Active Directory]], [[Kerberos]], [[Pass-the-Hash]], [[SAML]], [[Federation]], [[IdP and SP]].

## Layer 5 — Fileless / OS-feature persistence

Hiding inside legitimate OS machinery, often with nothing on disk.

- [[WMI Event Subscription]] — fire a payload on a system event, no file. *(ghost)*
- [[COM Hijacking]] — redirect a COM object reference to attacker code. *(ghost)*
- [[Fileless Malware]] — the umbrella for memory-only techniques. *(ghost)*
- Existing anchor: [[LotL]].

## Detection & hunting

The honest threat model: these are the *endgame* of an intrusion, not the entry. Prevent the [[Privilege Escalation]] that enables them, then catch the rare implant.

- [[Measured Boot]] + [[Remote Attestation]] — catch pre-boot tampering.
- [[CHIPSEC]] — open-source firmware / SPI integrity inspection. *(ghost)*
- [[Sysmon]] — driver loads, WMI events, process creation. *(ghost)*
- Existing anchors: [[EDR]], [[Threat Hunting]], [[Detection Engineering]].

## Dive deeper — the backlog

Stubs worth writing next, grouped:

- **Boot / firmware:** [[BIOS]], [[EFI System Partition]], [[Boot Loader]], [[MBR]], [[SPI Flash]], [[Option ROM]], [[Boot Guard]], [[Remote Attestation]], [[DMA Attack]]
- **Kernel / hypervisor:** [[Driver]], [[Code Signing]], [[Driver Signature Enforcement]], [[PatchGuard]], [[SMM]], [[Intel ME]], [[Blue Pill]], [[Hyper-V]], [[Secure Kernel]], [[User Space]]
- **Identity:** [[Silver Ticket]], [[Skeleton Key]], [[DSRM]], [[AD FS]], [[LSASS]]
- **Fileless:** [[WMI Event Subscription]], [[COM Hijacking]], [[Fileless Malware]]
- **Tooling:** [[CHIPSEC]], [[Sysmon]]

## See also

- [[07 - Threats and Attacks]]
- [[06 - Endpoint and Host Security]]
- [[04 - Identity and Access Management]]
- [[02 - Hardware & Architecture]]

---
← Back to [[_Home]]
