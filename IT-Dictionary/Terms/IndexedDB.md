---
type: "term"
branch: "Internet & Web"
aliases: ["Indexed Database API", "IDB"]
tags: [web]
status: "developed"
---

# IndexedDB

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Indexed Database API, IDB

The browser's built-in, low-level **client-side database**: a transactional, asynchronous store for large amounts of structured data — objects, files, and blobs — kept in *object stores* (not tables) and looked up by key or secondary index.

**Context.** It's where you go when [[Web Storage]] is too small or too dumb. IndexedDB handles tens of megabytes and up, runs off the main thread so it doesn't freeze the UI, wraps writes in transactions that roll back on failure, and supports indexed queries — it's the storage layer behind offline-capable PWAs and service-worker caches. The price is ergonomics: the raw event-based API is famously clunky (open a connection, bump a version number to migrate the schema in an `onupgradeneeded` handler, do everything inside transactions), so most projects reach for a wrapper such as Dexie or idb. Like all browser storage it obeys the [[Same-Origin Policy]] — one database per origin, invisible to others — and it persists anything the *structured clone* algorithm can serialize, which is why it can hold real objects and binary data that [[Web Storage]] (strings only) cannot.

## See also

- [[Web Storage]]
- [[Cookie]]
- [[Same-Origin Policy]]
- [[Database]]

## Often confused with

- [[Web Storage]] — localStorage/sessionStorage are small, synchronous, and strings-only; IndexedDB is large, asynchronous, transactional, and stores structured objects.

## Further reading

- [MDN: IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
