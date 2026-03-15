from django import forms

from medicos.models import Convenio
from .models import Guiche


class ChamarSenhaForm(forms.Form):
    guiche = forms.ModelChoiceField(
        queryset=Guiche.objects.filter(ativo=True).order_by("nome"),
        label="Guichê"
    )


class AtendimentoGuicheForm(forms.Form):
    nome_paciente = forms.CharField(max_length=150, label="Nome do paciente")
    cpf_paciente = forms.CharField(max_length=14, label="CPF")
    convenio = forms.ModelChoiceField(
        queryset=Convenio.objects.filter(ativo=True).order_by("nome"),
        required=False,
        label="Convênio"
    )
    observacao = forms.CharField(
        required=False,
        label="Observação",
        widget=forms.Textarea(attrs={"rows": 3})
    )

    def clean_cpf_paciente(self):
        cpf = self.cleaned_data["cpf_paciente"]
        cpf_numeros = "".join(filter(str.isdigit, cpf))

        if len(cpf_numeros) != 11:
            raise forms.ValidationError("CPF deve conter 11 números.")

        return cpf_numeros


class GuicheForm(forms.ModelForm):
    class Meta:
        model = Guiche
        fields = ["nome", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }