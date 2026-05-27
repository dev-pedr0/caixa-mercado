from service.produto_service import ConflitoRegraErro, RegistroNaoEncontradoErro, ValidacaoErro
from utils.conexoes import conectar_servico_produto


def executar_testes_servico():
    print("=" * 60)
    print("     INICIANDO TESTES DA CAMADA DE SERVIÇO (CLIENTE)     ")
    print("=" * 60 + "\n")

    servico = conectar_servico_produto()

    id_produto_teste = None
    # -------------------------------------------------------------------------
    # TESTE 1: LISTAR PRODUTOS DO BANCO
    # -------------------------------------------------------------------------
    print(">>> Teste 1: Listando produtos cadastrados...")
    try:
        lista = servico.listar_produtos()
        print(f"Sucesso! Encontrados {len(lista)} produtos no banco.")
        for p in lista[:3]:
            print(f"   {p}")
        if len(lista) > 3:
            print("   ... (outros omitidos para simplificar o log) ...")
    except Exception as e:
        print(f"Falha inesperada ao listar: {e}")
    print("-" * 60)
    # -------------------------------------------------------------------------
    # TESTE 2: CRIAR PRODUTO (Caminho Feliz)
    # -------------------------------------------------------------------------
    print(">>> Teste 2: Criando um novo produto válido...")
    try:
        novo_prod = servico.criar_produto(nome="Produto Inédito X", quantidade=20, preco=15.90)
        print(f"✅ Sucesso! Produto criado: {novo_prod}")
        id_produto_teste = novo_prod.id
    except Exception as e:
        print(f"Falha ao criar produto válido: {e}")
    print("-" * 60)
    # -------------------------------------------------------------------------
    # TESTE 3: VALIDAÇÃO DE NOME DUPLICADO (Cenário de Erro)
    # -------------------------------------------------------------------------
    print(">>> Teste 3: Tentando criar produto com nome que já existe...")
    try:
        servico.criar_produto(nome="Produto Inédito X", quantidade=5, preco=10.00)
        print("Erro: O sistema permitiu criar um nome duplicado! (Falha na regra)")
    except ConflitoRegraErro as e:
        print(f"Captura Correta (ConflitoRegraErro): {e}")
    except Exception as e:
        print(f"Captura incorreta do tipo de erro: {e}")
    print("-" * 60)
    # -------------------------------------------------------------------------
    # TESTE 4: VALIDAÇÃO DE VALORES NEGATIVOS (Cenário de Erro)
    # -------------------------------------------------------------------------
    print(">>> Teste 4: Tentando criar produto com preço e estoque inválidos...")
    try:
        servico.criar_produto(nome="Produto Fantasma", quantidade=-10, preco=5.00)
        print("Erro: O sistema permitiu estoque negativo!")
    except ValidacaoErro as e:
        print(f"Captura Correta para estoque negativo (ValidacaoErro): {e}")

    try:
        servico.criar_produto(nome="Produto Fantasma 2", quantidade=10, preco=-1.50)
        print("Erro: O sistema permitiu preço negativo!")
    except ValidacaoErro as e:
        print(f"Captura Correta para preço negativo (ValidacaoErro): {e}")
    print("-" * 60)
    # -------------------------------------------------------------------------
    # TESTE 5: BUSCAR POR ID INVÁLIDO OU INEXISTENTE
    # -------------------------------------------------------------------------
    print(">>> Teste 5: Testando validações de busca por ID...")
    try:
        servico.buscar_produto_por_id(0)
        print("Erro: O sistema permitiu buscar ID menor que 1!")
    except ValidacaoErro as e:
        print(f"Captura Correta para ID inválido: {e}")

    try:
        servico.buscar_produto_por_id(99999)
        print("Erro: O sistema fingiu encontrar um ID que não existe!")
    except RegistroNaoEncontradoErro as e:
        print(f"Captura Correta para ID inexistente: {e}")
    print("-" * 60)
    # -------------------------------------------------------------------------
    # TESTE 6: ATUALIZAÇÃO E VALIDAÇÃO DE ESTOQUE PARA VENDA
    # -------------------------------------------------------------------------
    if id_produto_teste:
        print(f">>> Teste 6: Testando simulação de VENDA no ID {id_produto_teste}...")
        
        print("   A) Tentando vender 25 unidades (Estoque disponível: 20)...")
        try:
            servico.atualizar_produto(
                produto_id=id_produto_teste, 
                nome_novo="Produto Inédito X", 
                quantidade_nova=0, 
                preco_novo=15.90, 
                eh_venda=True, 
                quantidade_venda=25
            )
            print("   Erro: O sistema permitiu vender mais do que o estoque disponível!")
        except ConflitoRegraErro as e:
            print(f"   Captura Correta para falta de estoque: {e}")

        print("\n   B) Tentando vender 5 unidades (Estoque disponível: 20)...")
        try:
            produto_pos_venda = servico.atualizar_produto(
                produto_id=id_produto_teste, 
                nome_novo="Produto Inédito X", 
                quantidade_nova=15, # 20 original - 5 da venda
                preco_novo=15.90, 
                eh_venda=True, 
                quantidade_venda=5
            )
            print(f"   Sucesso! Venda realizada. Novo estado no banco: {produto_pos_venda}")
        except Exception as e:
            print(f"   Falha ao realizar venda válida: {e}")
    else:
        print("Pulando Teste 6: O produto de teste não pôde ser gerado.")
    print("-" * 60)
    # -------------------------------------------------------------------------
    # TESTE 7: EXCLUSÃO (Delete)
    # -------------------------------------------------------------------------
    if id_produto_teste:
        print(f">>> Teste 7: Deletando o produto de teste (ID {id_produto_teste})...")
        try:
            sucesso = servico.deletar_produto(id_produto_teste)
            print(f"Removido do banco com sucesso? {sucesso}")
            
            try:
                servico.buscar_produto_por_id(id_produto_teste)
            except RegistroNaoEncontradoErro:
                print("Confirmado: O produto foi completamente apagado.")
        except Exception as e:
            print(f"Falha ao deletar produto de teste: {e}")
    else:
        print("Pulando Teste 7: Sem ID de teste disponível.")
        
    print("\n" + "=" * 60)
    print("              FIM DOS TESTES DA CAMADA DE SERVIÇO        ")
    print("=" * 60)

if __name__ == "__main__":
    executar_testes_servico()