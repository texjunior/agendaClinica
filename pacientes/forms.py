from django import forms
from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nome", "cpf", "telefone", "data_nascimento"]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        cpf_numeros = "".join(filter(str.isdigit, cpf))

        if len(cpf_numeros) != 11:
            raise forms.ValidationError("CPF deve conter 11 números.")

        return cpf_numeros