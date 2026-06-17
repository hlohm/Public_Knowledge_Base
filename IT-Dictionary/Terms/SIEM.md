---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
aliases: ["Security Information and Event Management"]
tags: ["secops"]
status: "note"
---

# SIEM

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]
> **Also known as:** Security Information and Event Management

**S**ecurity **I**nformation and **E**vent **M**anagement. Central log aggregation, correlation, and alerting platform.

**Context.** The SOC's central nervous system — and its biggest line item, because licensing usually meters ingest, so the eternal tension is log *everything* vs. log what you'll actually detect on. Value comes from correlation and tuned use-cases, not raw collection; a SIEM fed garbage produces expensive garbage. Common platforms: Splunk, Sentinel, Elastic. Increasingly paired with or absorbed into XDR.

## See also

- [[SOAR]]
- [[XDR]]
- [[Detection Engineering]]
