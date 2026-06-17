---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Static Application Security Testing"]
tags: ["appsec", "testing"]
status: "note"
---

# SAST

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Static Application Security Testing

**S**tatic **A**pplication **S**ecurity **T**esting. Analyzing source code without running it. Finds bugs early; high false-positive rate.

**Context.** Finds bugs early and cheap by reading source, and integrates into CI/PRs — but the false-positive rate is its reputation problem, and it's blind to runtime/config issues. The win is tuning: triage seriously at first, suppress noise, and gate only on high-confidence findings so developers don't learn to ignore it. CodeQL, Semgrep, SonarQube are common.

## See also

- [[DAST]]
- [[IAST]]
- [[SCA]]
- [[Shift Left]]

## Often confused with

- [[DAST]] — SAST reads code; DAST tests a running app from outside.
