import customtkinter as ctk
import threading
import time
import subprocess
from sms_api import verificar_saldo, comprar_numero, pegar_codigo, cancelar_numero, finalizar_numero
from clonador import clonar_instancia_base, listar_instancias
from ldplayer import iniciar_instancia, mudar_mac
from whatsapp import abrir_whatsapp_e_digitar, inserir_codigo_sms, run_adb_command
from vpn import conectar_vpn, desconectar_vpn, mostrar_ip

import re

LDPLAYER_PATH = r"C:\LDPlayer\LDPlayer9"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("tema_vermelho.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SuperConectador3000")
        self.geometry("500x420")

        self.saldo_label = ctk.CTkLabel(self, text="💰 Saldo: carregando...", font=("Arial", 15, "bold"))
        self.saldo_label.pack(pady=(15, 10))

        self.quantidade_entry = ctk.CTkEntry(self, placeholder_text="Quantidade de ciclos")
        self.quantidade_entry.pack(pady=5)

        self.botao_brasil = ctk.CTkButton(self, text="🇧🇷 Rodar Brasil", command=lambda: self.confirmar_execucao("br"))
        self.botao_brasil.pack(pady=5)

        self.botao_indonesia = ctk.CTkButton(self, text="🇮🇩 Rodar Indonésia", command=lambda: self.confirmar_execucao("id"))
        self.botao_indonesia.pack(pady=5)

        self.botao_apagar = ctk.CTkButton(self, text="🧨 Apagar todas as instâncias", command=self.apagar_instancias)
        self.botao_apagar.pack(pady=5)

        self.resultado_label = ctk.CTkLabel(self, text="", wraplength=450, justify="left")
        self.resultado_label.pack(pady=10)
        conectar_vpn()
        ip = mostrar_ip()
        self.resultado_label.configure(text=f"🌍 IP inicial: {ip}")

        self.atualizar_saldo()


    def atualizar_saldo(self):
        def loop():
            while True:
                bruto = verificar_saldo("br")  # só pra exibição
                if bruto.startswith("ACCESS_BALANCE:"):
                    valor = bruto.split(":")[1]
                    self.saldo_label.configure(text=f"💰 Saldo: {valor} USD")
                else:
                    self.saldo_label.configure(text=f"⚠️ Erro: {bruto}")
                time.sleep(5)
        threading.Thread(target=loop, daemon=True).start()

    def esperar_instancia_running(self, nome, timeout=240):
        inicio = time.time()
        while time.time() - inicio < timeout:
            resultado = subprocess.run([
                f"{LDPLAYER_PATH}\\ldconsole.exe", "list2"], capture_output=True, text=True)
            linhas = resultado.stdout.strip().splitlines()
            for linha in linhas:
                partes = linha.split(",")
                if nome in partes[1]:
                    try:
                        porta_adb = int(partes[3])
                        if porta_adb > 0:
                            print(f"✅ Instância {nome} está rodando com ADB {porta_adb}!")
                            time.sleep(5)
                            return True
                    except:
                        pass
            time.sleep(2)
        return False

    def encontrar_novo_emulador(self, emuladores_antigos, timeout=60):
        adb_path = f"{LDPLAYER_PATH}\\adb.exe"
        inicio = time.time()
        while time.time() - inicio < timeout:
            resultado = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
            linhas = resultado.stdout.strip().splitlines()
            novos = [linha.split("\t")[0] for linha in linhas if linha.startswith("emulator-") and "\tdevice" in linha]
            for emulador in novos:
                if emulador not in emuladores_antigos:
                    print(f"🎯 Novo emulador detectado: {emulador}")
                    return emulador
            time.sleep(2)
        return None

    def confirmar_execucao(self, pais):
        def validar():
            if senha_entry.get() == "1234":
                popup.destroy()
                try:
                    quantidade = int(self.quantidade_entry.get())
                    threading.Thread(target=self.executar_instancia, args=(pais, quantidade), daemon=True).start()
                except:
                    self.resultado_label.configure(text="❌ Quantidade inválida.")
            else:
                popup.destroy()
                self.resultado_label.configure(text="❌ Senha incorreta.")

        popup = ctk.CTkToplevel(self)
        popup.geometry("300x180")
        popup.title("Confirmação")
        popup.lift()
        popup.attributes("-topmost", True)
        popup.after(100, lambda: popup.attributes("-topmost", False))

        label = ctk.CTkLabel(popup, text="Digite a senha para executar:")
        label.pack(pady=10)

        senha_entry = ctk.CTkEntry(popup, show="*")
        senha_entry.pack(pady=5)

        confirmar = ctk.CTkButton(popup, text="Confirmar", command=validar)
        confirmar.pack(pady=10)

    def executar_instancia(self, pais, ciclos):
        
        ip = mostrar_ip()
        self.resultado_label.configure(text=f"🌍 IP atual: {ip}")

        for _ in range(ciclos):
            saldo_raw = verificar_saldo(pais)
            if not saldo_raw.startswith("ACCESS_BALANCE:"):
                self.resultado_label.configure(text="❌ Erro ao verificar saldo.")
                return
            saldo = float(saldo_raw.split(":")[1])
            minimo_necessario = ciclos * 1.6
            if saldo < minimo_necessario:
                self.resultado_label.configure(
                    text=f"⚠️ Saldo insuficiente. Precisa de pelo menos {minimo_necessario:.2f} USD para {ciclos} números.")
                return

            max_price = 1.6 if pais == "br" else 0.4
            activation_id, numero = comprar_numero(pais, max_price=max_price, use_cashback=False)
            numero_limpo = re.sub(r'\D', '', numero)[2:]
            if not activation_id or not numero:
                self.resultado_label.configure(text="❌ Erro ao comprar número.")
                return

            self.resultado_label.configure(text=f"📞 Número comprado: {numero}\nID Ativação: {activation_id}")
            nome = clonar_instancia_base()
            self.resultado_label.configure(text=f"✅ Instância clonada: {nome}\n🚀 Iniciando...")

            subprocess.run([f"{LDPLAYER_PATH}\\adb.exe", "disconnect"], capture_output=True)
            iniciar_instancia(nome)

            if not self.esperar_instancia_running(nome):
                self.resultado_label.configure(text=f"❌ Instância {nome} falhou.")
                cancelar_numero(pais, activation_id)
                continue

            res = subprocess.run([f"{LDPLAYER_PATH}\\adb.exe", "devices"], capture_output=True, text=True)
            emuladores_antes = [linha.split("\t")[0] for linha in res.stdout.strip().splitlines() if linha.startswith("emulator-")]
            emulador = self.encontrar_novo_emulador(emuladores_antes)
            if not emulador:
                self.resultado_label.configure(text="❌ ADB não detectou instância.")
                cancelar_numero(pais, activation_id)
                continue

            run_adb_command(emulador, "shell pm grant com.whatsapp android.permission.RECEIVE_SMS")
            run_adb_command(emulador, "shell pm grant com.whatsapp android.permission.READ_SMS")
            run_adb_command(emulador, "shell pm grant com.whatsapp android.permission.SEND_SMS")

            abrir_whatsapp_e_digitar(emulador, "+" + numero_limpo)
            self.resultado_label.configure(text=f"📲 Número inserido no WhatsApp: +{numero}\n⏳ Aguardando SMS...")

            codigo = None
            tempo_inicial = time.time()
            while time.time() - tempo_inicial < 600:
                codigo = pegar_codigo(pais, activation_id, tentativas=1, intervalo=1)
                if codigo:
                    break
                time.sleep(15)

            if codigo:
                self.resultado_label.configure(text=f"✅ Código recebido: {codigo}")
                inserir_codigo_sms(emulador, codigo)
                finalizar_numero(pais, activation_id)
            else:
                self.resultado_label.configure(text="❌ Código não chegou. Reiniciando...")
                cancelar_numero(pais, activation_id)

            desconectar_vpn()
            conectar_vpn()
            ip = mostrar_ip()
            self.resultado_label.configure(text=f"🌍 IP atualizado: {ip}")


    def apagar_instancias(self):
        def validar_senha():
            if senha_entry.get() == "banana123":
                popup.destroy()
                self.resultado_label.configure(text="🍌 Apagando instâncias...")
                threading.Thread(target=remover_instancias, daemon=True).start()
            else:
                popup.destroy()
                self.resultado_label.configure(text="❌ Senha incorreta.")

        def remover_instancias():
            for nome in listar_instancias():
                if nome.startswith("numero"):
                    comando = [f"{LDPLAYER_PATH}\\ldconsole.exe", "remove", "--name", nome]
                    subprocess.run(comando)
            self.resultado_label.configure(text="✅ Instâncias apagadas.")

        popup = ctk.CTkToplevel(self)
        popup.geometry("300x180")
        popup.title("Confirmação")
        popup.lift()
        popup.attributes("-topmost", True)
        popup.after(100, lambda: popup.attributes("-topmost", False))

        label = ctk.CTkLabel(popup, text="Digite a senha para apagar:")
        label.pack(pady=10)

        senha_entry = ctk.CTkEntry(popup, show="*")
        senha_entry.pack(pady=5)

        confirmar = ctk.CTkButton(popup, text="Confirmar", command=validar_senha)
        confirmar.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
