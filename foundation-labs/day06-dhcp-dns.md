# Day 6 — DHCP and DNS

## What I Learned
- DHCP hands out IP addresses automatically when a device connects — no manual configuration needed on the end device
- Before DHCP, every PC had to be configured by hand with an IP, mask, gateway, and DNS. DHCP does all of that in one shot
- The router acts as the DHCP server. You define a pool with the network range, default gateway, and DNS server, and it handles the rest
- `excluded-address` reserves IPs that shouldn't be handed out — like the router's own interface IP. Without this, the router might give its own address to a PC and break routing
- DHCP assigns the first available address in the pool. PC0 got `192.168.1.2` and PC1 got `192.168.2.2` — both skipped `.1` because that was excluded
- DNS translates names to IPs. We pointed both PCs to `8.8.8.8` (Google's DNS) via DHCP so they could resolve names without any extra config

## Lab Goal
Configure both routers as DHCP servers for their connected PCs. Verify the PCs receive IP addresses automatically and can reach each other across the network.

## Topology

![Topology](images/Day6%20images/day06-topology.png)

Same 2-router layout as previous labs. Routers serve as DHCP servers for their local networks.

| Device | Interface | IP | Subnet |
|--------|-----------|-----|--------|
| PC0 | NIC | DHCP (got 192.168.1.2) | /24 |
| R0 | G0/0 | 192.168.1.1 | /24 |
| R0 | G0/1 | 10.0.0.1 | /30 |
| R1 | G0/0 | 10.0.0.2 | /30 |
| R1 | G0/1 | 192.168.2.1 | /24 |
| PC1 | NIC | DHCP (got 192.168.2.2) | /24 |

## What I Configured

Set up DHCP pools on both routers:

R0:
```
ip dhcp pool PC0_NETWORK
network 192.168.1.0 255.255.255.0
default-router 192.168.1.1
dns-server 8.8.8.8
exit
ip dhcp excluded-address 192.168.1.1
```

R1:
```
ip dhcp pool PC1_NETWORK
network 192.168.2.0 255.255.255.0
default-router 192.168.2.1
dns-server 8.8.8.8
exit
ip dhcp excluded-address 192.168.2.1
```

Added static routes so traffic can flow between the two networks:
```
! On R0
ip route 192.168.2.0 255.255.255.0 10.0.0.2

! On R1
ip route 192.168.1.0 255.255.255.0 10.0.0.1
```

Then switched both PCs from Static to DHCP in Desktop → IP Configuration.

## What I Verified

### PC0 DHCP Lease
![PC0 DHCP](images/Day6%20images/day06-pc0-dhcp.png)

PC0 received `192.168.1.2` automatically — IP, mask, gateway, and DNS all filled in by DHCP without touching anything manually.

### Ping — PC0 to PC1
![Ping](images/Day6%20images/day06-ping-success.png)

4/4 packets received, 0% loss. PC0 (`192.168.1.2`) reached PC1 (`192.168.2.2`) through both routers.

## Issues I Ran Into
- After removing BGP from the previous lab, there were no routes between the two networks so the first ping failed completely. Had to add static routes on both routers before traffic could flow
- The ping target had to be `192.168.2.2` instead of `192.168.2.10` because DHCP assigned a different address than what was used in previous labs

## Practice Checklist
- [x] Configure DHCP pools on both routers with correct network, gateway, and DNS
- [x] Exclude router interface IPs from DHCP pool
- [x] Switch PCs to DHCP and verify they receive addresses automatically
- [x] Add static routes between networks
- [x] Ping across the network with 0% loss
