from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import PosVenda, Cliente, LogAuditoria
from pydantic import BaseModel
from datetime import datetime
from auth import verificar_token
from services.auditoria import registrar_log

router = APIRouter()

class PosVendaCreate(BaseModel):
    cliente_id: int
    feedback: str | None = None
    status: str = "pendente"
    data_retorno: datetime | None = None
    observacoes: str | None = None

def _serializar_pos_venda(pv: PosVenda, cliente_nome: str | None):
    return {
        "id": pv.id,
        "cliente_id": pv.cliente_id,
        "cliente_nome": cliente_nome,
        "feedback": pv.feedback,
        "status": pv.status,
        "data_retorno": pv.data_retorno,
        "observacoes": pv.observacoes,
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

def _nome_cliente(db: Session, cliente_id: int) -> str | None:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    return cliente.nome if cliente else None

@router.post("/pos-venda")
def create_pos_venda(pos_venda: PosVendaCreate, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    novo = PosVenda(**pos_venda.model_dump())
    db.add(novo)
    db.flush()
    dados_depois = _serializar_pos_venda(novo, _nome_cliente(db, novo.cliente_id))
    registrar_log(db, token.get("sub"), "create", "pos_venda", novo.id, None, dados_depois)
    db.commit()
    db.refresh(novo)
    return novo

@router.delete("/pos-venda/{id}")
def deletar_pos_venda(id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    pv = db.query(PosVenda).filter(PosVenda.id == id).first()
    if not pv:
        raise HTTPException(status_code=404, detail="Pós-venda não encontrado")

    dados_antes = _serializar_pos_venda(pv, _nome_cliente(db, pv.cliente_id))
    registrar_log(db, token.get("sub"), "delete", "pos_venda", pv.id, dados_antes, None)
    db.delete(pv)
    db.commit()
    return {"message": "Pós-venda deletado com sucesso"}

@router.put("/pos-venda/{id}")
def editar_pos_venda(id: int, pos_venda: PosVendaCreate, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    db_pv = db.query(PosVenda).filter(PosVenda.id == id).first()
    if not db_pv:
        raise HTTPException(status_code=404, detail="Pós-venda não encontrado")
    dados_antes = _serializar_pos_venda(db_pv, _nome_cliente(db, db_pv.cliente_id))
    for key, value in pos_venda.model_dump().items():
        setattr(db_pv, key, value)
    db.flush()
    dados_depois = _serializar_pos_venda(db_pv, _nome_cliente(db, db_pv.cliente_id))
    registrar_log(db, token.get("sub"), "update", "pos_venda", db_pv.id, dados_antes, dados_depois)
    db.commit()
    db.refresh(db_pv)
    return db_pv
