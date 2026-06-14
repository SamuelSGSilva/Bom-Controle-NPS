from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import AvaliacaoNPS, Cliente, PosVenda
from auth import verificar_token

router = APIRouter()

@router.get("/relatorios/nps")
def relatorio_nps(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    avaliacoes = db.query(AvaliacaoNPS).all()
    total = len(avaliacoes)

    if total == 0:
       return {"message": "Nenhuma avaliação encontrada"}
    
    promotores = len([a for a in avaliacoes if a.score >= 9])
    neutros = len([a for a in avaliacoes if 7 <= a.score <= 8])
    detratores = len([a for a in avaliacoes if a.score <= 6])

    nps = ((promotores - detratores) / total) * 100

    return {
        "total_avaliacoes": total,
        "promotores": promotores,
        "neutros": neutros,
        "detratores": detratores,
        "nps": round(nps, 2)
    }

@router.get("/relatorios/clientes/buscar/{nome}")
def buscar_cliente_por_nome(nome: str, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    from models.models import Cliente
    cliente = db.query(Cliente).filter(Cliente.nome.ilike(f"%{nome}%")).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    pos_vendas = db.query(PosVenda).filter(PosVenda.cliente_id == cliente.id).all()
    avaliacoes_nps = db.query(AvaliacaoNPS).filter(AvaliacaoNPS.cliente_id == cliente.id).all()

    return {
        "cliente": {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "cpf": cliente.cpf,
            "cnpj": cliente.cnpj,
            "cidade": cliente.cidade,
            "estado": cliente.estado,
            "created_at": cliente.created_at.isoformat() if cliente.created_at else None
        },
        "pos_vendas": pos_vendas,
        "avaliacoes_nps": avaliacoes_nps
    }

@router.get("/relatorios/clientes/{cliente_id}")
def relatorio_cliente(cliente_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return {"message": "Cliente não encontrado"}

    pos_vendas = db.query(PosVenda).filter(PosVenda.cliente_id == cliente_id).all()
    avaliacoes_nps = db.query(AvaliacaoNPS).filter(AvaliacaoNPS.cliente_id == cliente_id).all()

    return {
       "cliente": {
    "id": cliente.id,
    "nome": cliente.nome,
    "email": cliente.email,
    "telefone": cliente.telefone,
    "cpf": cliente.cpf,
    "cnpj": cliente.cnpj,
    "cidade": cliente.cidade,
    "estado": cliente.estado,
    "created_at": cliente.created_at.isoformat() if cliente.created_at else None
},
        "pos_vendas": pos_vendas,
        "avaliacoes_nps": avaliacoes_nps
    }