from controller.cliente_crud import ClienteCRUD
from controller.produto_crud import ProdutoCRUD
from data.gerenciamento_db import verificar_conexao_db
from repository.cliente_repository import ClienteRepository
from repository.produto_repository import ProdutoRepository
from service.cliente_service import ClienteService
from service.produto_service import ProdutoService

def conectar_engine():
    engine = verificar_conexao_db()
    return engine

def conectar_repositorio_produto():
    engine = conectar_engine()
    repositorio = ProdutoRepository(engine)
    return repositorio

def conectar_servico_produto():
    repositorio = conectar_repositorio_produto()
    servico = ProdutoService(repositorio)
    return servico

def conectar_crud_produto():
    servico = conectar_servico_produto()
    crud = ProdutoCRUD(servico)
    return crud

def conectar_repositorio_cliente():
    engine = conectar_engine()
    repositorio = ClienteRepository(engine)
    return repositorio

def conectar_servico_cliente():
    repositorio = conectar_repositorio_cliente()
    servico = ClienteService(repositorio)
    return servico

def conectar_crud_cliente():
    servico = conectar_servico_cliente()
    crud = ClienteCRUD(servico)
    return crud