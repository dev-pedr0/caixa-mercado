from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from classes.Produto import Produto

class ProdutoRepository:
    def __init__(self, engine):
        self.engine = engine
    
    def criar_produto(self, produto: Produto) -> Produto:
        try:
            with Session(self.engine) as session:
                session.add(produto)
                session.commit()
                #session.refresh(produto)
                return produto
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao criar produto: {e}")
        
    def buscar_produto_por_id(self, produto_id: int) -> Optional[Produto]:
        try:
            with Session(self.engine) as session:
                stmt = select(Produto).where(Produto.id == produto_id)
                return session.scalar(stmt)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao buscar produto por ID: {e}")
    
    def buscar_produto_por_nome(self, nome: str) -> Optional[Produto]:
        try:
            with Session(self.engine) as session:
                stmt = select(Produto).where(Produto.nome == nome.strip())
                return session.scalar(stmt)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao buscar produto por nome: {e}")
    
    def listar_produtos(self) -> list[Produto]:
        try:
            with Session(self.engine) as session:
                stmt = select(Produto).order_by(Produto.id)
                return list(session.scalars(stmt).all())
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao listar produtos: {e}")
    
    def atualizar_produto(self, produto_atualizado: Produto) -> Produto:
        try:
            with Session(self.engine) as session:
                produto_persistido = session.merge(produto_atualizado)
                session.commit()
                #session.refresh(produto_persistido)
                return produto_persistido
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao atualizar produto: {e}")
    
    def deletar_produto(self, produto_id: int) -> bool:
        try:
            with Session(self.engine) as session:
                stmt = select(Produto).where(Produto.id == produto_id)
                produto = session.scalar(stmt)
                
                if produto:
                    session.delete(produto)
                    session.commit()
                    return True
                
                return False
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao deletar produto: {e}")