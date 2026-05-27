from typing import List, Optional
from classes.Cliente import Cliente
from repository.cliente_repository import ClienteRepository


class ValidacaoErro(Exception):
    """Erro quando dados obrigatórios ou limites de tamanho são inválidos."""
    pass

class RegistroNaoEncontradoErro(Exception):
    """Erro quando um cliente consultado por ID ou Nome não existe no banco."""
    pass

class ConflitoRegraErro(Exception):
    """Erro para duplicidade de nomes de clientes no banco."""
    pass

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def validar_campos_cliente(self, nome: str, verificar_id: bool = False, id_cliente: Optional[int] = None) -> None:
        if verificar_id:
            if id_cliente is None:
                raise ValidacaoErro("O ID do cliente é obrigatório.")
            if id_cliente < 1:
                raise ValidacaoErro("O ID do cliente não pode ser menor que 1.")
                
        if not nome or not str(nome).strip():
            raise ValidacaoErro("O Nome do cliente é obrigatório e não pode ser vazio.")
            
        if len(str(nome)) > 50:
            raise ValidacaoErro("O Nome do cliente não pode conter mais de 50 caracteres.")
        
    def criar_cliente(self, nome: str) -> Cliente:
        try:
            self.validar_campos_cliente(nome)
            
            cliente_duplicado = self.repository.buscar_cliente_por_nome(nome)
            if cliente_duplicado:
                raise ConflitoRegraErro(f"Já existe um cliente cadastrado com o nome '{nome}'.")
                
            novo_cliente = Cliente(nome=nome.strip())
            return self.repository.criar_cliente(novo_cliente)
            
        except (ValidacaoErro, ConflitoRegraErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao criar cliente: {e}")
    
    def buscar_cliente_por_id(self, cliente_id: int) -> Cliente:
        try:
            if cliente_id is None or cliente_id < 1:
                raise ValidacaoErro("Consulta inválida: O ID do cliente deve ser maior que zero.")
                
            cliente = self.repository.buscar_cliente_por_id(cliente_id)
            if not cliente:
                raise RegistroNaoEncontradoErro(f"Cliente com ID {cliente_id} não existe no banco de dados.")
                
            return cliente
            
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao buscar cliente por ID: {e}")
    
    def buscar_cliente_por_nome(self, nome: str) -> Cliente:
        try:
            if not nome or not nome.strip():
                raise ValidacaoErro("Consulta inválida: O nome do cliente deve ser informado.")
                
            cliente = self.repository.buscar_cliente_por_nome(nome)
            if not cliente:
                raise RegistroNaoEncontradoErro(f"Cliente com o nome '{nome}' não foi encontrado.")
                
            return cliente
            
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao buscar cliente por nome: {e}")
        
    def listar_clientes(self) -> List[Cliente]:
        try:
            return self.repository.listar_clientes()
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao listar clientes: {e}")
    
    def atualizar_cliente(self, cliente_id: int, nome_novo: str) -> Cliente:
        try:
            cliente_atual = self.buscar_cliente_por_id(cliente_id)
            
            if nome_novo.strip().lower() != cliente_atual.nome.lower():
                colisao_nome = self.repository.buscar_cliente_por_nome(nome_novo)
                if colisao_nome:
                    raise ConflitoRegraErro(f"Não é possível alterar o nome: o nome '{nome_novo}' já está em uso.")
            
            self.validar_campos_cliente(nome_novo, verificar_id=True, id_cliente=cliente_id)
            
            cliente_atual.nome = nome_novo.strip()
            return self.repository.atualizar_cliente(cliente_atual)
            
        except (ValidacaoErro, RegistroNaoEncontradoErro, ConflitoRegraErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao atualizar cliente: {e}")
    
    def deletar_cliente(self, cliente_id: int) -> bool:
        try:
            if cliente_id is None or cliente_id < 1:
                raise ValidacaoErro("Exclusão inválida: O ID do cliente deve ser maior que zero.")
                
            foi_deletado = self.repository.deletar_cliente(cliente_id)
            if not foi_deletado:
                raise RegistroNaoEncontradoErro(f"Impossível deletar: Cliente com ID {cliente_id} não existe.")
                
            return True
            
        except (ValidacaoErro, RegistroNaoEncontradoErro) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Erro na camada de serviço ao deletar cliente: {e}")