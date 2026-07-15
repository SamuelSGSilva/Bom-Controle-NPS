import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/bom_controle?charset=utf8mb4",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def sincronizar_colunas():
    """Adiciona no banco as colunas novas que os models já têm mas as tabelas existentes ainda não.

    create_all() só cria tabelas que não existem; não altera tabelas já existentes.
    Sem um Alembic no projeto, isso evita que uma coluna nova quebre em produção
    (ex.: LogAuditoria.dados_depois adicionada depois que a tabela já existia).
    """
    inspector = inspect(engine)
    with engine.connect() as conn:
        for tabela in Base.metadata.sorted_tables:
            if not inspector.has_table(tabela.name):
                continue
            colunas_existentes = {col["name"] for col in inspector.get_columns(tabela.name)}
            for coluna in tabela.columns:
                if coluna.name in colunas_existentes:
                    continue
                tipo = coluna.type.compile(dialect=engine.dialect)
                conn.execute(text(f"ALTER TABLE {tabela.name} ADD COLUMN {coluna.name} {tipo}"))
                conn.commit()
