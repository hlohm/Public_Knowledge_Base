---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
aliases: ["TEE", "\"Trusted Execution Environment\""]
tags: ["cloud", "crypto", "modern"]
status: "note"
---

# Confidential Computing

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]
> **Also known as:** TEE, "Trusted Execution Environment"

Processing data in hardware-isolated **TEEs** (Trusted Execution Environments). Protects data *in use*.

**Context.** Closes the last gap in the at-rest/in-transit/in-use triad: the data is encrypted even against the cloud provider's hypervisor and admins, with hardware attestation proving the workload runs in a genuine enclave. The compelling use cases: regulated data in public cloud, multi-party computation between distrusting parties. Tech names: AMD SEV-SNP, Intel TDX/SGX.

## See also

- [[Remote Attestation]]
