from data.gerenciamento_db import salvar_produtos_para_csv
from interface.menus import exibir_menu_admin
from utils.conexoes import conectar_crud_cliente, conectar_crud_produto

def iniciar_interface_admin():
    crud_produto = conectar_crud_produto()
    crud_cliente = conectar_crud_cliente()

    while True:
        opcao = exibir_menu_admin()

        match opcao:
            case "1":
                print("\n--- CATÁLOGO DE PRODUTOS ---")
                resultado = crud_produto.listar_produtos()
                if resultado["sucesso"]:
                    produtos = resultado["dado"]
                    if not produtos:
                        print("Nenhum produto cadastrado no banco de dados.")
                    else:
                        for prod in produtos:
                            print(prod)
                else:
                    print(f"Erro: {resultado['mensagem']}")
            
            case "2":
                print("\n--- CADASTRAR NOVO PRODUTO ---")
                nome = input("Nome do produto: ").strip()
                try:
                    quantidade = int(input("Quantidade em estoque inicial: "))
                    preco = float(input("Preço unitário (ex: 10.50): "))
                    resultado = crud_produto.criar_produto(nome, quantidade, preco)
                    if resultado["sucesso"]:
                        print(f"{resultado['mensagem']}")
                    else:
                        print(f"Aviso: {resultado['mensagem']}")
                except ValueError:
                    print("Erro: Quantidade deve ser um número inteiro e Preço um número decimal.")
            
            case "3":
                print("\n--- CONSULTAR PRODUTO POR ID ---")
                try:
                    id_busca = int(input("Digite o ID do produto: "))
                    resultado = crud_produto.buscar_produto_por_id(id_busca)
                    if resultado["sucesso"]:
                        print(f"\nProduto Encontrado:\n   {resultado['dado']}")
                    else:
                        print(f"Aviso: {resultado['mensagem']}")
                except ValueError:
                    print("Erro: O ID deve ser um número inteiro maior que zero.")

            case "4":
                print("\n--- CONSULTAR PRODUTO POR NOME ---")
                nome_busca = input("Digite o nome exato do produto: ").strip()
                resultado = crud_produto.buscar_produto_por_nome(nome_busca)
                if resultado["sucesso"]:
                    print(f"\nProduto Encontrado:\n   {resultado['dado']}")
                else:
                    print(f"Aviso: {resultado['mensagem']}")

            case "5":
                print("\n--- ATUALIZAR / CORRIGIR PRODUTO ---")
                try:
                    id_alterar = int(input("Digite o ID do produto que deseja corrigir: "))
                    busca = crud_produto.buscar_produto_por_id(id_alterar)
                    if not busca["sucesso"]:
                        print(f"Aviso: {busca['mensagem']}")
                        continue
                    produto_atual = busca["dado"]
                    print(f"\nEstado atual: {produto_atual}")
                    print("Insira os novos dados para correção (ou pressione [ENTER] para manter o atual):")
                    nome_input = input(f"Novo Nome [{produto_atual.nome}]: ").strip()
                    nome_novo = nome_input if nome_input != "" else produto_atual.nome
                    qtd_input = input(f"Nova Quantidade em Estoque [{produto_atual.quantidade}]: ").strip()
                    qtd_nova = int(qtd_input) if qtd_input != "" else produto_atual.quantidade
                    preco_input = input(f"Novo Preço [{produto_atual.preco}]: ").strip()
                    preco_novo = float(preco_input) if preco_input != "" else produto_atual.preco
                    resultado = crud_produto.atualizar_produto(id_alterar, nome_novo, qtd_nova, preco_novo)
                
                    if resultado["sucesso"]:
                        print(f"{resultado['mensagem']}")
                    else:
                        print(f"Aviso: {resultado['mensagem']}")         
                        
                except ValueError:
                    print("Erro: Entrada de dados inválida para quantidade ou preço.")

            case "6":
                print("\n--- REMOVER PRODUTO ---")
                try:
                    id_remover = int(input("Digite o ID do produto que deseja EXCLUIR: "))
                    confirmar = input(f"Tem certeza que deseja apagar o produto ID {id_remover}? (S/N): ").strip().upper()
                    if confirmar == "S":
                        resultado = crud_produto.deletar_produto(id_remover)
                        if resultado["sucesso"]:
                            print(f"{resultado['mensagem']}")
                        else:
                            print(f"Aviso: {resultado['mensagem']}")
                    else:
                        print("Operação de exclusão cancelada.")
                except ValueError:
                    print("Erro: O ID deve ser um número inteiro.")
            
            case "7":
                print("\n--- LISTA DE CLIENTES ---")
                resultado = crud_cliente.listar_clientes()
                if resultado["sucesso"]:
                    clientes = resultado["dado"]
                    if not clientes:
                        print("Nenhum cliente cadastrado no banco de dados.")
                    else:
                        for cli in clientes:
                            print(cli)
                else:
                    print(f"Erro: {resultado['mensagem']}")

            case "8":
                print("\n--- CADASTRAR NOVO CLIENTE ---")
                nome = input("Nome do cliente: ").strip()
                resultado = crud_cliente.criar_cliente(nome)
                if resultado["sucesso"]:
                    print(f"{resultado['mensagem']}")
                else:
                    print(f"Aviso: {resultado['mensagem']}")

            case "9":
                print("\n--- CONSULTAR CLIENTE POR ID ---")
                try:
                    id_busca = int(input("Digite o ID do cliente: "))
                    resultado = crud_cliente.buscar_cliente_por_id(id_busca)
                    if resultado["sucesso"]:
                        print(f"\nCliente Encontrado:\n   {resultado['dado']}")
                    else:
                        print(f"Aviso: {resultado['mensagem']}")
                except ValueError:
                    print("Erro: O ID deve ser um número inteiro maior que zero.")

            case "10":
                print("\n--- CONSULTAR CLIENTE POR NOME ---")
                nome_busca = input("Digite o nome exato do cliente: ").strip()
                resultado = crud_cliente.buscar_cliente_por_nome(nome_busca)
                if resultado["sucesso"]:
                    print(f"\nCliente Encontrado:\n   {resultado['dado']}")
                else:
                    print(f"Aviso: {resultado['mensagem']}")
            
            case "11":
                print("\n--- ATUALIZAR CADASTRO DE CLIENTE ---")
                try:
                    id_alterar = int(input("Digite o ID do cliente que deseja modificar: "))
                    busca = crud_cliente.buscar_cliente_por_id(id_alterar)
                    if not busca["sucesso"]:
                        print(f"Aviso: {busca['mensagem']}")
                        continue
                    cliente_atual = busca["dado"]
                    print(f"\nEstado atual: {cliente_atual}")
                    
                    nome_input = input("Insira o novo nome (ou pressione [ENTER] para manter o atual): ").strip()
                    nome_novo = nome_input if nome_input != "" else cliente_atual.nome
                    
                    resultado = crud_cliente.atualizar_cliente(id_alterar, nome_novo)
                    if resultado["sucesso"]:
                        print(f"{resultado['mensagem']}")
                    else:
                        print(f"Aviso: {resultado['mensagem']}")
                except ValueError:
                    print("Erro: Entrada de dados inválida.")
            
            case "12":
                print("\n--- REMOVER CLIENTE DO SISTEMA ---")
                try:
                    id_remover = int(input("Digite o ID do cliente que deseja EXCLUIR: "))
                    confirmar = input(f"Tem certeza que deseja apagar o cliente ID {id_remover}? (S/N): ").strip().upper()
                    if confirmar == "S":
                        resultado = crud_cliente.deletar_cliente(id_remover)
                        if resultado["sucesso"]:
                            print(f"{resultado['mensagem']}")
                        else:
                            print(f"Aviso: {resultado['mensagem']}")
                    else:
                        print("Operação de exclusão cancelada.")
                except ValueError:
                    print("Erro: O ID deve ser um número inteiro.")

            case "13":
                print("\n--- SALVAR BANCO EM CSV ---")
                print("\nSincronizando dados com o arquivo de estoque...")
                salvar_produtos_para_csv(crud_produto)

            case "0":
                print("\nSaindo do Painel Administrativo...")
                break
        
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    iniciar_interface_admin()