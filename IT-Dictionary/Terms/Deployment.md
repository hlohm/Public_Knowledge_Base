---
type: "term"
branch: "DevOps & SRE"
aliases: ["Deploy"]
tags: ["devops", "fundamental"]
status: "developed"
---

# Deployment

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Deploy

Putting a built artifact into an environment and making it serve traffic. The interesting design space is *how* the cutover happens: all at once, rolling, [[Blue-green Deployment|blue-green]], or [[Canary Release|canary]].

**Context.** Two separations carry most of the modern thinking: build vs deploy (one immutable artifact promoted through environments — never rebuilt per environment) and deploy vs *release* (code can be deployed dark and released later via [[Feature Flag]]s). Deployment frequency is a DORA metric precisely because safe, boring, frequent deploys are the visible symptom of a healthy pipeline.

## See also

- [[CI-CD]]
- [[Rollback]]
- [[Canary Release]]
- [[Blue-green Deployment]]
- [[Feature Flag]]

## Further reading

- [Wikipedia: Software deployment](https://en.wikipedia.org/wiki/Software_deployment)
