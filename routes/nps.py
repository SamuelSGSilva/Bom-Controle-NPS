from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import AvaliacaoNPS
from pydantic import BaseModel
from auth import verificar_token

router = APIRouter()

class NPSSChema(BaseModel):
    cliente_id: int
    score: int
    feedback: str | None = None


@router.post("/nps")
def criar_avaliacao_nps(nps: NPSSChema, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
   novo = AvaliacaoNPS(**nps.model_dump())
   db.add(novo)
   db.commit()
   db.refresh(novo)
   return novo

@router.get("/nps/lista")
def listar_avaliacoes(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return db.query(AvaliacaoNPS).all()

@router.post("/nps/publico")
def avaliar_publico(nps: NPSSChema, db: Session = Depends(get_db)):
    novo = AvaliacaoNPS(**nps.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"message": "Avaliação registrada com sucesso!"}

@router.get("/nps/{cliente_id}")
def buscar_avaliacao(cliente_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
   return db.query(AvaliacaoNPS).filter(AvaliacaoNPS.cliente_id == cliente_id).first()

