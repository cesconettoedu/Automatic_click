import os
import signal
import subprocess
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime

# ==========================
# CONFIGURAÇÕES
# ==========================
VPN_CONFIG = "client.ovpn"
URL_TESTE = "https://www.freeresizenow.com"
NUM_CICLOS = 100
TEMPO_ESPERA = 5  # segundos entre ciclos
TEMPO_CONEXAO_VPN = 10  # segundos para VPN conectar
# ==========================

def print_log(msg, ok=False, warn=False, error=False):
    agora = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    prefix = ""
    if ok: prefix = "✓ "
    elif warn: prefix = "⚠ "
    elif error: prefix = "❌ "
    print(f"{agora} {prefix}{msg}")
    sys.stdout.flush()

def get_ip():
    try:
        r = requests.get("https://api.ipify.org", timeout=10)
        return r.text.strip()
    except Exception as e:
        print_log(f"Erro ao obter IP: {e}", warn=True)
        return None

def conectar_vpn():
    print_log("Conectando VPN via openvpn...")
    try:
        proc = subprocess.Popen(
            ["sudo", "openvpn", "--config", VPN_CONFIG],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print_log(f"Processo OpenVPN iniciado (PID: {proc.pid})")
        print_log(f"Aguardando {TEMPO_CONEXAO_VPN}s para VPN conectar...")
        time.sleep(TEMPO_CONEXAO_VPN)
        return proc
    except Exception as e:
        print_log(f"Erro ao conectar VPN: {e}", error=True)
        return None

def desconectar_vpn():
    print_log("Desconectando VPN...")
    try:
        subprocess.run(["sudo", "killall", "openvpn"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_log("✓ Processos OpenVPN terminados")
    except Exception as e:
        print_log(f"Erro ao terminar processo VPN: {e}", warn=True)

def testar_firefox():
    try:
        print_log("Inicializando Firefox (headless)...")
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(20)

        print_log(f"Navegando para: {URL_TESTE}")
        driver.get(URL_TESTE)
        time.sleep(3)

        titulo = driver.title
        print_log(f"✓ Página carregada: {titulo}")
        print_log(f"URL atual: {driver.current_url}")

        print_log("Aguardando no site...")
        time.sleep(5)

        driver.quit()
        print_log("✓ Firefox fechado")
        return True
    except Exception as e:
        print_log(f"Erro no Firefox: {e}", warn=True)
        return False

def main():
    print_log("=== Iniciando VPN Loop Automator ===")

    # Verificações iniciais
    if not os.path.exists(VPN_CONFIG):
        print_log(f"Arquivo de configuração {VPN_CONFIG} não encontrado!", error=True)
        sys.exit(1)

    print_log(f"VPN_CONFIG: {VPN_CONFIG}")
    print_log(f"URL_TESTE: {URL_TESTE}")
    print_log(f"NUM_CICLOS: {NUM_CICLOS}")
    print_log(f"TEMPO_ESPERA: {TEMPO_ESPERA}s")

    ip_inicial = get_ip()
    if ip_inicial:
        print_log(f"IP atual: {ip_inicial}")

    # Loop principal
    for ciclo in range(1, NUM_CICLOS + 1):
        print_log(f"--- Ciclo #{ciclo} ---")

        ip_antes = get_ip()
        proc = conectar_vpn()

        if not proc:
            print_log("Falha ao iniciar VPN", error=True)
            continue

        ip_depois = get_ip()
        if ip_depois and ip_antes and ip_depois == ip_antes:
            print_log("⚠ VPN conectada, mas IP não mudou", warn=True)

        else:
            print_log("✓ VPN conectada", ok=True)

        # Testar Firefox
        sucesso = testar_firefox()

        # Desconectar VPN
        desconectar_vpn()

        if sucesso:
            print_log(f"Ciclo {ciclo} finalizado com sucesso ✅")
        else:
            print_log(f"Ciclo {ciclo} falhou ❌", error=True)

        if ciclo < NUM_CICLOS:
            print_log(f"Aguardando {TEMPO_ESPERA}s...")
            time.sleep(TEMPO_ESPERA)

    print_log("Finalizado. Até logo!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_log("Sinal recebido. Encerrando...")
        print_log("Executando limpeza final...")
        desconectar_vpn()
