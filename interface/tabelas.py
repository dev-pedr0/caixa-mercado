from tabulate import tabulate

def exibir_tabela_nota_fiscal(produtos):
    print(tabulate(
        produtos,
        headers=["Item", "Produto", "Quant", "Preço", "Total"],
        tablefmt="simple"
    ))

def exibir_tabela_resumo_atendimentos(atendimentos):
    print(tabulate(
        atendimentos,
        headers=["Cliente", "Total"],
        tablefmt="simple"
    ))