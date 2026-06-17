---
type: "term"
branch: "DevOps & SRE"
tags: [devops]
status: "developed"
---

# Blue-green Deployment

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]

A release strategy running two identical production environments (blue = current, green = new); you switch traffic to green and can roll back instantly by switching back.

**Context.** Near-zero-downtime deploys with a fast escape hatch. The cost is double the infrastructure during a release, and database migrations don't switch cleanly (the schema must serve both versions), which is the recurring complication.

## See also

- [[Canary Release]]
- [[Deployment]]
- [[Rollback]]
- [[Feature Flag]]

## Often confused with

- [[Canary Release]] — Blue-green flips all traffic at once between two full environments; canary shifts a small percentage gradually to catch problems before full rollout.

## Further reading

- [Wikipedia: Blue–green deployment](https://en.wikipedia.org/wiki/Blue–green_deployment)
