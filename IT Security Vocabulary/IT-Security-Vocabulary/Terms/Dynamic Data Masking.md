---
domain: "Identity & Access Management"
aliases: ["DDM", "Dynamic Data Masking", "Data Masking"]
tags: [iam, data]
---

# Dynamic Data Masking

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** DDM

A data-protection technique that returns **obfuscated values** for sensitive columns at query time — e.g. `***-**-1234` in place of a full SSN — according to the querying user's privileges. The column is still returned and the stored data is never changed; only its *presentation* is altered for unprivileged users.

**Context.** Branded as a named feature in SQL Server / Azure SQL (`MASKED WITH`), and available as masking policies in Snowflake and BigQuery. The third axis of the data-access trio: [[RLS]] hides *rows*, [[CLS]] hides *columns*, and DDM *returns* the column but *garbles its values*. It's "dynamic" because masking is applied at read time against live data — contrast with **static data masking**, which permanently rewrites data (typically to safely populate non-production environments). Caveat worth memorizing: DDM is a presentation-layer convenience, not a hard security boundary — a user with query access can often infer or exfiltrate the real values (e.g. by filtering on them), so it complements rather than replaces [[CLS]] and proper encryption.

## See also

- [[RLS]]
- [[CLS]]
- [[Data Classification]]
- [[DLP]]
- [[Need to Know]]
- [[Least Privilege]]
- [[Authorization]]
- [[Defense in Depth]]

## Often confused with

- [[CLS]] — CLS *removes* the column from the result for unprivileged users (access denied); DDM *returns* the column but obfuscates its values. CLS is the harder boundary; DDM preserves the schema and queryability at the cost of being a weaker control.

## Further reading

- [Microsoft Learn: Dynamic Data Masking](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking)
