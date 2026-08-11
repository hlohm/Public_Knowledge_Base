---
type: "map"
tags: [map, devops]
---

# DevOps & SRE

> Shipping and operating software continuously and reliably — pipelines, observability, error budgets.

## Terms in this branch (24)

- [[Blue-green Deployment]] — A release strategy running two identical production environments (blue = current, green = new); you switch traffic to green and can roll back instantly by switching back.
- [[Canary Release]] — Rolling out a change to a small subset of users first, monitoring it, then gradually expanding if healthy — limiting the blast radius of a bad release.
- [[CI-CD]] — The automated pipeline from code commit to deployment — continuous integration (build + test every change) flowing into continuous delivery/deployment (automated release).
- [[Continuous Delivery]] — Keeping the main branch always releasable: every change flows through an automated pipeline to a deployable artifact, and shipping is a business decision, not an engineering project.
- [[Dead Man's Switch]] — A monitor that fires when an expected check-in *stops* arriving, catching things that die quietly.
- [[Declarative Configuration]] — Specifying the desired end state ('3 replicas, version 2.1') and letting a controller compute and apply the steps — versus imperative scripts that encode the steps themselves.
- [[Deploy Key]] — An SSH key scoped to exactly one repository — the credential you put on a machine you deliberately don't fully trust.
- [[Deployment]] — Putting a built artifact into an environment and making it serve traffic.
- [[DevOps]] — A culture and set of practices uniting software development and operations to shorten the delivery cycle through automation, shared ownership, and fast feedback.
- [[Error Budget]] — The amount of unreliability an SLO permits (100% minus the target), treated as a budget that can be 'spent' on risk, change, and feature velocity.
- [[File Versioning]] — Automatically keeping superseded copies of individual files for quick per-file rollback — the fat-finger recovery layer, not a backup.
- [[GitOps]] — An operational model where a Git repository is the single source of truth for declarative infrastructure and apps, and an agent continuously reconciles the live system to match it.
- [[Immutable Backup]] — A backup that can't be altered or deleted after writing (object lock / append-only) — the core ransomware defense.
- [[Maintenance Window]] — A pre-announced period during which a system may be down for planned work — and monitoring is expected to hold its fire.
- [[Monitoring]] — Collecting and watching predefined signals — metrics, logs, health checks — and alerting when they cross thresholds.
- [[Observability]] — The ability to understand a system's internal state from its external outputs — built on the three pillars: metrics, logs, and traces.
- [[Postmortem]] — A written analysis after an incident — timeline, impact, root causes, and corrective actions — ideally blameless, focused on systemic fixes rather than fault.
- [[Rollback]] — Reverting a deployment to the previous known-good version — the primary mitigation when a release goes bad, valued because it's fast and requires no diagnosis.
- [[SLA]] — The contractual promise about service levels — with defined measurement, exclusions, and consequences (typically service credits) when breached.
- [[SLI]] — The measured quantity reliability is judged by — e.g.
- [[SLO]] — A target value for a reliability metric (an SLI) over a window — e.g.
- [[SRE]] — Site Reliability Engineering — Google's formulation of operations as a software problem: engineers run production, automate away [[Toil]], and manage reliability quantitatively via SLOs and error budgets.
- [[Toil]] — In SRE, manual, repetitive, automatable operational work that scales linearly with service size and produces no lasting value.
- [[Twelve-factor App]] — A methodology of twelve principles for building cloud-native apps — config in the environment, stateless processes, explicit dependencies, logs as event streams, and so on.

---
← Back to [[_Home]]
