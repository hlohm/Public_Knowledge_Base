---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
aliases: ["Runbook"]
tags: ["secops", "ir"]
status: "note"
---

# Playbook

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]
> **Also known as:** Runbook

Documented response procedure. **Runbook** is often used as a synonym. SOAR automates these.

**Context.** Codified muscle memory so response doesn't depend on who's awake: per-scenario steps (phishing, ransomware, compromised account) covering triage, containment, eradication, comms, and escalation. The maturity arc is manual playbook → SOAR-automated for the repetitive parts (enrich the alert, isolate the host, open the ticket) so humans spend judgment where it matters. A playbook nobody rehearses is a document, not a capability.

## See also

- [[SOAR]]
- [[Incident Response]]
