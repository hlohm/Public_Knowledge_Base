---
type: "reference"
tags: [reference]
---

# Often Confused Pairs

The false friends of the infosec language — words close enough to swap, distinct enough to matter.

| Pair | The distinction |
|---|---|
| [[Authentication]] vs [[Authorization]] | AuthN = "who are you?" — AuthZ = "what can you do?" Order matters: AuthN first, then AuthZ. |
| [[Threat]] vs [[Vulnerability]] vs [[Risk]] | Threat = burglar; vulnerability = unlocked door; risk = likelihood × impact of that burglar using that door. |
| [[OAuth 2.0]] vs [[OIDC]] | OAuth = authorization (delegated access). OIDC = authentication, *built on top of* OAuth. Using OAuth alone for login is a classic mistake. |
| [[SAML]] vs [[OIDC]] | Both do federated SSO. SAML = older, XML, enterprise-heavy. OIDC = newer, JSON/JWT, mobile- and API-friendly. |
| [[Symmetric Encryption]] vs [[Asymmetric Encryption]] | Symmetric = same key both ways, fast. Asymmetric = key pair, slow, solves key distribution. Real systems use asymmetric to exchange a symmetric session key. |
| [[Hash Function]] vs [[HMAC]] vs [[Digital Signature]] | Hash = integrity only. HMAC = integrity + authenticity (shared secret). Digital signature = integrity + authenticity + non-repudiation (private key). |
| Encryption vs Encoding vs [[Hash Function\|Hashing]] | Encryption is reversible *with a key*. Encoding (Base64) is reversible *without one* — not security. Hashing is one-way. |
| [[CVE]] vs [[CWE]] | CVE = specific instance ("the Apache log4j RCE"). CWE = the weakness category ("improper input validation"). |
| [[IDS and IPS\|IDS]] vs [[IDS and IPS\|IPS]] | IDS detects and alerts. IPS detects and blocks. The "P" costs availability if it gets it wrong. |
| [[EPP]] vs [[EDR]] vs [[XDR]] vs [[MDR]] | EPP = prevention (modern AV). EDR = endpoint detection + response. XDR = cross-domain correlation. MDR = any of the above + humans, as a service. |
| [[SOC 2]] vs [[SOC 1 and SOC 3\|SOC 1]] | SOC 1 = controls relevant to *financial reporting*. SOC 2 = controls relevant to *security/availability/etc.* SOC 3 = the public-friendly summary of SOC 2. |
| SOC 2 Type I vs Type II | Type I = design at a point in time. Type II = effectiveness *over a period* (typically 6–12 months). |
| [[IOC]] vs [[IOA]] | IOC = forensic artifact ("we saw this hash"). IOA = behavior pattern ("we saw process injection"). IOAs are harder to change; you want both. |
| [[Red Team]] vs [[Blue Team]] vs [[Purple Team]] | Red = attack. Blue = defend. Purple = collaborate to improve detection. |
| [[Penetration Test\|Pentest]] vs [[Red Team]] | Pentest = broad coverage, find-as-many-vulns-as-possible, time-boxed. Red team = stealthy, goal-oriented, measures *defenders* as much as attackers. |
| [[Risk Appetite]] vs Risk Tolerance | Appetite = how much risk you *want* to take to pursue objectives. Tolerance = the boundary you won't cross. |
| Policy vs Standard vs Procedure | Policy = high-level direction. Standard = specific requirement. Procedure = step-by-step how. |
| DoS vs [[DDoS]] | Same goal, the second is **distributed** across many sources. |
| Reflected vs Stored [[XSS]] | Reflected = script in the request, echoed back. Stored = script saved server-side, served to other users. Stored is usually worse. |
| [[CSRF]] vs [[SSRF]] vs [[XSS]] | CSRF = attacker uses your browser. SSRF = attacker uses your server. XSS = attacker injects script that runs in another user's browser. |
| [[Reverse Shell\|Bind Shell]] vs [[Reverse Shell]] | Bind = target listens, attacker connects (firewall-hostile). Reverse = target connects out to attacker (firewall-friendly — usually preferred). |
| [[Inherent Risk]] vs [[Residual Risk]] | Inherent = before any controls. Residual = what's left after controls. You manage *residual*. |
| Mitigate vs Transfer vs Accept vs Avoid | The four [[Risk Treatment|risk treatments]]. Don't conflate "transfer" (e.g. cyber insurance) with "mitigate". |
| [[Vulnerability Scanner]] vs [[Penetration Test]] | Scan = automated, finds *known* vulns. Pentest = human, attempts exploitation, finds *unknown* combinations. |
| [[Coordinated Disclosure]] vs [[Full Disclosure]] | Coordinated = vendor-aligned timeline. Full = published unilaterally. |
| Black/Gray/White Box | Refers to how much the tester knows: nothing / some / everything. |
| [[Zero Day]] vs [[N-Day]] | 0-day = vendor doesn't know. N-day = patched but unapplied. Most real attacks are N-day. |

---
← Back to [[_Home]]
