from interface.gerenciamento_produtos import listar_produtos_zerados
from interface.tabelas import exibir_tabela_resumo_atendimentos
from utils.geradores import gerar_data_hoje

IDX_TOTAL_ATENDIMENTO_VALOR = 1

def fechar_caixa(total_atendimento, crud):
    dados_compras = registrar_total_compras(total_atendimento)
    zerados = listar_produtos_zerados(crud)
    resumir_atendimentos(dados_compras, zerados)

def registrar_total_compras(total_atendimento):
    data = gerar_data_hoje()
    total_vendas = sum(item[IDX_TOTAL_ATENDIMENTO_VALOR] for item in total_atendimento)
    return (data, total_atendimento, total_vendas)

def resumir_atendimentos(dados, zerados):
    data, atendimentos, total_vendas = dados
    print("\nFechamento do Caixa")
    print(f"Data: {data}\n")
    if not atendimentos:
        print("Nenhum atendimento realizado.")
        return
    exibir_tabela_resumo_atendimentos(atendimentos)
    print(f"\nTotal de vendas: R$ {total_vendas:.2f}".replace('.', ','))
    if not zerados:
        print("\nNenhum produto zerado")
    else:
        print("\nProdutos sem estoque:")
        for z in zerados:
            print(z)