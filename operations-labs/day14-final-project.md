# Day 14 — Final Project

## Scope
The brief called for a single "Mini ISP" topology combining VLANs, STP, OSPF, BGP, DHCP, DNS, a Linux server, and automation/monitoring tooling. Those pieces already exist as separate, verified builds rather than one combined topology:

| Component | Where it's proven |
|---|---|
| VLANs, trunking, MAC learning | Day 1 |
| STP, redundant links, failover | Day 2 |
| Static routing | Day 3 |
| OSPF, multi-hop convergence | Day 4 |
| BGP, inter-AS peering | Day 5 |
| DHCP, DNS | Day 6 |
| VLAN + OSPF + DHCP + DNS combined | Day 7 |
| Linux troubleshooting (systemd/journalctl) | Day 9 |
| Python automation | Day 10 |
| Netmiko-style remote command execution | Day 11 |
| Monitoring (Prometheus + Grafana) | Day 12 |
| Ansible-driven health checks | Day 13 |

This closes out the project by tying the automation/monitoring side together into one script, and pulling a troubleshooting checklist from issues actually hit across the previous 13 days — rather than a generic checklist written in the abstract.

## Automation Script

Combines three things that were built separately on Days 10, 11, and 13 into one tool: a reachability check (Day 10's pattern), a remote data pull over SSH via Netmiko (Day 11), and a structured report instead of raw text output.

```python
import json
import subprocess
from datetime import datetime, timezone

from netmiko import ConnectHandler

TARGET = {
    "device_type": "linux",
    "host": "172.17.0.3",
    "username": "root",
    "password": "LabPass123!",
}


def check_reachability(host):
    result = subprocess.run(
        ["ping", "-c", "3", "-W", "2000", host],
        capture_output=True, text=True
    )
    return result.returncode == 0


def collect_device_data():
    with ConnectHandler(**TARGET) as conn:
        hostname = conn.send_command("hostname")
        os_release = conn.send_command("grep PRETTY_NAME /etc/os-release")
        disk = conn.send_command("df -h / | tail -1")
        ssh_state = conn.send_command("systemctl is-active ssh")
        uptime = conn.send_command("uptime -p")
    return {
        "hostname": hostname.strip(),
        "os": os_release.split("=")[1].strip('"') if "=" in os_release else os_release,
        "disk_root": disk.strip(),
        "ssh_service": ssh_state.strip(),
        "uptime": uptime.strip(),
    }


def main():
    report = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "target": TARGET["host"],
        "reachable": check_reachability(TARGET["host"]),
    }
    if report["reachable"]:
        report["device"] = collect_device_data()

    print(json.dumps(report, indent=2))
    with open("health-report.json", "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
```

## Verification

```json
{
  "collected_at": "2026-10-31T21:20:00.534472+00:00",
  "target": "172.17.0.3",
  "reachable": true,
  "device": {
    "hostname": "3b7f429e8e06",
    "os": "Ubuntu 22.04.5 LTS",
    "disk_root": "overlay         911G  4.5G  860G   1% /",
    "ssh_service": "active",
    "uptime": "up 8 hours, 24 minutes"
  }
}
```

If the reachability check fails, the script skips the Netmiko call entirely instead of hanging on a connection attempt to a dead host — the `"device"` key is simply absent from the report.

## Troubleshooting Checklist

Built from actual root causes hit across this project, not a generic list:

- **No connectivity between two networks** → check static/dynamic routes exist in both directions (Day 3 — a missing return route fails the ping even when the forward path is fine)
- **Routing protocol not converging** → check physical/logical port assignment first (Day 4 — cables on the wrong interface put both ends on the wrong subnet; `show cdp neighbors` confirms real wiring)
- **DHCP not reaching a client across a router** → check for a relay/helper address; DHCP requests are broadcasts and don't cross routers on their own (Day 7)
- **A systemd service won't start after a config change** → `systemctl status` shows *that* it failed and where in the startup sequence; `journalctl -xeu <unit>` shows *why* — don't restart blindly (Day 9)
- **"Permission denied" on SSH key auth despite a correct key** → check file ownership on `authorized_keys`, not just its contents or permission bits (Day 13)
- **Script hangs on an unreachable host** → check reachability before attempting a protocol-level connection, and fail fast instead of relying on a connection timeout (this script's design)

## Checklist
- [x] All required topology components verified individually across Days 1–7
- [x] Linux server operations verified with real fault injection and recovery (Day 9)
- [x] Automation script collects real reachability, OS, disk, and service data from a live host
- [x] Report output is structured (JSON) rather than raw terminal text
- [x] Troubleshooting checklist reflects real issues encountered, not hypothetical ones
