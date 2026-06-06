from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Cliente
from pydantic import BaseModel
from auth import verificar_token

router = APIRouter()

class ClienteSchema(BaseModel):
    nome: str
    email: str
    telefone: str | None = None

@router.post("/clientes")
def criar_cliente(cliente: ClienteSchema, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    novo = Cliente(**cliente.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/clientes")
def listar_clientes(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return db.query(Cliente).all()

@router.get("/clientes/{id}")
def buscar_cliente(id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.delete("/clientes/{id}")
def deletar_cliente(id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}