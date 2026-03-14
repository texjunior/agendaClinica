from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from django.http import JsonResponse

from .forms import MedicoForm, EspecialidadeForm, ConvenioForm, AgendaMedicoForm, AgendaSemanalMedicoForm
from .models import Medico, Especialidade, Convenio, AgendaMedico

def lista_medicos(request):
    medicos = Medico.objects.select_related("especialidade").prefetch_related("convenios").order_by("nome")
    busca = request.GET.get("busca", "")
    ativo = request.GET.get("ativo", "")

    if busca:
        medicos = medicos.filter(nome__icontains=busca)

    if ativo == "1":
        medicos = medicos.filter(ativo=True)
    elif ativo == "0":
        medicos = medicos.filter(ativo=False)

    return render(request, "medicos/lista_medicos.html", {"medicos": medicos})


def novo_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico cadastrado com sucesso.")
            return redirect("lista_medicos")
    else:
        form = MedicoForm()

    return render(
        request,
        "medicos/form_medico.html",
        {
            "form": form,
            "titulo_pagina": "Novo Médico",
            "subtitulo_pagina": "Cadastre um novo médico no sistema.",
            "modo_edicao": False,
        },
    )


def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == "POST":
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico atualizado com sucesso.")
            return redirect("lista_medicos")
    else:
        form = MedicoForm(instance=medico)

    return render(
        request,
        "medicos/form_medico.html",
        {
            "form": form,
            "titulo_pagina": "Editar Médico",
            "subtitulo_pagina": "Atualize os dados do médico.",
            "modo_edicao": True,
        },
    )


def excluir_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == "POST":
        medico.delete()
        messages.success(request, "Médico excluído com sucesso.")
        return redirect("lista_medicos")

    return render(request, "medicos/confirmar_exclusao_medico.html", {"medico": medico})


def lista_especialidades(request):
    especialidades = Especialidade.objects.all().order_by("nome")
    busca = request.GET.get("busca", "").strip()

    if busca:
        especialidades = especialidades.filter(nome__icontains=busca)

    return render(
        request,
        "medicos/lista_especialidades.html",
        {"especialidades": especialidades},
    )


def nova_especialidade(request):
    if request.method == "POST":
        form = EspecialidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidade cadastrada com sucesso.")
            return redirect("lista_especialidades")
    else:
        form = EspecialidadeForm()

    return render(
        request,
        "medicos/form_especialidade.html",
        {
            "form": form,
            "titulo_pagina": "Nova Especialidade",
            "subtitulo_pagina": "Cadastre uma nova especialidade no sistema.",
            "modo_edicao": False,
        },
    )


def editar_especialidade(request, especialidade_id):
    especialidade = get_object_or_404(Especialidade, id=especialidade_id)

    if request.method == "POST":
        form = EspecialidadeForm(request.POST, instance=especialidade)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidade atualizada com sucesso.")
            return redirect("lista_especialidades")
    else:
        form = EspecialidadeForm(instance=especialidade)

    return render(
        request,
        "medicos/form_especialidade.html",
        {
            "form": form,
            "titulo_pagina": "Editar Especialidade",
            "subtitulo_pagina": "Atualize os dados da especialidade.",
            "modo_edicao": True,
        },
    )


def excluir_especialidade(request, especialidade_id):
    especialidade = get_object_or_404(Especialidade, id=especialidade_id)

    if request.method == "POST":
        especialidade.delete()
        messages.success(request, "Especialidade excluída com sucesso.")
        return redirect("lista_especialidades")

    return render(
        request,
        "medicos/confirmar_exclusao_especialidade.html",
        {"especialidade": especialidade},
    )


def lista_convenios(request):
    convenios = Convenio.objects.all().order_by("nome")
    busca = request.GET.get("busca", "").strip()
    ativo = request.GET.get("ativo", "").strip()

    if busca:
        convenios = convenios.filter(nome__icontains=busca)

    if ativo == "1":
        convenios = convenios.filter(ativo=True)
    elif ativo == "0":
        convenios = convenios.filter(ativo=False)

    return render(
        request,
        "medicos/lista_convenios.html",
        {"convenios": convenios},
    )


def novo_convenio(request):
    if request.method == "POST":
        form = ConvenioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Convênio cadastrado com sucesso.")
            return redirect("lista_convenios")
    else:
        form = ConvenioForm()

    return render(
        request,
        "medicos/form_convenio.html",
        {
            "form": form,
            "titulo_pagina": "Novo Convênio",
            "subtitulo_pagina": "Cadastre um novo convênio no sistema.",
            "modo_edicao": False,
        },
    )


def editar_convenio(request, convenio_id):
    convenio = get_object_or_404(Convenio, id=convenio_id)

    if request.method == "POST":
        form = ConvenioForm(request.POST, instance=convenio)
        if form.is_valid():
            form.save()
            messages.success(request, "Convênio atualizado com sucesso.")
            return redirect("lista_convenios")
    else:
        form = ConvenioForm(instance=convenio)

    return render(
        request,
        "medicos/form_convenio.html",
        {
            "form": form,
            "titulo_pagina": "Editar Convênio",
            "subtitulo_pagina": "Atualize os dados do convênio.",
            "modo_edicao": True,
        },
    )


def excluir_convenio(request, convenio_id):
    convenio = get_object_or_404(Convenio, id=convenio_id)

    if request.method == "POST":
        convenio.delete()
        messages.success(request, "Convênio excluído com sucesso.")
        return redirect("lista_convenios")

    return render(
        request,
        "medicos/confirmar_exclusao_convenio.html",
        {"convenio": convenio},
    )

def lista_agendas_medicas(request):
    agendas = AgendaMedico.objects.select_related("medico").order_by("medico__nome", "dia_semana", "hora_inicio")

    medico_id = request.GET.get("medico", "").strip()
    ativo = request.GET.get("ativo", "").strip()

    if medico_id:
        agendas = agendas.filter(medico_id=medico_id)

    if ativo == "1":
        agendas = agendas.filter(ativo=True)
    elif ativo == "0":
        agendas = agendas.filter(ativo=False)

    return render(
        request,
        "medicos/lista_agendas_medicas.html",
        {
            "agendas": agendas,
            "medicos": Medico.objects.filter(ativo=True).order_by("nome"),
        },
    )


def nova_agenda_medica(request):
    if request.method == "POST":
        form = AgendaMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agenda médica cadastrada com sucesso.")
            return redirect("lista_agendas_medicas")
    else:
        form = AgendaMedicoForm()

    return render(
        request,
        "medicos/form_agenda_medica.html",
        {
            "form": form,
            "titulo_pagina": "Nova Agenda Médica",
            "subtitulo_pagina": "Cadastre os dias e horários de atendimento do médico.",
            "modo_edicao": False,
        },
    )


def editar_agenda_medica(request, agenda_id):
    agenda = get_object_or_404(AgendaMedico, id=agenda_id)

    if request.method == "POST":
        form = AgendaMedicoForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            messages.success(request, "Agenda médica atualizada com sucesso.")
            return redirect("lista_agendas_medicas")
    else:
        form = AgendaMedicoForm(instance=agenda)

    return render(
        request,
        "medicos/form_agenda_medica.html",
        {
            "form": form,
            "titulo_pagina": "Editar Agenda Médica",
            "subtitulo_pagina": "Atualize os horários de atendimento do médico.",
            "modo_edicao": True,
        },
    )


def excluir_agenda_medica(request, agenda_id):
    agenda = get_object_or_404(AgendaMedico, id=agenda_id)

    if request.method == "POST":
        agenda.delete()
        messages.success(request, "Agenda médica excluída com sucesso.")
        return redirect("lista_agendas_medicas")

    return render(
        request,
        "medicos/confirmar_exclusao_agenda_medica.html",
        {"agenda": agenda},
    )


def nova_agenda_semanal_medica(request):
    if request.method == "POST":
        form = AgendaSemanalMedicoForm(request.POST)

        if form.is_valid():
            medico = form.cleaned_data["medico"]

            dias_config = [
                ("segunda", 0),
                ("terca", 1),
                ("quarta", 2),
                ("quinta", 3),
                ("sexta", 4),
                ("sabado", 5),
                ("domingo", 6),
            ]

            criados = 0

            for prefixo, dia_semana in dias_config:
                ativo = form.cleaned_data.get(f"{prefixo}_ativa")

                # sempre remove o que já existe nesse dia
                AgendaMedico.objects.filter(
                    medico=medico,
                    dia_semana=dia_semana
                ).delete()

                # se o dia estiver desmarcado, ele fica sem agenda
                if not ativo:
                    continue

                # recria as faixas preenchidas
                for faixa in (1, 2):
                    hora_inicio = form.cleaned_data.get(f"{prefixo}_{faixa}_hora_inicio")
                    hora_fim = form.cleaned_data.get(f"{prefixo}_{faixa}_hora_fim")
                    duracao = form.cleaned_data.get(f"{prefixo}_{faixa}_duracao")
                    vagas_convenio = form.cleaned_data.get(f"{prefixo}_{faixa}_vagas_convenio")
                    vagas_particular = form.cleaned_data.get(f"{prefixo}_{faixa}_vagas_particular")

                    if hora_inicio and hora_fim:
                        AgendaMedico.objects.create(
                            medico=medico,
                            dia_semana=dia_semana,
                            hora_inicio=hora_inicio,
                            hora_fim=hora_fim,
                            duracao_consulta=duracao,
                            vagas_convenio=vagas_convenio,
                            vagas_particular=vagas_particular,
                            ativo=True,
                        )
                        criados += 1

            messages.success(request, f"Agenda semanal atualizada com sucesso. {criados} faixa(s) ativa(s) foram salvas.")
            return redirect("lista_agendas_medicas")
    else:
        form = AgendaSemanalMedicoForm()

    return render(
        request,
        "medicos/form_agenda_semanal_medica.html",
        {
            "form": form,
            "titulo_pagina": "Nova Agenda Semanal",
            "subtitulo_pagina": "Marque os dias da semana e preencha até duas faixas de atendimento por dia.",
        },
    )


def agenda_semanal_do_medico(request):
    medico_id = request.GET.get("medico_id")

    if not medico_id:
        return JsonResponse({"dias": {}})

    try:
        medico = Medico.objects.get(id=medico_id, ativo=True)
    except Medico.DoesNotExist:
        return JsonResponse({"dias": {}})

    agendas = AgendaMedico.objects.filter(
        medico=medico,
        ativo=True
    ).order_by("dia_semana", "hora_inicio")

    mapa_dias = {
        0: "segunda",
        1: "terca",
        2: "quarta",
        3: "quinta",
        4: "sexta",
        5: "sabado",
        6: "domingo",
    }

    dias = {}

    for agenda in agendas:
        prefixo = mapa_dias.get(agenda.dia_semana)
        if not prefixo:
            continue

        if prefixo not in dias:
            dias[prefixo] = []

        dias[prefixo].append({
            "hora_inicio": agenda.hora_inicio.strftime("%H:%M"),
            "hora_fim": agenda.hora_fim.strftime("%H:%M"),
            "duracao": agenda.duracao_consulta,
            "vagas_convenio": agenda.vagas_convenio,
            "vagas_particular": agenda.vagas_particular,
        })

    return JsonResponse({"dias": dias})