from django.contrib import admin
from .models import Especialidade, Convenio, Medico, AgendaMedico


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo")
    search_fields = ("nome",)
    list_filter = ("ativo",)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "crm", "especialidade", "sala", "ativo")
    search_fields = ("nome", "crm")
    list_filter = ("especialidade", "ativo")
    filter_horizontal = ("convenios",)

@admin.register(AgendaMedico)
class AgendaMedicoAdmin(admin.ModelAdmin):
    list_display = (
        "medico",
        "dia_semana",
        "hora_inicio",
        "hora_fim",
        "duracao_consulta",
        "vagas_particular",
        "vagas_convenio",
        "ativo",
    )
    list_filter = ("dia_semana", "ativo", "medico")
    search_fields = ("medico__nome",)
    search_fields = ("nome", "crm")