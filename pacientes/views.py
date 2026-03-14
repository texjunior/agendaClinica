from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PacienteForm
from .models import Paciente


def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by("nome")

    busca = request.GET.get("busca", "").strip()
    if busca:
        pacientes = pacientes.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca) |
            Q(telefone__icontains=busca)
        )

    return render(request, "pacientes/lista_pacientes.html", {"pacientes": pacientes})


def novo_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente cadastrado com sucesso.")
            return redirect("lista_pacientes")
    else:
        form = PacienteForm()

    return render(
        request,
        "pacientes/form_paciente.html",
        {
            "form": form,
            "titulo_pagina": "Novo Paciente",
            "subtitulo_pagina": "Cadastre um novo paciente no sistema.",
            "modo_edicao": False,
        },
    )


def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente atualizado com sucesso.")
            return redirect("lista_pacientes")
    else:
        form = PacienteForm(instance=paciente)

    return render(
        request,
        "pacientes/form_paciente.html",
        {
            "form": form,
            "titulo_pagina": "Editar Paciente",
            "subtitulo_pagina": "Atualize os dados do paciente.",
            "modo_edicao": True,
        },
    )


def excluir_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == "POST":
        paciente.delete()
        messages.success(request, "Paciente excluído com sucesso.")
        return redirect("lista_pacientes")

    return render(request, "pacientes/confirmar_exclusao_paciente.html", {"paciente": paciente})