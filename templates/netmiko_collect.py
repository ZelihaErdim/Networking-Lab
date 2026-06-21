#!/usr/bin/env python3
"""Collect a command output from a Cisco-style device using Netmiko."""

import argparse
from pathlib import Path

from netmiko import ConnectHandler


def main():
    parser = argparse.ArgumentParser(
        description="Run a single command on a network device and save the output."
    )
    parser.add_argument("--host", default="10.1.1.1")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="pass")
    parser.add_argument(
        "--command",
        default="show ip interface brief",
        help="Command to run on the device.",
    )
    parser.add_argument(
        "--output",
        default="device-output.txt",
        help="Where to save the command output.",
    )
    args = parser.parse_args()

    router = {
        "device_type": "cisco_ios",
        "host": args.host,
        "username": args.username,
        "password": args.password,
        "fast_cli": True,
    }

    try:
        with ConnectHandler(**router) as conn:
            output = conn.send_command(args.command)
            print(output)

            output_path = Path(args.output)
            output_path.write_text(output + "\n", encoding="utf-8")
            print(f"Saved output to {output_path.resolve()}")
    except Exception as exc:
        print(f"Error connecting to {args.host}: {exc}")
        raise


if __name__ == "__main__":
    main()

