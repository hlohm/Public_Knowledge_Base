---
type: cheatsheet
area: "Networking & Protocols"
aliases: [dig, host, nslookup]
tags: [dns, networking, troubleshooting, dig]
status: working
---

# DNS

> **Area:** [[Networking & Protocols]]

DNS query and troubleshooting — `dig`, `host`, `nslookup`, and the practical record types you actually use. Concept definitions live in the IT-Dictionary; this is the operational side.

---

## 1. dig basics

`dig` is the go-to tool. It sends a DNS query and shows the full response, including the authority section and additional records.

```bash
dig example.com             # A record (default); uses system resolver
dig example.com A           # explicit type
dig example.com AAAA        # IPv6 address
dig example.com MX          # mail exchange records
dig example.com NS          # authoritative nameservers
dig example.com TXT         # SPF, DKIM, DMARC, and other text records
dig example.com SOA         # start of authority (serial, refresh, retry, expire, TTL)
dig example.com CNAME       # canonical name (alias)
dig example.com SRV         # service locator (_http._tcp.example.com)
dig -x 192.0.2.1            # reverse lookup (PTR record)
```

**Query a specific nameserver instead of the system resolver:**
```bash
dig @8.8.8.8 example.com            # query Google's public resolver
dig @1.1.1.1 example.com            # query Cloudflare's resolver
dig @ns1.example.com example.com    # query the authoritative nameserver directly
```

**Short output (just the answer):**
```bash
dig +short example.com              # just the IP(s)
dig +short example.com MX           # just the MX records
dig +short -x 192.0.2.1            # just the PTR result
```

## 2. Tracing and delegation

```bash
# Trace the full delegation chain from root to authoritative
dig +trace example.com

# Show which nameserver is authoritative
dig example.com NS +short

# Find who is authoritative for a subdomain
dig sub.example.com NS

# Check if the NS records in the parent zone match the authoritative server's SOA
dig example.com NS @a.gtld-servers.net   # NS as seen by the TLD (parent view)
dig example.com NS @ns1.example.com      # NS as seen by the auth server itself
```

## 3. DNSSEC validation

```bash
# +dnssec asks the resolver to return DNSSEC records and set the AD flag if validated
dig +dnssec example.com

# AD (Authenticated Data) flag in the header means the resolver validated the chain
# Check: ;; flags: qr rd ra ad;

# DNSKEY: the zone's public signing key
dig example.com DNSKEY

# DS: the Delegation Signer record (published at the parent, links to the child DNSKEY)
dig example.com DS
dig example.com DS @a.gtld-servers.net   # confirm DS is published at the TLD

# RRSIG: the signature covering each RRset
dig example.com A +dnssec    # RRSIG should appear alongside the A record
```

## 4. host command (quick lookups)

```bash
host example.com             # A and MX, concise
host -t MX example.com
host -t NS example.com
host 192.0.2.1               # reverse lookup
host example.com 8.8.8.8     # use specific resolver
```

## 5. Common record types

| Type | Purpose |
|---|---|
| A | IPv4 address |
| AAAA | IPv6 address |
| CNAME | Alias to another name |
| MX | Mail exchange (+ priority) |
| NS | Authoritative nameservers for the zone |
| PTR | Reverse lookup (IP → name) |
| SOA | Zone metadata: serial, refresh, retry, expire, minimum TTL |
| TXT | Free-text; used for SPF, DKIM, DMARC, site verification |
| SRV | Service discovery (`_service._proto.name TTL class SRV priority weight port target`) |
| CAA | Certificate Authority Authorization — which CAs may issue certs for the domain |
| DS | Delegation Signer — links parent to child DNSSEC chain |
| DNSKEY | Zone signing key (ZSK) and key signing key (KSK) |
| TLSA | DANE — associate a TLS certificate with a DNS name |

## 6. Troubleshooting patterns

```bash
# "Why can't I resolve X?"
dig example.com                             # does the system resolver return an answer?
dig @8.8.8.8 example.com                   # does a public resolver?
dig @ns1.example.com example.com           # does the authoritative server?
# If auth works but system resolver doesn't: caching issue or local DNS misconfiguration

# "Is the record correct?"
dig example.com A +short                   # what's the current answer?
dig example.com A +short @ns1.example.com  # what does auth say?
# Difference = stale cache; check TTL from auth, wait for expiry

# "Why is my email failing?"
dig example.com MX +short       # are MX records present?
dig example.com TXT +short      # is SPF present? (should start with v=spf1)
dig _dmarc.example.com TXT      # is DMARC published?
dig mail._domainkey.example.com TXT  # DKIM selector 'mail'

# "Is DNSSEC broken?"
dig example.com +dnssec | grep -E 'SERVFAIL|ad|RRSIG|DNSKEY'
# SERVFAIL with DNSSEC = signature validation failure; check TTLs and SOA serial

# Check TTL remaining on a cached record
dig example.com A | grep -A2 'ANSWER'
```

---

## Daily workflows

### "Find out what IP a domain resolves to right now"
```bash
dig +short example.com
```

### "Verify SPF / DMARC are published correctly"
```bash
dig +short TXT example.com | grep spf
dig +short TXT _dmarc.example.com
```

### "Trace why a new DNS record isn't resolving yet"
```bash
dig example.com A @ns1.example.com +short   # authoritative has it?
dig example.com A @8.8.8.8 +short           # public resolver has it?
dig example.com A +short                    # local resolver has it?
```

### "Confirm DNSSEC DS is published at the parent"
```bash
dig DS example.com @a.gtld-servers.net
```

## Gotchas / Golden rules

1. **`dig` without `@server` queries the system resolver, which may return cached data** — always query `@ns1.example.com` directly when verifying that a change has propagated to authoritative.
2. **TTL in the ANSWER section is the remaining cache time, not the original TTL** — dig at the authoritative server to see the record's original TTL.
3. **CNAME cannot coexist with other records at the zone apex** — `CNAME example.com` is illegal; use A/AAAA directly or an ALIAS/ANAME record if your DNS provider supports it.
4. **`+trace` bypasses the system resolver entirely** — it starts from a root hint and recurses itself, so it reflects what the real DNS tree contains regardless of local caching or resolver configuration.
5. **A missing PTR record will not break forward resolution** — but many mail servers check that the PTR of the sending IP matches the A record of the sending hostname (FCrDNS); missing or mismatched PTR causes mail delivery failures.
