from pywinauto.application import Application
from pywinauto import Desktop
import time
import keyboard
import threading

# Inicia o exe
app = Application(backend="uia").start(r"./SPED.exe")

# Conecta na janela principal pelo título
win = Desktop(backend="uia").window(title_re="SPED -.*")
win.set_focus()


def print_ids():
    other_win = Desktop(backend="uia").window(
        title_re=".*Validação.*", control_type="Window"
    )
    other_win.print_control_identifiers()


def auto_login():
    print("F3 pressed! Attempting to auto-login...")
    # Entrar no input de senha
    win.type_keys("{TAB}{TAB}")
    # Digita a senha
    win.type_keys("7711")
    win.child_window(title="Logar", control_type="Button").click_input()


def clicar_quando_aparecer(window, titulo, timeout=10):
    tempo_inicio = time.time()
    while time.time() - tempo_inicio < timeout:
        try:
            button = window.child_window(title=titulo, control_type="Button")
            button.click_input()
            print(f"Botão '{titulo}' clicado!")
            return True
        except:
            time.sleep(0.5)  # Espera 500ms antes de tentar novamente
    print(f"Botão '{titulo}' não apareceu após {timeout}s")
    return False


def corrigirCest(window):
    window.set_focus()
    time.sleep(0.4)
    # Clica na Lupa
    window.child_window(auto_id="btnPesquisarCEST").click_input()
    time.sleep(0.5)
    try:
        # Clica duas vezes no primeiro cest
        cest1 = window.child_window(title="CEST Linha 1", control_type="DataItem")
        cest1.double_click_input()
    except:
        # Caso não tenha cest, clica em "Sem Cest"
        print("CEST Linha 1 not found, trying CEST Linha 0")
        cest0 = window.child_window(title="CEST Linha 0", control_type="DataItem")
        cest0.double_click_input()
    window.child_window(title="Salvar", control_type="Button").click_input()
    clicar_quando_aparecer(window, "OK")


def list_windows():
    for win in Desktop(backend="uia").windows():
        print(win.window_text())


# Variável de controle do loop
loop_running = False
loop_thread = None


def toggle_and_run_loop():
    global loop_running, loop_thread
    loop_running = not loop_running
    if loop_running:
        print("Loop INICIADO! Pressione F4 novamente para parar.")
        # Inicia o loop em uma thread separada
        loop_thread = threading.Thread(target=executar_loop, daemon=True)
        loop_thread.start()
    else:
        print("Loop PARADO!")


def executar_loop():
    global loop_running
    window = Desktop(backend="uia").window(
        title_re=".*Validação.*", control_type="Window"
    )
    # Navega até o botão "Corrigir"
    window.type_keys("{TAB}{TAB}{TAB}{TAB}{TAB}")

    while loop_running and app.is_process_running():
        try:
            print("Executando tarefa do loop...")
            # Clica em Corrigir
            window.type_keys("{SPACE}")
            corrigirCest(window)
            time.sleep(1)
        except Exception as e:
            print(f"Erro no loop: {e}")
            time.sleep(1)
    print("Loop finalizado.")


keyboard.on_press_key("f3", lambda _: auto_login())
keyboard.on_press_key("f2", lambda _: list_windows())
keyboard.on_press_key("f1", lambda _: print_ids())
keyboard.on_press_key("f4", lambda _: toggle_and_run_loop())

# Keep listening until the SPED.exe process exits
print("Aguardando pressionamento de teclas:")
print("  F3 - Auto-login")
print("  F4 - Corrigir CEST (entrar ou sair do loop)")
print("Feche SPED.exe para sair.")
while app.is_process_running():
    time.sleep(0.1)  # Check every 100ms

print("SPED.exe fechado. Saindo do script.")
