from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Configuração do banco de dados
engine = create_engine("sqlite:///alunos.db", echo=True)  # Substitua pelo seu banco
Session = sessionmaker(bind=engine)
session = Session()

# Modelos
class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    serie = Column(String)
    turma = Column(String)
    turno = Column(String)
    data_atendimento = Column(DateTime, nullable=True)
    data_reuniao = Column(DateTime, nullable=True)
    demanda = Column(String)
    suporte = Column(String)
    retorno = Column(String)
    horario_atendimento = Column(String)
    resolucao = Column(String)


class Relatorio(Base):
    __tablename__ = "relatorios"

    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer)
    data_solicitacao = Column(DateTime, nullable=False)
    data_entrega = Column(DateTime, nullable=True)
    profissional_solicitante = Column(String)
    entregue = Column(Boolean, default=False)

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)
