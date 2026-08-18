---
type: cheatsheet
area: "Networking & Protocols"
aliases: [postconf, postqueue, postsuper, postmap, postcat, main.cf, master.cf]
tags: [networking, email, smtp, mta, cli, linux]
status: working
---

# postfix

> **Area:** [[Networking & Protocols]]

Operating the Postfix MTA: the process model, the two config files, lookup tables, the queue, and how to read the log. Covers the commands you drive it with (`postconf`, `postqueue`, `postsuper`, `postmap`, `postcat`) and the parameters you actually touch. Does **not** cover mailbox storage (Dovecot), webmail, or the DNS-side auth records — those are SPF/DKIM/DMARC/MTA-STS in the dictionary and [[dns]] here.

> For the conceptual picture this fits into — participants, ports, the authentication chain, transport security, and how personal / SMB / provider deployments differ — see the **Email Ecosystem** map in the IT-Dictionary (`IT-Dictionary/Maps/Email Ecosystem.md`, with an interactive version in `IT-Dictionary/assets/`).

> Postfix 3.x assumed. Two things moved in the 3.x line: logging can go through `postlogd` instead of syslog (§7), and `default_database_type` moved from `hash` to `lmdb` on several distros — check yours before writing `hash:` into a config (§4).

---

## 1. Orientation — the shape of the thing

Postfix is **not one daemon**. `master` is a supervisor that starts short-lived, single-purpose, mostly-unprivileged processes, each doing one job and talking over sockets. Nothing runs as root that doesn't have to, and no process both parses network input and writes to the queue.

```
      network :25 ──▶ smtpd ──┐
                              ├──▶ cleanup ──▶ incoming ──▶ qmgr ──▶ smtp    ──▶ remote MTA
   sendmail(1) ──▶ maildrop ──┤                  (queue)    (active)  local   ──▶ /var/mail
                    └─ pickup ─┘                                      virtual ──▶ mailbox
                                                                      lmtp    ──▶ Dovecot
                                                             deferred ◀── soft failure (4xx)
                                                             bounce   ◀── hard failure (5xx)
```

The whole operator's mental model is in that diagram: **mail enters, gets normalised, lands in a queue, and a scheduler retries it until it leaves or expires.** Almost every question you will ask Postfix is "where in that pipeline is my message, and why is it still there".

```bash
postfix status                    # is it running
postfix check                     # config sanity + permissions, changes nothing — run before every reload
postfix reload                    # re-read main.cf/master.cf; enough for almost every change
systemctl restart postfix         # needed for inet_interfaces changes (reload will NOT pick those up)
```

## 2. `postconf` — the real interface to the config

Editing `main.cf` by hand is fine; `postconf` is safer and is how you *read* it.

```bash
postconf -n                       # ONLY non-default settings — this is "your config", the thing to paste when asking for help
postconf -d                       # all built-in defaults
postconf mydestination            # one parameter's effective value
postconf -x smtpd_relay_restrictions   # expand $parameter references to literal values
postconf -e 'myhostname = mail.example.org'    # edit main.cf in place, safely (creates or replaces)
postconf -X smtpd_use_tls         # DELETE a setting → back to the built-in default
postconf -M                       # master.cf as parameters
postconf -P                       # master.cf per-service -o overrides
postconf -m                       # which lookup table types this build supports
postconf -c /etc/postfix-two      # operate on an alternate config directory
```

- **`postconf -n` is the single most useful command in Postfix.** It separates what you chose from what you inherited.
- `postconf -e` rewrites `main.cf` but does not reload — follow with `postfix check && postfix reload`.

## 3. The two config files

**`main.cf`** — `key = value` parameters, global. Values can reference others with `$name`.

```bash
myhostname = mail.example.org     # this host's FQDN; used in HELO and Received:
mydomain   = example.org
myorigin   = $mydomain            # domain appended to local, bare usernames
mydestination = $myhostname, localhost    # domains delivered LOCALLY — empty on a pure relay/forwarder
mynetworks = 127.0.0.0/8          # trusted clients; keep this TIGHT, it bypasses relay checks
relayhost  = [smtp.provider.tld]:587      # send everything via a smarthost; [] = skip MX lookup
inet_interfaces = all             # or loopback-only for a null client — needs a RESTART, not a reload
inet_protocols = ipv4             # stop it advertising v6 you can't actually serve
```

**`master.cf`** — which services run, and how. Whitespace-columnar:

```
# service  type  private unpriv chroot wakeup maxproc command + args
smtp       inet  n       -      y      -      -       smtpd
submission inet  n       -      y      -      -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
pickup     unix  n       -      y      60     1       pickup
cleanup    unix  n       -      y      -      0       cleanup
qmgr       unix  n       -      n      300    1       qmgr
smtp       unix  -       -      y      -      -       smtp
local      unix  -       n      n      -      -       local
```

- The indented **`-o key=value`** lines override `main.cf` *for that service only*. This is how one Postfix serves port 25 with one policy and port 587 with a completely different one.
- `-` in a column means "use the default". `maxproc 0` = unlimited-ish; `1` = singleton (qmgr, pickup).
- Add `-o` overrides under the service, never by duplicating parameters in `main.cf`.

## 4. Lookup tables (maps)

A map is `key → value`. The **type prefix matters more than the file**:

| Type | Indexed? | Re-read | Use for |
| --- | --- | --- | --- |
| `hash:` / `lmdb:` / `btree:` | yes — needs `postmap` | on process start | big static lists; the everyday default |
| `pcre:` / `regexp:` | no | on process start | patterns, one rule covering infinite keys |
| `cidr:` | no | on process start | IP ranges |
| `texthash:` | no | every lookup | small files you edit often; no `postmap` step |
| `inline:` | no | — | two or three entries, straight in `main.cf` |
| `ldap:` / `mysql:` / `pgsql:` | external | live | directory-backed setups |
| `static:` | no | — | always returns the same value |

```bash
postconf -m                             # what this build supports
postconf default_database_type          # hash or lmdb — write the type you actually have

postmap /etc/postfix/virtual            # (re)build the indexed .db/.lmdb — REQUIRED after every edit
postmap -q "user@example.org" hash:/etc/postfix/virtual      # test a lookup, exactly as postfix would
postmap -q "anything.ab12@example.org" pcre:/etc/postfix/tier3   # test a pattern map (no build step)
postmap -q - hash:/etc/postfix/virtual < keys.txt            # bulk test from stdin
newaliases                              # rebuild /etc/aliases.db (= postalias /etc/aliases)
```

**The five rewriting maps, and which one you want:**

| Map | Acts on | When |
| --- | --- | --- |
| `alias_maps` | local recipients only, after delivery to `local(8)` | classic `/etc/aliases`, `root: admin` |
| `virtual_alias_maps` | any recipient, before delivery | forwarding, aliasing, catch-alls |
| `canonical_maps` | envelope **and** header, both directions | global address rewriting |
| `smtp_generic_maps` | outbound SMTP only | make internal addresses externally valid |
| `transport_maps` | routing, not addresses | `example.org  relay:[host]:port` |

## 5. The queue

```bash
postqueue -p                      # queue listing (= mailq). Columns: qid, size, arrival, sender / reason / recipients
postqueue -j                      # same as JSON — parse this, not the human format
postqueue -f                      # flush: retry everything NOW
postqueue -i D3A9F1234            # flush one message
postqueue -s example.org          # flush everything for one destination

postcat -q D3A9F1234              # read a queued message
postcat -qe D3A9F1234             # envelope only — who it's REALLY from/to
postcat -qh D3A9F1234             # headers only

postsuper -d D3A9F1234            # delete one
postsuper -d ALL deferred         # delete the whole deferred queue (destructive, no undo)
postsuper -r D3A9F1234            # requeue: re-run it through cleanup (picks up config changes)
postsuper -h D3A9F1234            # hold — freeze it, no delivery attempts
postsuper -H D3A9F1234            # release from hold
postsuper -s                      # structure check / fix queue file placement
```

**The queues themselves**, under `/var/spool/postfix/`:

| Queue | Meaning |
| --- | --- |
| `maildrop` | submitted locally by `sendmail(1)`, awaiting `pickup` |
| `incoming` | accepted, normalised by `cleanup`, awaiting the scheduler |
| `active` | qmgr is working on it right now (bounded, small) |
| `deferred` | soft-failed (4xx / timeout); retried with backoff until `maximal_queue_lifetime` (default **5d**) |
| `hold` | frozen by an operator or a rule; never expires, never retries |
| `corrupt` | unreadable queue files — someone should look |

Retry pacing: `minimal_backoff_time` → `maximal_backoff_time`, scanned every `queue_run_delay`. **Senders retrying for days is why a backup MX is worth less than it feels.**

## 6. Restrictions — and never being an open relay

Restriction lists are evaluated in order; first `REJECT`/`OK` wins. By default (`smtpd_delay_reject = yes`) they are all evaluated at `RCPT TO`, so the client sees the rejection there regardless of which list produced it.

```bash
smtpd_client_restrictions   = ...     # by connecting IP/hostname
smtpd_helo_restrictions     = reject_invalid_helo_hostname
smtpd_sender_restrictions   = reject_unknown_sender_domain
smtpd_relay_restrictions    = permit_mynetworks,
                              permit_sasl_authenticated,
                              defer_unauth_destination      # ← THE anti-open-relay guard (2.10+)
smtpd_recipient_restrictions= reject_unauth_destination,    # ← the older place for the same job
                              reject_unlisted_recipient
smtpd_data_restrictions     = reject_unauth_pipelining
```

Common values: `permit_mynetworks`, `permit_sasl_authenticated`, `reject_unauth_destination`, `defer_unauth_destination`, `reject_unlisted_recipient`, `reject_rbl_client zen.spamhaus.org`, `reject_unknown_reverse_client_hostname`, `check_client_access <map>`, `check_recipient_access <map>`, `permit`, `reject`.

> **`reject_unauth_destination` (or its `defer_` twin) is the line that stops you being an Open Relay.** It says: accept mail for domains I am responsible for; refuse to carry anything else. If you write custom restriction lists and drop it, you have built a spam cannon. Verify from off-net, never by reading the config.

## 7. Logs — the operator's real instrument

```bash
journalctl -u postfix@-.service -f                  # systemd unit (the template instance, note the @-)
tail -f /var/log/mail.log                           # traditional syslog path
postconf maillog_file                               # if set, postlogd writes here and syslog is bypassed
```

Every message gets a **queue ID**; trace by it:

```bash
grep D3A9F1234 /var/log/mail.log                    # the whole life of one message
journalctl -u postfix@-.service | grep 'status=bounced'
```

A delivery line reads:

```
postfix/smtp[1234]: D3A9F1234: to=<a@example.org>, relay=mx.example.org[192.0.2.1]:25,
  delay=0.9, delays=0.1/0/0.4/0.4, dsn=2.0.0, status=sent (250 2.0.0 OK)
```

- `status=` is the verdict: `sent` · `deferred` (will retry) · `bounced` (gave up, Backscatter risk) · `expired`.
- `dsn=` is the class: **4.x.x temporary, 5.x.x permanent**.
- `delays=a/b/c/d` = before-queue / queue-wait / connect-setup / transmission. **Which number is large tells you which layer is slow** — a big `c` is the network, a big `b` is your own scheduler backlog.

**Targeted verbosity** without drowning the log:

```bash
postconf -e 'debug_peer_list = example.org'         # or an IP/CIDR
postconf -e 'debug_peer_level = 2'
postfix reload                                       # verbose ONLY for that peer
```

## 8. TLS — and the one-letter trap

**`smtp_` = outbound (Postfix as client). `smtpd_` = inbound (Postfix as server, the `d` is daemon.)** Nearly every confusing Postfix TLS problem is this letter.

```bash
smtpd_tls_security_level = may            # inbound: offer STARTTLS, don't require it (correct for :25)
smtpd_tls_cert_file = /etc/ssl/.../fullchain.pem
smtpd_tls_key_file  = /etc/ssl/.../privkey.pem
smtp_tls_security_level = dane            # outbound: use DANE/TLSA when published, else opportunistic
smtp_tls_loglevel = 1                     # log the negotiated cipher per delivery
smtp_dns_support_level = dnssec           # required for dane — and the resolver must return the AD bit
```

```bash
openssl s_client -starttls smtp -connect mail.example.org:25 -crlf   # what do we actually offer
posttls-finger -c example.org                                        # Postfix's own TLS prober: policy, DANE, cert
```

## 9. Milters & content filters

Milters (the Sendmail milter protocol) are how DKIM signing, DMARC checking and spam scoring bolt on.

```bash
smtpd_milters     = unix:/run/opendkim/opendkim.sock, unix:/run/opendmarc/opendmarc.sock
non_smtpd_milters = $smtpd_milters        # also sign locally-submitted mail
milter_default_action = accept            # accept if the milter is DOWN — the alternative is a self-inflicted outage
milter_protocol = 6
```

```bash
header_checks = pcre:/etc/postfix/header_checks    # /^X-Spam-Flag: YES/ DISCARD
body_checks   = pcre:/etc/postfix/body_checks
```

> **Anything that alters headers or body after signing breaks DKIM.** Footer-appending, subject-tagging and "helpful" rewriting are the usual culprits. On a forwarder, touch nothing.

---

## Daily workflows

### "Is it even listening, and does it answer?"
```bash
ss -lntp | grep -E ':25|:587|:465'
postconf -n | grep -E 'inet_interfaces|mydestination|mynetworks'
swaks --to you@example.org --server localhost      # the single best mail-testing tool; install it
# no swaks? by hand:
printf 'EHLO test\r\nQUIT\r\n' | nc -w5 localhost 25
```

### "Mail is stuck — where and why?"
```bash
postqueue -p | head -30                 # the reason is in the (parenthesised) text under each entry
postqueue -p | tail -1                  # "-- N Kbytes in M Requests." — the size of the problem
postcat -qe <qid>                       # envelope: is it even addressed the way you think?
grep <qid> /var/log/mail.log            # the full history
postqueue -f                            # after fixing the cause, retry now
```

### "Am I an open relay?" (ask from OUTSIDE)
```bash
swaks --server mail.example.org --from probe@example.net --to nobody@definitely-not-mine.tld
# MUST be rejected: 554 5.7.1 Relay access denied.
# Accepted → stop everything and fix smtpd_relay_restrictions.
```

### "Test a config change without sending anything anywhere"
```bash
postconf -e 'soft_bounce = yes'         # turns every permanent 5xx into a temporary 4xx
postfix reload                          # nothing is lost while you experiment — it all sits in deferred
# ... test ...
postconf -X soft_bounce && postfix reload && postqueue -f
```

### "Purge a spam flood out of the queue"
```bash
postqueue -j | jq -r 'select(.sender=="bad@example.net") | .queue_id' | postsuper -d -
```

### "Where did this message actually go?"
```bash
grep -E "$(grep -oP '(?<=: )[0-9A-F]{8,}(?=:)' <<<"$line")" /var/log/mail.log
sendmail -bv user@example.org           # dry-run: report deliverability without delivering
```

## Files & locations

| Path | What |
| --- | --- |
| `/etc/postfix/main.cf` | global parameters |
| `/etc/postfix/master.cf` | which services run, and their per-service overrides |
| `/etc/postfix/*.cf` | map definitions for `ldap:`/`mysql:` lookups |
| `/etc/aliases` | local alias map → rebuild with `newaliases` |
| `/var/spool/postfix/` | the queues (`incoming`, `active`, `deferred`, `hold`, `corrupt`) |
| `/var/spool/postfix/etc/` | **copies** of `/etc` files for chrooted services (§Gotchas) |
| `/var/log/mail.log`, `mail.err` | traditional syslog output |
| `/usr/libexec/postfix/`, `/usr/lib/postfix/sbin/` | the daemon binaries `master` starts |

## Gotchas / Golden rules

1. **`smtp_` vs `smtpd_`** — client/outbound vs server/inbound. One letter, opposite direction. When a TLS or restriction setting "does nothing", check this first.
2. **`postmap` after every map edit** — indexed types (`hash:`, `lmdb:`) serve the compiled `.db`, not your text file. Editing the text and reloading changes nothing, silently. Use `texthash:` for small files you edit constantly and skip the build step.
3. **`postfix reload` covers almost everything — `inet_interfaces` is the exception** and needs a real restart. Also re-check permissions with `postfix check` after touching anything by hand.
4. **`mydestination` on a relay must be EMPTY.** If your relay domain appears there, Postfix tries to deliver locally instead of forwarding, and mail vanishes into `/var/mail` or bounces as "unknown user".
5. **`mynetworks` is a trust list, not a convenience list.** Everything in it can relay through you. `mynetworks_style = subnet` silently trusts the whole attached subnet — set the CIDR explicitly.
6. **Never an open relay, and verify from off-net.** `reject_unauth_destination` / `defer_unauth_destination` must survive every edit to the restriction lists.
7. **Chroot bites.** Services with `y` in the chroot column see `/var/spool/postfix` as `/`, so they cannot read `/etc/resolv.conf`, `/etc/services` or your CA bundle unless copies exist under `/var/spool/postfix/etc/`. Symptom: DNS or TLS failures that make no sense from a shell on the same box.
8. **`message_size_limit` must exceed `mailbox_size_limit`**, or large-but-legal messages fail in a way the logs describe unhelpfully.
9. **Don't modify the body.** Footers, disclaimers and subject tags invalidate DKIM signatures downstream. On a forwarder this is the difference between working and mysteriously failing at one recipient domain.
10. **`soft_bounce = yes` is the safety net for every risky change** — nothing is permanently rejected while it's on. Remember to turn it off; a forgotten `soft_bounce` fills the deferred queue with mail that should have bounced.
11. **`postsuper -d ALL` has no undo.** There is no trash. Take a `postqueue -j` dump first if there is any chance you'll want the list.
12. **Read `postconf -n`, not `main.cf`.** The file may contain commented experiments, duplicate keys (last wins, silently) and settings shadowed by `master.cf` `-o` lines. `postconf -n` is what is actually in force.

## See also

- **IT-Dictionary** (separate vault — referenced by name, not linked): *MTA*, *MDA*, *MSA*, *Envelope Sender*, *Milter*, *SRS*, *Null Client*
- **IT-Dictionary**: *Open Relay*, *Backscatter*, *Greylisting*, *IP Reputation* — the failure modes
- [[dns]] — MX/PTR/TLSA lookups and DNSSEC validation
- [[openssl]] · [[nc]] — probing an SMTP endpoint by hand
- [[systemd]] — unit management and `journalctl` for the mail log
