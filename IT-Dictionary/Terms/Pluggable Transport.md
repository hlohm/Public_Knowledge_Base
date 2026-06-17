---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["PT"]
tags: ["anonymity", "censorship", "network"]
status: "developed"
---

# Pluggable Transport

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** PT

A swappable layer that reshapes [[Tor]] traffic so it doesn't *look* like Tor — defeating the [[DPI]] a censor uses to fingerprint and block it.

**Context.** Where a [[Tor Bridge]] hides *which servers* you reach, a pluggable transport hides *what the bytes look like* on the wire: **obfs4** makes the stream resemble random noise, **Snowflake** masquerades as a WebRTC video call, **meek** tunnels through a major CDN (domain fronting). This is the purpose-built tool for "hide that I'm using Tor from my ISP" — it beats routing Tor through a personal VPN because it's unlisted, designed to resist DPI, and not anchored to infrastructure that carries your name.

## See also

- [[Tor Bridge]]
- [[DPI]]
- [[Tor]]

## Further reading

- [Tor Browser Manual: Circumvention](https://tb-manual.torproject.org/circumvention/)
