---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Living off the Land"]
tags: ["threat", "modern"]
status: "developed"
---

# LotL

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Living off the Land

**L**iving **o**ff **t**he **L**and. Using legitimate built-in tools (PowerShell, WMI, certutil) for malicious purposes. Evades signature detection.

**Context.** The reason "the binary was signed by Microsoft" stopped being reassuring: PowerShell, WMI, certutil, rundll32, and friends (the LOLBAS catalog) are trusted, present everywhere, and do the attacker's work without dropping a file. Detection shifts from signatures to behavior — *why* is this server spawning PowerShell that base64-decodes and reaches out to the internet?

## See also

- [[Application Allowlisting]]
- [[EDR]]

## Further reading

- [LOLBAS Project](https://lolbas-project.github.io/)
