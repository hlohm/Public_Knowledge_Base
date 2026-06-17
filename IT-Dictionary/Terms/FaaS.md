---
type: "term"
branch: "Cloud & Infrastructure"
aliases: ["Function as a Service"]
tags: [cloud, modern]
status: "developed"
---

# FaaS

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]
> **Also known as:** Function as a Service

Cloud model where you deploy individual functions that run on demand, scaling to zero when idle — the core of 'serverless' (AWS Lambda, Cloud Functions).

**Context.** You pay per invocation and never see a server, but the model has sharp edges: cold starts (latency on the first call), execution time limits, and statelessness force a different architecture. Great for spiky, event-driven, glue workloads; awkward for long-running or latency-critical ones.

## See also

- [[Serverless]]
- [[PaaS]]
- [[Cold Start]]
- [[Event-driven Architecture]]

## Further reading

- [Wikipedia: Function as a service](https://en.wikipedia.org/wiki/Function_as_a_service)
