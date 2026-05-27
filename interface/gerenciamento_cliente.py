from interface.menus import exibir_menu_registro_cliente

def registrar_cliente(crud_cliente) -> object:
    while True:
        id_input = exibir_menu_registro_cliente()
        if id_input == "":
            return cadastrar_cliente(crud_cliente)
        
        elif id_input == "0":
            print("Atendimento cancelado")
            return None
        
        else:
            cliente = identificar_cliente(id_input, crud_cliente)
            if cliente is not None:
                return cliente

def identificar_cliente(id_input, crud_cliente):
    try:
        id_busca = int(id_input)
        if id_busca < 1:
            print(f"Aviso: O ID {id_busca} é inválido.")
            return cadastrar_cliente(crud_cliente)
        
        else:
            resultado_busca = crud_cliente.buscar_cliente_por_id(id_busca)
            if resultado_busca["sucesso"]:
                cliente_encontrado = resultado_busca["dado"]
                print(f"Cliente Identificado: {cliente_encontrado.nome} (ID: {cliente_encontrado.id})")
                return cliente_encontrado
            else:
                print(f"Aviso: {resultado_busca['mensagem']}")
                return cadastrar_cliente(crud_cliente)
    except ValueError:
            print("Aviso: Entrada inválida detectada (Não é um ID numérico).")
            return cadastrar_cliente(crud_cliente)

def cadastrar_cliente(crud_cliente):
    print("\n--> Cadastro de novo cliente...")
    while True:
        nome_novo = input("Digite o nome completo do novo cliente (ou '0' para cancelar): ").strip()
        if nome_novo == "0":
            return None
            
        resultado_criar = crud_cliente.criar_cliente(nome_novo)
        if resultado_criar["sucesso"]:
            cliente_novo = resultado_criar["dado"]
            print(f"Cliente cadastrado com sucesso! ID Gerado: {cliente_novo.id}")
            return cliente_novo
        else:
            print(f"Erro de validação: {resultado_criar['mensagem']}. Tente novamente.")