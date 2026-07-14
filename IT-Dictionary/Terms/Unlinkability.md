---
type: "term"
branch: "Security"
domain: "Core Principles"
tags: ["privacy", "anonymity"]
status: "developed"
---

# Unlinkability

> **Domain:** [[01 - Core Principles|Core Principles & Models]]

The property that an observer cannot tell whether two or more items of interest — messages, actions, identities, sessions — are related. Where confidentiality hides *content*, unlinkability hides *relationships*: that this payment belongs to that account, or that the packet entering a relay is the one leaving it.

**Context.** The design goal behind most metadata-protection systems. [[Mixnet|Mixnets]] buy it by batching, reordering, and padding traffic; [[Zero-Knowledge Proof|zero-knowledge credentials]] buy it by letting a user prove entitlement without presenting a reusable identifier; pseudonym rotation buys it cheaply but weakly. It is also the property that traffic analysis attacks — timing correlation, size fingerprinting — are designed to break, which is why fixed-size packets ([[Sphinx Packet Format]]) and [[Cover Traffic]] exist.

## See also

- [[Mixnet]]
- [[Cover Traffic]]
- [[Sphinx Packet Format]]
- [[Traffic Correlation Attack]]
- [[Zero-Knowledge Proof]]

## Often confused with

- [[Non-repudiation]] — the deliberate opposite: non-repudiation *guarantees* an action can be tied to an actor; unlinkability guarantees it cannot.

## Further reading

- [Pfitzmann & Hansen: Anonymity, Unlinkability, Undetectability — A Terminology Proposal](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf)
