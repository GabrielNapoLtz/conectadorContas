import requests
import time

BASE_URL = 'https://api.sms-activate.ae/stubs/handler_api.php'

def carregar_config(pais):
    if pais == "br":
        from config_brasil import API_KEY, CODIGO_PAIS, SERVICO
    elif pais == "id":
        from config_indonesia import API_KEY, CODIGO_PAIS, SERVICO
    else:
        raise Exception("País não suportado")
    return API_KEY, CODIGO_PAIS, SERVICO

def verificar_saldo(pais):
    API_KEY, _, _ = carregar_config(pais)
    params = {
        'api_key': API_KEY,
        'action': 'getBalance'
    }
    r = requests.get(BASE_URL, params=params)
    return r.text

def comprar_numero(pais, max_price=None, use_cashback=False, activation_type=0):
    API_KEY, CODIGO_PAIS, SERVICO = carregar_config(pais)
    params = {
        'api_key': API_KEY,
        'action': 'getNumber',
        'service': SERVICO,
        'country': CODIGO_PAIS,
        'activationType': activation_type
    }

    if max_price:
        params['maxPrice'] = max_price
    if use_cashback:
        params['useCashBack'] = 'true'

    r = requests.get(BASE_URL, params=params)

    if r.text.startswith('ACCESS_NUMBER'):
        _, activation_id, numero = r.text.split(':')
        return activation_id, numero

    print(f"❌ Falha ao comprar número [{pais}]: {r.text}")
    return None, None




def pegar_codigo(pais, activation_id, tentativas=10, intervalo=5):
    API_KEY, _, _ = carregar_config(pais)
    for _ in range(tentativas):
        time.sleep(intervalo)
        params = {
            'api_key': API_KEY,
            'action': 'getStatus',
            'id': activation_id
        }
        r = requests.get(BASE_URL, params=params)
        if r.text.startswith('STATUS_OK'):
            return r.text.split(':')[1]
    return None

def cancelar_numero(pais, activation_id):
    API_KEY, _, _ = carregar_config(pais)
    params = {
        'api_key': API_KEY,
        'action': 'setStatus',
        'status': 8,
        'id': activation_id
    }
    response = requests.get(BASE_URL, params=params)
    print(f"[CANCELAMENTO] ID: {activation_id} | STATUS: 8 | RESPOSTA: {response.text}")

def finalizar_numero(pais, activation_id):
    API_KEY, _, _ = carregar_config(pais)
    params = {
        'api_key': API_KEY,
        'action': 'setStatus',
        'status': 6,
        'id': activation_id
    }
    requests.get(BASE_URL, params=params)
