---
type: "term"
branch: "Internet & Web"
aliases: ["send-only MTA", "satellite system", "smarthost client"]
tags: ["web", "net", "email", "os"]
status: "developed"
---

# Null Client

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** send-only MTA, satellite system

An [[MTA]] configured to *send only*: it listens on nothing, accepts no inbound mail, delivers nothing locally, and forwards everything it is given to a designated smarthost.

**Context.** This is the correct configuration for the overwhelming majority of servers, because nearly every Unix box wants to *emit* mail — cron output, `smartd` disk warnings, unattended-upgrade reports, backup failures — and none of them want to *receive* any. The recipe is small and worth memorising: `mydestination =` (empty), `inet_interfaces = loopback-only`, `relayhost = [smarthost]:587`, plus credentials in `smtp_sasl_password_maps`. Two things routinely go wrong. First, `inet_interfaces` changes need a full restart, not a reload, so a half-applied config leaves the box listening when you believe it isn't. Second, the mail is emitted as `root@somehost.localdomain`, which most real mail providers reject as an invalid sender — hence `smtp_generic_maps`, which rewrites outbound addresses into something externally valid. A null client that has been quietly failing for months is a classic estate finding: nothing alerts you that your alerting cannot alert.

## See also

- [[MTA]]
- [[MSA]]
- [[SMTP]]
- [[IP Reputation]]

## Often confused with

- [[Open Relay]] — a null client relays only *for itself*, outbound, to one fixed destination. An open relay accepts mail from strangers for strangers. Opposite ends of the trust spectrum.

## Further reading

- [Postfix standard configuration examples](https://www.postfix.org/STANDARD_CONFIGURATION_README.html)
