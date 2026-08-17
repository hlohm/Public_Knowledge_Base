---
type: "map"
tags: [map, web]
---

# Internet & Web

> The application-layer world built on the network: HTTP, DNS, browsers, the request/response lifecycle.

## Terms in this branch (25)

- [[CDN]] — A geographically distributed network of caching servers that serve content from a location near each user, cutting latency and origin load.
- [[Cookie]] — A small key–value string a server sets in the browser and that the browser echoes back on later requests — the original way to add state to stateless HTTP.
- [[CORS]] — A browser mechanism letting a server opt in to requests from web pages on other origins, relaxing the same-origin policy under controlled rules.
- [[DOM]] — The browser's in-memory tree representation of an HTML page that scripts can read and modify to change what's displayed.
- [[GET]] — The HTTP method for retrieving a resource.
- [[GraphQL]] — A query language and runtime for APIs where the client specifies exactly which fields it wants from a typed schema, in a single request.
- [[HTML]] — The document language of the web: nested elements describing structure and meaning, parsed by the browser into the [[DOM]].
- [[HTTP]] — The request/response application protocol of the web: a client asks for a resource with a method (GET, POST…), a server answers with a status code and body.
- [[HTTPS]] — HTTP carried inside a TLS-encrypted connection, providing confidentiality, integrity, and server authentication.
- [[IndexedDB]] — The browser's built-in transactional, asynchronous client-side database for large amounts of structured data, held in object stores and queried by key or index.
- [[JSON]] — A lightweight, human-readable data format of nested objects, arrays, strings, numbers, booleans, and null — the default for web APIs.
- [[MDA]] — Mail Delivery Agent — the component that writes a message into the recipient's actual mailbox, at the end of the mail path.
- [[Milter]] — A protocol letting an external process inspect and modify a message while the SMTP transaction is still open — how DKIM signing and spam scoring bolt onto an MTA.
- [[MSA]] — Mail Submission Agent — the authenticated front door (port 587) where a mail client hands a new message to the infrastructure.
- [[MTA]] — Mail Transfer Agent — the server that accepts mail over SMTP, spools it to a queue, and retries until it is delivered or expires.
- [[Null Client]] — A send-only MTA: listens on nothing, delivers nothing locally, forwards everything to a smarthost. The right shape for almost every server.
- [[POST]] — The HTTP method for submitting data to be processed, typically creating a resource or triggering a state change.
- [[REST]] — An architectural style (Fielding) for web APIs: resources identified by URLs, manipulated with standard HTTP methods, stateless interactions.
- [[Reverse Proxy]] — A server sitting in front of backend servers, receiving client requests and forwarding them — handling TLS, caching, compression, and routing.
- [[Session]] — The server-side notion of a continuing relationship with one client across stateless HTTP requests, keyed by an opaque session ID the browser carries (usually in a cookie).
- [[SMTP]] — The protocol that moves email between servers — a plain-text dialogue of HELO/EHLO, MAIL FROM, RCPT TO, DATA.
- [[Status Code]] — A three-digit number in an HTTP response signalling outcome: 2xx success, 3xx redirect, 4xx client error, 5xx server error.
- [[WASM]] — A portable binary instruction format that runs in browsers (and beyond) at near-native speed, as a compilation target for C, Rust, Go, and more.
- [[Web Storage]] — A per-origin browser key–value store of strings, never sent to the server, in two flavours: localStorage (persistent) and sessionStorage (per-tab).
- [[WebSocket]] — A protocol providing a persistent, full-duplex connection between browser and server over a single TCP connection, after an HTTP upgrade handshake.

---
← Back to [[_Home]]
