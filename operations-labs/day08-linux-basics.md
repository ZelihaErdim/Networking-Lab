# Day 8 — Linux Basics

## What I Learned
- Everything on Linux lives under one root directory (`/`) — no C:\ drives, just one tree
- `/bin`, `/lib`, `/sbin` are symlinks to their `/usr` equivalents on newer systems
- `/etc/passwd` lists every account on the box: username, UID, GID, home dir, and login shell — service accounts get `/usr/sbin/nologin` so they can't be logged into directly
- UID is what the kernel actually tracks permissions by — the username is just a label on top of it
- `/etc/resolv.conf` is what tells the machine which DNS server to query
- A route table entry like `172.17.0.0/16 dev eth0` means "this whole block is local, no gateway needed" — anything outside it goes through the `default via` gateway line
- `ps aux` shows PID, CPU%, MEM%, and state for every running process — PID is what you'd target with `kill`
- `df -h` shows disk usage per mounted filesystem — a full disk is a classic cause of a service going down

## What I Configured
Used a Docker Ubuntu 22.04 container as a clean Linux box to run these commands against (keeps the host machine untouched and gives a disposable environment to practice on):

```
docker run -it --name day8-lab ubuntu:22.04 bash
```

Base image didn't ship with networking tools, so installed them:
```
apt update && apt install -y curl iproute2 iputils-ping net-tools
```

## What I Verified
- `pwd` / `cd` / `ls -la` — confirmed directory structure and that `cd` just changes the shell's working directory, nothing fancier
- `cat /etc/passwd` and `grep bash /etc/passwd` — only `root` had `/bin/bash` as a shell; every other account was `nologin`
- `head -5` / `tail -5 /etc/passwd` — first and last lines of the file, no surprises
- `find / -maxdepth 3 -name "*.conf" -type f` — turned up config files across `/etc`, including `/etc/resolv.conf`
- `ip addr` — container got `172.17.0.2/16` on `eth0`, a private address same as the RFC1918 ranges used in the switching labs
- `ip route` — default gateway `172.17.0.1`, matches the gateway concept from the routing labs just seen from an end host
- `ping 8.8.8.8` — 0% loss, confirmed outbound reachability
- `curl -sI https://google.com` — got a clean `HTTP/2 301` redirect, no connectivity issue
- `ps aux` and `df -h` — read process table and disk usage, both came back clean on a fresh container

## Practice Checklist
- [x] Navigate the filesystem with `pwd`, `cd`, `ls`
- [x] Read and filter files with `cat`, `grep`, `head`, `tail`
- [x] Search the filesystem with `find`
- [x] Read `/etc/passwd` and explain each field
- [x] Check IP config and routing with `ip addr` / `ip route`
- [x] Confirm connectivity with `ping` and `curl`
- [x] Check running processes and disk space with `ps aux` / `df -h`
