---
type: "map"
tags: [map, cloud]
---

# Cloud & Infrastructure

> Renting and orchestrating other people's computers — virtualization, containers, IaC, the service models.

## Terms in this branch (19)

- [[Cloud Computing]] — Renting computing as a metered utility: on-demand, self-service, elastic resources over the network, pooled across tenants.
- [[Cold Start]] — The first-invocation latency penalty in serverless platforms: before your function runs, the platform must allocate a sandbox, pull the runtime, and initialize your code.
- [[Container]] — A lightweight, isolated package bundling an application with its dependencies, sharing the host OS kernel (via namespaces and cgroups) rather than running its own.
- [[Distributed System]] — Multiple machines cooperating over a network to act as one system.
- [[Docker]] — The platform and tooling that popularised containers — building images from a Dockerfile, running them as containers, and sharing them via registries.
- [[FaaS]] — Cloud model where you deploy individual functions that run on demand, scaling to zero when idle — the core of 'serverless' (AWS Lambda, Cloud Functions).
- [[Hypervisor]] — The software layer that creates and runs virtual machines, mediating their access to physical hardware.
- [[IaaS]] — Cloud service model providing raw virtualised infrastructure — compute, storage, networking — that you manage above the hypervisor (EC2, raw VMs).
- [[Infrastructure as Code]] — Defining and provisioning infrastructure through machine-readable definition files rather than manual setup — infrastructure managed like source code.
- [[Kubernetes]] — An open-source container orchestration platform that automates deploying, scaling, healing, and networking containerised workloads across a cluster.
- [[PaaS]] — Cloud model providing a managed platform — runtime, OS, scaling, deploys — so you ship code without managing servers (Heroku, App Engine, Cloud Run).
- [[Pod]] — Kubernetes' smallest deployable unit — one or more tightly-coupled containers sharing network and storage, scheduled together on a node.
- [[SaaS]] — Cloud model delivering finished software over the web on subscription — the provider runs everything; you just use it (Gmail, Salesforce, Slack).
- [[Serverless]] — An execution model where the provider fully manages server allocation and scaling, including scaling to zero — you reason about code and events, not machines.
- [[Service Mesh]] — A dedicated infrastructure layer handling service-to-service communication — mTLS, retries, load balancing, observability — via sidecar proxies, transparently to the app.
- [[Terraform]] — A widely used Infrastructure-as-Code tool that provisions cloud resources declaratively from configuration, tracking real-world resources in a state file.
- [[Virtual Machine]] — A software emulation of a complete computer, running its own full OS atop a hypervisor, isolated from the host and other VMs.
- [[Virtualization]] — Abstracting physical hardware into multiple isolated virtual instances, so one machine runs many independent operating systems or environments.
- [[Warehouse-Scale Computer]] — The view of an entire datacenter as a single computer — the unit that is designed, provisioned and optimised as a whole — rather than as a pile of servers that merely share a building.

---
← Back to [[_Home]]
