from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)

    def __str__(self) -> str:
        return f"ID: {self.id} | Nome: {self.nome} | Estoque: {self.quantidade} | Preço: R${self.preco:.2f}"
    
    def exibir_selecao(self) -> None:
        print(f"{self.id} - {self.nome} (Estoque: {self.quantidade})")

    def calcular_total(self, quantidade_itens) -> float:
        return self.preco * quantidade_itens

    @property
    def esgotado(self) -> bool:
        return self.quantidade <= 0