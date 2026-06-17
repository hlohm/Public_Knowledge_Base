---
type: "term"
branch: "DevOps & SRE"
aliases: ["Desired State Configuration"]
tags: ["devops", "modern"]
status: "note"
---

# Declarative Configuration

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Desired State Configuration

Specifying the *desired end state* ('3 replicas, version 2.1') and letting a controller compute and apply the steps — versus imperative scripts that encode the steps themselves.

**Context.** Declarative is the idea underneath Terraform, Kubernetes, and [[GitOps]]: state in files means diffable changes, code review for infrastructure, and **reconciliation loops** that continuously repair drift instead of one-shot scripts that rot. The mental shift is from 'run commands' to 'edit the truth and let the system converge.'

## See also

- [[Infrastructure as Code]]
- [[GitOps]]
- [[Kubernetes]]
- [[Terraform]]
- [[Idempotent]]
