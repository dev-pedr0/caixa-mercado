def buscar_produtos_estoque(crud) -> list:
    resultado = crud.listar_produtos()
    if not resultado["sucesso"]:
        print(f"Erro ao carregar produtos: {resultado['mensagem']}")
        return None   
    return resultado["dado"]

def buscar_produto(opcao, crud):
    resultado_busca = crud.buscar_produto_por_id(opcao)  
    if not resultado_busca["sucesso"]:
        print(f"Erro: {resultado_busca['mensagem']}")
        return None   
    produto_banco = resultado_busca["dado"]
    return produto_banco

def atualizar_produto(crud, produto_banco, nova_quantidade, quantidade_compra):
    produto_atualizado = crud.service.atualizar_produto(
                produto_id=produto_banco.id,
                nome_novo=produto_banco.nome,
                quantidade_nova=nova_quantidade,
                preco_novo=produto_banco.preco,
                eh_venda=True,
                quantidade_venda=quantidade_compra
            )
    
def adicionar_produto_cliente(id_item, crud, produto_banco, nova_quantidade, quantidade_compra):
    atualizar_produto(crud, produto_banco, nova_quantidade, quantidade_compra)
    preco_total = produto_banco.preco * quantidade_compra
    item_cliente = [id_item, produto_banco.nome, quantidade_compra, produto_banco.preco, preco_total]
    return item_cliente 
    
def listar_produtos_zerados(crud) -> list:
    resultado_busca = crud.listar_produtos()
    if not resultado_busca["sucesso"] or not resultado_busca["dado"]:
        return []
    lista_produtos = resultado_busca["dado"]
    nomes_zerados = []
    for produto in lista_produtos:
        if produto.quantidade == 0:
            nomes_zerados.append(produto.nome)
            
    return nomes_zerados