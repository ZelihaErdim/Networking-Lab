# Day 13 — Ansible

## Example Playbook
```yaml
---
- hosts: routers
  tasks:
    - name: Show version
      ios_command:
        commands:
          - show version
```

## Practice Tasks
- Install Ansible
- Create an inventory file for your routers
- Run the playbook with `ansible-playbook`

## Notes
Focus on understanding what the playbook is doing before trying more advanced automation.
