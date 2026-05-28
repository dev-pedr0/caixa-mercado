from tabulate import tabulate

def exibir_tabela_nota_fiscal(produtos):
    produtos_formatados = [
        [
            item, 
            nome, 
            quant, 
            f"R$ {preco:.2f}".replace('.', ','), 
            f"R$ {total:.2f}".replace('.', ',')
        ]
        for item, nome, quant, preco, total in produtos
    ]
    
    print(tabulate(
        produtos_formatados,
        headers=["Item", "Produto", "Quant", "Preço", "Total"],
        tablefmt="simple",
        colalign=("left", "left", "right", "right", "right")
    ))

def exibir_tabela_resumo_atendimentos(atendimentos):
    atendimentos_formatados = [
        [cliente, f"R$ {total:.2f}".replace('.', ',')]
        for cliente, total in atendimentos
    ]
    
    print(tabulate(
        atendimentos_formatados,
        headers=["Cliente", "Total"],
        tablefmt="simple",
        colalign=("left", "right")
    ))