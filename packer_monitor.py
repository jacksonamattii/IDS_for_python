import socket
import struct
import os

# Verifica se o arquivo com a lista de IPs existe
if not os.path.exists('iplist.txt'):
    print("Error: 'iplist.txt' file not found.")
    exit()

# Lê a lista de IPs monitorados
with open('iplist.txt', 'r') as file:
    monitored_ips = {line.strip() for line in file.readlines()}  # Usando conjunto para busca mais eficiente

# Criando o socket de captura de pacotes (RAW)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind(("0.0.0.0", 0))  # Captura pacotes de todas as interfaces
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # No Windows, pode ser necessário ativar o modo promíscuo
    # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    print("Listening for incoming packets...")
except PermissionError:
    print("Error: You need to run this script as root (sudo).")
    exit()

# Loop de captura de pacotes
while True:
    packet, addr = s.recvfrom(65565)  # Captura pacotes

    # Extrai o cabeçalho IP
    ip_header = packet[0:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    # Calcula o tamanho do cabeçalho
    version_ihl = iph[0]
    ihl = version_ihl & 0xF
    iph_length = ihl * 4

    # Obtém os endereços IP de origem e destino
    src_addr = socket.inet_ntoa(iph[8])
    dst_addr = socket.inet_ntoa(iph[9])

    # Verifica se os IPs estão na lista de monitoramento
    if src_addr in monitored_ips:
        print(f"⚠️ ALERTA: Conexão de entrada de IP na blacklist: {src_addr}")

    if dst_addr in monitored_ips:
        print(f"⚠️ ALERTA: Conexão de saída para IP na blacklist: {dst_addr}")
