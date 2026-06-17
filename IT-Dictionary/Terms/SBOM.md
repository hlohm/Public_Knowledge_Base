---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Software Bill of Materials"]
tags: ["appsec", "modern"]
status: "developed"
---

# SBOM

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Software Bill of Materials

**S**oftware **B**ill **o**f **M**aterials. Inventory of components in a piece of software. Formats: SPDX, CycloneDX.

**Context.** Log4Shell made the case overnight: the first question was "where do we even use log4j?" and most orgs couldn't answer. An SBOM turns that from a frantic audit into a query. Generation is easy (Syft, CycloneDX tools); the value is in *consuming* it — feeding SCA, matching against new CVEs, and increasingly satisfying procurement/regulatory demands (US EO 14028).

## See also

- [[SCA]]
- [[Supply Chain Attack]]

## Further reading

- [CISA: Software Bill of Materials](https://www.cisa.gov/sbom)
