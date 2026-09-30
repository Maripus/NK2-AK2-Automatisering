import serial
import time
import getpass

# Input fra bruker
com_port = input("COM-port: ")
hostname = input("Hostname: ")
domain = input("Domain name: ")
username = input("SSH-brukernavn: ")
password = getpass.getpass("SSH-passord: ")

interface = input("Interface: ")
ip_address = input("IP-adresse: ")
subnet_mask = input("Subnet mask: ")

# Åpne serial-forbindelsen
console = serial.Serial(
    port=com_port,
    baudrate=9600,
    timeout=1
)

time.sleep(2)


def send(command, wait=1):
    print(f"Sender: {command}")
    console.write((command + "\r\n").encode())
    console.flush()
    time.sleep(wait)


# Ctrl+Z slik at vi starter fra vanlig privileged mode
console.write(b"\x1a\r\n")
time.sleep(1)

# Cisco-konfigurasjon
send("enable")
send("configure terminal")

send(f"hostname {hostname}")
send(f"ip domain-name {domain}")
send(f"username {username} privilege 15 secret {password}")

send(f"interface {interface}")
send(f"ip address {ip_address} {subnet_mask}")
send("no shutdown")
send("exit")

send("crypto key generate rsa modulus 2048", 5)

send("ip ssh version 2")

send("line vty 0 4")
send("login local")
send("transport input ssh")
send("exit")

send("end")
send("write memory", 3)

# Vis output
output = console.read_all().decode(errors="ignore")

print("\n--- Output fra Cisco-enheten ---")
print(output)

console.close()

print("SSH-oppsett ferdig.")