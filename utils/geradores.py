from datetime import datetime

FORMATO_DATA = "%d/%m/%Y %H:%M"

def gerar_cliente(numero_atual):
    numero_atual += 1
    nome_cliente = f"Cliente {numero_atual}"
    return numero_atual, nome_cliente

def gerar_data_hoje():
    data = datetime.now().strftime(FORMATO_DATA)
    return data