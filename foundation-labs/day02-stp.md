# Day 2 — Spanning Tree Protocol (STP)

## Learn
- Loops happen when there are multiple active paths between switches
- STP prevents loops by blocking redundant links
- Root bridge is the reference point for the spanning-tree topology
- Port roles include root, designated, and blocked
- Port states include blocking, listening, learning, and forwarding

## Commands to Practice
- `show spanning-tree`
- `show spanning-tree vlan 10`

## Lab Tasks
- Build a small looped switch topology
- Observe which port becomes blocked
- Break the loop and watch the topology recover

## Reflection Questions
- Why does STP block a port?
- Which switch becomes the root bridge?
- What happens if the root link fails?
