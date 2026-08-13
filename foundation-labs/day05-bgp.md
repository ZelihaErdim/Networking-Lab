# Day 5 — BGP

## What I Learned
- BGP is the routing protocol that runs the internet — it connects different organizations and ISPs to each other
- OSPF runs inside one network (same AS). BGP runs between networks (different AS numbers). That's the key difference
- Each organization has an Autonomous System number (AS). In this lab R0 was AS 100 and R1 was AS 200 — simulating two separate networks peering with each other
- BGP peers are called neighbors. You have to manually define who your neighbor is and what AS they belong to — BGP doesn't discover neighbors automatically like OSPF does
- The `network` command in BGP tells the router which of its own networks to advertise to the neighbor
- `show ip bgp summary` is the go-to command to check if the peering is up. A number in the `State/PfxRcd` column means it's working — `Active` or `Idle` means it's not
- BGP routes show up as `B` in the routing table, with an AD of 20 for eBGP

## Lab Goal
Build a 2-router topology across two different AS numbers, establish an eBGP peering session, and verify that each router learns the other's network automatically.

## Topology

![Topology](images/Day5%20images/day05-topology.png)

Two 1941 routers, each in a different AS, connected on a /30 point-to-point link.

| Device | Interface | IP | Subnet |
|--------|-----------|-----|--------|
| PC0 | NIC | 192.168.1.10 | /24 |
| R0 | G0/0 | 192.168.1.1 | /24 |
| R0 | G0/1 | 10.0.0.1 | /30 |
| R1 | G0/0 | 10.0.0.2 | /30 |
| R1 | G0/1 | 192.168.2.1 | /24 |
| PC1 | NIC | 192.168.2.10 | /24 |

## What I Configured

Assigned IPs and brought up interfaces on both routers — same process as previous days.

Then configured BGP on each router:

R0 (AS 100):
```
router bgp 100
neighbor 10.0.0.2 remote-as 200
network 192.168.1.0 mask 255.255.255.0
```

R1 (AS 200):
```
router bgp 200
neighbor 10.0.0.1 remote-as 100
network 192.168.2.0 mask 255.255.255.0
```

Each router points to the other's interface IP as the neighbor, and specifies the other's AS number with `remote-as`. The `network` command advertises the PC-facing subnet into BGP.

## What I Verified

### BGP Summary — R1
![BGP Summary](images/Day5%20images/day05-bgp-summary.png)

Neighbor `10.0.0.1` (R0) is listed with AS 100. Up/Down shows the session has been stable, and `State/PfxRcd` shows a number — that means the peering is established and routes are being received.

### Ping — PC0 to PC1
![Ping](images/Day5%20images/day05-ping-success.png)

3/4 packets received. First packet timed out while ARP resolved — same behavior as every previous lab. The three replies confirm end-to-end reachability through BGP.

## Issues I Ran Into
- None on this lab — the config was straightforward and the peering came up cleanly on the first try

## Practice Checklist
- [x] Assign IPs to all router interfaces and bring them up
- [x] Configure BGP with correct AS numbers on both routers
- [x] Define neighbors and advertise networks
- [x] Verify BGP peering with `show ip bgp summary` — number in PfxRcd column
- [x] Ping PC1 from PC0 and confirm reachability
