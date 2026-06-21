# Day 11 — Network Automation with Netmiko

## Example
```python
from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "host": "10.1.1.1",
    "username": "admin",
    "password": "pass"
}

conn = ConnectHandler(**router)
print(conn.send_command("show ip interface brief"))
conn.disconnect()
```

## Practice Tasks
- Connect to a lab router
- Run `show ip interface brief`
- Save the output to a file

## Tips
- Always close the connection when finished
- Avoid hardcoding credentials in shared files
