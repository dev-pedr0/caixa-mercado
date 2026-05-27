import sys
import os
from interface.menus import exibir_menu_testes
from tests.teste_repositorio_cliente import executar_testes_repositorio_cliente
from tests.teste_repositorio_produto import executar_testes_repositorio_produto
from tests.teste_servico_cliente import executar_testes_servico_cliente
from tests.teste_servico_produto import executar_testes_servico_produto

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def executar_testes():
    while True:
        opcao = exibir_menu_testes()

        match opcao:
            case "1":
                executar_testes_repositorio_produto()
            case "2":
                executar_testes_repositorio_cliente()
            case "3":
                executar_testes_servico_produto()
            case "4":
                executar_testes_servico_cliente()
            case "0":
                print("\nSaindo do Painel de testes...")
                break
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    executar_testes()