from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from database import Base
import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefone = Column(String(20), nullable=True)
    cpf = Column(String(14), nullable=True, unique=True)
    cnpj = Column(String(18), nullable=True, unique=True)
    cep = Column(String(9), nullable=True)
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(10), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    data_nascimento = Column(DateTime, nullable=True)
    bomcontrole_id = Column(Integer, nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PosVenda(Base):
    __tablename__ = "pos_vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    feedback = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="pendente")
    data_retorno = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AvaliacaoNPS(Base):
    __tablename__ = "avaliacao_nps"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_os = Column(String(50), nullable=True)
    produto_servico = Column(String(255), nullable=True)
    data_atendimento = Column(DateTime, nullable=True)
    cidade_estado = Column(String(100), nullable=True)
    nota_primeiro_contato = Column(Integer, nullable=True)
    nota_clareza_informacoes = Column(Integer, nullable=True)
    nota_processo_fechamento = Column(Integer, nullable=True)
    nota_link_pagamento = Column(Integer, nullable=True)
    nota_nota_fiscal = Column(Integer, nullable=True)
    nota_entrega_prazo = Column(Integer, nullable=True)
    nota_embalagem = Column(Integer, nullable=True)
    nota_entrega_tecnica = Column(Integer, nullable=True)
    nota_suporte_produto = Column(Integer, nullable=True)
    avaliacao_geral = Column(Integer, nullable=True)
    nps_score = Column(Integer, nullable=True)
    consideracoes = Column(String(1000), nullable=True)
    o_que_gostou = Column(String(1000), nullable=True)
    o_que_melhorar = Column(String(1000), nullable=True)
    media_geral = Column(Float, nullable=True)
    resp_entrega_tecnica = Column(String(100), nullable=True)
    cs_responsavel = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)