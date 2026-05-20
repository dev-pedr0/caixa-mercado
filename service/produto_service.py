from typing import List, Optional

from classes.Produto import Produto
from repository.produto_repository import ProdutoRepository


class ValidacaoErro(Exception):
    """Erro quando dados obrigatórios ou limites (valores negativos) são inválidos."""
    pass

class RegistroNaoEncontradoErro(Exception):
    """Erro quando um produto consultado por ID ou Nome não existe no banco."""
    pass

class ConflitoRegraErro(Exception):
    """Erro para duplicidade de nomes ou estoque insuficiente para venda."""
    pass

class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository
    
    def validar_campos_produto(self, nome: str, quantidade: int, preco: float, verificar_id: bool = False, id_prod: Optional[int] = None) -> None:
        if verificar_id:
            if id_prod is None:
                raise ValidacaoErro("O ID do produto é obrigatório.")
            if id_prod < 1:
                raise ValidacaoErro("O ID do produto não pode ser menor que 1.")
        if not nome or not str(nome).strip():
            raise ValidacaoErro("O Nome do produto é obrigatório e não pode ser vazio.")       
        if quantidade is None:
            raise ValidacaoErro("A Quantidade do produto é obrigatória.")
        if quantidade < 0:
            raise ValidacaoErro("A Quantidade do produto não pode ser menor que 0.")           
        if preco is None:
            raise ValidacaoErro("O Preço do produto é obrigatório.")
        if preco < 0:
            raise ValidacaoErro("O Preço do produto não pode ser menor que 0.")
    
    def criar_produto(self, nome: str, quantidade: int, preco: float) -> Produto:
        try:
            self.validar_campos_produto(nome, quantidade, preco)
            produto_duplicado = self.repository.buscar_produto_por_nome(nome)
            if produto_duplicado:
                raise ConflitoRegraErro(f"Já existe um produto cadastrado com o nome '{nome}'.")
            novo_produto = Produto(nome=nome.strip(), quantidade=quantidade, preco=preco)
            return self.repository.criar_produto(novo_produto)
        except (ValidacaoErro, ConflitoRegraErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao criar produto: {e}")
        
    def buscar_produto_por_id(self, produto_id: int) -> Produto:
        try:
            if produto_id is None or produto_id < 1:
                raise ValidacaoErro("Consulta inválida: O ID do produto deve ser maior que zero.")
            produto = self.repository.buscar_produto_por_id(produto_id)
            if not produto:
                raise RegistroNaoEncontradoErro(f"Produto com ID {produto_id} não existe no banco de dados.")     
            return produto
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao buscar por ID: {e}")
    
    def buscar_produto_por_nome(self, nome: str) -> Produto:
        try:
            if not nome or not nome.strip():
                raise ValidacaoErro("Consulta inválida: O nome do produto deve ser informado.")
            produto = self.repository.buscar_produto_por_nome(nome)
            if not produto:
                raise RegistroNaoEncontradoErro(f"Produto com o nome '{nome}' não foi encontrado.")
            return produto
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao buscar por nome: {e}")
    
    def listar_produtos(self) -> List[Produto]:
        try:
            return self.repository.listar_produtos()
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao listar produtos: {e}")
    
    def atualizar_produto(self, produto_id: int, nome_novo: str, quantidade_nova: int, preco_novo: float, eh_venda: bool = False, quantidade_venda: int = 0) -> Produto:
        try:
            produto_atual = self.buscar_produto_por_id(produto_id)
            
            if nome_novo.strip().lower() != produto_atual.nome.lower():
                colisao_nome = self.repository.buscar_produto_por_nome(nome_novo)
                if colisao_nome:
                    raise ConflitoRegraErro(f"Não é possível renomear: o nome '{nome_novo}' já está em uso por outro produto.")

            if eh_venda:
                if quantidade_venda <= 0:
                    raise ValidacaoErro("A quantidade a ser vendida deve ser maior que zero.")
                if produto_atual.quantidade < quantidade_venda:
                    raise ConflitoRegraErro(
                        f"Estoque insuficiente para a venda do produto '{produto_atual.nome}'. "
                        f"Estoque atual: {produto_atual.quantidade} | Solicitado: {quantidade_venda}"
                    )
                if quantidade_nova != (produto_atual.quantidade - quantidade_venda):
                    quantidade_nova = produto_atual.quantidade - quantidade_venda

            self.validar_campos_produto(nome_novo, quantidade_nova, preco_novo, verificar_id=True, id_prod=produto_id)

            produto_atual.nome = nome_novo.strip()
            produto_atual.quantidade = quantidade_nova
            produto_atual.preco = preco_novo
            return self.repository.atualizar_produto(produto_atual)
        except (ValidacaoErro, RegistroNaoEncontradoErro, ConflitoRegraErro) as e:
                raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao atualizar produto: {e}")
    
    def deletar_produto(self, produto_id: int) -> bool:
        try:
            if produto_id is None or produto_id < 1:
                raise ValidacaoErro("Exclusão inválida: O ID do produto deve ser maior que zero.")
            foi_deletado = self.repository.deletar_produto(produto_id)
            if not foi_deletado:
                raise RegistroNaoEncontradoErro(f"Impossível deletar: Produto com ID {produto_id} não existe.")
            return True
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao deletar produto: {e}")