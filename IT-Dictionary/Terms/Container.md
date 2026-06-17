---
type: "term"
branch: "Cloud & Infrastructure"
tags: [cloud, fundamental]
status: "developed"
---

# Container

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]

A lightweight, isolated package bundling an application with its dependencies, sharing the host OS kernel (via namespaces and cgroups) rather than running its own.

**Context.** Solves 'works on my machine' by shipping the environment with the app. Far lighter than a VM (seconds to start, shared kernel), which is exactly why isolation is weaker — a container escape reaches the host kernel. The unit Kubernetes orchestrates.

## See also

- [[Docker]]
- [[Kubernetes]]
- [[Virtual Machine]]
- [[Namespace]]
- [[Cgroups]]
- [[Image]]

## Further reading

- [Wikipedia: Containerization (computing)](https://en.wikipedia.org/wiki/Containerization_(computing))
