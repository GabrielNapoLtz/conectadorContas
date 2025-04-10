import subprocess
import time
import os
import requests

# Caminhos fixos
OPENVPN_EXE = r"C:\Program Files\OpenVPN\bin\openvpn.exe"
CAMINHO_OVPN = r"E:\superfabricadordecontas3000\vpn\br-44.protonvpn.udp.ovpn"
CAMINHO_AUTH = os.path.join(os.path.dirname(CAMINHO_OVPN), "auth.txt")

def mostrar_ip():
    try:
        resultado = subprocess.run(["curl", "ifconfig.me"], capture_output=True, text=True)
        ip = resultado.stdout.strip()
        print(f"🌍 IP atual: {ip}")
        return ip
    except Exception as e:
        print(f"⚠️ Erro ao obter IP: {e}")
        return "desconhecido"

def internet_ok():
    try:
        requests.get("https://api.sms-activate.ae", timeout=5)
        return True
    except:
        return False


def conectar_vpn():
    while True:
        print("🔐 Conectando VPN...")
        subprocess.Popen([
            OPENVPN_EXE,
            "--config", CAMINHO_OVPN,
            "--auth-user-pass", CAMINHO_AUTH
        ])
        time.sleep(15)

        if internet_ok():
            ip = mostrar_ip()
            print(f"✅ VPN conectada com IP limpo: {ip}")
            break
        else:
            print("❌ IP bloqueado ou sem internet. Reconectando...")
            desconectar_vpn()
            time.sleep(5)

def desconectar_vpn():
    subprocess.run("taskkill /f /im openvpn.exe", shell=True)
    print("🔌 VPN desconectada.")
