from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from classes.Modelo_Base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)

    def __str__(self) -> str:
        return f"ID: {self.id} | Cliente: {self.nome}"