# Day 1 — VLANs & Switching

## Learn
- VLANs separate traffic logically
- Access ports connect end devices
- Trunk ports carry multiple VLANs
- Native VLAN is the untagged VLAN on a trunk
- The MAC address table maps source MAC addresses to switch ports

## Commands to Practice
- `show vlan brief`
- `show mac address-table`
- `show interfaces trunk`

## Lab Goal
Build these VLANs:
- VLAN 10 = Users
- VLAN 20 = Servers
- VLAN 99 = Management

## Practice Checklist
- [ ] Create VLAN 10, 20, and 99
- [ ] Assign ports to the correct VLANs
- [ ] Verify trunking between switches/routers
- [ ] Confirm the MAC address table updates
