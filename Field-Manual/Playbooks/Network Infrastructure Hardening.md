---
type: playbook
area: "Networking & Protocols"
tags: [hardening, security, networking, routing, bgp, firewall, dns, vpn, wireless, snmp, switch, vlan, rpki, copp]
status: working
---

# Network Infrastructure Hardening

> **Area:** [[Networking & Protocols]]

A decision-tree hardening reference for network infrastructure: routers, switches, firewalls, DNS servers, VPN gateways, wireless infrastructure, and out-of-band management. Platform-agnostic principles throughout; Cisco IOS/IOS-XE syntax as the primary reference; platform addenda cover JunOS, Arista EOS, VyOS/FRR, and pfSense/OPNsense.

> **The three-plane model** is the conceptual skeleton of every section here. Every network device has three distinct planes of operation — harden each independently:
>
> - **Management plane** — how operators access and configure the device (SSH, SNMP, web UI, console)
> - **Control plane** — how the device learns network topology (routing protocols, STP, ARP, DHCP)
> - **Data plane** — how traffic is forwarded through the device (ACLs, uRPF, NAT, rate limiting)
>
> A device that is hardened only at the data plane while leaving the management plane open is compromised the moment an attacker reaches the management address. Harden all three.

## Situation

- You are deploying new network infrastructure and need to harden it from factory defaults, **or**
- An existing device needs a posture review, or an audit has identified hardening gaps.

## Quick assessment

```
show version                           ! IOS: OS version, uptime, hardware model
show running-config | include service|ip http|line vty|snmp|telnet
                                       ! What management services are active?
show ip interface brief                ! Which interfaces are up, what addresses
show access-lists                      ! ACLs present — are there any? Do they apply?
show users                             ! Who is currently logged in?
```

```bash
# Linux-based devices (VyOS, OpenWrt, FRR)
uname -r && cat /etc/os-release
ss -tlnp                               # what management services are listening
ip route && ip -6 route                # routing table
```

Three diagnostic questions:
1. Is management access restricted to a dedicated management network, or reachable from any interface?
2. Are routing protocols authenticated?
3. Is there a default-deny inbound policy on untrusted interfaces?

---

## Threat model

| Tier | Adversary | Typical context |
|---|---|---|
| **TM0** | Automated scanners, default-credential attacks, opportunistic DDoS | Any internet-facing device |
| **TM1** | Targeted attacker with commodity tools; BGP/routing manipulation; NTLM relay on the network | Enterprise infrastructure, multi-homed routers |
| **TM2** | Motivated adversary with custom tools; protocol-level exploitation; persistent access to backbone | ISP infrastructure, carrier networks, critical services |
| **TM3** | State-level; hardware implants; firmware supply-chain; BGP hijacking at internet scale | Critical national infrastructure, IXPs, large ISPs |

---

## System profiles

| Code | Role |
|---|---|
| **S1** | Edge / border router (BGP peering, internet uplinks) |
| **S2** | Core / distribution router-switch (internal backbone) |
| **S3** | Perimeter firewall |
| **S4** | Internal / segmentation firewall |
| **S5** | Access layer switch |
| **S6** | DNS infrastructure (recursive resolver + authoritative) |
| **S7** | VPN gateway / remote access concentrator |
| **S8** | Wireless infrastructure (APs + controllers) |
| **S9** | Out-of-band management network |

---

## Decision branches

Sections: **A** Baseline · **B** Management Plane · **C** Control Plane · **D** Data Plane · **E** Firewall · **F** Layer 2 · **G** DNS · **H** VPN & Remote Access · **I** Wireless · **J** Logging & Monitoring · **K** Firmware & Config · **L** Advanced Controls · **M** Out-of-Band

| Profile | TM0 minimum | + TM1 | + TM2 | + TM3 |
|---|---|---|---|---|
| S1 edge router | A B C D J K | + L M | + L M | + L M |
| S2 core switch-router | A B C D F J K | + L M | + L M | + M |
| S3 perimeter firewall | A B E J K | + L M | + L M | + M |
| S4 internal firewall | A B E J K | + L | + L M | + M |
| S5 access switch | A B F J K | + L | + L M | + M |
| S6 DNS | A B G J K | + L | + L M | + M |
| S7 VPN gateway | A B H J K | + L | + L M | + M |
| S8 wireless | A B I J K | + L | + L M | — |
| S9 OOB management | A B J K M | + M | + M | + M |

---

## Fix A — Universal Baseline

Applies to **every** network device before any role-specific hardening.

**Disable all default credentials** — every network device ships with known factory credentials; they are the first thing automated scanners try:

```
username <admin-name> privilege 15 secret <strong-password>
no username admin       ! remove the default account by name
```

**Remove or disable every management protocol not explicitly needed:**

```
no service finger
no service tcp-small-servers
no service udp-small-servers
no service pad
no ip bootp server
no cdp run              ! or disable per-interface: interface Gi0/0 → no cdp enable
no lldp run             ! restrict to internal-only interfaces if needed for discovery
no ip http server       ! disable HTTP; HTTPS only if GUI is needed
no ip source-route      ! drop IP packets with source-routing options
```

**Disable directed broadcasts** — the smurf amplification vector; off by default in modern IOS but verify:

```
interface <all-interfaces>
  no ip directed-broadcast
```

**Login banner** — required in most compliance frameworks; also notifies port scanners that access is monitored:

```
banner login ^
AUTHORIZED ACCESS ONLY
Unauthorized access is prohibited and may be subject to prosecution.
All sessions are logged and monitored.
^
```

**NTP synchronisation** — audit logs, routing timestamps, and certificate validation all require accurate time; configure before anything else:

```
ntp authenticate
ntp authentication-key 1 md5 <ntp-key>
ntp trusted-key 1
ntp server <ntp-server-1> key 1
ntp server <ntp-server-2> key 1
service timestamps log datetime msec localtime show-timezone
service timestamps debug datetime msec localtime show-timezone
```

**Encrypted password storage** — never store passwords in type 7 (reversible Vigenère); use type 9 (scrypt) on IOS-XE 16.x+ or type 8 (PBKDF2):

```
service password-encryption        ! baseline; encrypts type 7 for all existing passwords
enable algorithm-type scrypt secret <privileged-password>    ! type 9 — prefer this
username <admin> algorithm-type scrypt secret <password>
```

---

## Fix B — Management Plane

**SSH v2 only — disable Telnet on all lines:**

```
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

line vty 0 15
  transport input ssh
  login local
  exec-timeout 10 0
  logging synchronous

line con 0
  exec-timeout 10 0
  logging synchronous

line aux 0
  no exec
  transport input none    ! disable the AUX port entirely on devices that expose it
```

**Restrict VTY access to the management network** — the management plane must never be reachable from the data plane or from untrusted sources:

```
ip access-list standard MGMT-SOURCES
  permit <mgmt-subnet>
  deny   any log

line vty 0 15
  access-class MGMT-SOURCES in
```

**Strong SSH ciphers and key exchange** (IOS-XE 16.x+):

```
ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr
ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512
ip ssh server algorithm kex ecdh-sha2-nistp256 ecdh-sha2-nistp384
ip ssh server algorithm hostkey ecdsa-sha2-nistp256 rsa-sha2-512
```

**SNMPv3 with authPriv — never SNMPv1 or v2c for any operational purpose:**

SNMPv1/v2c community strings are transmitted in plaintext; any packet capture on the path reveals them, and write access via a known community is direct configuration control.

```
no snmp-server community public  ro    ! remove all community strings
no snmp-server community private rw

snmp-server group  SNMPV3-RO  v3 priv
snmp-server user   SNMPV3-USER SNMPV3-RO v3 auth sha <auth-passphrase> priv aes 128 <priv-passphrase>

ip access-list standard SNMP-ACL
  permit <nms-host>
  deny   any log

snmp-server host <nms-host> version 3 priv SNMPV3-USER
snmp-server ifindex persist           ! stable interface indices across reboots
```

**TACACS+ / RADIUS for centralised AAA** — local accounts as fallback only; every admin action attributed to an individual identity:

```
aaa new-model
aaa authentication login default group tacacs+ local
aaa authorization exec default group tacacs+ local
aaa accounting exec default start-stop group tacacs+
aaa accounting commands 15 default start-stop group tacacs+

tacacs server <tacacs-server>
  address ipv4 <tacacs-server-ip>
  key <tacacs-key>
```

**Privilege levels** — never leave the default "level 15 or nothing" model; create read-only and operations levels:

```
username <noc-user>  privilege 5  secret <password>
privilege exec level 5 show running-config
privilege exec level 5 show ip route
! etc. — define exactly what level 5 can see and do
```

**Disable NETCONF/RESTCONF/gRPC if not used** (IOS-XE):

```
no netconf-yang
no restconf
```

If used, restrict to the management VRF and require TLS client certificates for gRPC.

---

## Fix C — Control Plane

**Control Plane Policing (CoPP)** — rate-limits traffic destined for the device's CPU; prevents resource exhaustion from a sustained DDoS against the management or control plane:

```
ip access-list extended COPP-ROUTING-PROTOCOLS
  permit ospf any any
  permit tcp any any eq 179          ! BGP
  permit udp any any eq 520          ! RIP

ip access-list extended COPP-MGMT
  permit tcp <mgmt-subnet> any eq 22
  permit udp <nms-host> any eq 161   ! SNMP

class-map match-any COPP-CRITICAL
  match access-group name COPP-ROUTING-PROTOCOLS
  match access-group name COPP-MGMT

class-map match-any COPP-NORMAL
  match protocol icmp

policy-map COPP-POLICY
  class COPP-CRITICAL
    police rate 2000000 bps conform-action transmit exceed-action drop
  class COPP-NORMAL
    police rate 512000 bps  conform-action transmit exceed-action drop
  class class-default
    police rate 128000 bps  conform-action transmit exceed-action drop

control-plane
  service-policy input COPP-POLICY
```

Verify: `show policy-map control-plane` shows rates and drop counters.

**BGP hardening:**

```
router bgp <ASN>
  ! MD5 session authentication (minimum); use TCP-AO where available
  neighbor <peer-ip> password <peer-password>

  ! GTSM (Generalized TTL Security Mechanism) — drops BGP packets with TTL < 254;
  ! prevents spoofed BGP from off-link addresses; eBGP only (iBGP uses ttl-security internally)
  neighbor <peer-ip> ttl-security hops 1

  ! Prefix limit — prevent a misbehaving peer from flooding your RIB
  neighbor <peer-ip> maximum-prefix 750000 80 warning-only
  ! Remove warning-only for hard enforcement; 80 = alert at 80% of the limit

  ! Soft reconfiguration for inbound filtering without resetting sessions
  neighbor <peer-ip> soft-reconfiguration inbound
```

**BGP route filtering** — never accept routes from a peer without an explicit policy:

```
! Block bogons and private ranges inbound from any external peer
ip prefix-list BOGON-FILTER deny  0.0.0.0/8 le 32
ip prefix-list BOGON-FILTER deny  10.0.0.0/8 le 32
ip prefix-list BOGON-FILTER deny  100.64.0.0/10 le 32
ip prefix-list BOGON-FILTER deny  127.0.0.0/8 le 32
ip prefix-list BOGON-FILTER deny  169.254.0.0/16 le 32
ip prefix-list BOGON-FILTER deny  172.16.0.0/12 le 32
ip prefix-list BOGON-FILTER deny  192.0.0.0/24 le 32
ip prefix-list BOGON-FILTER deny  192.168.0.0/16 le 32
ip prefix-list BOGON-FILTER deny  198.18.0.0/15 le 32
ip prefix-list BOGON-FILTER deny  198.51.100.0/24 le 32
ip prefix-list BOGON-FILTER deny  203.0.113.0/24 le 32
ip prefix-list BOGON-FILTER deny  224.0.0.0/3 le 32
ip prefix-list BOGON-FILTER permit 0.0.0.0/0 le 32   ! pass everything else to next filter

! Apply inbound to all eBGP peers
route-map EBGP-IN permit 10
  match ip address prefix-list BOGON-FILTER
router bgp <ASN>
  neighbor <peer-ip> route-map EBGP-IN in
```

**RPKI — Route Origin Validation** — cryptographically verifies that the ASN announcing a prefix is authorised to do so; the most effective BGP hijacking mitigation available:

```
! IOS-XE: configure an RPKI cache (validator)
router bgp <ASN>
  bgp rpki server tcp <rpki-validator-ip> port 3323 refresh 600

! Create a route-map that rejects RPKI-invalid routes
route-map RPKI-POLICY deny 10
  match rpki invalid         ! drop routes with an explicit invalid ROA
route-map RPKI-POLICY permit 20
  ! valid and not-found routes pass

router bgp <ASN>
  neighbor <peer-ip> route-map RPKI-POLICY in
```

Enroll your own prefixes in RPKI (create ROAs at your RIR) separately from this — validation only helps if route origins are published.

**OSPF / IS-IS / EIGRP authentication:**

```
! OSPF area authentication (MD5; SHA via keychain on IOS 15.4+)
router ospf 1
  area 0 authentication message-digest

interface GigabitEthernet0/0
  ip ospf authentication message-digest
  ip ospf message-digest-key 1 md5 <ospf-key>

! EIGRP (named mode with SHA-256 — the only mode that supports strong auth)
router eigrp NAMED-MODE
  address-family ipv4 unicast autonomous-system <AS>
    af-interface GigabitEthernet0/0
      authentication mode hmac-sha-256 <key>
```

**First-hop redundancy (HSRP/VRRP) authentication** — unauthenticated HSRP is a trivial takeover:

```
interface GigabitEthernet0/0
  standby 1 authentication md5 key-string <hsrp-key>
  ! VRRP equivalent:
  vrrp 1 authentication md5 keystring <vrrp-key>
```

---

## Fix D — Data Plane

**uRPF (Unicast Reverse Path Forwarding)** — drops packets whose source address is not reachable via the ingress interface; the primary mechanism for preventing IP spoofing at your network edge (BCP38 compliance):

```
interface GigabitEthernet0/0   ! internet-facing
  ip verify unicast source reachable-via rx    ! strict mode
  ! Use 'any' (loose mode) only if asymmetric routing prevents strict mode
```

Apply strict mode on all customer-facing and internet-facing interfaces. Loose mode on backbone links where traffic is asymmetric. Never omit it entirely on edge interfaces.

**Ingress / egress ACLs on untrusted interfaces:**

```
ip access-list extended UNTRUSTED-IN
  ! Anti-spoofing: reject packets claiming to be from your own address space
  deny   ip <your-prefix> any log
  ! Reject RFC 1918 and bogons from the internet
  deny   ip 10.0.0.0 0.255.255.255 any log
  deny   ip 172.16.0.0 0.15.255.255 any log
  deny   ip 192.168.0.0 0.0.255.255 any log
  deny   ip 127.0.0.0 0.255.255.255 any log
  ! Permit legitimate traffic
  permit ip any any

interface GigabitEthernet0/0   ! internet-facing
  ip access-group UNTRUSTED-IN in
```

**Rate limiting broadcast and ICMP** — prevent amplification and reflection attacks:

```
interface GigabitEthernet0/0
  rate-limit output access-group rate-limit-acl 8000000 1000000 1500000 conform-action transmit exceed-action drop
  no ip proxy-arp         ! avoid leaking ARP information across subnets
```

**Null-routing / RTBH (Remote Triggered Black Hole)** — for dropping attack traffic under a DDoS:

```
! Create a null route for the target prefix
ip route <victim-prefix> 255.255.255.255 Null0
! Distribute via BGP community to trigger black-hole at upstream peers
```

---

## Fix E — Firewall Hardening

**Zone-based design** — every interface belongs to a security zone; traffic between zones is denied by default and permitted only by explicit policy. The flat "all-in-one" network where all VLANs can reach all others is the design failure that enables ransomware propagation.

Canonical zone hierarchy (adapt to your architecture):

| Zone | Trust level | Typical contents |
|---|---|---|
| OUTSIDE | Untrusted | Internet, unknown peers |
| DMZ | Limited trust | Public-facing services |
| INSIDE | Trusted | Internal user workstations |
| SERVERS | Medium trust | Internal application servers |
| MANAGEMENT | High trust | Network management, jump servers |
| RESTRICTED | Highest trust | Domain controllers, PAM, secrets stores |

Traffic flows:
- OUTSIDE → DMZ: permitted for specific service ports only
- OUTSIDE → INSIDE/SERVERS/MANAGEMENT/RESTRICTED: deny
- INSIDE → OUTSIDE: permitted for HTTP/HTTPS/DNS/NTP outbound; log and inspect
- INSIDE → SERVERS: permitted for specific application ports; log
- INSIDE/SERVERS → MANAGEMENT: deny (management access from MANAGEMENT zone only)
- Any → RESTRICTED: deny except from SERVERS/MANAGEMENT with specific rules

**Zone-based firewall (Cisco IOS-XE):**

```
zone security OUTSIDE
zone security DMZ
zone security INSIDE

zone-pair security OUTSIDE-to-DMZ source OUTSIDE destination DMZ
  service-policy type inspect OUTSIDE-to-DMZ-POLICY

zone-pair security DMZ-to-INSIDE source DMZ destination INSIDE
  service-policy type inspect DMZ-to-INSIDE-POLICY

! Default deny is implicit — no zone-pair = no traffic
```

**Firewall rule hygiene:**

```
! Audit rules periodically — deny everything not explicitly permitted
show ip access-lists                        ! IOS
show policy-map type inspect zone-pair      ! ZBF

! Flag:
! - ANY/ANY permit rules
! - Rules with no hit count in months (may be dead/unreachable)
! - Permit rules that precede a more specific deny
! - Rules permitting management protocols from ANY source
```

**Stateful TCP inspection** — reject TCP packets that are not part of an established session:

```
ip access-list extended ANTI-SPOOF-TCP
  deny tcp any any established    ! allow established elsewhere; here only deny non-SYN floods
  permit tcp any any syn          ! permit SYN (new connections)

! Better: use the ZBF or stateful firewall inspect — it tracks state automatically
```

**Geo-IP and reputation filtering (TM1+)** — reduce noise; not a primary control since adversaries use legitimate infrastructure. Useful as a first filter for ports that have no legitimate foreign-source reason (e.g., management access from outside your country of operations).

**Change management for firewall rules** — every rule change must be:
- Requested with a business justification
- Reviewed (does this expose something it shouldn't?)
- Time-bounded if temporary
- Logged (who added it, when, commit ID)
- Reviewed for removal when the justification expires

A firewall with 2,000 undocumented rules is indistinguishable from no firewall.

---

## Fix F — Layer 2 Switch Security

**VLAN hygiene:**

```
! Native VLAN 1 is the default and well-known — move it to an unused VLAN
! Never carry Native VLAN traffic on trunk links without explicit tagging
vlan dot1q tag native                     ! tag native VLAN frames (IOS-XE)

! Prune VLANs on trunks to only those actually needed
interface GigabitEthernet0/1             ! trunk uplink
  switchport trunk allowed vlan 10,20,30  ! not 'all'

! Park all unused access ports in a dead VLAN and shut them down
interface range GigabitEthernet0/10-24
  switchport access vlan 999              ! dead VLAN — no IP, no routing
  shutdown
```

**Spanning Tree hardening:**

```
! PortFast: skip STP convergence on access ports (no risk of loops on host ports)
! BPDU Guard: shut the port immediately if a BPDU arrives — a BPDU on an access port
!   means either a rogue switch or miscabling
interface range GigabitEthernet0/2-9     ! access ports
  spanning-tree portfast
  spanning-tree bpduguard enable

! Root Guard: prevent any port from becoming the root bridge
!   Apply on uplinks from access layer toward distribution
interface GigabitEthernet0/1             ! uplink
  spanning-tree guard root

! Enable BPDU Guard globally as a default for PortFast ports
spanning-tree portfast bpduguard default

! Enable Loop Guard on non-designated ports to detect unidirectional link failures
spanning-tree loopguard default
```

**DHCP snooping + Dynamic ARP Inspection:**

DHCP snooping builds a binding table of {MAC, IP, VLAN, port}; DAI uses that table to validate ARP requests and replies — the combination prevents ARP spoofing and rogue DHCP servers.

```
ip dhcp snooping
ip dhcp snooping vlan 10,20,30
no ip dhcp snooping information option    ! disable Option 82 if not using DHCP relay

interface GigabitEthernet0/1             ! trusted uplink / DHCP server port
  ip dhcp snooping trust

interface range GigabitEthernet0/2-24    ! untrusted access ports
  ip dhcp snooping limit rate 15         ! 15 DHCP packets/second; drops on excess

ip arp inspection vlan 10,20,30

interface GigabitEthernet0/1
  ip arp inspection trust
```

**IP Source Guard:**

```
! Builds on DHCP snooping; drops packets from IPs not in the DHCP binding table
interface range GigabitEthernet0/2-24
  ip verify source
```

**802.1X port authentication** (TM1+) — every device must authenticate before gaining network access; no unauthenticated device can squat on an unused port:

```
aaa new-model
aaa authentication dot1x default group radius
aaa authorization network default group radius
dot1x system-auth-control

interface GigabitEthernet0/2
  switchport access vlan 10
  authentication port-control auto
  dot1x pae authenticator
  spanning-tree portfast               ! still needed for fast auth convergence
```

**Port security** (lighter alternative to 802.1X where it is not feasible):

```
interface GigabitEthernet0/2
  switchport port-security maximum 2
  switchport port-security violation restrict   ! or 'shutdown' for stricter enforcement
  switchport port-security
```

**Private VLANs** (TM2+) — within a VLAN, prevent host-to-host traffic; hosts can only reach the promiscuous port (gateway):

```
vlan 10
  private-vlan primary
vlan 110
  private-vlan isolated    ! isolated ports cannot communicate with each other

vlan 10
  private-vlan association 110

interface GigabitEthernet0/1   ! gateway
  switchport mode private-vlan promiscuous
  switchport private-vlan mapping 10 110

interface range GigabitEthernet0/2-24
  switchport mode private-vlan host
  switchport private-vlan host-association 10 110
```

---

## Fix G — DNS Hardening

**Separate recursive and authoritative functions** — a server that is both a recursive resolver and an authoritative nameserver for public zones is harder to harden; each role has different trust relationships and different attack exposure.

**Recursive resolver hardening (BIND):**

```
// named.conf
options {
    recursion yes;
    allow-recursion { 192.0.2.0/24; 2001:db8::/32; };    // only internal clients
    allow-query     { 192.0.2.0/24; 2001:db8::/32; };
    allow-transfer  { none; };                             // no zone transfers from a resolver

    dnssec-validation auto;   // validate DNSSEC; auto = built-in root key

    // Response Rate Limiting — prevents this resolver from being used as an amplifier
    rate-limit {
        responses-per-second 5;
        window 5;
    };

    // DNS over TLS (requires BIND 9.18+)
    listen-on-v6 port 853 tls <tls-config> { any; };
};
```

**Authoritative nameserver hardening (BIND):**

```
options {
    recursion no;                      // authoritative servers do not recurse
    allow-recursion { none; };
    allow-query { any; };              // public-facing: answer queries for your zones from anywhere
    allow-transfer { key "tsig-secondary-key"; };   // zone transfer only to secondaries with TSIG

    dnssec-enable yes;                 // sign your zones
};

// TSIG key for authenticated zone transfers
key "tsig-secondary-key" {
    algorithm hmac-sha512;
    secret "<base64-key>";
};

zone "example.com" {
    type primary;
    file "db.example.com.signed";      // DNSSEC-signed zone file
    allow-transfer { key "tsig-secondary-key"; };
    notify yes;
    also-notify { <secondary-ip> key "tsig-secondary-key"; };
};
```

**DNSSEC signing (authoritative):**

```bash
# Generate KSK and ZSK
dnssec-keygen -a ECDSAP256SHA256 -f KSK example.com    # Key Signing Key
dnssec-keygen -a ECDSAP256SHA256 example.com            # Zone Signing Key

# Sign the zone
dnssec-signzone -A -3 <salt> -N INCREMENT -o example.com -t db.example.com

# Publish DS records at the parent registrar — this is the step most often forgotten
```

**Response Policy Zones (RPZ)** — block queries for known-malicious domains at the resolver:

```
// named.conf
response-policy { zone "rpz.example.internal"; };

zone "rpz.example.internal" {
    type primary;
    file "rpz.db";
    allow-query { none; };   // internal only
};
```

Subscribe to a threat-intelligence RPZ feed (e.g., from your DNS vendor or a security provider) rather than maintaining one manually.

**DNS logging:**

```
logging {
    channel queries_log {
        file "/var/log/named/queries.log" versions 10 size 50m;
        print-time yes;
        print-category yes;
        severity dynamic;
    };
    category queries { queries_log; };
    category security { queries_log; };
};
```

**Hidden primary architecture** — the authoritative primary nameserver is not published in the NS records; only secondary nameservers are public-facing. The primary is reachable only from within the management network, reducing its attack surface significantly.

---

## Fix H — VPN & Remote Access

**IKEv2 only — never IKEv1** — IKEv1 has structural weaknesses (Aggressive Mode PSK is offline-crackable); IKEv2 is cleaner, faster, and more secure:

```
! Disable IKEv1 entirely
no crypto ikev1 enable

! IKEv2 proposal — strong algorithms only
crypto ikev2 proposal STRONG
  encryption aes-cbc-256 aes-cbc-192
  integrity  sha512 sha384 sha256
  group 20 19 14        ! ECP-384, ECP-256, MODP-2048 (DH group 14 is the minimum)

crypto ikev2 policy 10
  proposal STRONG
```

**Certificate-based authentication (TM1+) — no PSK for production VPNs:**

Pre-shared keys are a single point of compromise; a leaked PSK authorises all peers. Certificate-based auth scopes the compromise to one key pair:

```
crypto pki trustpoint <PKI-CA>
  enrollment url http://<ca-server>/certsrv/mscep/mscep.dll
  subject-name CN=<vpn-gateway-fqdn>
  revocation-check crl
  rsakeypair <vpn-key> 4096

! IKEv2 auth using PKI
crypto ikev2 profile VPN-PROFILE
  match identity remote fqdn domain <client-domain>
  authentication remote rsa-sig
  authentication local rsa-sig
  pki trustpoint <PKI-CA>
```

**IPSec transform set — strong ciphers only:**

```
crypto ipsec transform-set STRONG-TS esp-aes 256 esp-sha512-hmac
  mode tunnel

! Enable Perfect Forward Secrecy
crypto map VPN-MAP 10 ipsec-isakmp
  set pfs group20    ! ECP-384
  set transform-set STRONG-TS
```

**Split tunneling policy** — full-tunnel (all traffic through VPN) is more secure for corporate laptops accessing sensitive resources; split-tunnel reduces load but exposes the client to threats from the local network while connected:

```
! Full-tunnel: route 0.0.0.0/0 through the VPN — client has no direct internet
! Split-tunnel: only route corporate subnets through the VPN — less secure, more practical

! If split-tunnel is unavoidable: force DNS through the VPN to prevent DNS leakage
! and enable client compliance checking (is the endpoint patched?)
```

**SSL/TLS VPN (OpenVPN / WireGuard / SSTP):**

```
# WireGuard — modern, audited, minimal code surface
# Server configuration: /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = nft add rule inet filter input udp dport 51820 accept

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.0.0.2/32     # full-tunnel: use 0.0.0.0/0, ::/0
```

WireGuard: uses Curve25519 + ChaCha20-Poly1305 + BLAKE2s + SipHash24; no negotiation of weak algorithms is possible by design.

**MFA for remote access** — certificate auth proves device identity; MFA proves user identity; both are needed:

Integrate RADIUS / TACACS+ with your IdP (SAML, OIDC) to enforce MFA at the VPN authentication step. RADIUS-based TOTP (e.g., via FreeRADIUS + Google Authenticator PAM) is a common pattern for non-cloud deployments.

---

## Fix I — Wireless Security

**WPA3-Enterprise for corporate networks** — 802.1X/EAP with certificate-based client authentication; the baseline for any network carrying sensitive traffic:

```
! Cisco WLC (CLI)
wlan CORP 1 CORP
  security wpa
  security wpa akm dot1x
  security wpa wpa3
  no security wpa wpa2 ciphers tkip enable
  no security wpa wpa2 akm psk enable
  no shutdown
```

**WPA2-Enterprise (802.1X/EAP-TLS) minimum** — if WPA3 is not supported; never WPA2-Personal (PSK) for corporate use. A shared WPA2-PSK means every device that has ever connected knows the credential, and rotation requires reconfiguring every client.

**SSID segmentation** — separate SSIDs for different trust levels; each on its own VLAN with appropriate firewall policy:

| SSID | Auth | VLAN | Firewall |
|---|---|---|---|
| CORP | 802.1X/EAP | Corp VLAN | Full access per policy |
| GUEST | Captive portal | Guest VLAN | Internet only; isolated from corporate |
| IOT | WPA2-PSK (dedicated) | IoT VLAN | Restrict to specific external destinations |

**Client isolation** on guest and IoT SSIDs — prevents client-to-client communication within the wireless segment:

```
! Cisco WLC
wlan GUEST 2 GUEST
  peer-blocking drop      ! or forward-uplink depending on architecture
```

**Management interface security:**

```
! Wireless controller / AP management — same principles as Fix B
! SSH only, no HTTP, restrict to management VLAN/IP range
! SNMPv3 only
! Change default AP join credentials before deployment
```

**Rogue AP detection** — enable on the WLAN controller; alert on any BSS not in your authorised AP list:

```
! Cisco WLC: Wireless → Rogue AP → Rogue Rules → Auto-classify and alert
! The controller uses neighbouring APs as sensors; coverage determines detection latency
```

**802.11 Management Frame Protection (MFP / 802.11w)** — authenticates management frames (deauth, disassoc) to prevent deauthentication attacks used to force client reconnects for PSK capture:

```
! Cisco WLC
wlan CORP 1 CORP
  security mfp client require     ! require MFP on clients; exclude older devices that lack it
```

---

## Fix J — Logging, Monitoring & NTP

**Syslog to remote server — all management plane events, minimum:**

```
logging trap informational
logging host <syslog-server> transport udp port 514    ! use TCP + TLS for TM1+
logging source-interface Loopback0    ! stable, interface-independent source address
no logging console                    ! avoid console flooding under attack
service timestamps log datetime msec localtime show-timezone
```

**Log what matters on network devices:**

| Category | What to capture |
|---|---|
| Management access | SSH login success/failure, privilege escalation, `enable` use |
| Configuration changes | `config t` entry/exit, every command that changes state |
| Routing events | BGP peer up/down, OSPF adjacency changes, route flap |
| Interface events | Link up/down, error counters exceeding threshold |
| ACL hits | `log` on deny rules; log selectively on permit rules for high-value paths |
| CoPP drops | Anything dropped by the control plane policy is an attack signal |

```
! Log all AAA events
aaa accounting exec default start-stop group tacacs+ local
aaa accounting commands 15 default start-stop group tacacs+
! Log configuration changes
archive
  log config
    logging enable
    logging size 1000
    notify syslog contenttype plaintext
    hidekeys      ! do not log passwords in the config archive
```

**NetFlow / IPFIX** — exports per-flow metadata (src/dst IP, port, protocol, bytes, packets) to a collector; enables traffic analysis, anomaly detection, and post-incident forensics without capturing full packet contents:

```
ip flow-export destination <netflow-collector> 9995
ip flow-export version 9
ip flow-export source Loopback0

interface GigabitEthernet0/0
  ip flow ingress
  ip flow egress
```

**SNMP traps for operational events:**

```
snmp-server enable traps bgp
snmp-server enable traps ospf
snmp-server enable traps syslog
snmp-server enable traps cpu threshold
snmp-server enable traps memory bufferpeak
snmp-server host <nms-host> version 3 priv SNMPV3-USER
```

**NTP authentication** (repeat from Fix A for emphasis — misconfigured time breaks log correlation):

```
ntp authenticate
ntp authentication-key 1 md5 <key>
ntp trusted-key 1
ntp server <ntp-server> key 1
ntp access-group peer   10    ! allow only known time peers
ntp access-group serve  11    ! allow only management subnet to query this device's time
```

**Alerting thresholds to monitor:**

- BGP peer down (immediate)
- Interface error rate > 0.1% (sustained)
- CPU > 80% for > 5 minutes
- CoPP drop counter increasing (rate of attack)
- RPKI invalid route received and rejected
- Failed authentication attempts (threshold)
- Configuration change outside maintenance window

---

## Fix K — Firmware & Configuration Management

**Firmware update policy:**

- Subscribe to the vendor's security advisory feed (Cisco PSIRT, Juniper SIRT, etc.)
- Treat critical/high severity advisories as requiring a patch within 72 hours on internet-facing devices; 30 days on internal devices.
- Verify firmware integrity before loading:
  ```
  verify /sha512 flash:<firmware-image>    ! compare against vendor-published hash
  ```
- Test in a lab or on a non-production device before fleet rollout.

**Configuration backup — automated, encrypted, version-controlled:**

```
! IOS: archive to a TFTP/SCP server on every change
archive
  path scp://<user>@<backup-server>/<device-name>-$h-$t
  write-memory      ! save running-config to startup automatically on copy
  maximum 10
  time-period 1440  ! or: triggered by change via EEM (preferred)
```

```bash
# Linux-based: use Oxidized, Rancid, or Netmiko scripts in a CI/CD pipeline
# Store encrypted in a git repository; every commit is a timestamped configuration snapshot
# Review diffs on every change — unexpected configuration drift is a breach indicator
```

**Rollback capability** — a failed firmware upgrade or misconfigured ACL must be recoverable without physical access:

```
! IOS: configure-replace with reload (timer-based automatic rollback)
configure replace flash:known-good-config force revert trigger error
! If the replaced config breaks SSH, the timer triggers a rollback after <N> minutes
```

**Secure image transfer** — never TFTP (plaintext); use SCP or HTTPS:

```
ip scp server enable
! Verify: copy scp://<server>/<image> flash:
```

---

## Fix L — Advanced Controls (TM2+)

**MACsec (802.1AE)** — Layer 2 encryption for point-to-point links between switches and between routers; prevents passive interception on transit links even when the physical media is shared:

```
! MKA (MACsec Key Agreement) with pre-shared key
key chain MACSEC-CHAIN macsec
  key 01
    cryptographic-algorithm aes-256-cmac
    key-string <hex-key>
    lifetime local <start-time> <end-time>

interface GigabitEthernet0/0
  mka policy MACSEC-POLICY
  macsec replay-protection window-size 64
```

**BFD with authentication** (Bidirectional Forwarding Detection) — fast failure detection; without authentication, a spoofed BFD packet can bring down a routing session:

```
bfd-template multi-hop SECURE-BFD
  interval min-tx 300 min-rx 300 multiplier 3
  authentication sha-1 keychain <bfd-keychain>
```

**IPSec on routed infrastructure links (TM2+)** — encrypts traffic between routers on backbone links; relevant when backbone links traverse untrusted physical infrastructure:

```
! Get/Set-Go tunnel with GRE + IPSec (or FlexVPN)
interface Tunnel0
  tunnel source GigabitEthernet0/0
  tunnel destination <peer-ip>
  tunnel protection ipsec profile BACKBONE-IPSEC
```

**BGP communities for DDoS mitigation coordination** — pre-negotiate blackhole and traffic engineering communities with upstreams before you are under attack; triggering a blackhole in 30 seconds during an incident vs in 30 minutes makes the difference:

```
! Tag routes to signal upstream black-hole action
! Community values are provider-specific; agree on them in advance and document
route-map UPSTREAM-BLACKHOLE permit 10
  set community <upstream-blackhole-community> additive
```

**MANRS (Mutually Agreed Norms for Routing Security)** — the four actions:
1. **Filter** — prevent propagation of incorrect routing information (bgp prefix lists, RPKI)
2. **Anti-spoofing** — prevent traffic with spoofed source addresses (uRPF, BCP38)
3. **Coordination** — maintain accurate contact and routing data (IRR, PeeringDB)
4. **Validation** — validate routing information against IRR and RPKI before accepting

MANRS membership (manrs.org) is a public signal that your network is operated responsibly; increasingly required by peering partners and IXPs.

**Network microsegmentation (TM2+)** — beyond VLANs, enforce granular access control between workloads using VXLAN + SDN policies, private VLANs (Fix F), or host-based firewalls (see [[Unix OS Hardening]] and [[Windows OS Hardening]]). The network cannot be the only enforcement point.

---

## Fix M — Out-of-Band Management

**Dedicated OOB network** — management traffic never shares the production data plane. If the production network is under attack or misconfigured, you must still be able to reach devices to diagnose and fix them:

```
! Dedicate a VRF for management traffic on capable platforms
vrf definition MGMT
  address-family ipv4

interface GigabitEthernet0/1   ! dedicated management interface
  vrf forwarding MGMT
  ip address <mgmt-ip> <mgmt-mask>

ip ssh vrf MGMT                ! SSH listens only on the MGMT VRF
```

**Console server** — provides console (out-of-band) access to devices; must itself be hardened:

- SSH-only access, key-based authentication, no shared credentials
- Cellular or DSL backup uplink (independent of the network being managed)
- Physical access logs / locked cabinet
- Syslog from the console server is especially valuable — console messages during a crash contain information that the network syslog never receives

**Physical security of management devices:**

- Console servers in locked cabinets; same physical access control as the network devices they manage
- OOB network physically separate from production cabling where possible
- OOB access credentials in a separate vault from production credentials; a compromised production credential must not yield OOB access

---

## Platform Addenda

### Juniper JunOS

Management plane:

```
# SSH only; disable telnet
delete system services telnet
set system services ssh root-login deny
set system services ssh protocol-version v2
set system login idle-timeout 10

# SNMPv3
set snmp v3 usm local-engine user SNMPV3-USER authentication-sha authentication-password <auth-pw>
set snmp v3 usm local-engine user SNMPV3-USER privacy-aes128 privacy-password <priv-pw>
set snmp v3 vacm security-to-group security-model usm security-name SNMPV3-USER group RO-GROUP

# Login banner
set system login message "AUTHORIZED ACCESS ONLY\nAll sessions are logged."

# Restrict management to management VRF
set system management-instance
set interfaces fxp0 unit 0 family inet address <mgmt-ip>/24
```

Control plane (JunOS routing policy):

```
# BGP prefix filtering
policy-options {
    prefix-list BOGONS {
        10.0.0.0/8;
        172.16.0.0/12;
        192.168.0.0/16;
    }
    policy-statement EBGP-IN {
        term block-bogons {
            from { prefix-list BOGONS; }
            then reject;
        }
        term accept-rest {
            then accept;
        }
    }
}
protocols bgp group UPSTREAM {
    import EBGP-IN;
    authentication-key <md5-key>;
    ttl 1;     # GTSM equivalent
}
```

Data plane (JunOS firewall filter):

```
firewall {
    filter PROTECT-RE {
        term allow-bgp {
            from { protocol tcp; destination-port 179; source-address { <peer-ip>/32; } }
            then accept;
        }
        term allow-mgmt {
            from { protocol tcp; destination-port 22; source-address { <mgmt-subnet>/24; } }
            then accept;
        }
        term default-deny {
            then { discard; log; syslog; }
        }
    }
}
interfaces lo0 {
    unit 0 {
        family inet { filter { input PROTECT-RE; } }
    }
}
```

### Arista EOS

EOS CLI syntax is close to Cisco IOS; key differences:

```
! Management plane — EOS uses a dedicated management VRF by default
interface Management1
   vrf MGMT
   ip address <mgmt-ip>/24

! Restrict SSH to management VRF
management ssh
   vrf MGMT
      enable

! Disable eAPI HTTP; HTTPS only
management api http-commands
   no protocol http
   protocol https
   no shutdown

! SNMPv3
snmp-server group SNMPV3-RO v3 priv
snmp-server user SNMPV3-USER SNMPV3-RO v3 auth sha <auth-pw> priv aes <priv-pw>
```

Arista EOS supports GNMI/OpenConfig natively; restrict it to the management VRF and require TLS client certificates.

### VyOS / Linux with FRR

```bash
# SSH — VyOS
set service ssh port 22
delete service telnet
set service ssh listen-address <mgmt-ip>

# FRR (routing daemon — vtysh interface, Cisco-like config)
# BGP authentication
router bgp <ASN>
  neighbor <peer-ip> password <password>
  neighbor <peer-ip> ttl-security hops 1

# OSPF authentication
router ospf
  area 0 authentication message-digest
interface eth0
  ip ospf authentication message-digest
  ip ospf message-digest-key 1 md5 <key>

# Firewall — nftables (see [[Unix OS Hardening]] Fix F for full template)
# Apply the same CoPP concept via nftables rate limiting on the loopback:
nft add rule inet filter input limit rate 100/second accept
nft add rule inet filter input drop

# uRPF on Linux
# Enable reverse path filtering per interface
echo 1 > /proc/sys/net/ipv4/conf/eth0/rp_filter
# Or via sysctl (permanent — add to /etc/sysctl.d/99-hardening.conf)
net.ipv4.conf.eth0.rp_filter = 1
```

### pfSense / OPNsense

- **No SSH from WAN by default** — confirm under System → Advanced → Admin Access → Secure Shell; restrict source to management subnet.
- **Disable the web GUI on WAN interface** — the admin web UI must not be reachable from untrusted interfaces.
- **Suricata / Zenarmor IDS** — install via package manager; apply to WAN interface in inline IPS mode for TM1+.
- **Unbound DNS with DNSSEC validation** — enable under Services → DNS Resolver → DNSSEC; add RPZ feeds if needed.
- **OpenVPN hardening** — TLS 1.3 only, ECDH P-384, AES-256-GCM, SHA-512 HMAC; require client certificates.
- **Configuration backup** — Diagnostics → Backup/Restore; automate via `scp` or the config sync feature; store encrypted.
- **Firewall rules:** pfSense/OPNsense uses a stateful PF back end; rules are evaluated top-to-bottom per interface; default is deny at the bottom. Audit rules in Firewall → Rules; remove `any/any` permits, flag rules without hit counts.

---

## Role Addenda

### Edge router / BGP peer

- Fix B (restrict management to OOB VRF or separate interface) + Fix C (BGP auth, GTSM, RPKI, bogon filters, prefix limits) + Fix D (uRPF strict on customer interfaces) are the non-negotiable core.
- **Announce only what you own** — filter outbound BGP to only your registered prefixes. A misconfigured eBGP full-table re-announcement is one of the most common causes of major internet routing incidents.
- **IRR registration** — register your prefixes and routing policy in an Internet Routing Registry (RADB, RIPE DB, ARIN IRR); required for filtering at most IXPs and many peers.
- **DDoS scrubbing path** — have a pre-arranged path to a scrubbing provider (or a Remotely Triggered Black Hole community with your upstream) before you are under attack.

### Firewall / perimeter / DMZ

- The zone model (Fix E) is the primary design artifact — get the zone hierarchy right before writing a single rule.
- **East-west traffic between DMZ services must also be firewalled** — a compromised DMZ web server should not be able to reach the DMZ database server on all ports.
- **Firewall rule review cadence** — every rule must be reviewed at minimum annually; critical rules (internet-to-DMZ permits) every quarter.
- **Egress filtering is not optional** — an internet-facing server with unrestricted outbound is half a firewall. Ransomware, C2, and exfiltration all need outbound connectivity.

### DNS infrastructure

- Deploy at minimum two geographically separated authoritative nameservers (NS records require at least two; best practice is four).
- **Anycasting authoritative nameservers** — use BGP anycast to announce the same IP from multiple PoPs; improves latency and resilience against volumetric DDoS targeting a single nameserver.
- **DNSSEC end-to-end** — signing your zone is only half; ensure your registrar has published the DS record at the parent zone. Verify with `dig DS example.com @a.gtld-servers.net`.
- **Monitor TTLs and NSEC walking** — very low TTLs amplify resolver load under attack; NSEC walking leaks your full zone unless you use NSEC3 with a hash iteration count.

### IXP / peering environment

- **Route server security** — all routes imported by the route server must be filtered via IRR and RPKI before being distributed to members; an IXP route server that forwards unfiltered routes amplifies the impact of any member's misconfiguration.
- **Route object validation** — reject BGP announcements at the IXP that do not have a corresponding IRR route object with matching origin AS.
- **RPKI mandatory** — consider requiring RPKI-valid-or-unknown routes only at the IXP; reject RPKI-invalid.
- **Peering LAN ACLs** — restrict traffic on the peering LAN to BGP (TCP/179) and ICMP between legitimate peer IPs only; a peering LAN with unrestricted access is a pivot point.

---

## Validation

```
! Management plane
show ip ssh                              ! SSH v2 only; cipher list
show snmp user                           ! SNMPv3 users; no community strings
show line vty 0 15                       ! transport input ssh only; access-class applied
show run | include snmp-server community ! must return nothing
show run | include ip http server        ! must return nothing (or 'no ip http server')

! Control plane
show bgp neighbors <peer-ip>             ! auth: yes; ttl-security; prefix count within limit
show ip bgp rpki table                   ! RPKI cache populated and reachable
show policy-map control-plane            ! CoPP drops — baseline and monitor for spikes
show ip ospf interface brief             ! authentication type: message digest

! Data plane
show ip interface brief                  ! confirm uRPF enabled on internet-facing interfaces
show ip interface GigabitEthernet0/0 | include verify  ! 'IP verify source...' active
show ip access-lists                     ! bogon + anti-spoof ACLs applied to right interfaces

! Layer 2 (switches)
show ip dhcp snooping                    ! DHCP snooping active; trusted ports correct
show ip arp inspection interfaces        ! DAI active on correct VLANs
show spanning-tree detail | include BPDUGuard   ! BPDU Guard active on access ports

! DNS
dig +dnssec example.com @<resolver>     ! AD flag = 1 (authenticated data — DNSSEC valid)
dig +short DS example.com @a.gtld-servers.net   ! DS record published at parent

! VPN
show crypto ikev2 sa                     ! active SA; cipher suite as configured
show crypto ipsec sa                     ! confirm PFS group, enc/auth alg

! Routing security
show bgp summary                         ! all peers established; prefix counts reasonable
show ip bgp regexp _<your-ASN>_          ! confirm you are not leaking third-party routes
```

---

## Escalation / After-action

**Baseline immediately after hardening:**
- Export the full running configuration; hash it and store it alongside the config in version control.
- Capture a `show policy-map control-plane` and `show ip access-lists` baseline; CoPP drop deltas from this baseline are the primary alert signal for control-plane attacks.

**Document the configuration decisions made** — why a particular ACL permits or denies a specific range, why a BGP prefix limit was set to a given value, which routing protocols are authenticated and why. Network devices accumulate undocumented rules faster than any other system type.

**Maintenance rhythm:**

| Frequency | Action |
|---|---|
| Daily | Check BGP peer state, RPKI cache reachability, syslog stream |
| Weekly | Review CoPP drop counters for trends; check for new routing anomalies |
| Monthly | Verify no new SNMP community strings; audit VTY access lists; review firewall rule hit counts |
| Quarterly | Firmware advisory review; check for new CVEs against deployed versions; re-validate RPKI ROA coverage |
| Annually | Full firewall rule review (justify each rule or remove it); routing policy audit; IRR object audit |
| After any incident | Review config diff against last-known-good backup; check for unexpected changes; update RPKI if prefixes changed |

**If a routing anomaly is detected (unexpected BGP advertisement, prefix hijack):**
1. Check RPKI: is the offending prefix/origin covered by an invalid ROA?
2. If your own prefix is hijacked: contact your upstream(s); trigger RTBH if available; file with RIPE/ARIN NOC if needed.
3. Check if your own router is re-advertising routes it should not — route leaks are often accidental.

## See also

- [[Unix OS Hardening]] — hardening the OS on a Linux-based network appliance or embedded device
- [[Windows OS Hardening]] — hardening Windows-based network management systems
- [[iptables]] · [[nc]] · [[ssh]] — referenced tools for testing and verification
- MANRS (manrs.org) · RPKI validators (Cloudflare RPKI, RIPE Validator, Routinator) · IRR (radb.net, ripe.net)
