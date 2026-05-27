import os
import sys
import pandas as pd
from sqlalchemy import Engine, create_engine, select
from classes.Modelo_Base import Base
from classes.Produto import Produto
from classes.Cliente import Cliente
from sqlalchemy.orm import Session

from data.web_scraping import realizar_scraping_produtos

DB_PATH = os.path.join("data", "mercado.db")
CSV_PATH = os.path.join("data", "produtos.csv")
JSON_PATH = os.path.join("data", "clientes.json")
CONN_STR = f"sqlite:///{DB_PATH}"

def criar_db() -> None:
    os.makedirs("data", exist_ok=True)
    
    print(f"Criando o banco de dados em: {DB_PATH}...")
    
    engine = create_engine(CONN_STR)
    
    Base.metadata.create_all(engine)
    
    print("Tabela 'produtos' e 'clientes' criada com sucesso!")

def verificar_conexao_db() -> Engine:
    if not os.path.exists(DB_PATH):
        print(f"Erro Crítico: O arquivo do banco de dados '{DB_PATH}' não foi encontrado.")
        sys.exit(1)
    
    try:
        engine = create_engine(CONN_STR)
        with engine.connect() as conexao:
            pass
        return engine
    except Exception as e:
        print(f"Erro Crítico ao conectar com o banco de dados: {e}")
        sys.exit(1)

def verificar_csv(caminho_csv: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(caminho_csv, sep=',')
        return df
    except FileNotFoundError:
        print(f"Erro Crítico: O arquivo CSV em '{caminho_csv}' não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        sys.exit(1)

def verificar_json(caminho_json: str) -> pd.DataFrame:
    try:
        df = pd.read_json(caminho_json)
        return df
    except FileNotFoundError:
        print(f"Erro Crítico: O arquivo CSV em '{caminho_json}' não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        sys.exit(1)


def sincronizar_db_csv (engine: Engine, caminho_csv: str) -> None:
    df = verificar_csv(caminho_csv)
    
    print("Iniciando a sincronização de produtos...")

    try:
        with Session(engine) as session:
            for _, linha in df.iterrows():
                nome_csv = str(linha["nome"]).strip()
                qtd_csv = int(linha["quantidade"])
                preco_csv = float(linha["preco"])
                stmt = select(Produto).where(Produto.nome == nome_csv)
                produto_existente = session.scalar(stmt)

                if produto_existente:
                    produto_existente.quantidade = qtd_csv
                    produto_existente.preco = preco_csv
                else:
                    novo_produto = Produto(
                        nome=nome_csv,
                        quantidade=qtd_csv,
                        preco=preco_csv
                    )
                    session.add(novo_produto)
            session.commit()

            print("Sincronização concluída com sucesso!")

    except Exception as e:
        print(f"Erro inesperado durante a alimentação do banco com produtos: {e}")
        sys.exit(1)

def sincronizar_db_json (engine: Engine, caminho_json: str) -> None:
    df = verificar_json(caminho_json)

    print("Iniciando a sincronização de clientes...")

    try:
        with Session(engine) as session:
            for _, linha in df.iterrows():
                nome_cliente = str(linha["nome"]).strip()

                stmt = select(Cliente).where(Cliente.nome == nome_cliente)
                cliente_existente = session.scalar(stmt)

                if not cliente_existente:
                    novo_cliente = Cliente(nome=nome_cliente)
                    session.add(novo_cliente)
            session.commit()

            print("Sincronização concluída com sucesso!")
    except Exception as e:
        print(f"Erro inesperado durante a alimentação do banco com clientes: {e}")
        sys.exit(1)

def alimentar_db() -> None:
    sucesso_scraping = realizar_scraping_produtos(CSV_PATH)
    if not sucesso_scraping:
        sys.exit(1)
        
    engine = verificar_conexao_db()
    sincronizar_db_csv(engine, CSV_PATH)
    sincronizar_db_json(engine, JSON_PATH)

def salvar_banco_para_csv(crud) -> None:
    resultado = crud.listar_produtos()
    if not resultado["sucesso"]:
        print(f"Erro ao ler banco para atualizar CSV: {resultado['mensagem']}")
    
    produtos_banco = resultado["dado"]
    try:
        dados_produtos = [
            {
                "nome": prod.nome,
                "quantidade": prod.quantidade,
                "preco": prod.preco
            }
            for prod in produtos_banco
        ]
        df = pd.DataFrame(dados_produtos)
        df.to_csv(CSV_PATH, sep=',', index=False, encoding='utf-8')
        print("\nAtualização de produtos feita com sucesso!")
    except Exception as e:
        print(f"Erro crítico ao salvar o produtos em arquivo CSV: {e}")