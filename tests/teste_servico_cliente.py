from service.cliente_service import ConflitoRegraErro, RegistroNaoEncontradoErro, ValidacaoErro
from utils.conexoes import conectar_servico_cliente

def executar_testes_servico_cliente():
    print("=" * 60)
    print("     INICIANDO TESTES DA CAMADA DE SERVIÇO (CLIENTE)     ")
    print("=" * 60 + "\n")

    servico = conectar_servico_cliente()

    id_cliente_teste = None

    # -------------------------------------------------------------------------
    # TESTE 1: LISTAR CLIENTES DO BANCO
    # -------------------------------------------------------------------------
    print(">>> Teste 1: Listando clientes cadastrados...")
    try:
        lista = servico.listar_clientes()
        print(f"Sucesso! Encontrados {len(lista)} clientes no banco.")
        for c in lista[:4]:
            print(f"   {c}")
        if len(lista) > 4:
            print("   ... (outros omitidos para simplificar o log) ...")
    except Exception as e:
        print(f"Falha inesperada ao listar clientes: {e}")
    print("-" * 60)

    # -------------------------------------------------------------------------
    # TESTE 2: CRIAR CLIENTE (Caminho Feliz)
    # -------------------------------------------------------------------------
    print(">>> Teste 2: Criando um novo cliente válido...")
    try:
        novo_cli = servico.criar_cliente(nome="Pedro de Souza")
        print(f"Sucesso! Cliente criado: {novo_cli}")
        id_cliente_teste = novo_cli.id
    except Exception as e:
        print(f"Falha ao criar cliente válido: {e}")
    print("-" * 60)

    # -------------------------------------------------------------------------
    # TESTE 3: VALIDAÇÃO DE NOME DUPLICADO (Cenário de Erro)
    # -------------------------------------------------------------------------
    print(">>> Teste 3: Tentando criar cliente com nome que já existe...")
    try:
        servico.criar_cliente(nome="Pedro de Souza")
        print("Erro: O sistema permitiu cadastrar um nome de cliente duplicado!")
    except ConflitoRegraErro as e:
        print(f"Captura Correta (ConflitoRegraErro): {e}")
    except Exception as e:
        print(f"Captura incorreta do tipo de erro: {e}")
    print("-" * 60)

    # -------------------------------------------------------------------------
    # TESTE 4: VALIDAÇÃO DE TAMANHO E OBRIGATORIEDADE DE NOME (Cenário de Erro)
    # -------------------------------------------------------------------------
    print(">>> Teste 4: Tentando criar clientes com nomes inválidos...")
    
    print("   A) Nome Vazio:")
    try:
        servico.criar_cliente(nome="   ")
        print("   Erro: O sistema aceitou um nome composto apenas por espaços!")
    except ValidacaoErro as e:
        print(f"   Captura Correta (ValidacaoErro): {e}")

    print("\n   B) Nome maior que 50 caracteres:")
    nome_gigante = "A" * 51
    try:
        servico.criar_cliente(nome=nome_gigante)
        print("   Erro: O sistema permitiu cadastrar um nome com mais de 50 caracteres!")
    except ValidacaoErro as e:
        print(f"   Captura Correta (ValidacaoErro): {e}")
    print("-" * 60)

    # -------------------------------------------------------------------------
    # TESTE 5: BUSCAR POR ID INVÁLIDO OU INEXISTENTE
    # -------------------------------------------------------------------------
    print(">>> Teste 5: Testando validações de busca por ID...")
    try:
        servico.buscar_cliente_por_id(0)
        print("Erro: O sistema permitiu buscar ID menor que 1!")
    except ValidacaoErro as e:
        print(f"Captura Correta para ID inválido: {e}")

    try:
        servico.buscar_cliente_por_id(99999)
        print("Erro: O sistema fingiu encontrar um ID de cliente inexistente!")
    except RegistroNaoEncontradoErro as e:
        print(f"Captura Correta para ID inexistente: {e}")
    print("-" * 60)

    # -------------------------------------------------------------------------
    # TESTE 6: ATUALIZAÇÃO DE CADASTRO
    # -------------------------------------------------------------------------
    if id_cliente_teste:
        print(f">>> Teste 6: Testando alteração de nome no ID {id_cliente_teste}...")
        try:
            cliente_modificado = servico.atualizar_cliente(
                cliente_id=id_cliente_teste, 
                nome_novo="Pedro de Souza Alterado"
            )
            print(f"Sucesso! Nome atualizado no banco: {cliente_modificado}")
        except Exception as e:
            print(f"Falha ao atualizar cliente: {e}")
    else:
        print("Pulando Teste 6: O cliente de teste não pôde ser gerado.")
    print("-" * 60)

    # -------------------------------------------------------------------------
    # TESTE 7: EXCLUSÃO (Delete)
    # -------------------------------------------------------------------------
    if id_cliente_teste:
        print(f">>> Teste 7: Deletando o cliente de teste (ID {id_cliente_teste})...")
        try:
            sucesso = servico.deletar_cliente(id_cliente_teste)
            print(f"Removido do banco com sucesso? {sucesso}")
            
            try:
                servico.buscar_cliente_por_id(id_cliente_teste)
                print("Erro: O cliente ainda foi localizado após ser deletado.")
            except RegistroNaoEncontradoErro:
                print("Confirmado: O cliente foi completamente apagado da base de dados.")
        except Exception as e:
            print(f"Falha ao deletar cliente de teste: {e}")
    else:
        print("Pulando Teste 7: Sem ID de teste disponível.")
        
    print("\n" + "=" * 60)
    print("               FIM DOS TESTES DE SERVIÇO (CLIENTE)        ")
    print("=" * 60)