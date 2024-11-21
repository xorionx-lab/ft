from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Define o modelo para Alunos
class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    serie = Column(String, nullable=True)
    turma = Column(String, nullable=True)
    turno = Column(String, nullable=True)
    data_atendimento = Column(DateTime, nullable=True)
    data_reuniao = Column(DateTime, nullable=True)
    data_encontro = Column(DateTime, nullable=True)  # Nova coluna
    demanda = Column(String, nullable=True)
    suporte = Column(String, nullable=True)
    retorno = Column(String, nullable=True)
    horario_atendimento = Column(String, nullable=True)
    resolucao = Column(String, nullable=True)

    relatorios = relationship("Relatorio", back_populates="aluno")

# Define o modelo para Relatórios
class Relatorio(Base):
    __tablename__ = 'relatorios'

    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    data_solicitacao = Column(DateTime, nullable=False)
    data_entrega = Column(DateTime, nullable=True)
    profissional_solicitante = Column(String, nullable=False)
    entregue = Column(Boolean, default=False)

    aluno = relationship("Aluno", back_populates="relatorios")

# Cria o banco de dados
engine = create_engine('sqlite:///alunos.db')
Base.metadata.create_all(engine)

# Configura o Session
Session = sessionmaker(bind=engine)
session = Session()
