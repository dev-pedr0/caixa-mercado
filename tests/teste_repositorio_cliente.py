from classes.Cliente import Cliente
from utils.conexoes import conectar_repositorio_cliente

def executar_testes_repositorio_cliente():
    repositorio = conectar_repositorio_cliente()
    
    try:
        # ---------------------------------------------------------------------
        # TESTE 1: LISTAR TODOS OS CLIENTES (R do CRUD)
        # ---------------------------------------------------------------------
        print("1. Testando 'listar_clientes'...")
        clientes_iniciais = repositorio.listar_clientes()
        print(f"Total de clientes cadastrados no banco atualmente: {len(clientes_iniciais)}")
        for cli in clientes_iniciais:
            print(f"   -> {cli}")
        print("-" * 50)

        # ---------------------------------------------------------------------
        # TESTE 2: CRIAR UM NOVO CLIENTE (C do CRUD)
        # ---------------------------------------------------------------------
        print("2. Testando 'criar_cliente'...")
        novo_cliente = Cliente(nome="Cliente Teste Lab")
        cliente_criado = repositorio.criar_cliente(novo_cliente)
        print("Sucesso! Cliente cadastrado com ID automático.")
        print(f"Dados salvos: {cliente_criado}")
        id_teste = cliente_criado.id
        print("-" * 50)

        # ---------------------------------------------------------------------
        # TESTE 3: BUSCAR CLIENTE POR ID (R do CRUD)
        # ---------------------------------------------------------------------
        print(f"3. Testando 'buscar_cliente_por_id' com o ID {id_teste}...")
        cliente_encontrado = repositorio.buscar_cliente_por_id(id_teste)
        if cliente_encontrado:
            print(f"Cliente localizado com sucesso: {cliente_encontrado}")
        else:
            print("Erro: O cliente deveria ter sido encontrado.")
        print("-" * 50)

        # ---------------------------------------------------------------------
        # TESTE 4: BUSCAR CLIENTE POR NOME (R do CRUD)
        # ---------------------------------------------------------------------
        print("4. Testando 'buscar_cliente_por_nome'...")
        cliente_por_nome = repositorio.buscar_cliente_por_nome("Cliente Teste Lab")
        if cliente_por_nome:
            print(f"Cliente localizado pelo nome: {cliente_por_nome}")
        else:
            print("Erro: O cliente deveria ter sido encontrado pelo nome.")
        print("-" * 50)

        # ---------------------------------------------------------------------
        # TESTE 5: ATUALIZAR CLIENTE (U do CRUD)
        # ---------------------------------------------------------------------
        print(f"5. Testando 'atualizar_cliente' no ID {id_teste} (Alterando o nome)...")
        cliente_encontrado.nome = "Cliente Teste Lab Modificado"
        cliente_atualizado = repositorio.atualizar_cliente(cliente_encontrado)
        print(f"Dados atualizados no banco de dados: {cliente_atualizado}")
        print("-" * 50)

        # ---------------------------------------------------------------------
        # TESTE 6: DELETAR CLIENTE (D do CRUD)
        # ---------------------------------------------------------------------
        print(f"6. Testando 'deletar_cliente' o cliente de ID {id_teste}...")
        foi_deletado = repositorio.deletar_cliente(id_teste)
        print(f"Removido com sucesso? {foi_deletado}")
        
        print("Confirmando exclusão no banco...")
        cliente_sumiu = repositorio.buscar_cliente_por_id(id_teste)
        if cliente_sumiu is None:
            print("Sucesso: Cliente não existe mais no banco de dados.")
        else:
            print("Erro: O cliente ainda consta no banco de dados.")
        print("-" * 50)

    except RuntimeError as e:
        print(f"\n[FALHA NO TESTE] A camada superior capturou um erro: {e}")
        
    print("\n=== FIM DOS TESTES DO REPOSITÓRIO DE CLIENTES ===")

if __name__ == "__main__":
    executar_testes_repositorio_cliente()