from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import models
from models.models import Usuario
from routes import clientes, pos_venda, nps, auth, relatorios
from fastapi.middleware.cors import CORSMiddleware
from auth import gerar_hash_senha
import os

Base.metadata.create_all(bind=engine)

def criar_usuario_padrao():
    db = SessionLocal()
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        db.close()
        return

    existente = db.query(Usuario).filter(Usuario.username == username).first()
    if not existente:
        usuario = Usuario(
            username=username,
            hashed_password=gerar_hash_senha(password)
        )
        db.add(usuario)
        db.commit()
        print(f"Usuário {username} criado com sucesso!")
    db.close()

criar_usuario_padrao()

app = FastAPI(title="Bom Controle NPS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(pos_venda.router)
app.include_router(nps.router)
app.include_router(relatorios.router)

@app.get("/")
def root():
    return {"message": "API está funcionando!"}