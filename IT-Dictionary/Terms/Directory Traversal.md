---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Path Traversal"]
tags: ["threat", "appsec"]
status: "developed"
---

# Directory Traversal

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Path Traversal

`../../../etc/passwd` and friends. Escaping the intended file-system root.

**Context.** Still appears wherever code builds file paths from user input — download endpoints, template loaders, archive extractors (the "Zip Slip" variant). Defense is canonicalize-then-validate against an allowlisted base directory; naive `../` stripping is bypassable with encoding tricks. Cousin of LFI/RFI in web apps.

## See also

- [[Input Validation]]

## Further reading

- [OWASP: Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
