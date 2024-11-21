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
    turma = ft.TextField(label="Turma: ")
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

    # Função para adicionar relatório
    def adicionar_relatorio(e):
        try:
            relatorio = Relatorio(
                aluno_id=int(aluno_id.value),
                data_solicitacao=datetime.strptime(data_solicitacao.value, "%d/%m/%Y"),
                data_entrega=datetime.strptime(data_entrega.value, "%d/%m/%Y") if data_entrega.value else None,
                profissional_solicitante=profissional_solicitante.value,
                entregue=entregue.value,
            )
            session.add(relatorio)
            session.commit()
            carregar_relatorios()
        except ValueError:
            page.dialog = ft.AlertDialog(title="Erro", content=ft.Text("Formato de data inválido! Use o formato dd/mm/yyyy"))
            page.dialog.open = True
            page.update()

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
                ]
            ))
        page.update()

    # Função para carregar relatórios
    def carregar_relatorios():
        tabela_relat.rows.clear()
        relatorios = session.query(Relatorio).all()
        for relatorio in relatorios:
            tabela_relat.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(relatorio.id))),
                    ft.DataCell(ft.Text(str(relatorio.aluno_id))),
                    ft.DataCell(ft.Text(relatorio.data_solicitacao.strftime("%d/%m/%Y"))),
                    ft.DataCell(ft.Text(relatorio.data_entrega.strftime("%d/%m/%Y") if relatorio.data_entrega else "")),
                    ft.DataCell(ft.Text(relatorio.profissional_solicitante)),
                    ft.DataCell(ft.Text("Sim" if relatorio.entregue else "Não")),
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

    # Função para exportar dados para Excel
    def exportar_excel(e):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Alunos"

        # Adicionar cabeçalho
        ws.append(["ID", "Nome", "Série", "Turma", "Turno", "Data Atendimento", "Data Reunião"])

        alunos = session.query(Aluno).all()
        for aluno in alunos:
            ws.append([
                aluno.id,
                aluno.nome,
                aluno.serie,
                aluno.turma,
                aluno.turno,
                aluno.data_atendimento.strftime("%d/%m/%Y") if aluno.data_atendimento else "",
                aluno.data_reuniao.strftime("%d/%m/%Y") if aluno.data_reuniao else ""
            ])

        output_dir = 'exportados'
        os.makedirs(output_dir, exist_ok=True)

        excel_path = os.path.join(output_dir, "dados_alunos_relatorios.xlsx")
        wb.save(excel_path)

        page.snack_bar = ft.SnackBar(ft.Text("Arquivo Excel exportado com sucesso!"), open=True)
        page.update()

    # Layout principal
    guia_alunos = ft.Column([
        ft.Text("Gerenciamento de Alunos", size=20),
        nome, serie, turma, turno, data_atendimento, data_reuniao, demanda, suporte, retorno, horario_atendimento, resolucao,
        ft.ElevatedButton("Adicionar Aluno", on_click=adicionar_aluno),
        tabela_alunos
    ])

    guia_relatórios = ft.Column([
        ft.Text("Gerenciamento de Relatórios", size=20),
        aluno_id, data_solicitacao, data_entrega, profissional_solicitante, entregue,
        ft.ElevatedButton("Adicionar Relatório", on_click=adicionar_relatorio),
        tabela_relat
    ])

    guia_exportacao = ft.Column([
        ft.Text("Exportação de Dados", size=20),
        ft.ElevatedButton("Exportar para Excel", on_click=exportar_excel),
    ])

    # Correção: Estrutura das abas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Alunos", content=guia_alunos),
            ft.Tab(text="Relatórios", content=guia_relatórios),
            ft.Tab(text="Exportação", content=guia_exportacao),
        ]
    )

    # Adicionando as abas no page
    page.add(tabs)

    carregar_alunos()

ft.app(target=main)