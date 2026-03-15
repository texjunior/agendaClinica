from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from agendamentos.models import Agendamento
from pacientes.models import Paciente
from .forms import ChamarSenhaForm, AtendimentoGuicheForm, GuicheForm
from .models import SenhaAtendimento, ChamadaSenha, AtendimentoGuiche, Guiche
from .utils import criar_senha, chamar_proxima_senha


def emitir_senha(request):
    if request.method == "POST":
        tipo_prioridade = request.POST.get("tipo_prioridade")
        tipo_atendimento = request.POST.get("tipo_atendimento")

        if tipo_prioridade in ["preferencial", "normal"] and tipo_atendimento in ["particular", "convenio"]:
            senha = criar_senha(tipo_prioridade, tipo_atendimento)
            messages.success(request, f"Senha {senha.codigo} gerada com sucesso.")
            return redirect("senha_emitida", senha_id=senha.id)

        messages.error(request, "Não foi possível gerar a senha.")

    return render(request, "recepcao/emitir_senha.html")


def senha_emitida(request, senha_id):
    senha = get_object_or_404(SenhaAtendimento, id=senha_id)
    return render(request, "recepcao/senha_emitida.html", {"senha": senha})


def painel_senhas(request):
    ultima_chamada = ChamadaSenha.objects.select_related("senha", "guiche").first()
    ultimas_chamadas = ChamadaSenha.objects.select_related("senha", "guiche")[:10]

    return render(
        request,
        "recepcao/painel_senhas.html",
        {
            "ultima_chamada": ultima_chamada,
            "ultimas_chamadas": ultimas_chamadas,
        },
    )


def guiche_atendimento(request):
    chamada_atual = None
    alerta_agendamento = None

    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "chamar":
            chamar_form = ChamarSenhaForm(request.POST)
            atendimento_form = AtendimentoGuicheForm()

            if chamar_form.is_valid():
                guiche = chamar_form.cleaned_data["guiche"]
                chamada = chamar_proxima_senha(guiche)

                if chamada:
                    request.session["guiche_id"] = guiche.id
                    request.session["senha_atual_id"] = chamada.senha.id
                    messages.success(request, f"Senha {chamada.senha.codigo} chamada no {guiche.nome}.")
                else:
                    messages.warning(request, "Não há senhas aguardando atendimento.")

                return redirect("guiche_atendimento")

        elif acao == "salvar_atendimento":
            chamar_form = ChamarSenhaForm(initial={"guiche": request.session.get("guiche_id")})
            atendimento_form = AtendimentoGuicheForm(request.POST)

            senha_id = request.session.get("senha_atual_id")
            senha = SenhaAtendimento.objects.filter(id=senha_id).first()

            if not senha:
                messages.error(request, "Nenhuma senha em atendimento no momento.")
                return redirect("guiche_atendimento")

            if atendimento_form.is_valid():
                nome = atendimento_form.cleaned_data["nome_paciente"]
                cpf = atendimento_form.cleaned_data["cpf_paciente"]
                convenio = atendimento_form.cleaned_data["convenio"]
                observacao = atendimento_form.cleaned_data["observacao"]

                paciente, criado = Paciente.objects.get_or_create(
                    cpf=cpf,
                    defaults={"nome": nome}
                )

                if not criado and nome and paciente.nome != nome:
                    paciente.nome = nome
                    paciente.save()

                agendamento_hoje = Agendamento.objects.filter(
                    paciente=paciente,
                    data_consulta=timezone.localdate()
                ).exclude(status="cancelado")

                if agendamento_hoje.exists():
                    alerta_agendamento = "Este paciente já possui agendamento para hoje."

                AtendimentoGuiche.objects.update_or_create(
                    senha=senha,
                    defaults={
                        "guiche_id": request.session.get("guiche_id"),
                        "paciente": paciente,
                        "convenio": convenio,
                        "observacao": observacao,
                    }
                )

                senha.status = "em_atendimento"
                senha.save()

                messages.success(request, "Atendimento do guichê salvo com sucesso.")
                return redirect("guiche_atendimento")
    else:
        chamar_form = ChamarSenhaForm(initial={"guiche": request.session.get("guiche_id")})
        atendimento_form = AtendimentoGuicheForm()

    senha_id = request.session.get("senha_atual_id")
    if senha_id:
        chamada_atual = SenhaAtendimento.objects.filter(id=senha_id).first()

    return render(
        request,
        "recepcao/guiche_atendimento.html",
        {
            "chamar_form": chamar_form,
            "atendimento_form": atendimento_form,
            "chamada_atual": chamada_atual,
            "alerta_agendamento": alerta_agendamento,
        },
    )


def lista_guiches(request):
    guiches = Guiche.objects.all().order_by("nome")
    busca = request.GET.get("busca", "").strip()
    ativo = request.GET.get("ativo").strip()
    if busca:
        guiches = guiches.filter(nome__icontains=busca)
    if ativo == "1":
        guiches = guiches.filter(ativo=True)
    elif ativo == "0":
        guiches = guiches.filter(ativo=False)
        
    return render(request, "recepcao/lista_guiches.html", {"guiches": guiches})

def novo_guiche(request):
    if request.method == "POST":
        form = GuicheForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guichê criado com sucesso.")
            return redirect("lista_guiches")
    else:
        form = GuicheForm()

    return render(request, "recepcao/form_guiche.html", {"form": form,"titulo_pagina": "Novo Guichê","subtitulo_pagina": "Crie um novo guichê para atendimento.","modo_edicao": True})

def exlcuir_guiche(request, guiche_id):
    guiche = get_object_or_404(Guiche, id=guiche_id)
    if request.method == "POST":
        guiche.delete()
        messages.success(request, "Guichê excluído com sucesso.")
        return redirect("lista_guiches")

    return render(request, "recepcao/confirmar_exclusao_guiche.html", {"guiche": guiche})