from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from medicos.models import Medico
from pacientes.models import Paciente
from .forms import AgendamentoForm
from .models import Agendamento
from .utils import gerar_horarios_disponiveis
from django.db.models import Q


def horarios_disponiveis(request):
    medico_id = request.GET.get("medico_id") or request.GET.get("medico")
    data_str = request.GET.get("data")
    tipo_atendimento = request.GET.get("tipo_atendimento")

    if not medico_id or not data_str:
        return JsonResponse({"horarios": []}, status=200)

    medico = get_object_or_404(Medico, id=medico_id)

    try:
        data_consulta = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"horarios": []}, status=200)

    horarios = gerar_horarios_disponiveis(
        medico=medico,
        data_consulta=data_consulta,
        tipo_atendimento=tipo_atendimento,
    )

    return JsonResponse({
        "medico": medico.nome,
        "data": data_consulta.strftime("%d/%m/%Y"),
        "horarios": [h.strftime("%H:%M") for h in horarios]
    })


def novo_agendamento(request):
    horarios = []

    medico_id = request.POST.get("medico") or request.GET.get("medico")
    data_str = request.POST.get("data_consulta") or request.GET.get("data_consulta")
    tipo_atendimento = request.POST.get("tipo_atendimento") or request.GET.get("tipo_atendimento")

    if medico_id and data_str and tipo_atendimento:
        try:
            medico = Medico.objects.get(id=medico_id)
            data_consulta = datetime.strptime(data_str, "%Y-%m-%d").date()
            horarios = gerar_horarios_disponiveis(
                medico=medico,
                data_consulta=data_consulta,
                tipo_atendimento=tipo_atendimento,
            )
        except (Medico.DoesNotExist, ValueError):
            horarios = []

    if request.method == "POST":
        form = AgendamentoForm(
            horarios=horarios,
            medico_id=medico_id,
            initial={
                "medico": medico_id,
                "data_consulta": data_str,
                "tipo_atendimento": tipo_atendimento,
            }
        )

        if form.is_valid():
            cpf = form.cleaned_data["cpf_paciente"]
            nome = form.cleaned_data["nome_paciente"]
            telefone = form.cleaned_data["telefone_paciente"]
            data_nascimento = form.cleaned_data["data_nascimento_paciente"]

            paciente, criado = Paciente.objects.get_or_create(
                cpf=cpf,
                defaults={
                    "nome": nome,
                    "telefone": telefone,
                    "data_nascimento": data_nascimento,
                }
            )

            if not criado:
                alterado = False

                if paciente.nome != nome and nome:
                    paciente.nome = nome
                    alterado = True

                if telefone and paciente.telefone != telefone:
                    paciente.telefone = telefone
                    alterado = True

                if data_nascimento and paciente.data_nascimento != data_nascimento:
                    paciente.data_nascimento = data_nascimento
                    alterado = True

                if alterado:
                    paciente.save()

            agendamento = form.save(commit=False)
            agendamento.paciente = paciente

            agendamento_mesmo_dia = Agendamento.objects.filter(
                paciente=paciente,
                data_consulta=agendamento.data_consulta
            ).exclude(pk=agendamento.pk)

            if agendamento_mesmo_dia.exists():
                messages.warning(
                    request,
                    "Atenção: este paciente já possui um agendamento para este dia."
                )

            agendamento.save()
            messages.success(request, "Agendamento realizado com sucesso.")
            return redirect("novo_agendamento")
    else:
        form = AgendamentoForm(
            horarios=horarios,
            medico_id=medico_id,
        )

    contexto = {
        "form": form,
        "modo_edicao": False,
        "titulo_pagina": "Novo Agendamento",
        "subtitulo_pagina": "Cadastre o paciente e agende a consulta em uma única tela.",
    }
    return render(request, "agendamentos/novo_agendamento.html", contexto)




def convenios_do_medico(request):
    medico_id = request.GET.get("medico_id")

    if not medico_id:
        return JsonResponse({"convenios": []})

    try:
        medico = Medico.objects.get(id=medico_id, ativo=True)
    except Medico.DoesNotExist:
        return JsonResponse({"convenios": []})

    convenios = medico.convenios.filter(ativo=True).order_by("nome")

    return JsonResponse({
        "convenios": [
            {"id": convenio.id, "nome": convenio.nome}
            for convenio in convenios
        ]
    })


def lista_agendamentos(request):
    agendamentos = Agendamento.objects.select_related(
        "paciente", "medico", "convenio"
    ).order_by("data_consulta", "hora_consulta")

    data = request.GET.get("data")
    medico_id = request.GET.get("medico")
    status = request.GET.get("status")
    busca = request.GET.get("busca")

    if data:
        agendamentos = agendamentos.filter(data_consulta=data)

    if medico_id:
        agendamentos = agendamentos.filter(medico_id=medico_id)

    if status:
        agendamentos = agendamentos.filter(status=status)

    if busca:
        agendamentos = agendamentos.filter(
            Q(paciente__nome__icontains=busca) |
            Q(paciente__cpf__icontains=busca) |
            Q(medico__nome__icontains=busca)
        )

    contexto = {
        "agendamentos": agendamentos,
        "medicos": Medico.objects.filter(ativo=True).order_by("nome"),
        "status_choices": Agendamento.STATUS_CHOICES,
    }
    return render(request, "agendamentos/lista_agendamentos.html", contexto)


def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    horarios = []
    medico_id = request.POST.get("medico") or request.GET.get("medico") or agendamento.medico_id
    data_str = request.POST.get("data_consulta") or request.GET.get("data_consulta") or agendamento.data_consulta.strftime("%Y-%m-%d")
    tipo_atendimento = request.POST.get("tipo_atendimento") or request.GET.get("tipo_atendimento") or agendamento.tipo_atendimento

    if medico_id and data_str:
        try:
            medico = Medico.objects.get(id=medico_id)
            data_consulta = datetime.strptime(str(data_str), "%Y-%m-%d").date()
            horarios = gerar_horarios_disponiveis(
                medico=medico,
                data_consulta=data_consulta,
                tipo_atendimento=tipo_atendimento,
                ignorar_agendamento_id=agendamento.id,
            )

            if agendamento.hora_consulta not in horarios:
                horarios.append(agendamento.hora_consulta)
                horarios = sorted(horarios)
        except (Medico.DoesNotExist, ValueError):
            horarios = []

    if request.method == "POST":
        form = AgendamentoForm(
            request.POST,
            instance=agendamento,
            horarios=horarios,
            medico_id=medico_id,
        )

        if form.is_valid():
            cpf = form.cleaned_data["cpf_paciente"]
            nome = form.cleaned_data["nome_paciente"]
            telefone = form.cleaned_data["telefone_paciente"]
            data_nascimento = form.cleaned_data["data_nascimento_paciente"]

            paciente, criado = Paciente.objects.get_or_create(
                cpf=cpf,
                defaults={
                    "nome": nome,
                    "telefone": telefone,
                    "data_nascimento": data_nascimento,
                }
            )

            if not criado:
                alterado = False

                if paciente.nome != nome and nome:
                    paciente.nome = nome
                    alterado = True

                if telefone and paciente.telefone != telefone:
                    paciente.telefone = telefone
                    alterado = True

                if data_nascimento and paciente.data_nascimento != data_nascimento:
                    paciente.data_nascimento = data_nascimento
                    alterado = True

                if alterado:
                    paciente.save()

            agendamento_editado = form.save(commit=False)
            agendamento_editado.paciente = paciente
            agendamento_editado.save()

            messages.success(request, "Agendamento atualizado com sucesso.")
            return redirect("lista_agendamentos")
    else:
        form = AgendamentoForm(
            instance=agendamento,
            horarios=horarios,
            medico_id=medico_id,
            initial={
                "nome_paciente": agendamento.paciente.nome,
                "cpf_paciente": agendamento.paciente.cpf,
                "telefone_paciente": agendamento.paciente.telefone,
                "data_nascimento_paciente": agendamento.paciente.data_nascimento,
            }
        )

    contexto = {
        "form": form,
        "modo_edicao": True,
        "titulo_pagina": "Editar Agendamento",
        "subtitulo_pagina": "Atualize os dados do paciente e do agendamento.",
    }
    return render(request, "agendamentos/novo_agendamento.html", contexto)

def cancelar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == "POST":
        agendamento.status = "cancelado"
        agendamento.save()
        messages.success(request, "Agendamento cancelado com sucesso.")
        return redirect("lista_agendamentos")

    return render(
        request,
        "agendamentos/confirmar_cancelamento.html",
        {"agendamento": agendamento}
    )


