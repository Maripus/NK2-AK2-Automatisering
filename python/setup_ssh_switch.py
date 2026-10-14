import serial
import time
import getpass

com_port = input("COM-port [COM4]: ") or "COM4"
hostname = input("Hostname [SW2]: ") or "SW2"
domain = input("Domain [lab.local]: ") or "lab.local"
username = input("Username [admin]: ") or "admin"
password = getpass.getpass("Password: ")

mgmt_vlan = input("Management VLAN [20]: ") or "20"
mgmt_ip = input("Management IP [172.16.2.2]: ") or "172.16.2.2"
mgmt_mask = input("Subnet mask [255.255.255.0]: ") or "255.255.255.0"

uplink = input("Port mot R2 [GigabitEthernet1/0/2]: ") or "GigabitEthernet1/0/2"
pc_port = input("Port mot PC [GigabitEthernet1/0/4]: ") or "GigabitEthernet1/0/4"

ser = serial.Serial(com_port, 9600, timeout=1)
time.sleep(2)

# Vekk konsollen
ser.write(b"\r\n")
time.sleep(1)

# Hvis switchen spør om initial configuration dialog
ser.write(b"no\r\n")
time.sleep(2)

commands = [
    "enable",
    "configure terminal",
    f"hostname {hostname}",
    f"ip domain-name {domain}",
    f"username {username} privilege 15 secret {password}",

    f"vlan {mgmt_vlan}",
    "name STUD2",
    "exit",

    f"interface Vlan{mgmt_vlan}",
    f"ip address {mgmt_ip} {mgmt_mask}",
    "no shutdown",
    "exit",

    f"interface {uplink}",
    "switchport mode access",
    f"switchport access vlan {mgmt_vlan}",
    "no shutdown",
    "exit",

    f"interface {pc_port}",
    "switchport mode access",
    f"switchport access vlan {mgmt_vlan}",
    "no shutdown",
    "exit",

    "crypto key generate rsa modulus 2048",
    "ip ssh version 2",

    "line vty 0 15",
    "login local",
    "transport input ssh",
    "exit",

    "end",
    "write memory"
]

for command in commands:
    ser.write((command + "\r\n").encode())
    time.sleep(1)

time.sleep(3)

output = ser.read_all().decode(errors="ignore")
print(output)

ser.close()