import sys
import os
from tests.teste_repositorio_cliente import executar_testes_repositorio_cliente
from tests.teste_repositorio_produto import executar_testes_repositorio_produto

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def executar_testes_repositorio():
    print("=== INICIANDO TESTES DO REPOSITÓRIO DE PRODUTOS ===\n")
    executar_testes_repositorio_produto()

    print("=== INICIANDO TESTES DO REPOSITÓRIO DE CLIENTES ===\n")
    executar_testes_repositorio_cliente()

if __name__ == "__main__":
    executar_testes_repositorio()