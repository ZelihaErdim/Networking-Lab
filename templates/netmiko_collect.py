from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "host": "10.1.1.1",
    "username": "admin",
    "password": "pass"
}

conn = ConnectHandler(**router)
output = conn.send_command("show ip interface brief")
print(output)
conn.disconnect()
