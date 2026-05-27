from interface.gerenciamento_cliente import registrar_cliente
from interface.gerenciamento_produtos import adicionar_produto_cliente, buscar_produto, buscar_produtos_estoque
from interface.menus import exibir_menu_compra
from interface.registro_atendimento import gerar_dados_nota, imprimir_nota, registrar_atendimento
from utils.validador import validar_numero

OPCAO_ENCERRAR = 0
IDX_TOTAL_COMPRA = 4

def atender_cliente(total_atendimento, crud_produto, crud_cliente):
    cliente = registrar_cliente(crud_cliente)
    if cliente is None:
        print("Atendimento abortado sem registrar compras.")
        return
    
    nome_cliente = cliente.nome
    total_compra = comprar_produtos(nome_cliente, crud_produto)
    registrar_atendimento(
        total_atendimento,
        nome_cliente,
        total_compra
    )

def comprar_produtos(nome_cliente, crud_produto):
    compras_cliente = []
    id_item = 1
    
    while True:
        produtos = buscar_produtos_estoque(crud_produto)
        if produtos is None:
            break
        opcao = exibir_menu_compra(nome_cliente, produtos)

        if opcao == OPCAO_ENCERRAR:
            dados_nota = gerar_dados_nota(nome_cliente, compras_cliente)
            imprimir_nota(dados_nota)
            return dados_nota[IDX_TOTAL_COMPRA]
        
        compra_validada = validar_compra(opcao, crud_produto, id_item)
        if compra_validada is None:
            continue
        compras_cliente.append(compra_validada)
        id_item += 1

def validar_compra(opcao, crud_produto, id_item):  
    produto_banco = buscar_produto(opcao, crud_produto)
    if produto_banco == None:
        return None 

    quantidade_compra = validar_numero("Quantidade: ")
    if quantidade_compra <= 0:
        print("Erro na compra: A quantidade a ser vendida deve ser maior que zero.")
        return None
    nova_quantidade = produto_banco.quantidade - quantidade_compra
    
    try:
        item_cliente = adicionar_produto_cliente(
            id_item, crud_produto, produto_banco, nova_quantidade, quantidade_compra
        )
        print(f"{quantidade_compra}x '{produto_banco.nome}' adicionado ao carrinho!")
        return item_cliente       
    except Exception as e:
        print(f"Erro na compra: {e}")
        return None       