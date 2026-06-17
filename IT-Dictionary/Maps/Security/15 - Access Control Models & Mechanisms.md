---
type: "reference"
tags: [reference, security]
---

# Access Control Models & Mechanisms

> Every access-control design answers three questions: **who sets the policy** (the owner, or the system), **what the decision keys on** (identity, label, path, or token possession), and **what holds by default** (ambient authority, or deny). This map collects the models, then walks the Linux enforcement stack that implements them, gate by gate. Ghost (unlinked) terms are deliberate: each is a stub waiting to be written.

## The formal anchor

- [[Access Control Matrix]] — the subjects × objects grid everything else compresses. Store it by column and you get ACLs; by row, capability lists; derive cells from rules and you get policy-based MAC.

## The models

- [[Discretionary Access Control]] — the owner grants; ambient authority; root bypasses.
- [[Mandatory Access Control]] — the system mandates; owners can't override; binds root.
- [[RBAC]] — permissions to roles, roles to users.
- [[ABAC]] — decisions from attributes, evaluated per request.
- [[MLS]] — clearances and classifications; no read up, no write down.
- [[Capability-Based Security]] — possession of an unforgeable token *is* the access.
- [[Bell–LaPadula Model]] — the canonical MLS confidentiality policy. *(ghost)*
- [[Biba Model]] — its integrity mirror. *(ghost)*
- [[Reference Monitor]] — the ideal: every access mediated, tamper-proof, verifiable. *(ghost)*
- [[Confused Deputy Problem]] — the failure mode capabilities structurally avoid. *(ghost)*
- Existing anchors: [[Authorization]], [[Least Privilege]], [[Permissions]].

## The Linux enforcement stack

Order matters: classic DAC is checked first; the [[LSM]] hook fires only on pass — MAC can restrict, never grant.

- [[Permissions]] — mode bits and [[ACL]]s: the DAC gate.
- [[LSM]] — the kernel's hook framework every MAC module plugs into.
- [[SELinux]] — label-based MAC; [[Type Enforcement]] as the workhorse; default deny.
- [[AppArmor]] — path-based MAC; per-program profiles; the ergonomic alternative.
- [[Capabilities]] — root's power sliced into ~40 droppable privileges.
- [[seccomp]] — filter the syscall menu itself; not an LSM.
- [[Landlock]] — unprivileged self-sandboxing, the newest LSM of note. *(ghost)*
- Existing anchors: [[Kernel]], [[System Call]], [[Sandbox]], [[Hardening]], [[Container Security]].

## The Windows mirror

- [[Active Directory]] and [[Group Policy]] — where enterprise authorization actually lives.
- [[DACL and SACL]] — the NTFS security descriptor's allow-list and audit-list. *(ghost)*
- [[Mandatory Integrity Control]] — Windows' slim mandatory layer (low-IL browsers can't write up). *(ghost)*
- [[UAC]] — the consent gate between standard and elevated tokens. *(ghost)*

## Dive deeper — the backlog

Stubs worth writing next, grouped:

- **Models & theory:** [[Bell–LaPadula Model]], [[Biba Model]], [[Reference Monitor]], [[Trusted Computing Base]], [[Confused Deputy Problem]], [[Ambient Authority]], [[Common Criteria]]
- **SELinux internals:** [[Security Context]], [[Domain Transition]], [[AVC]], [[MCS]]
- **Linux neighbours:** [[Landlock]], [[Smack]], [[TOMOYO]], [[setuid]], [[chroot]], [[Namespace]], [[cgroups]]
- **Windows:** [[DACL and SACL]], [[Security Descriptor]], [[Mandatory Integrity Control]], [[UAC]]
- **Capability systems:** [[Capsicum]]

## See also

- [[04 - Identity and Access Management]]
- [[06 - Endpoint and Host Security]]
- [[03 - Operating Systems]]
- [[14 - Advanced Persistence & Below-OS Threats]] — the other side of the coin: what happens when enforcement layers are subverted from below.

---
← Back to [[_Home]]
