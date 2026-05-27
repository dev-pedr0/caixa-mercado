from datetime import datetime

FORMATO_DATA = "%d/%m/%Y %H:%M"

def gerar_data_hoje():
    data = datetime.now().strftime(FORMATO_DATA)
    return data