from datetime import date, datetime

from .models import SenhaAtendimento


def gerar_codigo_senha(tipo_prioridade, tipo_atendimento):
    prefixos_prioridade = {
        "preferencial": "P",
        "normal": "N",
    }

    prefixos_atendimento = {
        "particular": "P",
        "convenio": "C",
    }

    prefixo = f"{prefixos_prioridade[tipo_prioridade]}{prefixos_atendimento[tipo_atendimento]}"

    hoje = date.today()

    ultimo_numero = (
        SenhaAtendimento.objects.filter(
            data_emissao=hoje,
            tipo_prioridade=tipo_prioridade,
            tipo_atendimento=tipo_atendimento,
        )
        .order_by("-numero")
        .values_list("numero", flat=True)
        .first()
    )

    proximo_numero = 1 if ultimo_numero is None else ultimo_numero + 1
    codigo = f"{prefixo}{proximo_numero:02d}"

    return codigo, proximo_numero


def criar_senha(tipo_prioridade, tipo_atendimento):
    codigo, numero = gerar_codigo_senha(tipo_prioridade, tipo_atendimento)
    agora = datetime.now()

    senha = SenhaAtendimento.objects.create(
        codigo=codigo,
        tipo_prioridade=tipo_prioridade,
        tipo_atendimento=tipo_atendimento,
        numero=numero,
        data_emissao=agora.date(),
        hora_emissao=agora.time(),
        status="aguardando",
    )

    return senha


from django.utils import timezone
from .models import ChamadaSenha


def buscar_proxima_senha():
    return (
        SenhaAtendimento.objects.filter(status="aguardando")
        .order_by(
            "data_emissao",
            "tipo_prioridade",
            "hora_emissao",
            "numero",
        )
        .first()
    )


def chamar_proxima_senha(guiche):
    senha = buscar_proxima_senha()

    if not senha:
        return None

    senha.status = "chamada"
    senha.save()

    chamada = ChamadaSenha.objects.create(
        senha=senha,
        guiche=guiche
    )

    return chamada