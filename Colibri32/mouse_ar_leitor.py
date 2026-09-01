"""
MOUSE AEREO - Leitor Serial (Windows)
--------------------------------------
Le as linhas "dx,dy" enviadas pelo ESP32 via cabo USB
e move o cursor do mouse de verdade.

INSTALAR ANTES DE RODAR (uma vez so):
    pip install pyserial pynput

COMO USAR:
    1. Feche o Monitor Serial da Arduino IDE (a porta so pode
       ser usada por um programa por vez)
    2. Descubra o numero da porta COM do ESP32:
       Gerenciador de Dispositivos (Device Manager) -> Portas (COM & LPT)
       Vai aparecer algo como "Silicon Labs CP210x (COM5)" ou
       "USB-SERIAL CH340 (COM7)"
    3. Ajuste a variavel PORTA abaixo com o numero certo
    4. Rode: python mouse_ar_leitor.py
    5. Para parar, feche a janela ou Ctrl+C
"""

import serial
import time
import traceback
from pynput.mouse import Controller

# ============ AJUSTE AQUI ============
PORTA = "COM4"       # troque pelo numero da sua porta COM
BAUD_RATE = 115200
DEBUG = True         # True = mostra tudo que chega, mesmo o que nao reconhece
# ======================================

mouse = Controller()

def conectar():
    while True:
        try:
            ser = serial.Serial(PORTA, BAUD_RATE, timeout=1)
            print(f"Conectado em {PORTA}")
            return ser
        except serial.SerialException:
            print(f"Nao foi possivel abrir {PORTA}. Tentando de novo em 2s...")
            print("Verifique se a porta esta certa e se o Monitor Serial da IDE esta fechado.")
            time.sleep(2)

def main():
    ser = conectar()
    ultimo_dado = time.time()

    while True:
        try:
            linha = ser.readline().decode("utf-8", errors="ignore").strip()

            if not linha:
                if DEBUG and (time.time() - ultimo_dado > 3):
                    print("...nenhum dado recebido nos ultimos segundos (silencio na serial)")
                    ultimo_dado = time.time()
                continue

            ultimo_dado = time.time()

            partes = linha.split(",")
            if len(partes) != 2:
                if DEBUG:
                    print(f"[ignorado, formato inesperado] {linha}")
                continue  # ignora qualquer linha que nao seja "dx,dy"

            dx = int(partes[0])
            dy = int(partes[1])

            if DEBUG:
                print(f"movendo dx={dx} dy={dy}")

            mouse.move(dx, dy)

        except (ValueError, UnicodeDecodeError):
            continue  # ignora linha corrompida/lixo

        except serial.SerialException:
            print("Conexao serial perdida. Reconectando...")
            ser.close()
            ser = conectar()

        except KeyboardInterrupt:
            print("Encerrado pelo usuario.")
            break

        except Exception:
            # Mostra o erro real em vez de sumir com exit code 1 sem explicação
            print("ERRO INESPERADO:")
            traceback.print_exc()
            time.sleep(1)

    ser.close()

if __name__ == "__main__":
    main()
