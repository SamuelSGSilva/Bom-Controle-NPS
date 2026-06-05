from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import PosVenda
from pydantic import BaseModel
from datetime import datetime
from auth import verificar_token

router = APIRouter()

class PosVendaCreate(BaseModel):
    cliente_id: int
    feedback: str | None = None
    status: str = "pendente"
    data_retorno: datetime | None = None

@router.post("/pos_venda/")
def create_pos_venda(pos_venda: PosVendaCreate, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    novo = PosVenda(**pos_venda.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/pos-venda/{cliente_id}")
def buscar_pos_venda(cliente_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return db.query(PosVenda).filter(PosVenda.cliente_id == cliente_id).all()