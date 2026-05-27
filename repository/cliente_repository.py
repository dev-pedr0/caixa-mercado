from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from classes.Cliente import Cliente

class ClienteRepository:
    def __init__(self, engine):
        self.engine = engine

    def criar_cliente(self, cliente: Cliente) -> Cliente:
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                session.add(cliente)
                session.commit()
                return cliente
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao criar cliente: {e}")
        
    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[Cliente]:
        try:
            with Session(self.engine) as session:
                stmt = select(Cliente).where(Cliente.id == cliente_id)
                return session.scalar(stmt)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao buscar cliente por ID: {e}")
    
    def buscar_cliente_por_nome(self, nome: str) -> Optional[Cliente]:
        try:
            with Session(self.engine) as session:
                stmt = select(Cliente).where(Cliente.nome == nome.strip())
                return session.scalar(stmt)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao buscar cliente por nome: {e}")
    
    def listar_clientes(self) -> list[Cliente]:
        try:
            with Session(self.engine) as session:
                stmt = select(Cliente).order_by(Cliente.id)
                return list(session.scalars(stmt).all())
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao listar clientes: {e}")
        
    def atualizar_cliente(self, cliente_atualizado: Cliente) -> Cliente:
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                cliente_persistido = session.merge(cliente_atualizado)
                session.commit()
                return cliente_persistido
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao atualizar cliente: {e}")
    
    def deletar_cliente(self, cliente_id: int) -> bool:
        try:
            with Session(self.engine) as session:
                stmt = select(Cliente).where(Cliente.id == cliente_id)
                cliente = session.scalar(stmt)
                
                if cliente:
                    session.delete(cliente)
                    session.commit()
                    return True
                
                return False
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro no repositório ao deletar cliente: {e}")