from sqlalchemy.orm import Session

from models.models import Cliente
from services.bomcontrole_api import listar_clientes, mapear_cliente

# Campos de status que devem sempre refletir o BomControle, diferente dos
# campos de cadastro (nome, telefone, endereço etc.) que só são preenchidos
# se estiverem vazios, para não sobrescrever edições feitas aqui.
CAMPOS_SEMPRE_SINCRONIZADOS = {"bloqueado"}


def sincronizar_todos_clientes(db: Session) -> dict:
    registros = listar_clientes()

    criados = 0
    atualizados = 0
    ignorados = 0

    for dados in registros:
        mapeado = mapear_cliente(dados)
        if not mapeado.get("email"):
            ignorados += 1
            continue

        cliente = db.query(Cliente).filter(Cliente.bomcontrole_id == mapeado["bomcontrole_id"]).first()
        if not cliente:
            cliente = db.query(Cliente).filter(Cliente.email == mapeado["email"]).first()

        if cliente:
            for key, value in mapeado.items():
                if key in CAMPOS_SEMPRE_SINCRONIZADOS:
                    if value is not None:
                        setattr(cliente, key, value)
                elif value is not None and getattr(cliente, key) is None:
                    setattr(cliente, key, value)
        else:
            cliente = Cliente(**mapeado)
            db.add(cliente)

        eh_novo = cliente.id is None
        try:
            db.commit()
        except Exception:
            db.rollback()
            ignorados += 1
            continue

        if eh_novo:
            criados += 1
        else:
            atualizados += 1

    return {
        "total_bomcontrole": len(registros),
        "criados": criados,
        "atualizados": atualizados,
        "ignorados": ignorados,
    }
