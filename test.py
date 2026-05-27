from classes.Produto import Produto
from data.gerenciamento_db import verificar_conexao_db
from repository.produto_repository import ProdutoRepository

def executar_testes_repositorio():
    print("=== INICIANDO TESTES DO REPOSITÓRIO ===\n")
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    
    try:
        # ---------------------------------------------------------------------
        # TESTE 1: LISTAR TODOS OS PRODUTOS (R do CRUD)
        # ---------------------------------------------------------------------
        print("1. Testando 'listar_todos'...")
        produtos_iniciais = repositorio.listar_produtos()
        print(f"Total de produtos cadastrados no banco atualmente: {len(produtos_iniciais)}")
        for prod in produtos_iniciais:
            print(f"   -> {prod}")
        print("-" * 50)
        # ---------------------------------------------------------------------
        # TESTE 2: CRIAR UM NOVO PRODUTO (C do CRUD)
        # ---------------------------------------------------------------------
        print("2. Testando 'criar'...")
        novo_item = Produto(nome="Produto Teste Lab", quantidade=15, preco=99.90)
        produto_criado = repositorio.criar_produto(novo_item)
        print(f"Sucesso! Produto cadastrado com ID automático.")
        print(f"Dados salvos: {produto_criado}")
        id_teste = produto_criado.id
        print("-" * 50)
        # ---------------------------------------------------------------------
        # TESTE 3: BUSCAR PRODUTO POR ID (R do CRUD)
        # ---------------------------------------------------------------------
        print(f"3. Testando 'buscar_por_id' com o ID {id_teste}...")
        produto_encontrado = repositorio.buscar_produto_por_id(id_teste)
        if produto_encontrado:
            print(f"Produto localizado com sucesso: {produto_encontrado}")
        else:
            print("Erro: O produto deveria ter sido encontrado.")
        print("-" * 50)
        # ---------------------------------------------------------------------
        # TESTE 4: BUSCAR PRODUTO POR NOME (R do CRUD)
        # ---------------------------------------------------------------------
        print("4. Testando 'buscar_por_nome'...")
        produto_por_nome = repositorio.buscar_produto_por_nome = repositorio.buscar_produto_por_nome("Produto Teste Lab")
        if produto_por_nome:
            print(f"Produto localizado pelo nome: {produto_por_nome}")
        print("-" * 50)
        # ---------------------------------------------------------------------
        # TESTE 5: ATUALIZAR PRODUTO (U do CRUD)
        # ---------------------------------------------------------------------
        print(f"5. Testando 'atualizar' no ID {id_teste} (Alterando estoque e preço)...")
        produto_encontrado.quantidade = 80
        produto_encontrado.preco = 120.45
        produto_atualizado = repositorio.atualizar_produto(produto_encontrado)
        print(f"Dados atualizados no banco de dados: {produto_atualizado}")
        print("-" * 50)
        # ---------------------------------------------------------------------
        # TESTE 6: DELETAR PRODUTO (D do CRUD)
        # ---------------------------------------------------------------------
        print(f"6. Testando 'deletar' o produto de ID {id_teste}...")
        foi_deletado = repositorio.deletar_produto(id_teste)
        print(f"Removido com sucesso? {foi_deletado}")
        
        # Confirmando a exclusão tentando buscar novamente
        print("Confirmando exclusão no banco...")
        produto_sumiu = repositorio.buscar_produto_por_id(id_teste)
        if produto_sumiu is None:
            print("Sucesso: Produto não existe mais no banco de dados.")
        print("-" * 50)

    except RuntimeError as e:
        print(f"\n[FALHA NO TESTE] A camada superior capturou um erro: {e}")
        
    print("\n=== FIM DOS TESTES DO REPOSITÓRIO ===")

if __name__ == "__main__":
    executar_testes_repositorio()