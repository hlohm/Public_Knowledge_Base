---
type: "term"
branch: "Cloud & Infrastructure"
tags: ["cloud", "modern"]
status: "developed"
---

# Cold Start

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]

The first-invocation latency penalty in serverless platforms: before your function runs, the platform must allocate a sandbox, pull the runtime, and initialize your code.

**Context.** Cold starts are the tax on scale-to-zero — the same property that makes [[FaaS]] cheap when idle makes it slow when waking. Severity scales with runtime weight (JVM ≫ Go) and package size; mitigations (provisioned concurrency, keep-warm pings, snapshot restore) all amount to paying to keep instances warm, partially un-serverlessing the design.

## See also

- [[FaaS]]
- [[Serverless]]
- [[Lambda]]
- [[Latency]]

## Further reading

- [Wikipedia: Cold start (computing)](https://en.wikipedia.org/wiki/Cold_start_(computing))
