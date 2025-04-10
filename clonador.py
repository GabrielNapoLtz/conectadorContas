import subprocess
import re

LDPLAYER_PATH = r"C:\LDPlayer\LDPlayer9"  # ajusta se for diferente

def listar_instancias():
    comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "list"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    linhas = resultado.stdout.strip().splitlines()
    return [linha.split(',')[0] for linha in linhas if linha]

def gerar_nome_instancia():
    existentes = listar_instancias()
    numeros = [int(re.search(r'numero(\d+)', nome).group(1)) for nome in existentes if re.match(r'numero\d+', nome)]
    proximo_num = max(numeros, default=0) + 1
    return f"numero{proximo_num}"

def clonar_instancia_base(base="base", nome_novo=None):
    if nome_novo is None:
        nome_novo = gerar_nome_instancia()
    comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "copy", "--name", nome_novo, "--from", base]
    subprocess.run(comando)
    return nome_novo


