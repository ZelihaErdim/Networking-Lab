# Day 13 — Ansible

## Objective
Run a real Ansible playbook against a live host over SSH — fact-gathering, a disk check, and a service-state assertion — rather than a dry-run example against a placeholder inventory.

## Target
`day9-lab`, reached over SSH with key-based auth (no password, no `sshpass`).

## Inventory

```ini
[lab]
day9-lab ansible_host=172.17.0.3 ansible_user=root ansible_ssh_private_key_file=/work/id_ed25519

[lab:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
```

## Playbook

```yaml
---
- name: Operational health check
  hosts: lab
  gather_facts: true
  tasks:
    - name: Report OS and kernel
      debug:
        msg: "{{ ansible_distribution }} {{ ansible_distribution_version }} / kernel {{ ansible_kernel }}"

    - name: Check root filesystem usage
      shell: df -h / | tail -1
      register: disk_usage
      changed_when: false

    - name: Report disk usage
      debug:
        var: disk_usage.stdout

    - name: Confirm ssh.service is active
      systemd:
        name: ssh
      register: ssh_status

    - name: Report ssh.service state
      debug:
        msg: "ssh.service is {{ ssh_status.status.ActiveState }}"

    - name: Fail the play if ssh is not active
      fail:
        msg: "ssh.service is not active — found {{ ssh_status.status.ActiveState }}"
      when: ssh_status.status.ActiveState != "active"
```

The last two tasks turn a status check into an actual pass/fail gate instead of just printing a value — the play only fails if `ActiveState` isn't `active`, which is the pattern for using Ansible as a verification step rather than just a config pusher.

## Run

```
ansible-playbook -i inventory.ini playbook.yml
```

```
PLAY [Operational health check] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [day9-lab]

TASK [Report OS and kernel] ****************************************************
ok: [day9-lab] => {
    "msg": "Ubuntu 22.04 / kernel 7.0.14-linuxkit"
}

TASK [Check root filesystem usage] *********************************************
ok: [day9-lab]

TASK [Report disk usage] *******************************************************
ok: [day9-lab] => {
    "disk_usage.stdout": "overlay         911G  4.5G  860G   1% /"
}

TASK [Confirm ssh.service is active] *******************************************
ok: [day9-lab]

TASK [Report ssh.service state] ************************************************
ok: [day9-lab] => {
    "msg": "ssh.service is active"
}

TASK [Fail the play if ssh is not active] **************************************
skipping: [day9-lab]

PLAY RECAP *********************************************************************
day9-lab                   : ok=6    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

The final task shows `skipping` — correct behavior, since the `when` condition wasn't met. A skipped task here means the health check passed.

## Issue
First run failed with `Permission denied (publickey,password)` even though the public key was correctly installed in `/root/.ssh/authorized_keys`. Cause: the key file had been copied in with the host machine's UID as owner instead of `root`. `sshd` silently refuses to use an `authorized_keys` file it doesn't trust the ownership of — no error pointing at the cause, just a generic auth failure. Fixed with `chown root:root /root/.ssh/authorized_keys`.

## Checklist
- [x] Build an inventory file targeting a real reachable host
- [x] Set up key-based SSH auth instead of passwords
- [x] Run a playbook that gathers facts and reports real system state
- [x] Use a registered variable and a conditional `fail` to turn a check into a pass/fail gate
- [x] Confirm a clean run with `ok` across all tasks
