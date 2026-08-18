---
type: "term"
branch: "Internet & Web"
aliases: ["Multipurpose Internet Mail Extensions"]
tags: ["web", "net", "email"]
status: "developed"
---

# MIME

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Multipurpose Internet Mail Extensions

**M**ultipurpose **I**nternet **M**ail **E**xtensions — the standard that turns a plain 7-bit ASCII message into a tree of typed parts, giving email attachments, HTML alternatives, inline images and non-Latin text.

**Context.** The original message format (RFC 822) carried US-ASCII text and nothing else. MIME adds headers describing a structure: `multipart/alternative` for a plain-text and HTML version of the same content, `multipart/mixed` for attachments, `multipart/related` for inline images, plus transfer encodings (base64, quoted-printable) so binary survives relays that only pass 7 bits. It also gave the wider internet its content-type vocabulary — the same `text/html` and `application/json` labels HTTP uses are MIME types. For security work, MIME is the parsing surface: deeply nested parts, unusual encodings and content-type mismatches are standard techniques for showing a filter one thing and the mail client another.

## See also

- [[SMTP]]
- [[MUA]]
- [[Email Ecosystem]]

## Further reading

- [RFC 2045 — MIME Part One](https://datatracker.ietf.org/doc/html/rfc2045)
- [Wikipedia: MIME](https://en.wikipedia.org/wiki/MIME)
