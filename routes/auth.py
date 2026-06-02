from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.models import Usuario
from auth import criar_token, gerar_hash_senha, verificar_senha

router = APIRouter()

class LoginSchema(BaseModel):
    username: str
    password: str

class UsuarioSchema(BaseModel):
    username: str
    password: str

@router.post("/registrar")
def registrar(dados: UsuarioSchema, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.username == dados.username).first()
    if existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    novo = Usuario(username=dados.username, hashed_password=gerar_hash_senha(dados.password))
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"message": "Usuário registrado com sucesso"}

@router.post("/token")
def login(dados: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == dados.username).first()
    if not usuario:
        raise HTTPException(status_code=401, detail = "Usuário inválido")
    if not verificar_senha(dados.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail = "Senha inválida")
    token = criar_token({"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}