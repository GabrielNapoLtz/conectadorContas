# SuperConectador3000 ✨

Automatize a criação e ativação de contas no WhatsApp usando instâncias LDPlayer, números SMS Activate e controle via Python com interface customtkinter. Ideal para testes em massa, automação comercial e integrações.

---

## ⚙️ Requisitos

### Python
- Python 3.10 ou superior
- Instale os pacotes:
  ```bash
  pip install customtkinter requests
  ```

### LDPlayer
- Baixe e instale o LDPlayer 9
- Crie uma instância chamada `base`
- Na instância base:
  - Instale o WhatsApp (APK ou LD Store)
  - Ative o modo desenvolvedor
  - Ative as opções:
    - **Root**
    - **Depuração USB / ADB**
  - Ajuste a resolução para `720x1280`
  - NÃO feche a base enquanto o programa estiver rodando

### API do SMS Activate
- Cadastre-se em https://sms-activate.guru/en/api2
- Pegue sua `api_key`
- Insira nos arquivos:
  - `config_brasil.py`
  - `config_indonesia.py`

### VPN com ProtonVPN (recomendado)
- Baixe o **OpenVPN** no site oficial: https://openvpn.net/community-downloads/
- Instale o OpenVPN em sua máquina
- Após instalar:
  - Vá até a pasta onde o OpenVPN foi instalado (ex: `C:\Program Files\OpenVPN\bin`)
  - Copie esse caminho
  - Abra o menu Iniciar e pesquise por **variáveis de ambiente**
  - Clique em **Variáveis de Ambiente > Path > Editar > Novo**
  - Cole o caminho e salve
- Baixe o arquivo `.ovpn` da sua conta ProtonVPN (via painel web)
- Crie um `auth.txt` com:
  ```
  SEU_USUARIO
  SUA_SENHA
  ```
- O sistema já está preparado para:
  - Conectar automaticamente à VPN antes de cada ciclo
  - Usar IPs diferentes por sessão usando esse `.ovpn`

---

## 🔢 Como usar (passo a passo)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuuser/superconectador3000.git
   cd superconectador3000
   ```

2. **Configure as chaves de API:**
   - Edite `config_brasil.py` e `config_indonesia.py`
   ```python
   API_KEY = "sua_api_key_aqui"
   CODIGO_PAIS = 73  # ou 6 para indonésia
   SERVICO = 'wa'
   ```

3. **Configure a VPN:**
   - Baixe e instale o OpenVPN (https://openvpn.net/community-downloads/)
   - Adicione o caminho do executável `openvpn.exe` ao Path do sistema (veja instruções acima)
   - Salve seu `.ovpn` com os dados da sua conta Proton
   - Crie um `auth.txt` com login e senha
   - O sistema já usa esse `.ovpn` automaticamente antes de iniciar o ciclo

4. **Rode o programa:**
   ```bash
   python main.py
   ```

5. **Use a interface:**
   - Clique para clonar instância
   - O sistema vai abrir o WhatsApp, colar número, aguardar SMS
   - Se der erro, a instância é automaticamente deletada

---

## 🌐 Estrutura de Arquivos

| Arquivo             | Função                                 |
|----------------------|----------------------------------------|
| `main.py`            | Interface, controle principal          |
| `sms_api.py`         | Conexão com API SMS Activate           |
| `ldplayer.py`        | Funções de controle ADB, LDPlayer      |
| `whatsapp.py`        | Abertura do app, inserção do número, SMS |
| `config_brasil.py`   | API config para números do Brasil       |
| `config_indonesia.py`| API config para números da Indonésia    |
| `vpn.py`             | Conexão automática com arquivo .ovpn    |

---

## ✨ Feito com carinho pelo Gabriel Napo 🐒💻

