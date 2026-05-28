import pandas as pd
from interface.tabelas import exibir_tabela_nota_fiscal
from utils.geradores import gerar_data_hoje

IDX_PRODUTOS_PRECO = 4

def gerar_dados_nota(nome_cliente, produtos_cliente):
    data = gerar_data_hoje()
    if not produtos_cliente:
        return (nome_cliente, data, [], 0, 0.0)
    colunas = ["id", "produto", "quantidade", "preco_unitario", "preco_total"]
    df = pd.DataFrame(produtos_cliente, columns=colunas)
    df_agrupado = df.groupby("produto").agg({
        "quantidade": "sum",
        "preco_unitario": "first",
        "preco_total": "sum"
    }).reset_index()
    df_agrupado.insert(0, "id", range(1, len(df_agrupado) + 1))
    produtos_agrupados = df_agrupado.values.tolist()
    total_itens = len(df_agrupado)
    total_compra = df_agrupado["preco_total"].sum()
    return (nome_cliente, data, produtos_agrupados, total_itens, total_compra)

def imprimir_nota(dados):
    nome_cliente, data, produtos, total_itens, total_compra = dados
    print(f"\n{nome_cliente}")
    print(f"Data: {data}\n")
    if not produtos:
        print("Nenhum produto comprado.")
        return
    exibir_tabela_nota_fiscal(produtos)
    print(f"\nItens: {total_itens}")
    print(f"Total de vendas: R$ {total_compra:.2f}\n")

def registrar_atendimento(total_atendimento, nome_cliente, total_compra):
    registro = [nome_cliente, total_compra]
    total_atendimento.append(registro)
    return total_atendimento