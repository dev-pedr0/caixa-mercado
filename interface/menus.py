from utils.validador import validar_numero

def exibir_menu_admin():
    print("\n" + "=" * 50)
    print("      PAINEL ADMINISTRATIVO - GERENCIAR PRODUTOS     ")
    print("=" * 50)
    print("[1] Listar Todos os Produtos (Catálogo)")
    print("[2] Cadastrar Novo Produto")
    print("[3] Consultar Produto por ID")
    print("[4] Consultar Produto por Nome")
    print("[5] Atualizar/Corrigir Produto")
    print("[6] Remover Produto do Sistema")
    print("[7] Salvar banco de dados em CSV")
    print("[0] Sair do Painel Administrativo")
    print("=" * 50)
    opcao = input("Escolha uma opção: ").strip()
    return opcao

def exibir_menu_caixa():
    print("\n" + "=" * 50)
    print("      PAINEL DO CAIXA    ")
    print("=" * 50)
    print("[1] Iniciar atendimento")
    print("[2] Finalizar atendimento")
    opcao = input("Escolha uma opção: ").strip()
    return opcao

def exibir_menu_compra(nome_cliente, produtos_banco):
    print("\n" + "=" * 50)
    print(f"      ATENDIMENTO DO {nome_cliente}    ")
    print("=" * 50)
    
    if not produtos_banco:
        print("Nenhum produto disponível no estoque neste momento.")
        print("[0] Encerrar Atendimento")
        print("=" * 50)
    else:
        print("\n--- PRODUTOS DISPONÍVEIS ---")
        for prod in produtos_banco:
            print(prod)
        print("[0] Encerrar Atendimento")
        print("=" * 50)
    opcao = validar_numero("Escolha um produto [ID]: ")
    return opcao