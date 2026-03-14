from datetime import datetime

from django import forms

from medicos.models import Medico, Convenio
from .models import Agendamento
from .utils import gerar_horarios_disponiveis

class AgendamentoForm(forms.ModelForm):
    nome_paciente = forms.CharField(
        max_length=150,
        label="Nome do paciente",
        widget=forms.TextInput(attrs={"id": "id_nome_paciente"})
    )
    cpf_paciente = forms.CharField(
        max_length=14,
        label="CPF",
        widget=forms.TextInput(attrs={"id": "id_cpf_paciente"})
    )
    telefone_paciente = forms.CharField(
        max_length=20,
        required=False,
        label="Telefone",
        widget=forms.TextInput(attrs={"id": "id_telefone_paciente"})
    )
    data_nascimento_paciente = forms.DateField(
        required=False,
        label="Data de nascimento",
        widget=forms.DateInput(attrs={"type": "date", "id": "id_data_nascimento_paciente"})
    )

    class Meta:
        model = Agendamento
        fields = [
            "nome_paciente",
            "cpf_paciente",
            "telefone_paciente",
            "data_nascimento_paciente",
            "medico",
            "tipo_atendimento",
            "convenio",
            "data_consulta",
            "hora_consulta",
            "observacao",
        ]
        widgets = {
            "medico": forms.Select(attrs={"id": "id_medico"}),
            "tipo_atendimento": forms.Select(attrs={"id": "id_tipo_atendimento"}),
            "convenio": forms.Select(attrs={"id": "id_convenio"}),
            "data_consulta": forms.DateInput(attrs={"type": "date", "id": "id_data_consulta"}),
            "observacao": forms.Textarea(attrs={"rows": 3, "id": "id_observacao"}),
        }

    def __init__(self, *args, **kwargs):
        horarios = kwargs.pop("horarios", [])
        medico_id = kwargs.pop("medico_id", None)
        super().__init__(*args, **kwargs)

        self.fields["medico"].queryset = Medico.objects.filter(ativo=True).order_by("nome")
        self.fields["convenio"].queryset = Convenio.objects.none()

        if medico_id:
            try:
                medico = Medico.objects.get(id=medico_id, ativo=True)
                self.fields["convenio"].queryset = medico.convenios.filter(ativo=True).order_by("nome")
            except Medico.DoesNotExist:
                pass

        if self.instance and self.instance.pk and self.instance.medico_id:
            self.fields["convenio"].queryset = self.instance.medico.convenios.filter(ativo=True).order_by("nome")

        self.fields["hora_consulta"] = forms.ChoiceField(
            choices=[("", "Selecione um horário")] + [
                (horario.strftime("%H:%M"), horario.strftime("%H:%M"))
                for horario in horarios
            ],
            label="Horário",
            widget=forms.Select(attrs={"id": "id_hora_consulta"})
        )

    def clean_hora_consulta(self):
        hora_str = self.cleaned_data["hora_consulta"]

        try:
            return datetime.strptime(hora_str, "%H:%M").time()
        except ValueError:
            raise forms.ValidationError("Horário inválido.")

    def clean_cpf_paciente(self):
        cpf = self.cleaned_data["cpf_paciente"]
        cpf_numeros = "".join(filter(str.isdigit, cpf))

        if len(cpf_numeros) != 11:
            raise forms.ValidationError("CPF deve conter 11 números.")

        return cpf_numeros
    
    def clean(self):
        cleaned_data = super().clean()

        medico = cleaned_data.get("medico")
        data_consulta = cleaned_data.get("data_consulta")
        hora_consulta = cleaned_data.get("hora_consulta")
        tipo_atendimento = cleaned_data.get("tipo_atendimento")

        if medico and data_consulta and hora_consulta and tipo_atendimento:
            horarios_disponiveis = gerar_horarios_disponiveis(
                medico=medico,
                data_consulta=data_consulta,
                tipo_atendimento=tipo_atendimento,
                ignorar_agendamento_id=self.instance.pk if self.instance and self.instance.pk else None,
            )

            if self.instance and self.instance.pk:
                horario_original = self.instance.hora_consulta
                medico_original = self.instance.medico
                data_original = self.instance.data_consulta
                tipo_original = self.instance.tipo_atendimento

                if (
                    medico == medico_original and
                    data_consulta == data_original and
                    hora_consulta == horario_original and
                    tipo_atendimento == tipo_original
                ):
                    return cleaned_data

            if hora_consulta not in horarios_disponiveis:
                raise forms.ValidationError(
                    "O horário escolhido não está disponível para esse médico nessa data e nesse tipo de atendimento."
                )

        return cleaned_data