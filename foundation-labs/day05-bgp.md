# Day 5 — BGP

## Learn
- BGP is the protocol used between autonomous systems
- ASN identifies a network
- eBGP is used between different ASNs
- iBGP is used inside the same ASN
- Routers advertise networks to peers

## Commands to Practice
- `show ip bgp`
- `show ip bgp summary`
- `show bgp neighbors`

## Lab Goal
Build a simple BGP setup:
- ASN 65001
- ASN 65002

## Checklist
- [ ] Configure eBGP between the two routers
- [ ] Verify neighbor session state
- [ ] Check learned routes
- [ ] Confirm end-to-end reachability
