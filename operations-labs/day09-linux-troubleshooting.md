# Day 9 — Linux Troubleshooting

## Objective
Diagnose and recover a failed systemd-managed service using `systemctl` and `journalctl`, without just restarting blindly.

## Environment
Ubuntu 22.04 container running systemd as PID 1 (`--privileged`, host cgroup namespace), with `openssh-server` installed and enabled as a real systemd unit.

## Fault Injection
Added an invalid directive to `/etc/ssh/sshd_config` and attempted a restart:

```
echo 'InvalidDirectiveXYZ yes' >> /etc/ssh/sshd_config
systemctl restart ssh
```

```
Job for ssh.service failed because the control process exited with error code.
See "systemctl status ssh.service" and "journalctl -xeu ssh.service" for details.
```

## Diagnosis
`systemctl status ssh` confirmed the unit was in a failed state with an exit code, and showed systemd hitting its restart-rate limit:

```
Active: failed (Result: exit-code)
Process: 86 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=255/EXCEPTION)
ssh.service: Start request repeated too quickly.
```

The exit code alone doesn't say why — `ExecStartPre` runs `sshd -t` (a config syntax check) before the real start, so a 255 there means the config itself is invalid, not a runtime crash. `journalctl -xeu ssh` gave the actual line:

```
sshd[86]: /etc/ssh/sshd_config: line 123: Bad configuration option: InvalidDirectiveXYZ
sshd[86]: terminating, 1 bad configuration options
```

## Fix
Removed the bad line and re-validated before touching the service:

```
sed -i '/InvalidDirectiveXYZ/d' /etc/ssh/sshd_config
sshd -t
systemctl restart ssh
```

Second failure, different cause — `sshd -t` passed, but the restart still failed:

```
Missing privilege separation directory: /run/sshd
```

`/run` is tmpfs and gets rebuilt on boot; this directory is normally created by the package's postinst/tmpfiles config, which hadn't run against this container state. Created it manually and retried:

```
mkdir -p /run/sshd && chmod 755 /run/sshd
systemctl restart ssh
systemctl is-active ssh
```

```
active
```

## Takeaway
`systemctl status` tells you *that* something failed and where in the startup sequence; `journalctl -xeu <unit>` tells you *why*. A clean `sshd -t` doesn't guarantee a clean service start — runtime dependencies like `/run/sshd` can fail independently of config syntax, and each failure needs its own evidence from the logs rather than assuming the first fix covers both.

## Checklist
- [x] Confirm a healthy service baseline with `systemctl status`
- [x] Break the service with an invalid config change
- [x] Capture the failure with `systemctl status` and `journalctl -xeu`
- [x] Identify root cause from log output rather than guessing
- [x] Apply a fix, re-validate config, and confirm `active` state
