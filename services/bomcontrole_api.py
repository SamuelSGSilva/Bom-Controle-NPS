import json
import os
import ssl
import urllib.request
import urllib.error
from typing import Any, Dict, List

import truststore

BASE_URL = "https://apinewintegracao.bomcontrole.com.br/integracao"

_ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _headers() -> Dict[str, str]:
    api_key = os.getenv("BOMCONTROLE_API_KEY")
    if not api_key:
        raise ValueError("Defina BOMCONTROLE_API_KEY no ambiente")
    return {"Authorization": f"ApiKey {api_key}"}


def obter_cliente(id: int) -> Dict[str, Any]:
    url = f"{BASE_URL}/Cliente/Obter/{id}"
    request = urllib.request.Request(url, headers=_headers())

    try:
        with urllib.request.urlopen(request, timeout=15, context=_ssl_context) as response:
            conteudo = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        corpo = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"BomControle retornou erro {exc.code} ao buscar o cliente {id}: {corpo}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Não foi possível acessar a API do BomControle: {exc.reason}"
        ) from exc

    return json.loads(conteudo)


def listar_clientes() -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/Cliente/Pesquisar"
    request = urllib.request.Request(url, headers=_headers())

    try:
        with urllib.request.urlopen(request, timeout=30, context=_ssl_context) as response:
            conteudo = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        corpo = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"BomControle retornou erro {exc.code} ao listar clientes: {corpo}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Não foi possível acessar a API do BomControle: {exc.reason}"
        ) from exc

    return json.loads(conteudo)


def mapear_cliente(dados: Dict[str, Any]) -> Dict[str, Any]:
    tipo = dados.get("TipoPessoa")
    endereco = dados.get("Endereco") or {}
    contatos = dados.get("Contatos") or []
    contato = next((c for c in contatos if c.get("Padrao")), contatos[0] if contatos else {})

    cpf = None
    cnpj = None
    nome = None
    data_nascimento = None

    if tipo == "Juridica":
        pessoa = dados.get("PessoaJuridica") or {}
        cnpj = pessoa.get("Documento")
        nome = pessoa.get("RazaoSocial") or pessoa.get("NomeFantasia")
    else:
        pessoa = dados.get("PessoaFisica") or {}
        cpf = pessoa.get("Documento")
        nome = pessoa.get("Nome")
        data_nascimento = pessoa.get("DataNascimento")

    return {
        "bomcontrole_id": dados.get("Id"),
        "nome": nome or contato.get("Nome"),
        "email": contato.get("Email"),
        "telefone": contato.get("Telefone"),
        "cpf": cpf,
        "cnpj": cnpj,
        "cep": endereco.get("Cep"),
        "logradouro": endereco.get("Logradouro"),
        "numero": endereco.get("Numero"),
        "bairro": endereco.get("Bairro"),
        "cidade": endereco.get("Cidade"),
        "estado": endereco.get("Uf"),
        "data_nascimento": data_nascimento,
    }
