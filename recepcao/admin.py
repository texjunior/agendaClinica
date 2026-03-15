from django.contrib import admin
from .models import Guiche, SenhaAtendimento, ChamadaSenha, AtendimentoGuiche


@admin.register(Guiche)
class GuicheAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo")
    search_fields = ("nome",)
    list_filter = ("ativo",)


@admin.register(SenhaAtendimento)
class SenhaAtendimentoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "tipo_prioridade",
        "tipo_atendimento",
        "numero",
        "data_emissao",
        "hora_emissao",
        "status",
    )
    search_fields = ("codigo",)
    list_filter = ("tipo_prioridade", "tipo_atendimento", "status", "data_emissao")


@admin.register(ChamadaSenha)
class ChamadaSenhaAdmin(admin.ModelAdmin):
    list_display = ("senha", "guiche", "hora_chamada")
    list_filter = ("guiche", "hora_chamada")


@admin.register(AtendimentoGuiche)
class AtendimentoGuicheAdmin(admin.ModelAdmin):
    list_display = ("senha", "guiche", "paciente", "convenio", "iniciado_em", "finalizado_em")
    search_fields = ("senha__codigo", "paciente__nome", "paciente__cpf")
    list_filter = ("guiche", "iniciado_em", "finalizado_em")