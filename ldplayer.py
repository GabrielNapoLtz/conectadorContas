import subprocess
import os
import re
import random

LDPLAYER_PATH = r"C:\LDPlayer\LDPlayer9"  # ajuste se necessário

def gerar_nome_instancia():
    existentes = listar_instancias()
    numeros = [int(re.search(r'numero(\d+)', nome).group(1)) for nome in existentes if re.match(r'numero\d+', nome)]
    proximo_num = max(numeros, default=0) + 1
    return f"numero{proximo_num}"

def listar_instancias():
    comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "list"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    linhas = resultado.stdout.strip().splitlines()
    return [linha.split(',')[0] for linha in linhas if linha]

def criar_instancia(nome=None):
    if nome is None:
        nome = gerar_nome_instancia()
    comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "add", "--name", nome]
    subprocess.run(comando)
    return nome

def iniciar_instancia(nome):
    comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "launch", "--name", nome]
    subprocess.run(comando)

def conectar_adb(nome, timeout=240):
    import time
    inicio = time.time()

    while time.time() - inicio < timeout:
        comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "adb", "--name", nome, "--command", "devices"]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        saida = resultado.stdout.strip().splitlines()
        for linha in saida:
            if linha.strip().endswith("device") and not linha.startswith("List of"):
                return "\n".join(saida)

        time.sleep(3)

    return "❌ Dispositivo não apareceu no ADB dentro do tempo limite."



def gerar_mac_aleatorio():
    return "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
def mudar_mac(nome):
    novo_mac = gerar_mac_aleatorio()
    comandos_adb = [
        f"shell su -c 'ifconfig wlan0 hw ether {novo_mac}'",
        f"shell su -c 'svc wifi disable'",
        f"shell su -c 'svc wifi enable'"
    ]
    for cmd in comandos_adb:
        comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "adb", "--name", nome, "--command", cmd]
        subprocess.run(comando)
    return novo_mac

