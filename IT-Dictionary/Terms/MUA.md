---
type: "term"
branch: "Internet & Web"
aliases: ["Mail User Agent", "Mail Client"]
tags: ["web", "net", "email"]
status: "developed"
---

# MUA

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Mail User Agent, Mail Client

**M**ail **U**ser **A**gent — the program a person actually reads and writes mail in: Thunderbird, Outlook, a phone app, or a webmail interface.

**Context.** The MUA composes the message and its [[MIME]] structure, then hands it to an [[MSA]] over authenticated submission; it never talks to the recipient's server directly. Coming back the other way it fetches from the mailbox over [[IMAP]], [[POP3]] or [[JMAP]]. Two things make it more security-relevant than its humble position suggests. It decides what the reader sees — display names, whether remote images load, whether authentication results are surfaced — so it is the last line where a message that passed every server-side check can still be recognised as a fraud. And webmail is simply an MUA that happens to run on the provider's server, which is why the same role can be either the most or the least trusted component depending on where it sits.

## See also

- [[MSA]]
- [[MIME]]
- [[IMAP]]
- [[POP3]]
- [[JMAP]]
- [[SMTP]]
- [[Phishing]]
- [[Email Ecosystem]]

## Often confused with

- [[MSA]] — the MUA is the client; the MSA is the server it submits to.

## Further reading

- [Wikipedia: Email client](https://en.wikipedia.org/wiki/Email_client)
