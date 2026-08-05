---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec", "testing"]
status: "developed"
---

# Fuzzing

> **Domain:** [[08 - Application Security|Application Security]]

Feeding malformed/random input to find crashes and security bugs.

**Context.** Throw malformed input at code until it crashes, then triage the crashes for security bugs — coverage-guided fuzzers (AFL++, libFuzzer) evolve inputs to reach deep code paths. It's how parsers, codecs, and protocol stacks get hardened, and Google's OSS-Fuzz finds thousands of bugs in critical open source continuously. Most valuable on anything that parses untrusted bytes.

## See also

- [[DAST]]
- [[Buffer Overflow]]
- [[Property-Based Testing]]

## Further reading

- [Google OSS-Fuzz](https://google.github.io/oss-fuzz/)
