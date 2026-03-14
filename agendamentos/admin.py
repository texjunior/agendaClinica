from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        "paciente",
        "medico",
        "tipo_atendimento",
        "convenio",
        "data_consulta",
        "hora_consulta",
        "status",
    )
    list_filter = (
        "tipo_atendimento",
        "status",
        "data_consulta",
        "medico",
    )
    search_fields = (
        "paciente__nome",
        "paciente__cpf",
        "medico__nome",
    )
    autocomplete_fields = ("paciente", "medico", "convenio")