from controller.produto_crud import ProdutoCRUD
from data.gerenciamento_db import verificar_conexao_db
from repository.produto_repository import ProdutoRepository
from service.produto_service import ProdutoService

def conectar_engine():
    engine = verificar_conexao_db()
    return engine

def conectar_repositorio():
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    return repositorio

def conectar_servico():
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    servico = ProdutoService(repositorio)
    return servico

def conectar_crud():
    engine = verificar_conexao_db()
    repositorio = ProdutoRepository(engine)
    servico = ProdutoService(repositorio)
    crud = ProdutoCRUD(servico)
    return crud