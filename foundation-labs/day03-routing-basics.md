# Day 3 — Routing Basics

## What I Learned
- Switches forward by MAC address, routers forward by IP address — that's the core difference between Layer 2 and Layer 3
- Every router interface connects to one network and needs its own IP assigned manually
- Routers only know about networks directly plugged into them — everything else needs a static route
- Static routes have to exist in both directions. R0 needs a route to PC1's network, R1 needs a route back to PC0's. Miss one and the ping fails on the return trip
- TTL in a ping reply tells you how many routers the packet crossed — TTL=126 means it started at 128 and hit 2 routers
- /30 subnets are used on point-to-point router links because only 2 usable IPs are needed — no reason to waste a /24

## Lab Goal
Build a two-router topology, assign IPs to all interfaces, add static routes on both routers, and verify end-to-end connectivity from PC0 to PC1.

## Topology

![Topology](images/Day3%20images/day03-topology.png)

Two 1941 routers connected in a straight line with two PCs on each end.

| Device | Interface | IP | Subnet |
|--------|-----------|-----|--------|
| PC0 | NIC | 192.168.1.10 | /24 |
| R0 | G0/0 | 192.168.1.1 | /24 |
| R0 | G0/1 | 10.0.0.1 | /30 |
| R1 | G0/0 | 10.0.0.2 | /30 |
| R1 | G0/1 | 192.168.2.1 | /24 |
| PC1 | NIC | 192.168.2.10 | /24 |

## What I Configured

Assigned IPs and brought up interfaces on R0:
```
interface g0/0
ip address 192.168.1.1 255.255.255.0
no shutdown

interface g0/1
ip address 10.0.0.1 255.255.255.252
no shutdown
```

Same on R1 with its addresses:
```
interface g0/0
ip address 10.0.0.2 255.255.255.252
no shutdown

interface g0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
```

Added static routes — R0 needs to know about PC1's network, R1 needs to know about PC0's:
```
! On R0
ip route 192.168.2.0 255.255.255.0 10.0.0.2

! On R1
ip route 192.168.1.0 255.255.255.0 10.0.0.1
```

## What I Verified

### Routing Table — R0
![R0 route table](images/Day3%20images/day03-r0-route-table.png)

Two `C` connected routes for R0's own interfaces. One `S` static route to `192.168.2.0/24` via `10.0.0.2`.

### Routing Table — R1
![R1 route table](images/Day3%20images/day03-r1-route-table.png)

Two `C` connected routes for R1's own interfaces. One `S` static route to `192.168.1.0/24` via `10.0.0.1`.

### Ping — PC0 to PC1
![Ping](images/Day3%20images/day03-ping-success.png)

4/4 packets received, 0% loss, TTL=126. First attempt had 2 timeouts while ARP resolved — clean on the second run.

### Tracert — PC0 to PC1
![Tracert](images/Day3%20images/day03-tracert-pc0.png)

- Hop 1: `192.168.1.1` — R0
- Hop 2: `10.0.0.2` — R1
- Hop 3: `192.168.2.10` — PC1

Three hops, confirms traffic is actually being routed through both routers.

## Issues I Ran Into
- Forgot to configure PC0 and PC1's IPs before pinging — got 100% packet loss until I set the addresses and default gateways on both PCs
- Both routers have the default hostname "Router" in Packet Tracer, which made it impossible to tell which CLI window belonged to which device. Kept running `show ip route` on R0 by mistake. Fixed it by renaming them with `hostname R0` and `hostname R1`
- First ping attempt showed 50% loss — the first two packets timed out while ARP was resolving MAC addresses. Normal behavior, not a config issue

## Practice Checklist
- [x] Assign IPs to all router interfaces and bring them up with no shutdown
- [x] Set IP addresses and default gateways on both PCs
- [x] Add static routes on both routers
- [x] Verify routing tables show C and S entries
- [x] Ping PC1 from PC0 with 0% loss
- [x] Run tracert and confirm 3 hops with correct IPs
