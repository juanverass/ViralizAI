import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurações do banco
USER = "postgres"
PASSWORD = "masterkey"
HOST = "localhost"
PORT = "5432"
DB_NAME = "ViralizaiAI"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Base do SQLAlchemy
Base = declarative_base()

def create_database_if_not_exists():
    conn = psycopg2.connect(dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Banco '{DB_NAME}' criado com sucesso!")
    else:
        print(f"Banco '{DB_NAME}' já existe.")
    cursor.close()
    conn.close()

create_database_if_not_exists()

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
