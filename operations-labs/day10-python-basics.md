# Day 10 — Python Basics

## Objective
Write a script that checks reachability for a set of hosts, stores the result per host in a dictionary, and prints a clean pass/fail summary — using `subprocess` instead of a networking library, since reachability checks in real ops scripts are usually wrapping the same CLI tools used manually.

## Script

```python
import subprocess

def check_host(host):
    result = subprocess.run(
        ["ping", "-c", "3", "-W", "2000", host],
        capture_output=True, text=True
    )
    return {
        "host": host,
        "reachable": result.returncode == 0,
        "output": result.stdout.strip(),
    }

def main():
    targets = ["8.8.8.8", "1.1.1.1", "10.255.255.1"]
    results = {t: check_host(t) for t in targets}

    print(f"{'HOST':<15}{'STATUS'}")
    for host, data in results.items():
        status = "UP" if data["reachable"] else "DOWN"
        print(f"{host:<15}{status}")

if __name__ == "__main__":
    main()
```

## Verification

Ran against two known-reachable public resolvers and one deliberately unreachable address (`10.255.255.1`, a non-routed private address with nothing listening):

```
HOST           STATUS
8.8.8.8        UP
1.1.1.1        UP
10.255.255.1   DOWN
```

`subprocess.run().returncode` is the signal being checked — `ping` returns `0` on success and non-zero on any failure (timeout, unreachable, unresolved host), which is why `reachable` is derived from `returncode == 0` rather than parsing the text output.

## Checklist
- [x] Write a function that checks reachability for a single host
- [x] Store per-host results in a dictionary, keyed by host
- [x] Print a summary table instead of raw ping output
- [x] Confirm the script correctly distinguishes an UP host from a DOWN host
