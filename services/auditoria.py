import json
from sqlalchemy.orm import Session

from models.models import LogAuditoria


def registrar_log(
    db: Session,
    usuario: str | None,
    acao: str,
    entidade: str,
    entidade_id: int,
    dados_antes: dict | None = None,
    dados_depois: dict | None = None,
) -> LogAuditoria:
    log = LogAuditoria(
        usuario=usuario,
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        dados_antes=json.dumps(dados_antes, ensure_ascii=False, default=str) if dados_antes is not None else None,
        dados_depois=json.dumps(dados_depois, ensure_ascii=False, default=str) if dados_depois is not None else None,
    )
    db.add(log)
    return log
