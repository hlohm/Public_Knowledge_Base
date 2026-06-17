---
type: "term"
branch: "Internet & Web"
tags: [web]
status: "developed"
---

# Reverse Proxy

> **Branch:** [[05 - Internet & Web|Internet & Web]]

A server sitting in front of backend servers, receiving client requests and forwarding them — handling TLS, caching, compression, and routing.

**Context.** nginx/Envoy/Traefik in this role centralise concerns (TLS termination, rate limiting) off the app. A *forward* proxy fronts clients; a reverse proxy fronts servers.

## See also

- [[Proxy]]
- [[Load Balancer]]
- [[CDN]]

## Often confused with

- [[Proxy]] — A forward proxy represents the client to the internet; a reverse proxy represents the server to clients.

## Further reading

- [Wikipedia: Reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)
