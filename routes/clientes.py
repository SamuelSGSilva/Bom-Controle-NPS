from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Cliente
from pydantic import BaseModel
from auth import verificar_token
from datetime import datetime
from services.bomcontrole_api import obter_cliente, mapear_cliente
from services.sincronizacao_clientes import sincronizar_todos_clientes

router = APIRouter()

class ClienteSchema(BaseModel):
    nome: str
    email: str
    telefone: str | None = None
    cpf: str | None = None
    cnpj: str | None = None
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    data_nascimento: datetime | None = None

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

@router.post("/clientes/sincronizar-bomcontrole/{bomcontrole_id}")
def sincronizar_cliente_bomcontrole(bomcontrole_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    try:
        dados = obter_cliente(bomcontrole_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    mapeado = mapear_cliente(dados)

    if not mapeado.get("email"):
        raise HTTPException(
            status_code=400,
            detail="Cliente do BomControle não possui e-mail de contato cadastrado.",
        )

    cliente = db.query(Cliente).filter(Cliente.bomcontrole_id == bomcontrole_id).first()
    if cliente:
        for key, value in mapeado.items():
            if value is not None:
                setattr(cliente, key, value)
    else:
        cliente = Cliente(**mapeado)
        db.add(cliente)

    db.commit()
    db.refresh(cliente)
    return cliente

@router.post("/clientes/sincronizar-bomcontrole")
def sincronizar_todos_clientes_bomcontrole(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    try:
        return sincronizar_todos_clientes(db)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@router.put("/clientes/{id}")
def editar_cliente(id: int, cliente: ClienteSchema, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente