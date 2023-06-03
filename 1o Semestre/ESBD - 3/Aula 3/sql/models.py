from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Motorista(Base):
    __tablename__ = "tbl_motoristas"

    cpf = Column("cpf", String(15), primary_key=True)
    nome = Column("nome", String())
    telefone = Column("telefone", String())
    endereco = Column("endereco", String())
    num_cnh = Column("num_cnh", String(), unique=True)
    nascimento = Column("nascimento", DateTime(), default=datetime.utcnow)

    def __init__(self, nome, telefone, cpf, endereco, nascimento):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.endereco = endereco
        self.nascimento = nascimento


class Caminhao(Base):
    __tablename__ = "tbl_caminhoes"

    placa = Column("placa", String(8), primary_key=True)
    modelo = Column("tipo", String())
    eficiencia = Column("eficiencia", Float())
    carga_maxima = Column("carga_maxima", Float())

    def __init__(
        self,
        placa,
        modelo,
        eficiencia,
        carga_maxima,
    ):
        self.placa = placa
        self.modelo = modelo
        self.eficiencia = eficiencia
        self.carga_maxima = carga_maxima


class Frete(Base):
    __tablename__ = "tbl_fretes"

    cpf_motorista = Column(
        "cpf_motorista", String(), ForeignKey("tbl_motoristas.cpf"), primary_key=True
    )
    placa_caminhao = Column(
        "placa_caminhao", String(), ForeignKey("tbl_caminhoes.placa"), primary_key=True
    )
    timestamp = Column(
        "timestamp", DateTime(timezone=True), default=datetime.utcnow, primary_key=True
    )
    distancia = Column("distancia", Float())
    valor = Column("valor", Float())

    def __init__(
        self,
        cpf_motorista,
        placa_caminhao,
        timestamp,
        distancia,
        valor,
    ):
        self.cpf_motorista = cpf_motorista
        self.placa_caminhao = placa_caminhao
        self.timestamp = timestamp
        self.distancia = distancia
        self.valor = valor