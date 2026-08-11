---
type: "term"
branch: "Operating Systems"
aliases: []
tags: [os]
status: "developed"
---

# Locale

> **Branch:** [[03 - Operating Systems|Operating Systems]]

The bundle of settings telling programs how to speak to a human: language of messages, date and time formats, number and currency formatting, sort order. On POSIX systems it's controlled per category through environment variables — `LC_TIME`, `LC_MESSAGES`, `LC_COLLATE`, … — with `LANG` as the default and `LC_ALL` as the override hammer.

**Context.** The categories being independent is both the feature and the trap: a mixed setup (English messages, European time format) is perfectly legal, but plenty of software reads *one* category and infers the rest — an app deriving its 12/24-hour clock from `LC_MESSAGES` instead of `LC_TIME` will ignore your carefully set time format, and the fix is choosing which variable to bend (e.g. a `LC_MESSAGES=en_DK.UTF-8` style compromise). Collation silently changes `sort` and glob order, which is why robust scripts pin `LC_ALL=C`. Locales must be *generated* on the host (`locale-gen`) before they can be used; a missing one degrades to `C`.

## See also

- [[Shell]]
- [[UTF-8]]
- [[Operating System]]

## Further reading

- [Wikipedia: Locale (computer software)](https://en.wikipedia.org/wiki/Locale_(computer_software))
