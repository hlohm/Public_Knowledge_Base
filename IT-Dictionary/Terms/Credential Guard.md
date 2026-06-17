---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Windows Defender Credential Guard"]
tags: [iam, modern]
status: "developed"
---

# Credential Guard

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Windows Defender Credential Guard

A Windows feature that uses [[VBS]] to move credential secrets — [[Kerberos]] ticket-granting tickets, NTLM hashes, cached domain credentials — out of the normal LSASS process into an isolated LSA process the rest of the OS can't read. It directly breaks the harvest step that [[Pass-the-Hash]] depends on.

**Context.** With Credential Guard on, dumping LSASS no longer yields reusable secrets, because they live in the VBS secure world (`LSAIso.exe`). Two important limits: it protects a *member* machine's cached secrets, **not** the [[Active Directory]] database on a domain controller — so [[DCSync]] against a DC is unaffected — and it doesn't help legacy protocols (NTLMv1, CredSSP) that still need the raw credential. Requires VBS + [[Secure Boot]].

## See also

- [[VBS]]
- [[Pass-the-Hash]]
- [[Kerberos]]
- [[Active Directory]]
- [[LSASS]]

## Often confused with

- [[HVCI]] — both ride on [[VBS]], but HVCI protects *kernel code integrity* while Credential Guard protects *credential secrets*.

## Further reading

- [Microsoft Learn: How Credential Guard works](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/how-it-works)
