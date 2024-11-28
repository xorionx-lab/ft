import os
import flet as ft
from db import session, Aluno, Relatorio
from datetime import datetime
import openpyxl

def main(page: ft.Page):
    page.title = "Gerenciamento de Alunos e Relatórios"
    page.scroll = "auto"

    # Campos de entrada para alunos
    nome = ft.TextField(label="Nome: ")
    serie = ft.TextField(label="Série: ")
    turma = ft.TextField(label="Turma:")
    turno = ft.TextField(label="Turno: ")
    data_atendimento = ft.TextField(label="Data de Atendimento (dd/mm/yyyy): ")
    data_reuniao = ft.TextField(label="Data de Reunião (dd/mm/yyyy): ")
    demanda = ft.TextField(label="Demanda: ")
    suporte = ft.TextField(label="Suporte: ")
    retorno = ft.TextField(label="Retorno: ")
    horario_atendimento = ft.TextField(label="Horário de Atendimento: ")
    resolucao = ft.TextField(label="Resolução da Demanda: ")

    # Campos de entrada para relatórios
    aluno_id = ft.TextField(label="ID do Aluno: ")
    data_solicitacao = ft.TextField(label="Data da Solicitação (dd/mm/yyyy): ")
    data_entrega = ft.TextField(label="Data da Entrega (dd/mm/yyyy): ")
    profissional_solicitante = ft.TextField(label="Profissional Solicitante: ")
    entregue = ft.Checkbox(label="Entregue", value=False)

    # Tabelas para exibir os dados
    tabela_alunos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Série")),
            ft.DataColumn(ft.Text("Turma")),
            ft.DataColumn(ft.Text("Turno")),
            ft.DataColumn(ft.Text("Data Atendimento")),
            ft.DataColumn(ft.Text("Data Reunião")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )

    tabela_relat = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("ID Aluno")),
            ft.DataColumn(ft.Text("Data Solicitação")),
            ft.DataColumn(ft.Text("Data Entrega")),
            ft.DataColumn(ft.Text("Profissional Solicitante")),
            ft.DataColumn(ft.Text("Entregue")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )

    # Função para adicionar aluno
    def adicionar_aluno(e):
        try:
            aluno = Aluno(
                nome=nome.value,
                serie=serie.value,
                turma=turma.value,
                turno=turno.value,
                data_atendimento=datetime.strptime(data_atendimento.value, "%d/%m/%Y") if data_atendimento.value else None,
                data_reuniao=datetime.strptime(data_reuniao.value, "%d/%m/%Y") if data_reuniao.value else None,
                demanda=demanda.value,
                suporte=suporte.value,
                retorno=retorno.value,
                horario_atendimento=horario_atendimento.value,
                resolucao=resolucao.value,
            )
            session.add(aluno)
            session.commit()
            carregar_alunos()
            limpar_campos()
        except ValueError:
            page.dialog = ft.AlertDialog(title="Erro", content=ft.Text("Formato de data inválido! Use o formato dd/mm/yyyy"))
            page.dialog.open = True
            page.update()

    # Função para editar aluno
    def editar_aluno(aluno_id):
        aluno = session.query(Aluno).filter_by(id=aluno_id).first()
        if aluno:
            nome.value = aluno.nome
            serie.value = aluno.serie
            turma.value = aluno.turma
            turno.value = aluno.turno
            data_atendimento.value = aluno.data_atendimento.strftime("%d/%m/%Y") if aluno.data_atendimento else ""
            data_reuniao.value = aluno.data_reuniao.strftime("%d/%m/%Y") if aluno.data_reuniao else ""
            demanda.value = aluno.demanda
            suporte.value = aluno.suporte
            retorno.value = aluno.retorno
            horario_atendimento.value = aluno.horario_atendimento
            resolucao.value = aluno.resolucao

            def salvar_edicao(e):
                aluno.nome = nome.value
                aluno.serie = serie.value
                aluno.turma = turma.value
                aluno.turno = turno.value
                aluno.data_atendimento = datetime.strptime(data_atendimento.value, "%d/%m/%Y") if data_atendimento.value else None
                aluno.data_reuniao = datetime.strptime(data_reuniao.value, "%d/%m/%Y") if data_reuniao.value else None
                aluno.demanda = demanda.value
                aluno.suporte = suporte.value
                aluno.retorno = retorno.value
                aluno.horario_atendimento = horario_atendimento.value
                aluno.resolucao = resolucao.value
                session.commit()
                carregar_alunos()
                limpar_campos()

            page.dialog = ft.AlertDialog(
                title=ft.Text("Editar Aluno"),
                content=ft.Column([nome, serie, turma, turno, data_atendimento, data_reuniao, demanda, suporte, retorno, horario_atendimento, resolucao]),
                actions=[ft.ElevatedButton("Salvar", on_click=salvar_edicao)],
            )
            page.dialog.open = True
            page.update()

    # Função para excluir aluno
    def excluir_aluno(aluno_id):
        aluno = session.query(Aluno).filter_by(id=aluno_id).first()
        if aluno:
            session.delete(aluno)
            session.commit()
            carregar_alunos()

    # Função para carregar alunos
    def carregar_alunos():
        tabela_alunos.rows.clear()
        alunos = session.query(Aluno).all()
        for aluno in alunos:
            tabela_alunos.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(aluno.id))),
                    ft.DataCell(ft.Text(aluno.nome)),
                    ft.DataCell(ft.Text(aluno.serie)),
                    ft.DataCell(ft.Text(aluno.turma)),
                    ft.DataCell(ft.Text(aluno.turno)),
                    ft.DataCell(ft.Text(aluno.data_atendimento.strftime("%d/%m/%Y") if aluno.data_atendimento else "")),
                    ft.DataCell(ft.Text(aluno.data_reuniao.strftime("%d/%m/%Y") if aluno.data_reuniao else "")),
                    ft.DataCell(ft.Row([
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, aluno_id=aluno.id: editar_aluno(aluno_id)),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, aluno_id=aluno.id: excluir_aluno(aluno_id)),
                    ])),
                ]
            ))
        page.update()

    # Função para limpar campos
    def limpar_campos():
        nome.value = serie.value = turma.value = turno.value = ""
        data_atendimento.value = data_reuniao.value = demanda.value = ""
        suporte.value = retorno.value = horario_atendimento.value = resolucao.value = ""
        aluno_id.value = data_solicitacao.value = data_entrega.value = profissional_solicitante.value = ""
        entregue.value = False
        page.update()

    # Estrutura da página
    guia_alunos = ft.Column([
        ft.Text("Gerenciamento de Alunos", size=20),
        nome, serie, turma, turno, data_atendimento, data_reuniao, demanda, suporte, retorno, horario_atendimento, resolucao,
        ft.ElevatedButton("Salvar Aluno", on_click=adicionar_aluno),
        tabela_alunos
    ])

    page.add(guia_alunos)
    carregar_alunos()

ft.app(target=main)
