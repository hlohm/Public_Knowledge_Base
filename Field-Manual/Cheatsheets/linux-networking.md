---
type: cheatsheet
area: "Linux Administration"
aliases: [ip, ss, nmcli, ifconfig, netstat]
tags: [linux, networking, ip, ss, nmcli, interfaces, routes]
status: working
---

# Linux Networking

> **Area:** [[Linux Administration]]

Interface configuration, routing, socket inspection, and network troubleshooting on Linux. The modern toolchain: `ip` (replaces `ifconfig`/`route`), `ss` (replaces `netstat`), and `nmcli` for NetworkManager-managed hosts.

---

## 1. ip — interface and route management

### Interfaces

```bash
ip link show                         # list all interfaces and their state
ip link show eth0                    # one interface
ip addr show                         # interfaces with IP addresses
ip addr show eth0                    # one interface
ip -4 addr                           # IPv4 only
ip -6 addr                           # IPv6 only
ip -brief addr                       # compact one-line-per-interface summary

# Bring up / down
ip link set eth0 up
ip link set eth0 down

# Assign and remove IP addresses
ip addr add 192.0.2.10/24 dev eth0
ip addr del 192.0.2.10/24 dev eth0
ip addr flush dev eth0               # remove all addresses from interface

# MTU
ip link set eth0 mtu 9000
```

### Routes

```bash
ip route show                        # main routing table
ip route show table all              # all routing tables
ip -6 route show                     # IPv6 routes

ip route add default via 192.0.2.1 dev eth0          # default gateway
ip route add 10.0.0.0/8 via 172.16.0.1               # static route
ip route add blackhole 198.51.100.0/24               # drop matching traffic
ip route del 10.0.0.0/8 via 172.16.0.1               # remove a route
ip route replace default via 192.0.2.254             # replace the default gateway

# Which route would be used for a specific destination?
ip route get 8.8.8.8
ip route get 2001:4860:4860::8888    # IPv6
```

### ARP and neighbors

```bash
ip neigh show                        # ARP table (neighbor cache)
ip neigh flush dev eth0              # flush ARP cache for an interface
ip neigh add 192.0.2.2 lladdr aa:bb:cc:dd:ee:ff dev eth0  # static ARP entry
```

### Tun/tap, VLANs, bridges

```bash
# VLAN
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 10.0.100.1/24 dev eth0.100
ip link set eth0.100 up

# Bridge
ip link add br0 type bridge
ip link set eth0 master br0
ip link set eth1 master br0
ip link set br0 up
```

## 2. ss — socket statistics

`ss` is faster than `netstat` and queries kernel directly.

```bash
ss -tulnp                 # TCP+UDP, listening only, numeric addresses, with PID
ss -tnp                   # TCP connections, numeric, with PID
ss -unp                   # UDP, numeric, with PID
ss -xnp                   # Unix domain sockets, numeric, with PID
ss -s                     # summary statistics

# Filter by state
ss state established
ss state listening

# Filter by port
ss -tnp '( dport = :443 or sport = :443 )'
ss -tnp 'sport = :22'

# Filter by address
ss -tnp dst 192.0.2.1
ss -tnp src 192.0.2.10

# Find what is listening on a specific port
ss -tnlp | grep ':80 '
```

Column reference: `Netid` (protocol), `State`, `Recv-Q`, `Send-Q`, `Local Address:Port`, `Peer Address:Port`, `Process`

## 3. nmcli — NetworkManager CLI

Most desktop and server distros (RHEL/Fedora/Ubuntu) use NetworkManager. `nmcli` is the CLI.

```bash
# Status
nmcli general status           # overall NM status
nmcli device status            # all devices and their managed state
nmcli connection show          # all configured connections
nmcli device show eth0         # detailed device info (IP, MAC, DNS, gateway)

# Connect / disconnect
nmcli device connect eth0
nmcli device disconnect eth0
nmcli connection up "Connection Name"
nmcli connection down "Connection Name"

# Create connections
nmcli connection add type ethernet ifname eth0 con-name mycon \
  ipv4.addresses 192.0.2.10/24 \
  ipv4.gateway 192.0.2.1 \
  ipv4.dns "8.8.8.8 1.1.1.1" \
  ipv4.method manual

nmcli connection add type ethernet ifname eth0 con-name mycon-dhcp \
  ipv4.method auto

# Modify an existing connection
nmcli connection modify mycon ipv4.dns "1.1.1.1 9.9.9.9"
nmcli connection modify mycon +ipv4.dns "8.8.8.8"   # append
nmcli connection modify mycon -ipv4.dns "8.8.8.8"   # remove

# Apply changes
nmcli connection up mycon

# Wi-Fi
nmcli device wifi list
nmcli device wifi connect <SSID> password <password>
```

## 4. Troubleshooting patterns

```bash
# Is the interface up and does it have an IP?
ip -brief addr show

# Is the gateway reachable?
ping -c 4 <gateway-ip>
ip route get 8.8.8.8          # shows which interface + gateway would be used

# Can we reach DNS?
dig @1.1.1.1 example.com +short   # bypass local resolver to test connectivity
cat /etc/resolv.conf               # what resolver is configured?

# Can we reach the internet?
curl -sI https://example.com | head -1

# What is listening on port 80?
ss -tnlp | grep ':80 '
fuser 80/tcp                       # also shows PID

# Trace the route to a destination
traceroute example.com
tracepath example.com     # no root required; UDP-based
mtr example.com           # continuous traceroute + latency stats

# Capture traffic on an interface
tcpdump -i eth0 -n port 80
tcpdump -i eth0 -n -w /tmp/capture.pcap   # write to file for Wireshark
tcpdump -i eth0 host 192.0.2.1            # filter by host

# Check open ports from the inside vs outside
ss -tnlp                          # what this host is listening on
nmap -sV <this-host-ip>           # what is reachable from another host
```

## 5. Persistent configuration without NetworkManager

```bash
# systemd-networkd — /etc/systemd/network/20-wired.network:
[Match]
Name=eth0

[Network]
Address=192.0.2.10/24
Gateway=192.0.2.1
DNS=1.1.1.1
DNS=8.8.8.8

# Activate:
systemctl enable --now systemd-networkd systemd-resolved

# Debian /etc/network/interfaces (legacy, no NM):
auto eth0
iface eth0 inet static
    address 192.0.2.10/24
    gateway 192.0.2.1
    dns-nameservers 1.1.1.1 8.8.8.8
```

---

## Daily workflows

### "Find out what IP is assigned to an interface"
```bash
ip -brief addr show eth0
```

### "Find what process is listening on a port"
```bash
ss -tnlp | grep ':8080 '
```

### "Add a static route for an internal network"
```bash
ip route add 10.10.0.0/16 via 192.0.2.254
# Persist via nmcli or /etc/systemd/network/
```

### "Check why internet connectivity is failing"
```bash
ip route get 8.8.8.8              # is there a route?
ping -c 2 $(ip route get 8.8.8.8 | awk '/via/{print $3}')  # is the gateway up?
dig @1.1.1.1 example.com +short   # is DNS working independently of local resolver?
```

## Gotchas / Golden rules

1. **`ip addr` changes are not persistent across reboots** — use `nmcli` or a network config file; `ip` commands configure the running kernel only.
2. **`ss -tulnp` requires root (or `sudo`) to show PIDs** — without root, the Process column is empty.
3. **`ifconfig` and `netstat` are deprecated** — they still exist on many systems (from `net-tools`) but read from `/proc`; `ip` and `ss` talk directly to the kernel via netlink and are authoritative.
4. **`/etc/resolv.conf` may be a symlink managed by systemd-resolved or NetworkManager** — editing it directly may be overwritten on the next NM event; configure DNS via `nmcli` or `systemd-resolved`.
5. **VLANs need the underlying physical interface to stay up** — the VLAN sub-interface goes down if the parent goes down; don't `ip link set eth0 down` when eth0.100 is carrying traffic.
