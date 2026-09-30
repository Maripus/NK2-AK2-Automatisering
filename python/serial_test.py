import serial
import time

console = serial.Serial(
    port="COM3",
    baudrate=9600,
    timeout=2
)

time.sleep(2)

print("Svarar no på initial configuration dialog...")

console.write(b"no\r\n")
console.flush()

time.sleep(2)

console.write(b"\r\n")
console.flush()

time.sleep(3)

output = console.read_all().decode(errors="ignore")
print(output)

console.close()