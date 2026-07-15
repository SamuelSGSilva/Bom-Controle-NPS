from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import PosVenda, Cliente, LogAuditoria
from pydantic import BaseModel
from datetime import datetime
import json
from auth import verificar_token

router = APIRouter()

class PosVendaCreate(BaseModel):
    cliente_id: int
    feedback: str | None = None
    status: str = "pendente"
    data_retorno: datetime | None = None

def _serializar_pos_venda(pv: PosVenda, cliente_nome: str | None):
    return {
        "id": pv.id,
        "cliente_id": pv.cliente_id,
        "cliente_nome": cliente_nome,
        "feedback": pv.feedback,
        "status": pv.status,
        "data_retorno": pv.data_retorno,
        "created_at": pv.created_at,
    }

@router.get("/pos-venda")
def listar_pos_vendas(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    resultados = (
        db.query(PosVenda, Cliente.nome)
        .outerjoin(Cliente, Cliente.id == PosVenda.cliente_id)
        .all()
    )
    return [_serializar_pos_venda(pv, nome) for pv, nome in resultados]

@router.get("/pos-venda/buscar/{id}")
def buscar_pos_venda_por_id(id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    pv = db.query(PosVenda).filter(PosVenda.id == id).first()
    if not pv:
        raise HTTPException(status_code=404, detail="Pós-venda não encontrado")
    return pv

@router.get("/logs-auditoria")
def listar_logs_auditoria(entidade: str | None = None, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    query = db.query(LogAuditoria)
    if entidade:
        query = query.filter(LogAuditoria.entidade == entidade)
    return query.order_by(LogAuditoria.created_at.desc()).all()

@router.get("/pos-venda/{cliente_id}")
def buscar_pos_venda(cliente_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return db.query(PosVenda).filter(PosVenda.cliente_id == cliente_id).all()

@router.post("/pos-venda")
def create_pos_venda(pos_venda: PosVendaCreate, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    novo = PosVenda(**pos_venda.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.delete("/pos-venda/{id}")
def deletar_pos_venda(id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    pv = db.query(PosVenda).filter(PosVenda.id == id).first()
    if not pv:
        raise HTTPException(status_code=404, detail="Pós-venda não encontrado")

    dados_antes = _serializar_pos_venda(pv, None)
    dados_antes["data_retorno"] = str(dados_antes["data_retorno"]) if dados_antes["data_retorno"] else None
    dados_antes["created_at"] = str(dados_antes["created_at"]) if dados_antes["created_at"] else None

    log = LogAuditoria(
        usuario=token.get("sub"),
        acao="delete",
        entidade="pos_venda",
        entidade_id=pv.id,
        dados_antes=json.dumps(dados_antes, ensure_ascii=False),
    )
    db.add(log)
    db.delete(pv)
    db.commit()
    return {"message": "Pós-venda deletado com sucesso"}

@router.put("/pos-venda/{id}")
def editar_pos_venda(id: int, pos_venda: PosVendaCreate, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    db_pv = db.query(PosVenda).filter(PosVenda.id == id).first()
    if not db_pv:
        raise HTTPException(status_code=404, detail="Pós-venda não encontrado")
    for key, value in pos_venda.model_dump().items():
        setattr(db_pv, key, value)
    db.commit()
    db.refresh(db_pv)
    return db_pv
