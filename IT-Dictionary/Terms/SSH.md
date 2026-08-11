---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Secure Shell"]
tags: ["network", "protocol", "fundamental"]
status: "developed"
---

# SSH

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Secure Shell

Secure Shell — the standard protocol for encrypted remote login and command execution over an untrusted network (RFC 4251–4254, default port 22). One authenticated channel carries interactive shells, single commands, file transfer (SFTP/SCP), and forwarded TCP streams ([[SSH Tunneling]]).

**Context.** Its trust model is the opposite of the web's: no CAs — the server presents a *host key* that the client accepts on first contact and pins thereafter (trust on first use), which is why a changed-fingerprint warning deserves attention and why automation must pre-seed `known_hosts` or fail. Per-user `authorized_keys` files make key-based auth the norm and password auth the thing you disable first when [[Hardening]]; options on a key line (`restrict`, `command=`, `permitlisten=`) can cut an account down to a single narrow capability. Nearly all infrastructure tooling — git, rsync, Ansible, CI deploys — rides on it, which makes port 22 both the most useful and the most attacked service on any host.

## See also

- [[SSH Tunneling]]
- [[Bastion Host]]
- [[Key Exchange]]
- [[VPN]]
- [[Deploy Key]]
- [[Forced Command]]

## Often confused with

- [[TLS]] — both provide an encrypted, authenticated transport; TLS authenticates servers via CA-issued certificates, SSH via host keys trusted on first use.

## Further reading

- [Wikipedia: Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell)
- [RFC 4251: The Secure Shell (SSH) Protocol Architecture](https://www.rfc-editor.org/rfc/rfc4251)
