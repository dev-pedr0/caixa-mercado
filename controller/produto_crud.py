from service.produto_service import ConflitoRegraErro, ProdutoService, RegistroNaoEncontradoErro, ValidacaoErro

class ProdutoCRUD:
    def __init__(self, service: ProdutoService):
        self.service = service

    def criar_produto(self, nome: str, quantidade: int, preco: float) -> dict:
            try:
                produto_criado = self.service.criar_produto(nome, quantidade, preco)
                return {
                    "sucesso": True,
                    "mensagem": f"Produto '{produto_criado.nome}' cadastrado com sucesso!",
                    "dado": produto_criado
                }
            except (ValidacaoErro, ConflitoRegraErro) as e:
                return {"sucesso": False, "mensagem": str(e), "dado": None}
            except Exception as e:
                return {"sucesso": False, "mensagem": f"Erro inesperado: {e}", "dado": None}

    def buscar_produto_por_id(self, produto_id: int) -> dict:
            try:
                produto = self.service.buscar_produto_por_id(produto_id)
                return {
                    "sucesso": True,
                    "mensagem": "Produto localizado.",
                    "dado": produto
                }
            except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
                return {"sucesso": False, "mensagem": str(e), "dado": None}
            except Exception as e:
                return {"sucesso": False, "mensagem": f"Erro inesperado: {e}", "dado": None}
    
    def buscar_produto_por_nome(self, nome: str) -> dict:
        try:
            produto = self.service.buscar_produto_por_nome(nome)
            return {
                "sucesso": True,
                "mensagem": "Produto localizado.",
                "dado": produto
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": None}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado: {e}", "dado": None}
    
    def listar_produtos(self) -> dict:
        try:
            produtos = self.service.listar_produtos()
            return {
                "sucesso": True,
                "mensagem": f"{len(produtos)} produtos listados.",
                "dado": produtos
            }
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro ao listar catálogo: {e}", "dado": []}
    
    def atualizar_produto(self, produto_id: int, nome_novo: str, quantidade_nova: int, preco_novo: float) -> dict:
        try:
            produto_atualizado = self.service.atualizar_produto(
                produto_id=produto_id,
                nome_novo=nome_novo,
                quantidade_nova=quantidade_nova,
                preco_novo=preco_novo,
                eh_venda=False
            )
            return {
                "sucesso": True,
                "mensagem": "Produto atualizado com sucesso!",
                "dado": produto_atualizado
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro, ConflitoRegraErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": None}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado ao atualizar: {e}", "dado": None}
    
    def deletar_produto(self, produto_id: int) -> dict:
        try:
            self.service.deletar_produto(produto_id)
            return {
                "sucesso": True,
                "mensagem": f"Produto de ID {produto_id} foi removido com sucesso.",
                "dado": True
            }
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            return {"sucesso": False, "mensagem": str(e), "dado": False}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro inesperado ao remover: {e}", "dado": False}