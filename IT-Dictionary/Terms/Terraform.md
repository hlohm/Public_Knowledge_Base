---
type: "term"
branch: "Cloud & Infrastructure"
tags: [cloud, modern]
status: "developed"
---

# Terraform

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]

A widely used Infrastructure-as-Code tool that provisions cloud resources declaratively from configuration, tracking real-world resources in a **state file**.

**Context.** Cloud-agnostic via providers, which is its main appeal over cloud-specific tools. The state file is the crux and the footgun — it's the source of truth that maps config to real resources, and corrupting or losing it is a classic operational disaster (hence remote, locked state).

## See also

- [[Infrastructure as Code]]
- [[Declarative Configuration]]
- [[Idempotent]]
- [[State Management]]

## Further reading

- [Wikipedia: Terraform (software)](https://en.wikipedia.org/wiki/Terraform_(software))
