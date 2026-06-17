---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["IDS", "\"IPS\""]
tags: ["network", "detection"]
status: "note"
---

# IDS and IPS

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** IDS, "IPS"

**I**ntrusion **D**etection / **P**revention **S**ystem. IDS detects and alerts; IPS detects and **blocks**. Can be network-based (NIDS) or host-based (HIDS).

**Context.** The IPS promise comes with the false-positive tax: inline blocking of a misclassified business application is a self-inflicted outage, so deployments typically start in detect-mode and graduate rules to blocking. Open-source standbys: Suricata and Snort signatures, Zeek for the network-metadata angle that feeds threat hunting.

## See also

- [[HIDS and HIPS]]
- [[NGFW]]
- [[WAF]]

## Often confused with

- [[HIDS and HIPS]] — Network vs host placement. Network-IDS sees the wire; host-IDS sees the kernel/processes.
