import serial
import time

console = serial.Serial(
    port="COM3",       # Endre til riktig COM-port
    baudrate=9600,
    timeout=1
)

time.sleep(2)

# Ctrl+Z sørger for at vi kommer ut av config mode
console.write(b"\x1a\r\n")
time.sleep(1)

console.write(b"show ip interface brief\r\n")
time.sleep(3)

output = console.read_all().decode(errors="ignore")
print(output)

console.close()