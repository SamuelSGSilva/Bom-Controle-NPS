from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.models import Avaliacao, Cliente
from pydantic import BaseModel
from auth import verificar_token
import openpyxl
from io import BytesIO

router = APIRouter()

class AvaliacaoSchema(BaseModel):
    cliente_id: int
    numero_os: str | None = None
    produto_servico: str | None = None
    nota_primeiro_contato: int | None = None
    nota_clareza_informacoes: int | None = None
    nota_processo_fechamento: int | None = None
    nota_link_pagamento: int | None = None
    nota_nota_fiscal: int | None = None
    nota_entrega_prazo: int | None = None
    nota_embalagem: int | None = None
    nota_entrega_tecnica: int | None = None
    nota_suporte_produto: int | None = None
    avaliacao_geral: int | None = None
    nps_score: int | None = None
    o_que_gostou: str | None = None
    o_que_melhorar: str | None = None
    cs_responsavel: str | None = None

@router.get("/avaliacoes")
def listar_avaliacoes(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return db.query(Avaliacao).all()

@router.post("/avaliacoes/publico")
def criar_avaliacao_publico(avaliacao: AvaliacaoSchema, db: Session = Depends(get_db)):
    nova = Avaliacao(**avaliacao.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return {"message": "Avaliação registrada com sucesso!"}

@router.post("/avaliacoes")
def criar_avaliacao(avaliacao: AvaliacaoSchema, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    nova = Avaliacao(**avaliacao.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/avaliacoes/{cliente_id}")
def buscar_avaliacoes_cliente(cliente_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return db.query(Avaliacao).filter(Avaliacao.cliente_id == cliente_id).all()

@router.post("/avaliacoes/importar")
async def importar_planilha(file: UploadFile = File(...), db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    conteudo = await file.read()
    wb = openpyxl.load_workbook(BytesIO(conteudo), data_only=True)

    if "Registros" not in wb.sheetnames:
        raise HTTPException(status_code=400, detail="Aba 'Registros' não encontrada na planilha")

    ws = wb["Registros"]

    importados = 0

    for i, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
        nome_cliente = row[2]

        if not nome_cliente:
            continue

        cliente = db.query(Cliente).filter(Cliente.nome == nome_cliente).first()

        if not cliente:
            cliente = Cliente(
                nome=nome_cliente,
                email=f"sem-email-{i}@autoluiz.com"
            )
            db.add(cliente)
            db.commit()
            db.refresh(cliente)

        nova = Avaliacao(
            cliente_id=cliente.id,
            numero_os=str(row[1]) if row[1] else None,
            produto_servico=row[4],
            nota_primeiro_contato=row[5],
            nota_clareza_informacoes=row[6],
            nota_processo_fechamento=row[7],
            nota_link_pagamento=row[8],
            nota_nota_fiscal=row[9],
            nota_entrega_prazo=row[10],
            nota_embalagem=row[11],
            nota_entrega_tecnica=row[12],
            nota_suporte_produto=row[13],
            nps_score=row[14],
            o_que_gostou=row[15] if row[15] else None,
            cs_responsavel=row[18] if len(row) > 18 else None
        )
        db.add(nova)
        importados += 1

    db.commit()
    return {"message": f"{importados} avaliações importadas com sucesso!"}