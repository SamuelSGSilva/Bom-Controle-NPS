import csv
import os
import urllib.request
from typing import List, Tuple, Dict, Any
from datetime import datetime


def _parse_data(value: Any):
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value)

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue

    return value


def converter_linha_para_payload(row: List[Any], linha_num: int) -> Tuple[Dict[str, Any], str]:
    nome_cliente = row[2] if len(row) > 2 else None
    if not nome_cliente:
        return {}, ""

    payload = {
        "numero_os": str(row[1]) if len(row) > 1 and row[1] else None,
        "produto_servico": row[4] if len(row) > 4 else None,
        "data_atendimento": _parse_data(row[0]) if len(row) > 0 else None,
        "cidade_estado": row[3] if len(row) > 3 else None,
        "nota_primeiro_contato": row[5] if len(row) > 5 else None,
        "nota_clareza_informacoes": row[6] if len(row) > 6 else None,
        "nota_processo_fechamento": row[7] if len(row) > 7 else None,
        "nota_link_pagamento": row[8] if len(row) > 8 else None,
        "nota_nota_fiscal": row[9] if len(row) > 9 else None,
        "nota_entrega_prazo": row[10] if len(row) > 10 else None,
        "nota_embalagem": row[11] if len(row) > 11 else None,
        "nota_entrega_tecnica": row[12] if len(row) > 12 else None,
        "nota_suporte_produto": row[13] if len(row) > 13 else None,
        "nps_score": row[14] if len(row) > 14 else None,
        "consideracoes": row[15] if len(row) > 15 else None,
        "media_geral": row[16] if len(row) > 16 else None,
        "resp_entrega_tecnica": row[17] if len(row) > 17 else None,
        "cs_responsavel": row[18] if len(row) > 18 else None,
    }

    if isinstance(payload.get("nps_score"), (int, float)):
        payload["nps_score"] = int(payload["nps_score"])

    return payload, str(nome_cliente)


def buscar_registros_google_sheets():
    spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
    if not spreadsheet_id:
        raise ValueError("Defina GOOGLE_SPREADSHEET_ID no ambiente")

    url = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        "/gviz/tq?tqx=out:csv&sheet=Registros"
    )

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            conteudo = response.read().decode("utf-8")
    except Exception as exc:
        raise RuntimeError(
            "Não foi possível acessar a planilha. Verifique se ela está "
            "compartilhada como 'Qualquer pessoa com o link pode visualizar'."
        ) from exc

    return list(csv.reader(conteudo.splitlines()))
