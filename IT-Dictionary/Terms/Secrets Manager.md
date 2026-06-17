---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Secrets Manager

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Tool that stores and rotates secrets (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).

**Context.** The properties that matter: central audit of every read, rotation without redeploying, access via the workload's identity instead of via another password. That last point is the *secret-zero* problem — something must authenticate the app to the vault — solved by platform identity (managed identities, instance roles, Kubernetes service accounts).

## See also

- [[Secret]]
- [[HSM]]
