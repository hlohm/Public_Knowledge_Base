---
type: cheatsheet
area: "Networking & Protocols"
aliases: [dig, host, nslookup, resource record]
tags: [dns, networking, troubleshooting, dig]
status: working
---

# DNS

> **Area:** [[Networking & Protocols]]

DNS query and troubleshooting — how a lookup resolves, what a resource record is made of,
what each record type carries, and the `dig` / `host` / `nslookup` commands to inspect all of
it. Concept definitions live in the IT-Dictionary; this is the operational side. Zone-file
authoring for a specific server (BIND, Knot, PowerDNS) is out of scope.

---

## 1. Mental model — how a lookup resolves

A **stub resolver** on your machine asks one question and wants a final answer. A **recursive
resolver** does the legwork: it walks the tree from the root downwards, asking the same
question at each level and following **referrals** until something answers **authoritatively**.

```
 ┌─ your machine ──────────────────────────────────────────────────────────┐
 │  application ──getaddrinfo()──► stub resolver   (/etc/resolv.conf)      │
 └────────────────────────────────────────┬────────────────────────────────┘
                                          │ ① QUERY  www.example.com A
                                          │   flags: rd  ("recursion desired")
                                          ▼
 ┌─ recursive resolver (ISP · 1.1.1.1 · your own Unbound) ─────────────────┐
 │  in cache and not expired?  ──yes──►  answer immediately, no packets    │
 │           │ no                        leave the resolver                │
 └───────────┼─────────────────────────────────────────────────────────────┘
             │
             │ ② "www.example.com A?"              ┌─────────────────────────┐
             ├────────────────────────────────────►│  root zone  ( . )       │
             │◄─ referral: NS a.gtld-servers.net   │  13 identities,         │
             │   + glue A/AAAA in ADDITIONAL       │  anycast worldwide      │
             │                                     └─────────────────────────┘
             │ ③ same question, asked again        ┌─────────────────────────┐
             ├────────────────────────────────────►│  .com TLD servers       │
             │◄─ referral: NS ns1.example.com      │                         │
             │   + glue A 192.0.2.53               └─────────────────────────┘
             │ ④ same question, third time         ┌─────────────────────────┐
             ├────────────────────────────────────►│  ns1.example.com        │
             │◄─ ANSWER  www.example.com.          │  — authoritative for    │
             │   300 IN A 192.0.2.10  (flags: aa)  │    the example.com zone │
             │                                     └─────────────────────────┘
             ▼
   ⑤ resolver caches the RRset for its TTL (300 s), then answers the stub
   ⑥ stub hands 192.0.2.10 to the application
```

**What each hop actually returns.** Only step ④ is an *answer*; ② and ③ are **referrals** —
an empty ANSWER section, the next level's `NS` records in AUTHORITY, and their addresses as
**glue** in ADDITIONAL. Glue exists to break the circularity of `ns1.example.com` being the
nameserver *for* `example.com`: the parent must hand out the address, because you cannot look
it up without already being able to.

**Response sections** (what `dig` prints):

| Section | Contains |
| --- | --- |
| `QUESTION` | the query echoed back — name, class, type |
| `ANSWER` | the records that answer it (empty in a referral) |
| `AUTHORITY` | the `NS` records for the zone that owns the answer, or `SOA` on a negative reply |
| `ADDITIONAL` | records the server volunteers — glue addresses, `SRV`/`MX` targets, OPT pseudo-record |

**Header flags worth reading:**

| Flag | Meaning |
| --- | --- |
| `qr` | this is a response, not a query |
| `rd` | recursion desired — the client asked for the full walk |
| `ra` | recursion available — the server is willing to do it |
| `aa` | **authoritative answer** — came from a server that holds the zone, not a cache |
| `ad` | authenticated data — the resolver validated DNSSEC for this answer |
| `cd` | checking disabled — client asked to skip DNSSEC validation |

**Response codes:**

| RCODE | Meaning | Usual cause |
| --- | --- | --- |
| `NOERROR` | success | — |
| `NOERROR` + 0 answers | **NODATA** — name exists, but not with this type | asking `AAAA` of an IPv4-only host |
| `NXDOMAIN` | the name does not exist at all | typo, or record never created |
| `SERVFAIL` | resolver could not complete | broken delegation, DNSSEC validation failure, all auth servers unreachable |
| `REFUSED` | server declines to answer | querying a recursive resolver that doesn't serve you, or an auth server for a zone it doesn't host |

**Caching happens in more places than you think** — each layer can serve you stale data:
the application (browsers keep their own short cache), the OS stub (`systemd-resolved`,
`nscd`), the recursive resolver, and any forwarder in between. Negative answers are cached
too, governed by the SOA `minimum` field — which is why a typo'd record can appear "stuck"
even after you fix it.

## 2. Anatomy of a record

Every resource record (RR) has the same five parts, in this order:

```
 www.example.com.        300      IN      A        192.0.2.10
 └──── NAME ─────┘   └─ TTL ─┘  └CLASS┘ └TYPE┘  └──── RDATA ────┘
```

| Field | What it is |
| --- | --- |
| **NAME** | the owner name the record is attached to. A trailing dot makes it a fully-qualified name; without one, the zone's `$ORIGIN` is appended. `@` means the zone apex itself. |
| **TTL** | how many **seconds** a resolver may cache this record. Omitted in a zone file, the `$TTL` directive supplies it. |
| **CLASS** | effectively always `IN` (Internet). `CH` (Chaos) survives only for oddities like `dig @ns CH TXT version.bind`; `HS` (Hesiod) is historical. |
| **TYPE** | `A`, `MX`, `TXT`, … — determines how RDATA is parsed. |
| **RDATA** | the payload. Its shape is entirely type-specific — an IP for `A`, a priority plus a hostname for `MX`, seven numbers and two names for `SOA`. |

**RRsets are the real unit.** All records sharing the same NAME + CLASS + TYPE form one
**RRset**, and DNS moves them as a block — you never get "one of the three A records". Two
consequences: every record in an RRset **must carry the same TTL**, and DNSSEC signs the
RRset as a whole (one `RRSIG` covers all of them).

**Names, origin, and the trailing dot** — the single most common zone-file bug:

```dns
$ORIGIN example.com.
$TTL 3600

@       IN  A      192.0.2.10      ; example.com.        itself
www     IN  A      192.0.2.10      ; www.example.com.    — relative, $ORIGIN appended
www.    IN  A      192.0.2.10      ; www.  ← at the ROOT. almost certainly a typo
mail    IN  CNAME  ghs.google.com. ; trailing dot: absolute, left alone
mail    IN  CNAME  ghs.google.com  ; NO dot: becomes ghs.google.com.example.com.
```

**TTL is a budget, not a promise.** The TTL you publish is the *maximum* a well-behaved
resolver caches; the value `dig` shows you from a recursive resolver is the **remaining**
time, counting down. Query the authoritative server to see the configured value:

```bash
dig +noall +answer example.com A                    # remaining TTL (cached, counts down)
dig +noall +answer example.com A @ns1.example.com   # the real, configured TTL
```

Before a planned change, drop the TTL well in advance (to e.g. 300), let the old long TTL
expire, make the change, then raise it again. Lowering the TTL *at* change time does nothing
for records already cached under the old value.

## 3. Record types in detail

Quick lookup first, detail below:

| Type | Purpose | RDATA shape |
| --- | --- | --- |
| `A` | IPv4 address | one IPv4 address |
| `AAAA` | IPv6 address | one IPv6 address |
| `CNAME` | alias to another name | one target name |
| `DNAME` | alias for an entire subtree | one target name |
| `MX` | mail exchange | preference + hostname |
| `NS` | authoritative nameservers | one hostname |
| `PTR` | reverse lookup (IP → name) | one hostname |
| `SOA` | zone metadata | 2 names + 5 numbers |
| `TXT` | free text — SPF, DKIM, DMARC, verification | one or more strings ≤255 bytes |
| `SRV` | service location | priority + weight + port + target |
| `CAA` | which CAs may issue certs | flags + tag + value |
| `TLSA` | DANE — pin a cert to a name | usage + selector + type + data |
| `HTTPS` / `SVCB` | endpoint parameters (ALPN, hints, ECH) | priority + target + params |
| `DS` | delegation signer — parent → child DNSSEC link | keytag + alg + digest type + digest |
| `DNSKEY` | zone's public signing key | flags + protocol + alg + key |
| `RRSIG` | signature over one RRset | 9 fields incl. validity window |
| `NSEC` / `NSEC3` | authenticated denial of existence | next name + type bitmap |
| `CDS` / `CDNSKEY` | child-published, to automate the parent's DS | as `DS` / `DNSKEY` |

### Addressing

```dns
www     IN  A      192.0.2.10          ; IPv4. multiple A records = one RRset, client picks
www     IN  AAAA   2001:db8::10        ; IPv6. independent of the A record
shop    IN  CNAME  www.example.com.    ; alias — resolvers chase it, then resolve the target
old     IN  DNAME  new.example.com.    ; redirects the whole subtree: a.old → a.new
```

**`CNAME` has hard rules**, and violating them breaks things in confusing ways:

- A name with a `CNAME` may hold **no other record type** (DNSSEC records excepted). No
  `CNAME` + `MX`, no `CNAME` + `TXT`.
- It therefore **cannot exist at the zone apex** — the apex must carry `SOA` and `NS`. Use
  `A`/`AAAA`, or a provider-specific `ALIAS`/`ANAME` pseudo-record that flattens to addresses
  at query time.
- `MX`, `NS`, and `SRV` targets **must not point at a `CNAME`**. Legal in a zone file, but
  it's a protocol violation and some mail servers will refuse it.

**`PTR` lives in its own reverse tree**, not next to the forward record — this is why reverse
DNS is usually delegated by whoever owns the address block, not by you:

```dns
; 192.0.2.10  →  reverse the octets, append in-addr.arpa
10.2.0.192.in-addr.arpa.        IN  PTR  www.example.com.

; 2001:db8::10  →  reverse the nibbles, append ip6.arpa
0.1.0.0.0.0.…0.0.8.b.d.0.1.0.0.2.ip6.arpa.  IN  PTR  www.example.com.
```

### Zone infrastructure

```dns
@   IN  SOA  ns1.example.com. hostmaster.example.com. (
             2026081601   ; serial  — bump on EVERY change, or secondaries won't transfer
             7200         ; refresh — secondary re-checks the serial this often
             3600         ; retry   — wait this long after a failed refresh
             1209600      ; expire  — secondary stops answering after this long out of contact
             300 )        ; minimum — NEGATIVE caching TTL, not a default TTL

@   IN  NS   ns1.example.com.        ; must be present at the apex AND at the parent
@   IN  NS   ns2.example.com.
```

Two `SOA` traps: the **RNAME** is an email address with the `@` replaced by a dot
(`hostmaster.example.com.` means `hostmaster@example.com`), and **`minimum` has not meant
"default TTL" since RFC 2308** — it is the TTL for negative answers (`NXDOMAIN`/NODATA).
Set it too high and a typo you already fixed keeps returning "does not exist".

`NS` records exist in **two places** and are not required to agree — the parent's copy drives
the delegation, the child's copy is the authoritative one. When they disagree you get
intermittent, resolver-dependent failures. Compare them explicitly:

```bash
dig example.com NS @a.gtld-servers.net +norec   # parent's view (the delegation)
dig example.com NS @ns1.example.com             # child's view (authoritative)
```

### Mail

```dns
@       IN  MX   10 mx1.example.com.       ; lower preference number wins
@       IN  MX   20 mx2.example.com.       ; used when mx1 is unreachable
@       IN  MX   0  .                      ; "null MX" (RFC 7505): accepts no mail at all

@       IN  TXT  "v=spf1 mx -all"          ; SPF — which hosts may send as this domain
_dmarc  IN  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
mail._domainkey IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBg…"   ; DKIM, selector "mail"
```

**`TXT` strings are capped at 255 bytes each.** A longer value (any real DKIM key) is stored
as several quoted strings that consumers concatenate — this is a wire-format detail, not
something you choose, and it's why a DKIM record looks like `"…" "…"` in `dig` output.
`dig +short TXT` prints the quoting; strip it before comparing.

### Services and TLS

```dns
; _service._proto.name    prio weight port target
_sip._tcp    IN  SRV  10  60  5060  sipserver.example.com.
_sip._tcp    IN  SRV  10  40  5060  sipbackup.example.com.
_sip._tcp    IN  SRV  20   0  5060  sipfallback.example.com.
_imap._tcp   IN  SRV   0   0     .    ; target "." = service explicitly NOT offered
```

`SRV` clients try the **lowest priority** first, and distribute across equal-priority targets
in proportion to **weight** (here 60/40). Weight only ever compares within one priority level.

```dns
@            IN  CAA  0 issue "letsencrypt.org"       ; only this CA may issue
@            IN  CAA  0 issuewild ";"                 ; nobody may issue wildcards
@            IN  CAA  0 iodef "mailto:security@example.com"   ; report violations here

; DANE: usage 3 (DANE-EE) · selector 1 (SubjectPublicKeyInfo) · matching 1 (SHA-256)
_443._tcp.www  IN  TLSA  3 1 1 abc123…deadbeef

; SVCB/HTTPS (RFC 9460) — advertise HTTP/3, address hints, Encrypted ClientHello
@            IN  HTTPS  1 . alpn="h3,h2" ipv4hint=192.0.2.10 ipv6hint=2001:db8::10
```

A `CAA` flags byte of `128` marks the property **critical**: a CA that doesn't understand the
tag must refuse to issue rather than ignore it. Absent any `CAA` record, *every* CA is
permitted — the record only ever narrows.

### DNSSEC

```dns
@  IN  DNSKEY  257 3 13 <pubkey>   ; flags 257 = KSK (signs DNSKEYs); 256 = ZSK (signs data)
                                    ; protocol is always 3; 13 = ECDSAP256SHA256
; published at the PARENT, not here — this is what links the chain:
example.com.  IN  DS  12345 13 2 <sha256-digest-of-the-KSK>
                        │    │  └─ digest type 2 = SHA-256
                        │    └──── algorithm, must match the DNSKEY
                        └───────── key tag, identifies which key
```

`RRSIG` carries the type it covers, the algorithm, the original TTL, an **inception and
expiration timestamp**, the key tag, the signer's name, and the signature. The validity
window is the operational hazard: signatures expire on a schedule regardless of whether
anything changed, so a stalled re-signing job takes the zone down with `SERVFAIL` days later.

`NSEC`/`NSEC3` prove that a name *doesn't* exist without letting an attacker forge a denial.
`NSEC3` additionally hashes the names so the zone can't be trivially enumerated.

`CDS`/`CDNSKEY` are published **in the child zone** to tell the parent "here is my new DS,
please update" — the basis of automated key rollover (RFC 7344/8078) instead of a registrar
web form.

## 4. dig basics

`dig` is the go-to tool. It sends a DNS query and shows the full response, including the
authority section and additional records.

```bash
dig example.com             # A record (default); uses system resolver
dig example.com A           # explicit type
dig example.com AAAA        # IPv6 address
dig example.com MX          # mail exchange records
dig example.com NS          # authoritative nameservers
dig example.com TXT         # SPF, DKIM, DMARC, and other text records
dig example.com SOA         # start of authority (serial, refresh, retry, expire, negative TTL)
dig example.com CNAME       # canonical name (alias)
dig example.com SRV         # service locator (_http._tcp.example.com)
dig example.com CAA         # which CAs may issue
dig example.com HTTPS       # SVCB/HTTPS parameters (ALPN, hints, ECH)
dig example.com ANY         # mostly refused these days (RFC 8482) — don't rely on it
dig -x 192.0.2.1            # reverse lookup (PTR record)
```

**Query a specific nameserver instead of the system resolver:**
```bash
dig @8.8.8.8 example.com            # query Google's public resolver
dig @1.1.1.1 example.com            # query Cloudflare's resolver
dig @ns1.example.com example.com    # query the authoritative nameserver directly
```

**Control the output — these three cut the noise the most:**
```bash
dig +short example.com              # just the answer values
dig +short example.com MX           # just the MX records
dig +noall +answer example.com      # the ANSWER section with full record syntax + TTL
dig +norec example.com @ns1…        # don't ask for recursion — see the raw referral
```

## 5. Tracing and delegation

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

## 6. DNSSEC validation

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

# Is a SERVFAIL actually a validation failure? Ask again with checking disabled:
dig example.com +cd          # if this succeeds where the plain query failed, DNSSEC is broken
```

## 7. host command (quick lookups)

```bash
host example.com             # A and MX, concise
host -t MX example.com
host -t NS example.com
host 192.0.2.1               # reverse lookup
host example.com 8.8.8.8     # use specific resolver
```

## 8. Troubleshooting patterns

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

# "NXDOMAIN or NODATA?" — the distinction tells you what to fix
dig example.com AAAA
# NOERROR with an empty ANSWER  = name exists, no AAAA         → add the record
# NXDOMAIN                      = name doesn't exist at all    → check spelling/zone

# "Why is my email failing?"
dig example.com MX +short       # are MX records present?
dig example.com TXT +short      # is SPF present? (should start with v=spf1)
dig _dmarc.example.com TXT      # is DMARC published?
dig mail._domainkey.example.com TXT  # DKIM selector 'mail'
dig -x 192.0.2.10 +short        # does the sending IP have a PTR…
dig +short "$(dig -x 192.0.2.10 +short)"   # …and does that name resolve back? (FCrDNS)

# "Is DNSSEC broken?"
dig example.com +dnssec | grep -E 'SERVFAIL|ad|RRSIG|DNSKEY'
# SERVFAIL with DNSSEC = signature validation failure; check TTLs and SOA serial
dig example.com +cd            # succeeds with checking disabled? then it IS DNSSEC

# "Did the zone actually publish my change?" — the serial is the ground truth
dig example.com SOA +short @ns1.example.com
dig example.com SOA +short @ns2.example.com   # secondaries lagging = serial not bumped

# Check TTL remaining on a cached record
dig +noall +answer example.com A
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

### "Prepare a record change without a propagation gap"
```bash
dig +noall +answer example.com A @ns1.example.com   # note the current TTL, e.g. 86400
# lower the TTL to 300 and publish; wait out the OLD ttl (86400s) before changing the value
# make the actual change, verify, then raise the TTL again
```

## Files & locations

| Path | What it holds |
| --- | --- |
| `/etc/resolv.conf` | stub resolver config — nameservers, `search` domains, options. Often a symlink managed by `systemd-resolved` or NetworkManager |
| `/etc/hosts` | static overrides consulted before DNS (order set by `/etc/nsswitch.conf`) |
| `/etc/nsswitch.conf` | the `hosts:` line decides whether files, mDNS, or DNS is asked first |
| `/etc/systemd/resolved.conf` | `systemd-resolved` settings; inspect live state with `resolvectl status` |

## Gotchas / Golden rules

1. **`dig` without `@server` queries the system resolver, which may return cached data** — always query `@ns1.example.com` directly when verifying that a change has propagated to authoritative.
2. **TTL in the ANSWER section is the remaining cache time, not the original TTL** — dig at the authoritative server to see the record's original TTL.
3. **Lowering a TTL takes one old-TTL-period to take effect** — the reduction is itself cached under the previous value. Lower it *before* you need it, not during the change.
4. **CNAME cannot coexist with other records at the zone apex** — `CNAME example.com` is illegal; use A/AAAA directly or an ALIAS/ANAME record if your DNS provider supports it.
5. **MX, NS, and SRV targets must be real hostnames with A/AAAA, never CNAMEs and never IPs** — zone files accept it, the protocol doesn't, and mail servers are the ones that punish you.
6. **A relative name without a trailing dot gets `$ORIGIN` appended** — `CNAME ghs.google.com` silently becomes `ghs.google.com.example.com.`. Every zone-file target should end in a dot.
7. **The SOA `minimum` field is the negative-cache TTL, not a default TTL** (RFC 2308) — set it high and a name you just created keeps returning NXDOMAIN.
8. **Bump the SOA serial on every change** — secondaries compare serials to decide whether to transfer. Forget it and the primary is correct while the secondaries serve yesterday's zone.
9. **All records in an RRset must share one TTL**, and DNSSEC signs the RRset as a unit — you cannot give one of three A records a different lifetime.
10. **`+trace` bypasses the system resolver entirely** — it starts from a root hint and recurses itself, so it reflects what the real DNS tree contains regardless of local caching or resolver configuration.
11. **A missing PTR record will not break forward resolution** — but many mail servers check that the PTR of the sending IP matches the A record of the sending hostname (FCrDNS); missing or mismatched PTR causes mail delivery failures.
12. **DNSSEC signatures expire on a wall clock, not on change** — a zone nobody has touched in months can still go `SERVFAIL` because the re-signing job died. Monitor RRSIG expiry, not just resolution.
13. **`ANY` queries are mostly refused now** (RFC 8482 returns a minimal or synthesised answer) — enumerate the types you care about explicitly instead.
