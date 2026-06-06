# Laboratorio 4: Ataque de Denegación de Servicio mediante DHCP Starvation

## 🎥 Enlace del Video Demostrativo
[Haz clic aquí para ver la demostración del laboratorio en Google Drive]https://drive.google.com/file/d/1S5lCxFFF9Z9AfMq8C1rLZAmczzzGDSXc/view?usp=sharing

---

## 1. Objetivo del Laboratorio
El propósito de esta práctica es demostrar la ejecución de un ataque de Denegación de Servicio (DoS) contra la infraestructura de red local, específicamente orientado al agotamiento de recursos del servidor DHCP legítimo del Router (R1). El fin es comprender el impacto de la falta de control de accesos en la Capa 2 y analizar los mecanismos de hardening requeridos.

---

## 2. Objetivo del Script
El script desarrollado en Python y Scapy tiene la finalidad de automatizar una inundación masiva de tramas broadcast. Genera de forma continua direcciones MAC de origen aleatorias (`RandMAC`) y las asocia con identificadores de transacción únicos (`xid`) dentro de peticiones `DHCP DISCOVER`. Al procesar esto, el Router reserva una dirección IP del pool legítimo para cada cliente ficticio, agotando la totalidad de su espacio de direccionamiento disponible en cuestión de segundos.

---

## 3. Documentación de la Red
* **Mi Matrícula:** 2024-2421
* **Segmento de Red Local:** `10.24.21.0/24`
* **IP del Servidor DHCP / Gateway (R1):** `10.24.21.1`
* **IP del Atacante (Kali Linux):** `10.24.21.2`
* **Interfaz de Inyección:** `eth0`

---

## 4. Evidencias de Funcionamiento (PoC)
<img width="912" height="670" alt="image" src="https://github.com/user-attachments/assets/94c24def-2d8c-4abd-a7ae-c9398d255415" />
<img width="565" height="433" alt="image" src="https://github.com/user-attachments/assets/3e0f5f60-2aef-4882-89e7-328ee43ee441" />


---

## 5. Medidas Técnicas de Mitigación (Hardening)
Para neutralizar de forma efectiva el vector de ataque de DHCP Starvation, se deben aplicar las siguientes directivas de seguridad en los switches de acceso de la infraestructura:

1. **DHCP Snooping:** Configura la base de datos de enlaces confiables para inspeccionar el tráfico DHCP que transita por la red.
2. **Rate Limiting (Límite de Tasa):** Se restringe la cantidad máxima de paquetes DHCP permitidos por segundo en todos los puertos clasificados como "untrusted" (puertos de usuarios finales). Si un script intenta inundar la red excediendo el umbral establecido, el switch cambia el estado del puerto a `err-disable`, apagándolo inmediatamente y generando una alerta de seguridad.

### Ejemplo de Configuración en switches Cisco:
```text
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 1
Switch(config)# interface FastEthernet 0/5
Switch(config-if)# ip dhcp snooping limit rate 10
