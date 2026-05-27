from service.cliente_service import ClienteService, ConflitoRegraErro, RegistroNaoEncontradoErro, ValidacaoErro

class ClienteCRUD:
    def __init__(self, service: ClienteService):
        self.service = service
    
    def criar_cliente(self, nome: str) -> dict:
        try:
            cliente_criado = self.service.criar_cliente(nome)
            return {
                "sucesso": True,
                "mensagem": f"Cliente '{cliente_criado.nome}' cadastrado com sucesso!",
                "dado": cliente_criado
            }
        except (ValidacaoErro, ConflitoRegraErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": None}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado: {e}", "dado": None}
    
    def buscar_cliente_por_id(self, cliente_id: int) -> dict:
        try:
            cliente = self.service.buscar_cliente_por_id(cliente_id)
            return {
                "sucesso": True,
                "mensagem": "Cliente localizado.",
                "dado": cliente
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": None}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado: {e}", "dado": None}
    
    def buscar_cliente_por_nome(self, nome: str) -> dict:
        try:
            cliente = self.service.buscar_cliente_por_nome(nome)
            return {
                "sucesso": True,
                "mensagem": "Cliente localizado.",
                "dado": cliente
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": None}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado: {e}", "dado": None}
    
    def listar_clientes(self) -> dict:
        try:
            clientes = self.service.listar_clientes()
            return {
                "sucesso": True,
                "mensagem": f"{len(clientes)} clientes listados.",
                "dado": clientes
            }
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro ao listar clientes: {e}", "dado": []}
    
    def atualizar_cliente(self, cliente_id: int, nome_novo: str) -> dict:
        try:
            cliente_atualizado = self.service.atualizar_cliente(
                cliente_id=cliente_id,
                nome_novo=nome_novo
            )
            return {
                "sucesso": True,
                "mensagem": "Cadastro do cliente atualizado com sucesso!",
                "dado": cliente_atualizado
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro, ConflitoRegraErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": None}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado ao atualizar: {e}", "dado": None}
    
    def deletar_cliente(self, cliente_id: int) -> dict:
        try:
            self.service.deletar_cliente(cliente_id)
            return {
                "sucesso": True,
                "mensagem": f"Cliente de ID {cliente_id} foi removido com sucesso.",
                "dado": True
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": False}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado ao remover: {e}", "dado": False}