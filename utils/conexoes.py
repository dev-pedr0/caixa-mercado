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
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    return repositorio

def conectar_servico_produto():
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    servico = ProdutoService(repositorio)
    return servico

def conectar_crud_produto():
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    servico = ProdutoService(repositorio)
    crud = ProdutoCRUD(servico)
    return crud

def conectar_repositorio_cliente():
    engine = verificar_conexao_db()
    repositorio = ClienteRepository(engine)
    return repositorio

def conectar_servico_cliente():
    engine = verificar_conexao_db()
    repositorio = ClienteRepository(engine)
    servico = ClienteService(repositorio)
    return servico