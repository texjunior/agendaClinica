from datetime import datetime, timedelta

from medicos.models import AgendaMedico
from .models import Agendamento


STATUS_OCUPA_HORARIO = ["agendado", "confirmado", "aguardando", "em_atendimento"]


def gerar_horarios_disponiveis(medico, data_consulta, tipo_atendimento=None, ignorar_agendamento_id=None):
    dia_semana = data_consulta.weekday()

    agendas = AgendaMedico.objects.filter(
        medico=medico,
        dia_semana=dia_semana,
        ativo=True
    ).order_by("hora_inicio")

    horarios_livres_totais = []

    for agenda in agendas:
        inicio = datetime.combine(data_consulta, agenda.hora_inicio)
        fim = datetime.combine(data_consulta, agenda.hora_fim)

        horarios_faixa = []
        atual = inicio

        while atual < fim:
            horarios_faixa.append(atual.time())
            atual += timedelta(minutes=agenda.duracao_consulta)

        agendamentos_faixa = Agendamento.objects.filter(
            medico=medico,
            data_consulta=data_consulta,
            status__in=STATUS_OCUPA_HORARIO,
            hora_consulta__gte=agenda.hora_inicio,
            hora_consulta__lt=agenda.hora_fim,
        )

        if ignorar_agendamento_id:
            agendamentos_faixa = agendamentos_faixa.exclude(id=ignorar_agendamento_id)

        horarios_ocupados = set(
            agendamentos_faixa.values_list("hora_consulta", flat=True)
        )

        horarios_livres_faixa = [
            horario for horario in horarios_faixa
            if horario not in horarios_ocupados
        ]

        if tipo_atendimento == "convenio":
            capacidade = agenda.vagas_convenio
            usados_tipo = agendamentos_faixa.filter(tipo_atendimento="convenio").count()
            restante = max(capacidade - usados_tipo, 0)
            horarios_livres_faixa = horarios_livres_faixa[:restante]

        elif tipo_atendimento == "particular":
            capacidade = agenda.vagas_particular
            usados_tipo = agendamentos_faixa.filter(tipo_atendimento="particular").count()
            restante = max(capacidade - usados_tipo, 0)
            horarios_livres_faixa = horarios_livres_faixa[:restante]

        horarios_livres_totais.extend(horarios_livres_faixa)

    return sorted(horarios_livres_totais)