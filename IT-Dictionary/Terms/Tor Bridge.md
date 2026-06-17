---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Bridge Relay"]
tags: ["anonymity", "censorship", "network"]
status: "developed"
---

# Tor Bridge

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Bridge Relay

A [[Tor]] entry relay that is **not** published in the public directory, so a censor or ISP can't just block the known list of Tor nodes — used to reach Tor where access to it is filtered or watched.

**Context.** A bridge solves the "my network blocks or flags that I use Tor" problem, and pairs with a [[Pluggable Transport]] (obfs4, Snowflake) to also disguise *what the traffic looks like*. It's a cleaner answer than tunnelling Tor through a personal [[VPN]]: a bridge is unlisted and not tied to infrastructure registered in your name, whereas a self-hosted VPN merely *relocates* the "this identity uses Tor" signal from your ISP to your VPS provider's egress.

## See also

- [[Pluggable Transport]]
- [[Entry Guard]]
- [[Tor]]

## Often confused with

- [[VPN]] — both can hide Tor use from a local network, but a bridge is purpose-built, unlisted, and identity-neutral; a VPN adds a trusted middleman and a single identifiable chokepoint.

## Further reading

- [Tor Browser Manual: Bridges](https://tb-manual.torproject.org/bridges/)
