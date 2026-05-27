from data.gerenciamento_db import alimentar_db, salvar_banco_para_csv
from interface.atendimento_cliente import atender_cliente
from interface.fechamento_caixa import fechar_caixa
from interface.menus import exibir_menu_caixa
from utils.conexoes import conectar_crud_produto

def caixa_mercado():
    alimentar_db()
    crud = conectar_crud_produto()
    numero_cliente = 0
    total_atendimento = []
    while True:
        opcao = exibir_menu_caixa()
        match opcao:
            case "1":
                numero_cliente = atender_cliente(
                    numero_cliente,
                    total_atendimento,
                    crud
                )
            case "2":
                fechar_caixa(total_atendimento, crud)
                salvar_banco_para_csv(crud)
                break
            case _:
                print("Valor inválido")