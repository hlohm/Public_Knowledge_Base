---
type: "reference"
tags: [reference, map]
---

# Concept Map

Visual overview of the major domains and key terms. The dotted lines are the connections worth memorizing: **identity bridges crypto and cloud; vulnerabilities live where threats meet apps; SecOps consumes outputs from almost every other domain.**

```mermaid
graph TD
    SEC[IT Security]

    SEC --> PRIN[Core Principles<br/>CIA · AAA · Zero Trust<br/>Defense in Depth · Least Privilege]
    SEC --> RISK[Risk and Governance<br/>Asset · Threat · Vulnerability<br/>GRC · Frameworks]
    SEC --> CRYPTO[Cryptography<br/>Symmetric · Asymmetric<br/>Hashing · PKI · TLS]
    SEC --> IAM[Identity and Access<br/>AuthN · AuthZ · MFA<br/>SSO · OAuth · SAML · OIDC]
    SEC --> NET[Network Security<br/>Firewall · IDS/IPS · VPN<br/>WAF · Segmentation · DMZ]
    SEC --> ENDPOINT[Endpoint and Host<br/>AV · EDR · XDR · EPP]
    SEC --> THREATS[Threats and Attacks<br/>Malware · Phishing · Injection<br/>MITM · DDoS · Ransomware · APT]
    SEC --> APPSEC[Application Security<br/>OWASP Top 10 · SAST/DAST<br/>SCA · SBOM · Secure SDLC]
    SEC --> VULN[Vulnerabilities<br/>CVE · CVSS · CWE<br/>Zero-day · Exploit · Patch]
    SEC --> CLOUD[Cloud and Modern<br/>SaaS/PaaS/IaaS · CSPM · CWPP<br/>CASB · CIEM · SASE · ZTNA]
    SEC --> SECOPS[SecOps and Response<br/>SOC · SIEM · SOAR · MDR<br/>IOC · IR · DFIR · ATT&CK]
    SEC --> OFFENSE[Offensive Security<br/>Pentest · Red/Blue/Purple<br/>Kill Chain · Bug Bounty]
    SEC --> COMPLY[Compliance and Standards<br/>ISO 27001 · NIST CSF · SOC 2<br/>PCI DSS · HIPAA · GDPR · CIS]

    CRYPTO -.- IAM
    IAM -.- CLOUD
    NET -.- CLOUD
    THREATS -.- VULN
    VULN -.- APPSEC
    APPSEC -.- SECOPS
    OFFENSE -.- SECOPS
    RISK -.- COMPLY
    ENDPOINT -.- SECOPS
```

> Mermaid renders natively in Obsidian. Switch to **Reading View** (Ctrl/Cmd-E) to see the diagram.

---
← Back to [[_Home]]
