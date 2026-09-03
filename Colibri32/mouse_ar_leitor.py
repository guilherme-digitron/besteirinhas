import serial
import socket
import pyautogui
import keyboard
import time
import os
import glob

# --- SELEÇÃO DE MODO ---
print("=" * 60)
print("SISTEMA DE MOUSE DE CABEÇA - SELEÇÃO DE CONEXÃO")
print("=" * 60)
print(" 1 - Usar CABO USB (Comunicação Serial)")
print(" 2 - Usar WI-FI (Comunicação Sem Fio UDP)")
print("=" * 60)
opcao = input("Escolha a opção (1 ou 2): ").strip()

MODO = "wifi" if opcao == "2" else "serial"

PORTA_COM = 'COM3'
BAUD_RATE = 115200
UDP_PORT = 12345

esp32_serial = None
sock = None
esp32_ip_cliente = None

pyautogui.PAUSE = 0 
pyautogui.FAILSAFE = False 

congelado = False
ultima_digitacao = 0
TEMPO_GUARDA_DIGITACAO = 0.4

# Inicialização da interface escolhida
if MODO == "serial":
    try:
        esp32_serial = serial.Serial(PORTA_COM, BAUD_RATE, timeout=0.1)
        print(f"[OK] Escutando porta Serial {PORTA_COM}...")
    except Exception as e:
        print(f"[Erro Serial]: {e}")
        exit()
else:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", UDP_PORT))
        sock.settimeout(0.01)
        print(f"[OK] Escutando pacotes Wi-Fi UDP na porta {UDP_PORT}...")
    except Exception as e:
        print(f"[Erro Wi-Fi]: {e}")
        exit()

# --- FUNÇÕES ---

def abrir_lista_atalhos():
    pasta_atual = os.path.dirname(os.path.realpath(__file__))
    arquivos = glob.glob(os.path.join(pasta_atual, "lista-atalhos*"))
    if arquivos:
        os.startfile(arquivos[0])

def centralizar_cursor():
    largura, altura = pyautogui.size()
    pyautogui.moveTo(largura // 2, altura // 2)

def recalibrar_esp32():
    if MODO == "serial" and esp32_serial and esp32_serial.is_open:
        esp32_serial.write(b'R')
        print("[Ação] Sinal de Recalibração enviado via Serial")
    elif MODO == "wifi" and sock and esp32_ip_cliente:
        sock.sendto(b'R', (esp32_ip_cliente, UDP_PORT))
        print("[Ação] Sinal de Recalibração enviado via Wi-Fi")

def alternar_pausa():
    global congelado
    congelado = not congelado
    print(f"[Estado] Mouse: {'PAUSADO' if congelado else 'ATIVO'}")

def registrar_digitacao(e):
    global ultima_digitacao
    if e.name not in ['ctrl', 'alt', 'shift', 'windows']:
        ultima_digitacao = time.time()

def ler_coordenadas():
    global esp32_ip_cliente
    if MODO == "serial":
        if esp32_serial.in_waiting > 0:
            linha = esp32_serial.readline().decode('utf-8', errors='ignore').strip()
            esp32_serial.reset_input_buffer()
            return linha
    else:
        try:
            data, addr = sock.recvfrom(1024)
            esp32_ip_cliente = addr[0] # Guarda o IP do ESP32 para enviar respostas
            return data.decode('utf-8', errors='ignore').strip()
        except socket.timeout:
            return None
    return None

# Mapeamento de Atalhos
keyboard.on_press(registrar_digitacao)
keyboard.add_hotkey('ctrl+alt+windows', abrir_lista_atalhos)
keyboard.add_hotkey('ctrl+alt+r', recalibrar_esp32)
keyboard.add_hotkey('ctrl+alt', centralizar_cursor)
keyboard.add_hotkey('ctrl+alt+p', alternar_pausa)

print("Sistema pronto. Opção de transporte ativa:", MODO.upper())

# --- LOOP PRINCIPAL ---
while True:
    try:
        linha = ler_coordenadas()
        
        if congelado or (time.time() - ultima_digitacao < TEMPO_GUARDA_DIGITACAO):
            continue

        if linha and "," in linha:
            partes = linha.split(',')
            if len(partes) == 2:
                dx = int(partes[0])
                dy = int(partes[1])
                
                if keyboard.is_pressed('shift'):
                    dx = int(dx / 3)
                    dy = int(dy / 3)
                
                if dx != 0 or dy != 0:
                    pyautogui.move(dx, dy)
                    
    except ValueError:
        pass
    except KeyboardInterrupt:
        print("\nEncerrando...")
        break