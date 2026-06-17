---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Endpoint Detection and Response"]
tags: ["endpoint", "detection"]
status: "note"
---

# EDR

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Endpoint Detection and Response

**E**ndpoint **D**etection and **R**esponse. Records endpoint telemetry, hunts for threats, enables response actions (isolate host, kill process).

**Context.** What changed with EDR is the recorded history: process trees, network connections, file and registry events — so an analyst can answer "how did this start and where did it spread" instead of just "AV deleted a file". Two operational notes: response features (isolate host) are the panic-button you'll be glad exists, and EDR tamper-protection matters because attackers now routinely try to kill the agent first.

## See also

- [[EPP]]
- [[XDR]]
- [[MDR]]
- [[SIEM]]

## Often confused with

- [[XDR]] — EDR is endpoint-only; XDR correlates across endpoint, network, identity, cloud, email.
