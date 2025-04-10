import subprocess
import time
import re

LDPLAYER_PATH = r"C:\LDPlayer\LDPlayer9"

def run_adb_command(device_id, cmd, timeout=10):
    adb_path = f"{LDPLAYER_PATH}\\adb.exe"
    full_cmd = [adb_path, "-s", device_id] + cmd.split()
    return subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)

def tocar_em(device_id, x, y):
    run_adb_command(device_id, f"shell input tap {x} {y}")
    time.sleep(2)

def abrir_whatsapp_e_digitar(device_id, numero):
    print("▶️ Abrindo WhatsApp...")
    run_adb_command(device_id, "shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1")
    time.sleep(10)

    print("👉 Tocando em 'Concordar e continuar'")
    tocar_em(device_id, 360, 1220)
    time.sleep(3)

    print("👉 Tocando no campo do número")
    tocar_em(device_id, 300, 660)
    time.sleep(1)

    print(f"⌨️ Digitando número...{numero}")
    numero_formatado = numero.replace("+", "").replace(" ", "").replace("-", "")
    run_adb_command(device_id, f"shell input text {numero_formatado}")
    time.sleep(1)

    print("👉 Tocando em 'Seguinte'")
    tocar_em(device_id, 360, 1220)
    time.sleep(10)

    print("👉 Confirmando 'Sim'")
    tocar_em(device_id, 530, 745)
    time.sleep(3)

def device_id_to_nome(device_id):
    porta = device_id.split('-')[1]
    resultado = subprocess.run(
        [f"{LDPLAYER_PATH}\\ldconsole.exe", "list2"],
        capture_output=True, text=True
    )
    for linha in resultado.stdout.strip().splitlines():
        partes = linha.split(',')
        if len(partes) > 3 and partes[3] == porta:
            return partes[1]
    return None

def inserir_codigo_sms(device_id, codigo):
    print(f"⌨️ Inserindo código: {codigo}")
    time.sleep(1)
    run_adb_command(device_id, f"shell input text {codigo}")
    time.sleep(10)
    tocar_em(device_id, 250, 1000)
    time.sleep(2)
    tocar_em(device_id, 250, 1000)
    time.sleep(2)
    run_adb_command(device_id, f"shell input text Maria Silva")
    print("👉 Tocando em 'Concordar e continuar'")
    tocar_em(device_id, 360, 1220)
    time.sleep(5)
    tocar_em(device_id, 360, 1220)
    time.sleep(5)
    tocar_em(device_id, 677, 110)
    time.sleep(5)
    tocar_em(device_id, 350, 790)
    time.sleep(5)
    tocar_em(device_id, 320, 450)
    time.sleep(5)
    tocar_em(device_id, 200, 560)
    time.sleep(5)
    tocar_em(device_id, 350, 1200)
    time.sleep(5)
    run_adb_command(device_id, f"shell input text 777777")
    time.sleep(3)
    run_adb_command(device_id, f"shell input text 777777")
    tocar_em(device_id, 350, 1200)
    time.sleep(5)
    tocar_em(device_id, 350, 1200)
    time.sleep(1)
    tocar_em(device_id, 500, 750)
    run_adb_command(device_id, f"shell input text {codigo}") 
    nome = device_id_to_nome(device_id)
    if nome:
        subprocess.run([f"{LDPLAYER_PATH}\\ldconsole.exe", "quit", "--name", nome])
    else:
        print(f"⚠️ Não foi possível identificar o nome da instância para {device_id}")
