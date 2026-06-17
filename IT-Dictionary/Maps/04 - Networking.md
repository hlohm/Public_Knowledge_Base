---
type: "map"
tags: [map, net]
---

# Networking

> Moving bytes between machines reliably and in order — the stack from cables to sockets.

## Terms in this branch (28)

- [[A Record]] — The DNS record mapping a name to an IP address — A for IPv4, AAAA for IPv6.
- [[ARP]] — How a host on a LAN learns which MAC address owns an IP: broadcast 'who has 192.168.1.1?', cache the answer.
- [[Authoritative DNS Server]] — A nameserver that holds the actual records for a zone and answers for it as the source of truth, rather than by asking anyone else.
- [[Bandwidth]] — The maximum rate a link can carry data, e.g.
- [[CIDR]] — Address blocks of any power-of-two size written as prefix length: 10.0.0.0/8, 192.168.1.0/24.
- [[CNAME]] — A record that aliases one name to another _name_ (its canonical name); the resolver then continues resolving the target.
- [[Collective Communication]] — Communication patterns that involve a whole group of processes at once — broadcast, scatter, gather, reduce, all-reduce — as opposed to point-to-point messages.
- [[DHCP]] — Hands a joining host its IP address, mask, gateway, and DNS servers automatically, as a time-limited lease.
- [[DNS]] — The distributed, hierarchical directory translating human names (example.com) into IP addresses and other records.
- [[DNS Forwarding]] — Configuring a resolver to hand queries (all of them, or just for certain domains) to a specified upstream resolver instead of recursing from the root itself.
- [[DNS Zone]] — A contiguous portion of the DNS namespace administered as a unit — one SOA Record, a set of records, and a single authority.
- [[Dynamic DNS]] — Keeping a DNS record automatically updated as a host's IP changes — typically a client that pushes its current address to the DNS provider on a schedule or on change.
- [[Ethernet]] — The dominant wired LAN technology (IEEE 802.3): frames addressed by MAC, carried today over twisted pair or fiber at 1/10/25/100+ Gb/s.
- [[FQDN]] — A fully qualified domain name: a name complete to the root, unambiguous on its own — conventionally written with a trailing dot, `host.example.com.`.
- [[Glue Record]] — An A/AAAA record for a nameserver, served by the _parent_ zone, to resolve a circular dependency where the nameserver's name lives inside the zone it serves.
- [[ICMP]] — IP's control channel: echo request/reply (ping), destination unreachable, TTL exceeded (traceroute), fragmentation needed.
- [[IP]] — The network-layer protocol that addresses and routes packets across interconnected networks, best-effort and connectionless.
- [[IPv4]] — The 32-bit version of IP that built the internet: ~4.3 billion addresses in dotted-quad notation (203.0.113.7), long since exhausted and kept usable by NAT and private ranges (RFC 1918: 10/8, 172.16/12, 192.168/16).
- [[IPv6]] — The 128-bit successor to IPv4: colon-hex notation (2001:db8::1), address space vast enough that every device gets a globally unique address, killing the need for NAT.
- [[Latency]] — The time for one unit of data to travel from source to destination — a delay, measured in milliseconds.
- [[Load Balancer]] — A device/service distributing incoming traffic across multiple backend servers for capacity and availability.
- [[MAC Address]] — The 48-bit link-layer address burned into (or assigned to) a network interface, written as six hex pairs (a4:5e:60:…).
- [[MX Record]] — The DNS record naming the mail servers that accept email for a domain, each with a preference number (lower = tried first).
- [[NAT]] — Rewriting IP addresses/ports at a boundary so many private hosts share one public address.
- [[NS Record]] — The record naming the authoritative nameservers for a zone.
- [[NXDOMAIN]] — The DNS response code meaning _this name does not exist_ (no records of any type, and no such name).
- [[OSI Model]] — A 7-layer reference model (Physical, Data Link, Network, Transport, Session, Presentation, Application) for reasoning about network functions.
- [[Packet]] — The unit of data at the network layer: a header (addresses, TTL, protocol) plus payload.
- [[Port]] — A 16-bit number (0–65535) that identifies a specific service endpoint on a host, so one IP address can host many conversations.
- [[PTR Record]] — The reverse mapping: from an IP address back to a name, served out of the special `in-addr.arpa` (IPv4) / `ip6.arpa` (IPv6) zones.
- [[QUIC]] — A UDP-based transport with built-in TLS 1.3, multiplexed streams, and 0/1-RTT setup — the foundation of HTTP/3.
- [[RDMA]] — Network technology that lets one machine read or write another's memory directly, bypassing both CPUs and the OS networking stack.
- [[Recursive Resolver]] — A resolver that answers a client's query in full by chasing the delegation chain itself — root → TLD → authoritative — and caching each answer by its TTL.
- [[Router]] — A layer-3 device that forwards packets between networks, choosing the next hop per destination from its routing table (longest prefix match) and decrementing TTL on the way.
- [[Search Domain]] — A suffix (or list of them) the resolver appends to a _single-label_ name before querying, so `grafana` becomes `grafana.lan.example`.
- [[SOA Record]] — The record at a zone apex carrying the zone's administrative parameters: primary nameserver, admin contact, serial number, and the refresh/retry/expire/negative-TTL timers.
- [[Socket]] — The OS endpoint for network communication, identified by IP + port + protocol; the programming interface apps use to send/receive.
- [[Split-horizon DNS]] — Serving different answers for the same name depending on who's asking — typically an internal view (private IPs, internal-only hostnames) and a public view, from two separate authorities.
- [[SRV Record]] — A record advertising the host and port for a named service under a domain, as `_service._proto.name`, with priority and weight for selection.
- [[Stub Resolver]] — The minimal resolver built into the OS or libc that applications call; it doesn't recurse itself but forwards queries to a configured recursive resolver and returns the answer.
- [[Subnet]] — A contiguous block of IP addresses sharing a prefix, defined by a subnet mask / prefix length (255.255.255.0 = /24).
- [[Switch]] — A layer-2 device that learns which MAC address lives on which port (from source addresses of passing frames) and then forwards frames only to the right port, instead of repeating them everywhere like a hub.
- [[TCP]] — Connection-oriented transport giving ordered, reliable, byte-stream delivery with flow and congestion control, atop unreliable IP.
- [[Three-way Handshake]] — TCP's connection setup: SYN, SYN-ACK, ACK — synchronising sequence numbers before data flows.
- [[Throughput]] — The data rate actually achieved over a path, as opposed to the link's rated capacity.
- [[TTL]] — In DNS, the number of seconds a record may be cached by resolvers before it must be re-fetched.
- [[TXT Record]] — A DNS record holding arbitrary text, long repurposed as the carrier for machine-readable policy and proof-of-control strings.
- [[UDP]] — Connectionless transport: send datagrams with no handshake, ordering, or delivery guarantee — minimal overhead.

---
← Back to [[_Home]]
