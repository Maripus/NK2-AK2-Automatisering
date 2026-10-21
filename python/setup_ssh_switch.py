import serial
import time
import getpass

print("=== Cisco switch SSH bootstrap ===")

com_port = input("COM-port [COM4]: ") or "COM4"
hostname = input("Hostname: ")
domain = input("Domain [lab.local]: ") or "lab.local"
username = input("SSH-brukernavn [admin]: ") or "admin"
password = getpass.getpass("SSH-passord: ")

print("\nVelg switch-type:")
print("1 = Multilayer switch / CORE")
print("2 = Layer 2 switch")

switch_type = input("Valg [1/2]: ")

commands = [
    "enable",
    "configure terminal",
    f"hostname {hostname}",
    f"ip domain-name {domain}",
    f"username {username} privilege 15 secret {password}",
]

if switch_type == "1":
    interface = input("Management-interface [GigabitEthernet1/0/1]: ") or "GigabitEthernet1/0/1"
    ip = input("Management-IP [172.16.2.2]: ") or "172.16.2.2"
    mask = input("Subnet mask [255.255.255.0]: ") or "255.255.255.0"

    commands += [
        f"interface {interface}",
        "no switchport",
        f"ip address {ip} {mask}",
        "no shutdown",
        "exit",
    ]

elif switch_type == "2":
    vlan = input("Management VLAN [10]: ") or "10"
    ip = input("Management-IP: ")
    mask = input("Subnet mask [255.255.255.0]: ") or "255.255.255.0"
    uplink = input("Trunk-port for management [FastEthernet0/1]: ") or "FastEthernet0/1"
    gateway = input("Default gateway [192.168.10.1]: ") or "192.168.10.1"

    commands += [
        f"vlan {vlan}",
        f"name MGMT",
        "exit",
        f"interface Vlan{vlan}",
        f"ip address {ip} {mask}",
        "no shutdown",
        "exit",
        f"interface {uplink}",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {vlan}",
        "no shutdown",
        "exit",
        f"ip default-gateway {gateway}",
    ]

else:
    print("Ugyldig valg.")
    exit()

commands += [
    "crypto key generate rsa modulus 2048",
    "ip ssh version 2",
    "line vty 0 15",
    "login local",
    "transport input ssh",
    "exit",
    "end",
    "write memory",
]

print("\nKontroller fysisk at konsollkabelen står i riktig Cisco-switch.")
if input("Skriv JA for å sende konfigurasjonen: ").strip().lower() != "ja":
    raise SystemExit("Avbrutt.")

console = serial.Serial(
    port=com_port,
    baudrate=9600,
    timeout=1
)

time.sleep(2)

# Vekk konsollen
console.write(b"\r\n")
time.sleep(1)

# Hvis enheten spør om initial configuration dialog
console.write(b"no\r\n")
time.sleep(2)

for command in commands:
    # Ikke skriv passordkommandoen til skjermen
    if command.startswith("username"):
        print("Sender: oppretter SSH-bruker")
    else:
        print(f"Sender: {command}")

    console.write((command + "\r\n").encode())
    time.sleep(1)

time.sleep(3)

output = console.read_all().decode(errors="ignore")
print("\n--- Output fra Cisco-enheten ---")
if password:
    output = output.replace(password, "[SKJULT]")
print(output)

console.close()

print("\nSSH-kommandoer sendt. Kontroller med ping og SSH at oppsettet fungerer.")
