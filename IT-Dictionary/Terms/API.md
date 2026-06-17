---
type: "term"
branch: "Software Engineering"
aliases: ["Application Programming Interface"]
tags: [se, fundamental]
status: "developed"
---

# API

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** Application Programming Interface

The defined contract through which one piece of software is used by another — function signatures, endpoints, data formats. The interface, deliberately hiding the implementation.

**Context.** Spans library APIs (function calls) to web APIs (REST/GraphQL over HTTP). A good API is hard to misuse and stable; once published it's a promise, which is why versioning and backward compatibility loom so large. 'API design is UX for developers.'

## See also

- [[ABI]]
- [[REST]]
- [[Interface]]
- [[Backward Compatibility]]
- [[API Versioning]]

## Often confused with

- [[ABI]] — An API is a source-level contract (compile against it); an ABI is a binary-level contract (link/run against it) — calling conventions, struct layout.

## Further reading

- [Wikipedia: API](https://en.wikipedia.org/wiki/API)
