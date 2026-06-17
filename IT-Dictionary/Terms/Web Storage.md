---
type: "term"
branch: "Internet & Web"
aliases: ["localStorage", "sessionStorage", "Web Storage API", "DOM Storage"]
tags: [web, fundamental]
status: "developed"
---

# Web Storage

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** localStorage, sessionStorage, Web Storage API, DOM Storage

A browser key–value store, scoped per origin, that holds strings and is read and written from JavaScript via `setItem`/`getItem`. It comes in two flavours: **localStorage** (persists with no expiry until explicitly cleared) and **sessionStorage** (lives only as long as the tab, and is partitioned per tab as well as per origin).

**Context.** The defining contrast with a [[Cookie]] is that Web Storage data is *never sent to the server* — it stays on the client — and the quota is far larger (≈5 MB each per origin, ~10 MB total, against a cookie's ~4 KB). That makes it the natural home for UI preferences, drafts, and cached view state. The catch is that the API is *synchronous*: it blocks the main thread, so large or frequent reads/writes hurt responsiveness, and anything bigger or structured belongs in [[IndexedDB]]. It is governed by the [[Same-Origin Policy]] but, unlike a cookie, has no `HttpOnly` equivalent — any script on the page can read everything in it, so putting auth tokens in localStorage trades CSRF-immunity (nothing auto-sends it) for full [[XSS]] exposure. A `storage` event lets *other* tabs of the same origin observe changes, which is a tidy cross-tab sync channel. In private/incognito windows, localStorage is treated like sessionStorage and wiped on close.

## See also

- [[Cookie]]
- [[IndexedDB]]
- [[Same-Origin Policy]]
- [[DOM]]

## Often confused with

- [[Cookie]] — Web Storage stays in the browser; a cookie is transmitted to the server on every matching request.
- [[IndexedDB]] — Web Storage is synchronous, strings-only, ~5 MB; IndexedDB is asynchronous, transactional, and stores structured objects at much larger scale.

## Further reading

- [MDN: Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)
