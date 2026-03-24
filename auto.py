from pywinauto.application import Application
from pywinauto import Desktop
import time
import keyboard
import threading
from pywinauto.keyboard import SendKeys


def abrir_sped(timeout=10):
    app_iniciado = Application(backend="uia").start(r"./SPED.exe")
    janela_principal = Desktop(backend="uia").window(title_re="SPED -.*")
    janela_principal.wait("visible ready", timeout=timeout)
    janela_principal.set_focus()
    print("SPED.exe não estava aberto. Aplicação iniciada automaticamente.")
    return app_iniciado, janela_principal


def conectar_sped_em_execucao(timeout=10):
    try:
        janela_principal = Desktop(backend="uia").window(title_re="SPED -.*")
        janela_principal.wait("visible ready", timeout=timeout)
        app_conectado = Application(backend="uia").connect(
            process=janela_principal.process_id()
        )
        janela_principal.set_focus()
        print("Conectado ao SPED já em execução.")
        return app_conectado, janela_principal
    except Exception:
        return abrir_sped(timeout=timeout)


app, win = conectar_sped_em_execucao()


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


def corrigir_pis_cofins(window):
    window.set_focus()
    window.child_window(title_re=".*Pis/COFINS", control_type="TabItem").click_input()
    window.child_window(
        control_type="ComboBox", auto_id="cbSdPisCofinsGrupoReceita"
    ).click_input()
    SendKeys("{DOWN}{ENTER}")

    window.child_window(
        control_type="ComboBox", auto_id="cbSdPisCofinsNaturezaReceita"
    ).click_input()

    SendKeys("{DOWN}{ENTER}")
    window.child_window(title="Salvar", control_type="Button").click_input()
    clicar_quando_aparecer(window, "OK")


def clicar_quando_aparecer(window, titulo, timeout=10):
    tempo_inicio = time.time()
    while time.time() - tempo_inicio < timeout:
        time.sleep(0.01)
        try:
            button = window.child_window(title=titulo, control_type="Button")
            if button.exists():
                try:
                    message_elem = window.child_window(
                        title_re="Código Natureza inválido.*", control_type="Text"
                    )
                    message = (
                        message_elem.window_text()
                        if message_elem.exists()
                        else ""
                    )

                except Exception:
                    message = ""
                finally:
                    button.click_input()
                if message:
                    corrigir_pis_cofins(window)
                    print(f"Botão '{titulo}' clicado! Mensagem: {message}")
                else:
                    print(f"Botão '{titulo}' clicado!")
                return True
        except Exception:
            time.sleep(0.02) # Espera um pouco antes de tentar novamente
    print(f"Botão '{titulo}' não apareceu após {timeout}s")
    return False


def corrigirCest(window):
    window.set_focus()
    # Clica na Lupa
    window.child_window(auto_id="btnPesquisarCEST").click_input()
    try:
        # Clica duas vezes no primeiro cest
        cest1 = window.child_window(title="CEST Linha 1", control_type="DataItem")
        cest1.double_click_input()
    except:
        # Caso não tenha cest, clica em "Sem Cest"
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
        loop_thread = threading.Thread(target=executar_loop_correcao, daemon=True)
        loop_thread.start()
    else:
        print("Loop PARADO!")


def executar_loop_correcao():
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
        except Exception as e:
            print(f"Erro no loop: {e}")
            time.sleep(0.3)
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
