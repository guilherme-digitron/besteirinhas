import pyautogui
import keyboard
import time
import os
import glob
import ctypes
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

NOME_ARQUIVO_CONFIG = "config_mouse_numpad.json"
config_padrao = {
    "velocidade_inicial": 4.0,
    "velocidade_maxima": 22.0,
    "fator_aceleracao": 1.12,
    "atalhos": [
        {"ferramenta": "Windows / Geral", "atalho": "Ctrl + Alt + Win", "funcao": "Abrir lista de atalhos externa"},
        {"ferramenta": "Windows / Geral", "atalho": "Ctrl + Alt", "funcao": "Centralizar cursor na tela"},
        {"ferramenta": "Windows / Geral", "atalho": "Ctrl + Alt + P", "funcao": "Pausar/Despausar mouse numérico"},
        {"ferramenta": "Numpad Mouse", "atalho": "Num /", "funcao": "Alternar entre botão Esquerdo e Direito"},
        {"ferramenta": "Numpad Mouse", "atalho": "Num 5", "funcao": "Clique simples"},
        {"ferramenta": "Numpad Mouse", "atalho": "Num +", "funcao": "Duplo clique"},
        {"ferramenta": "Numpad Mouse", "atalho": "Shift (segurar)", "funcao": "Modo precisão (velocidade reduzida)"},
        {"ferramenta": "Numpad Mouse", "atalho": "Scroll Lock", "funcao": "Ativar modo de rolagem (Scroll) nas setas"}
    ]
}
def carregar_configuracoes():
    if os.path.exists(NOME_ARQUIVO_CONFIG):
        try:
            with open(NOME_ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "atalhos" not in data:
                    data["atalhos"] = config_padrao["atalhos"]
                return data
        except Exception as e:
            print(f"[Aviso] Erro ao ler {NOME_ARQUIVO_CONFIG}. Usando valores padrão: {e}")
    return config_padrao.copy()

def salvar_configuracoes(data):
    try:
        with open(NOME_ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[Erro] Falha ao salvar arquivo de configurações: {e}")

dados_app = carregar_configuracoes()
congelado = False
botao_atual = 'left'
janela_aberta = False
pressionou_5 = False
pressionou_mais = False
pressionou_barra = False
def verificar_numlock():
    """Verifica se o Num Lock do Windows está ativado."""
    hllDll = ctypes.WinDLL("User32.dll")
    return bool(hllDll.GetKeyState(0x90) & 1)

def verificar_scrolllock():
    """Verifica se o Scroll Lock do Windows está ativado."""
    hllDll = ctypes.WinDLL("User32.dll")
    return bool(hllDll.GetKeyState(0x91) & 1)

def abrir_lista_atalhos():
    pasta_atual = os.path.dirname(os.path.realpath(__file__))
    arquivos = glob.glob(os.path.join(pasta_atual, "lista-atalhos*"))
    if arquivos:
        os.startfile(arquivos[0])

def centralizar_cursor():
    largura, altura = pyautogui.size()
    pyautogui.moveTo(largura // 2, altura // 2)

def alternar_pausa():
    global congelado
    congelado = not congelado
    print(f"[Estado] Mouse NumPad: {'PAUSADO' if congelado else 'ATIVO'}")

def alternar_botao_mouse():
    global botao_atual
    if botao_atual == 'left':
        botao_atual = 'right'
        print("[Ação] Botão Selecionado: DIREITO")
    else:
        botao_atual = 'left'
        print("[Ação] Botão Selecionado: ESQUERDO")

def executar_clique():
    if not congelado and verificar_numlock():
        pyautogui.click(button=botao_atual)

def executar_duplo_clique():
    if not congelado and verificar_numlock():
        pyautogui.doubleClick(button=botao_atual)
def abrir_interface_config():
    global janela_aberta
    if janela_aberta:
        return
    
    janela_aberta = True
    
    root = tk.Tk()
    root.title("Gerenciador de Atalhos e Sensibilidade do Mouse")
    root.geometry("680x520")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use('clam')

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    tab_atalhos = ttk.Frame(notebook)
    notebook.add(tab_atalhos, text=" Atalhos ")

    frame_busca = ttk.Frame(tab_atalhos)
    frame_busca.pack(fill='x', padx=10, pady=5)
    
    ttk.Label(frame_busca, text="Pesquisar:").pack(side='left', padx=(0, 5))
    entry_busca = ttk.Entry(frame_busca)
    entry_busca.pack(side='left', fill='x', expand=True)

    colunas = ("ferramenta", "atalho", "funcao")
    tabela = ttk.Treeview(tab_atalhos, columns=colunas, show='headings', selectmode='browse')
    tabela.heading("ferramenta", text="Ferramenta")
    tabela.heading("atalho", text="Atalho")
    tabela.heading("funcao", text="Função")
    
    tabela.column("ferramenta", width=150)
    tabela.column("atalho", width=150)
    tabela.column("funcao", width=330)
    
    tabela.pack(fill='both', expand=True, padx=10, pady=5)

    def atualizar_tabela(filtro=""):
        for item in tabela.get_children():
            tabela.delete(item)
        for item in dados_app["atalhos"]:
            termo = filtro.lower()
            if (termo in item["ferramenta"].lower() or 
                termo in item["atalho"].lower() or 
                termo in item["funcao"].lower()):
                tabela.insert("", "end", values=(item["ferramenta"], item["atalho"], item["funcao"]))

    atualizar_tabela()

    def filtrar(e):
        atualizar_tabela(entry_busca.get())

    entry_busca.bind("<KeyRelease>", filtrar)

    frame_form = ttk.LabelFrame(tab_atalhos, text=" Cadastrar Novo Atalho ")
    frame_form.pack(fill='x', padx=10, pady=5)

    ttk.Label(frame_form, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)
    entry_ferramenta = ttk.Entry(frame_form, width=15)
    entry_ferramenta.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Atalho:").grid(row=0, column=2, padx=5, pady=5)
    entry_atalho = ttk.Entry(frame_form, width=15)
    entry_atalho.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(frame_form, text="Função:").grid(row=0, column=4, padx=5, pady=5)
    entry_funcao = ttk.Entry(frame_form, width=25)
    entry_funcao.grid(row=0, column=5, padx=5, pady=5)

    def adicionar_atalho():
        f = entry_ferramenta.get().strip()
        a = entry_atalho.get().strip()
        fn = entry_funcao.get().strip()
        
        if f and a and fn:
            novo = {"ferramenta": f, "atalho": a, "funcao": fn}
            dados_app["atalhos"].append(novo)
            salvar_configuracoes(dados_app)
            atualizar_tabela()
            entry_ferramenta.delete(0, tk.END)
            entry_atalho.delete(0, tk.END)
            entry_funcao.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos do atalho!")

    def remover_atalho():
        selecionado = tabela.selection()
        if selecionado:
            item_vals = tabela.item(selecionado[0], "values")
            dados_app["atalhos"] = [
                x for x in dados_app["atalhos"]
                if not (x["ferramenta"] == item_vals[0] and x["atalho"] == item_vals[1] and x["funcao"] == item_vals[2])
            ]
            salvar_configuracoes(dados_app)
            atualizar_tabela(entry_busca.get())

    btn_add = ttk.Button(frame_form, text="Adicionar", command=adicionar_atalho)
    btn_add.grid(row=0, column=6, padx=5, pady=5)

    btn_del = ttk.Button(tab_atalhos, text="Excluir Atalho Selecionado", command=remover_atalho)
    btn_del.pack(anchor='e', padx=10, pady=(0, 5))
    tab_sens = ttk.Frame(notebook)
    notebook.add(tab_sens, text=" Sensibilidade ")

    frame_sens = ttk.Frame(tab_sens)
    frame_sens.pack(fill='both', expand=True, padx=20, pady=20)

    ttk.Label(frame_sens, text="Velocidade Inicial (Precisão de início):").pack(anchor='w', pady=(5, 0))
    scale_vinicial = ttk.Scale(frame_sens, from_=1.0, to=15.0, value=dados_app["velocidade_inicial"])
    scale_vinicial.pack(fill='x', pady=5)
    lbl_vinicial = ttk.Label(frame_sens, text=f"Valor: {dados_app['velocidade_inicial']:.1f}")
    lbl_vinicial.pack(anchor='w')

    ttk.Label(frame_sens, text="Velocidade Máxima (Após aceleração):").pack(anchor='w', pady=(15, 0))
    scale_vmax = ttk.Scale(frame_sens, from_=5.0, to=60.0, value=dados_app["velocidade_maxima"])
    scale_vmax.pack(fill='x', pady=5)
    lbl_vmax = ttk.Label(frame_sens, text=f"Valor: {dados_app['velocidade_maxima']:.1f}")
    lbl_vmax.pack(anchor='w')

    ttk.Label(frame_sens, text="Fator de Aceleração (Suavidade):").pack(anchor='w', pady=(15, 0))
    scale_acel = ttk.Scale(frame_sens, from_=1.01, to=1.35, value=dados_app["fator_aceleracao"])
    scale_acel.pack(fill='x', pady=5)
    lbl_acel = ttk.Label(frame_sens, text=f"Valor: {dados_app['fator_aceleracao']:.2f}")
    lbl_acel.pack(anchor='w')

    def atualizar_labels(val=None):
        lbl_vinicial.config(text=f"Valor: {scale_vinicial.get():.1f}")
        lbl_vmax.config(text=f"Valor: {scale_vmax.get():.1f}")
        lbl_acel.config(text=f"Valor: {scale_acel.get():.2f}")

    scale_vinicial.config(command=atualizar_labels)
    scale_vmax.config(command=atualizar_labels)
    scale_acel.config(command=atualizar_labels)

    def salvar_sensibilidade():
        dados_app["velocidade_inicial"] = round(scale_vinicial.get(), 1)
        dados_app["velocidade_maxima"] = round(scale_vmax.get(), 1)
        dados_app["fator_aceleracao"] = round(scale_acel.get(), 2)
        salvar_configuracoes(dados_app)
        messagebox.showinfo("Sucesso", "Configurações de sensibilidade salvas!")

    btn_salvar_sens = ttk.Button(frame_sens, text="Salvar Sensibilidade", command=salvar_sensibilidade)
    btn_salvar_sens.pack(anchor='e', pady=20)

    def ao_fechar():
        global janela_aberta
        janela_aberta = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()

def abrir_gui_thread():
    threading.Thread(target=abrir_interface_config, daemon=True).start()
TECLAS_NUMPAD = [
    '5', '/', '+', '8', '2', '4', '6', '7', '9', '1', '3', 
    'up', 'down', 'left', 'right', 'home', 'page up', 'end', 'page down'
]

def bloquear_teclas_numpad():
    for tecla in TECLAS_NUMPAD:
        try:
            keyboard.block_key(tecla)
        except Exception:
            pass

bloquear_teclas_numpad()
keyboard.add_hotkey('ctrl+i', abrir_gui_thread)
keyboard.add_hotkey('ctrl+alt+windows', abrir_lista_atalhos)
keyboard.add_hotkey('ctrl+alt', centralizar_cursor)
keyboard.add_hotkey('ctrl+alt+p', alternar_pausa)

print("=" * 60)
print("SISTEMA DE MOUSE VIA TECLADO NUMÉRICO (NUMPAD)")
print("=" * 60)
print(" Pressione CTRL + I para abrir a Interface de Atalhos / Ajustes")
print(" Status: Ligue a tecla NUM LOCK para ativar o controle.")
print(" Mover/Scroll: Teclas 1, 2, 3, 4, 6, 7, 8, 9 (Scroll Lock alterna Modo Scroll)")
print(" Clique: 5 | Duplo Clique: + | Alternar Botão (Esq/Dir): /")
print(" Precisão: Segurar SHIFT reduz a velocidade.")
print("=" * 60)
velocidade_atual = dados_app["velocidade_inicial"]

while True:
    try:
        if not verificar_numlock() or congelado:
            time.sleep(0.05)
            velocidade_atual = dados_app["velocidade_inicial"]
            continue
        if keyboard.is_pressed('5'):
            if not pressionou_5:
                executar_clique()
                pressionou_5 = True
        else:
            pressionou_5 = False

        if keyboard.is_pressed('+'):
            if not pressionou_mais:
                executar_duplo_clique()
                pressionou_mais = True
        else:
            pressionou_mais = False

        if keyboard.is_pressed('/'):
            if not pressionou_barra:
                alternar_botao_mouse()
                pressionou_barra = True
        else:
            pressionou_barra = False
        dx = 0
        dy = 0

        if keyboard.is_pressed('8') or keyboard.is_pressed('up'):
            dy -= 1
        if keyboard.is_pressed('2') or keyboard.is_pressed('down'):
            dy += 1
        if keyboard.is_pressed('4') or keyboard.is_pressed('left'):
            dx -= 1
        if keyboard.is_pressed('6') or keyboard.is_pressed('right'):
            dx += 1
        if keyboard.is_pressed('7') or keyboard.is_pressed('home'):
            dx -= 1
            dy -= 1
        if keyboard.is_pressed('9') or keyboard.is_pressed('page up'):
            dx += 1
            dy -= 1
        if keyboard.is_pressed('1') or keyboard.is_pressed('end'):
            dx -= 1
            dy += 1
        if keyboard.is_pressed('3') or keyboard.is_pressed('page down'):
            dx += 1
            dy += 1

        if dx != 0 or dy != 0:
            if verificar_scrolllock():
                if dy != 0:
                    pyautogui.scroll(int(-dy * (velocidade_atual * 12)))
                if dx != 0:
                    pyautogui.hscroll(int(dx * (velocidade_atual * 12)))
            else:
                passo_x = dx * velocidade_atual
                passo_y = dy * velocidade_atual

                if keyboard.is_pressed('shift'):
                    passo_x /= 3
                    passo_y /= 3

                pyautogui.move(passo_x, passo_y)

            velocidade_atual = min(
                velocidade_atual * dados_app["fator_aceleracao"], 
                dados_app["velocidade_maxima"]
            )
            time.sleep(0.01)
        else:
            velocidade_atual = dados_app["velocidade_inicial"]
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nEncerrando o Mouse Numpad...")
        break
    except Exception:
        time.sleep(0.01)