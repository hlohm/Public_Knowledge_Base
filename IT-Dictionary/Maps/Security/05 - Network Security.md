---
type: "domain"
tags: [domain]
---

# Network Security

> The terms here describe where controls sit and what they decide on. Notice the layering: from packet-level (firewall) to protocol-aware (IDS) to application-aware (WAF).

## Terms in this domain

- [[Air Gap]] — Physical isolation from other networks.
- [[Bastion Host]] — Hardened entry point used to reach internal systems.
- [[Backscatter]] — Bounce messages sent to an innocent third party, because a server accepted mail with a forged sender and only then found it undeliverable.
- [[CAA Record]] — A DNS record listing which CAs are permitted to issue certificates for a domain.
- [[CDS and CDNSKEY]] — Child-published records that signal the desired DS (CDS) or key (CDNSKEY) to the parent, so DS updates can be automated instead of hand-carried to the registrar.
- [[Cover Traffic]] — Fake traffic sent to mask the pattern of the real messages.
- [[DANE]] — Publishing a TLS certificate (or its CA, or public key) as a signed TLSA record in DNS, so a client can verify the server's cert against DNS instead of — or in addition to — the public CA system.
- [[DKIM]] — DomainKeys Identified Mail — cryptographic signature on outbound mail.
- [[DMARC]] — Ties SPF + DKIM to the visible From:, sets a fail policy, and reports.
- [[DMZ]] — DeMilitarized Zone.
- [[DNSKEY]] — The record publishing a zone's public signing key(s).
- [[DNSSEC]] — Extensions that add origin authentication and integrity to DNS by signing records, so a resolver can verify an answer genuinely came from the zone's owner and wasn't forged in transit.
- [[DNS Security]] — Protecting name resolution.
- [[DPI]] — Deep Packet Inspection.
- [[DS Record]] — A record in the _parent_ zone holding a hash of the child zone's signing key — the link that lets the parent vouch for the child in the DNSSEC chain.
- [[East-West vs North-South Traffic]] — North-south = client ↔ data center (external); east-west = server ↔ server (internal).
- [[Entry Guard]] — The persistent, IP-seeing first hop of a Tor circuit.
- [[Envelope Sender]] — The address given in the SMTP `MAIL FROM` command — the transport-level sender, where bounces go — as opposed to the `From:` header the recipient actually sees.
- [[Firewall]] — Filters traffic based on rules.
- [[Greylisting]] — Temporarily rejecting a first delivery attempt from an unknown sender triple, on the bet that only a real MTA will retry.
- [[Honeypot]] — Decoy system designed to attract attackers, gather intel, and waste their time.
- [[IDS and IPS]] — Intrusion Detection / Prevention System.
- [[IP Reputation]] — The score mail providers attach to an IP from its history — poor reputation gets mail junked regardless of correct SPF/DKIM/DMARC.
- [[Microsegmentation]] — Segmentation at workload or process level, often in cloud or SDN environments.
- [[Mixnet]] — Anonymity network that batches, reorders, and delays messages to defeat traffic analysis.
- [[MTA-STS]] — A policy that lets a domain require inbound SMTP be delivered over authenticated TLS, published over HTTPS and discovered via a DNS TXT record — the non-DNSSEC alternative to DANE.
- [[NAC]] — Network Access Control.
- [[Network Segmentation]] — Splitting networks into zones so a breach in one doesn't spread.
- [[NGFW]] — Next-Generation Firewall.
- [[NSEC]] — The DNSSEC mechanism for _signing a negative answer_ — proving that a name (or record type) genuinely does not exist, since you can't sign a record that isn't there.
- [[Onion Routing]] — Nested per-hop encryption so no single relay knows both ends.
- [[Pluggable Transport]] — Reshapes Tor traffic to evade DPI (obfs4, Snowflake, meek).
- [[Proxy]] — Intermediary between client and server.
- [[RRSIG]] — The signature record covering a set of DNS records of one type/name — the actual cryptographic proof a validating resolver checks against the zone's DNSKEY.
- [[SDN]] — Software-Defined Networking.
- [[Open Relay]] — An SMTP server that will carry mail from strangers to strangers; a misconfiguration that gets your IP blocklisted within a day.
- [[SPF]] — Sender Policy Framework — DNS list of authorized sending IPs.
- [[Sphinx Packet Format]] — Fixed-size onion packet format for mix networks; unlinkable, replay-resistant, supports anonymous replies.
- [[SRS]] — A scheme for rewriting the envelope sender when _forwarding_ mail, so the forwarded message still passes SPF at the final destination.
- [[SSH]] — Secure Shell: encrypted remote login, command execution, and transport for file transfer and tunneling.
- [[SSH Tunneling]] — Forwarding arbitrary TCP connections through an authenticated SSH session (local, remote/reverse, dynamic).
- [[SURB]] — Single-Use Reply Block: a sealed return path for replying to an anonymous sender.
- [[TLS Inspection]] — Terminating TLS at a gateway to inspect content, then re-encrypting.
- [[Tor]] — Volunteer anonymity network; layered encryption across three relays.
- [[Tor Bridge]] — Unlisted Tor entry, for reaching Tor where it's blocked.
- [[VLAN]] — Virtual Local Area Network.
- [[VPN]] — Virtual Private Network.
- [[WAF]] — Web Application Firewall.
- [[WireGuard]] — Small, modern, kernel-level VPN tunnel protocol keyed by public keys.

---
← Back to [[_Home]]