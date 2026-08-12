# Day 4 — OSPF

## What I Learned
- OSPF is a link-state protocol — routers share topology information with each other and each one builds its own map of the network
- Unlike static routing, OSPF discovers routes automatically. No need to manually type every destination
- Routers send Hello packets to find neighbors. Once two routers agree on area and settings, they form an adjacency and share their link-state databases
- FULL state in `show ip ospf neighbor` means the routers have fully exchanged their databases and are ready to route
- `O` in the routing table means the route came from OSPF. `[110/2]` means AD 110 (OSPF default) and a cost of 2
- The cost goes up with each hop — R0 saw 192.168.2.0/24 at cost 3, R1 saw it at cost 2, because R1 is one hop closer to R2
- TTL in a ping reply tells you how many routers the packet crossed. PC0 to PC1 went through 3 routers, so TTL was 125 (128 − 3)

## Lab Goal
Build a 3-router linear topology and run OSPF across all of them in Area 0. No static routes — OSPF handles everything automatically.

## Topology

![Topology](images/Day4%20images/day04-topology.png)

Three 1941 routers in a line with a PC on each end. /30 subnets on the router-to-router links, /24 on the PC-facing interfaces.

| Device | Interface | IP | Subnet |
|--------|-----------|-----|--------|
| PC0 | NIC | 192.168.1.10 | /24 |
| R0 | G0/0 | 192.168.1.1 | /24 |
| R0 | G0/1 | 10.0.0.1 | /30 |
| R1 | G0/0 | 10.0.0.2 | /30 |
| R1 | G0/1 | 10.0.1.1 | /30 |
| R2 | G0/0 | 10.0.1.2 | /30 |
| R2 | G0/1 | 192.168.2.1 | /24 |
| PC1 | NIC | 192.168.2.10 | /24 |

## What I Configured

Assigned IPs and brought up interfaces on all three routers — same process as Day 3.

R0:
```
interface g0/0
ip address 192.168.1.1 255.255.255.0
no shutdown

interface g0/1
ip address 10.0.0.1 255.255.255.252
no shutdown
```

R1:
```
interface g0/0
ip address 10.0.0.2 255.255.255.252
no shutdown

interface g0/1
ip address 10.0.1.1 255.255.255.252
no shutdown
```

R2:
```
interface g0/0
ip address 10.0.1.2 255.255.255.252
no shutdown

interface g0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
```

Then enabled OSPF on all three routers using wildcard masks to match the interfaces:

R0:
```
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
network 10.0.0.0 0.0.0.3 area 0
```

R1:
```
router ospf 1
network 10.0.0.0 0.0.0.3 area 0
network 10.0.1.0 0.0.0.3 area 0
```

R2:
```
router ospf 1
network 10.0.1.0 0.0.0.3 area 0
network 192.168.2.0 0.0.0.255 area 0
```

The wildcard mask is the inverse of the subnet mask. `0.0.0.3` matches a /30, `0.0.0.255` matches a /24.

## What I Verified

### OSPF Neighbors — R1
![OSPF Neighbor](images/Day4%20images/day04-ospf-neighbor.png)

R1 shows two neighbors, both in FULL state:
- `192.168.1.1` = R0, reachable via G0/0 at `10.0.0.1`
- `192.168.2.1` = R2, reachable via G0/1 at `10.0.1.2`

FULL means the routers have exchanged their link-state databases completely.

### Routing Table — R0
![Route Table](images/Day4%20images/day04-route-table.png)

R0 shows two `O` entries — routes it learned from OSPF without any manual configuration:
- `O 10.0.1.0/30 [110/2]` — the R1–R2 link
- `O 192.168.2.0/24 [110/3]` — PC1's network, 3 hops away

### Ping — PC0 to PC1
![Ping](images/Day4%20images/day04-ping-success.png)

4/4 packets received, 0% loss, TTL=125. Three routers in the path so TTL dropped by 3 from the default 128.

## Issues I Ran Into
- Cables were connected to the wrong ports on R1 — R0 ended up on G0/1 and R2 on G0/0, which put both on the wrong subnets. Found it with `show cdp neighbors`, which showed exactly which device was on which interface. Rewired the cables and neighbors formed immediately
- While fixing an OSPF typo with a `no network` command, the wildcard mask caused it to also remove a correct network statement. Had to re-add it manually and verify with `show running-config | section ospf`
- `log-adjacency-changes` appeared in the OSPF config without being typed — that's a default IOS line, it just logs when neighbor state changes. Not a problem

## Practice Checklist
- [x] Assign IPs to all router interfaces and bring them up
- [x] Configure OSPF with correct network statements and area 0
- [x] Verify neighbors form with `show ip ospf neighbor` — both in FULL state
- [x] Confirm `O` routes appear in routing tables on all routers
- [x] Ping PC1 from PC0 with 0% loss
