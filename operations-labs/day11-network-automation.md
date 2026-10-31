# Day 11 — Network Automation with Netmiko

## Objective
Use Netmiko to open a real SSH session to a device and pull command output programmatically, instead of logging in manually. No Cisco hardware available, so the target is a Linux host reachable over SSH — Netmiko's `linux` device type handles this the same way `cisco_ios` handles IOS: it logs in, matches the shell prompt, sends the command, and captures the output until the prompt returns.

## Target
`day9-lab` — the systemd-enabled Ubuntu container from Day 9, reachable at `172.17.0.3` with SSH enabled and a root login configured for this test.

## Script

```python
from netmiko import ConnectHandler

device = {
    "device_type": "linux",
    "host": "172.17.0.3",
    "username": "root",
    "password": "LabPass123!",
}

with ConnectHandler(**device) as conn:
    output = conn.send_command("ip -br addr")
    print(output)
    with open("/tmp/device-output.txt", "w") as f:
        f.write(output + "\n")
```

## Verification

Ran from a separate disposable container on the same Docker network (Netmiko installed via `pip install netmiko`, nothing installed on the host):

```
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0@if22        UP             172.17.0.3/16
```

Output matches `172.17.0.3` — confirms the connection, authentication, and command execution round-trip against the live container, not a cached or local result.

## Notes
- Connection closes automatically on exiting the `with` block — no dangling SSH session left on the target even if the script errors mid-run
- Credentials here are thrown away with the container at the end of the lab; a shared script would pull them from environment variables or a vault, never hardcode them

## Checklist
- [x] Establish a real SSH session with Netmiko against a live host
- [x] Run a command remotely and capture the output
- [x] Save the output to a file
- [x] Confirm the connection closes cleanly
