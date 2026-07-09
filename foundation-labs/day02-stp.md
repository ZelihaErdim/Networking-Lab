# Day 2 — Spanning Tree Protocol (STP)

## What I Learned
- Redundant links between switches create loops — broadcast frames circle forever and kill the network
- STP prevents this by blocking one of the redundant links automatically
- The root bridge is elected based on priority first, then lowest MAC address as tiebreaker
- Port roles: root (best path to root bridge), designated (forwarding for a segment), alternate (blocked backup)
- When an active link goes down, STP reconverges and unblocks the backup path

## Lab Goal
Build a 3-switch triangle topology, identify the root bridge and blocked port, simulate a link failure, and watch STP recover.

## Topology

![Topology](images/Day2%20images/day02-topology.png)

Three 2960 switches connected in a triangle with crossover cables.

| Link | From | To |
|------|------|----|
| SW0 Fa0/1 | SW0 | SW1 |
| SW0 Fa0/2 | SW0 | SW2 |
| SW1 Fa0/2 | SW1 | SW2 |

## What I Verified

### STP State on All Three Switches

**SW0** — not the root bridge
![SW0 STP](images/Day2%20images/day02-stp-sw0.png)

- Bridge ID: `0030.F253.C851`
- Fa0/1: Alternate — **BLOCKED** (the orange dot in the topology)
- Fa0/2: Root — forwarding (best path to the root bridge)

**SW1** — not the root bridge
![SW1 STP](images/Day2%20images/day02-stp-sw1.png)

- Bridge ID: `000D.BD30.4B08`
- Fa0/1: Designated — forwarding
- Fa0/2: Root — forwarding (path to root bridge)

**SW2** — the root bridge
![SW2 STP](images/Day2%20images/day02-stp-sw2.png)

- Bridge ID: `0001.C953.A894` — lowest MAC, so it won the election
- Says "This bridge is the root"
- Both ports designated and forwarding — the root bridge never blocks

### Why SW2 Won the Election
All three switches had the same priority (32769). When priority ties, the switch with the lowest MAC address wins. SW2 had `0001.C953.A894`, which is lower than SW1 (`000D.BD30.4B08`) and SW0 (`0030.F253.C851`).

## Link Failure Test

### After Shutting Down SW0 Fa0/2
![After Shutdown](images/Day2%20images/day02-stp-after-shutdown.png)

I shut down Fa0/2 on SW0 (`shutdown` command), which killed the direct path to the root bridge (SW2). STP reconverged:
- Fa0/1 went from **blocked to Root FWD** — it became the new best path
- The root bridge changed from SW0's perspective to SW1 (`000D.BD30.4B08`) since it could no longer see SW2 directly

### After Bringing the Link Back Up
![After Recovery](images/Day2%20images/day02-stp-after-recovery.png)

I brought Fa0/2 back up with `no shutdown`. After about 30 seconds, STP reconverged again:
- SW2 became the root bridge again (`0001.C953.A894`)
- Fa0/2 went back to Root FWD
- The blocked port moved to the SW1-SW2 link instead of back to SW0 Fa0/1 — STP doesn't always restore the exact same state, it just picks the best loop-free topology

## Issues I Ran Into
- Had to wait about 30 seconds after `no shutdown` before STP fully reconverged — running `show spanning-tree` too early showed the old state
- After recovery the blocked port moved to a different location than where it started — this is normal STP behavior

## Reflection Questions
- **Why does STP block a port?** To prevent loops. Without STP, broadcast frames would circle forever between redundant links.
- **Which switch becomes the root bridge?** The one with the lowest priority. If priority is tied, the one with the lowest MAC address wins.
- **What happens if the root link fails?** STP detects the failure, unblocks the backup path, and reconverges. It takes about 30 seconds with classic STP.

## Practice Checklist
- [x] Build a looped switch topology
- [x] Identify the root bridge and blocked port
- [x] Shut down an active link and observe reconvergence
- [x] Bring the link back up and verify recovery
