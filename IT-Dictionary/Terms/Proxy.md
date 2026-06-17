---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network"]
status: "note"
---

# Proxy

> **Domain:** [[05 - Network Security|Network Security]]

Intermediary between client and server. **Forward proxy** sits in front of clients (outbound); **reverse proxy** sits in front of servers (inbound).

**Context.** Both directions matter to security: the forward proxy is where egress policy, URL filtering, and malware scanning live; the reverse proxy is where TLS terminates, WAFs hook in, and backend topology hides. Debugging habit: when something "can't reach the internet" in an enterprise, ask about the proxy and its PAC file before blaming DNS.

## See also

- [[SWG]]
- [[WAF]]
- [[Bastion Host]]
