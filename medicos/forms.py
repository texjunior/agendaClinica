from django import forms
from .models import Medico, Especialidade, Convenio, AgendaMedico


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ["nome", "crm", "especialidade", "convenios", "sala", "ativo"]
        widgets = {
            "convenios": forms.CheckboxSelectMultiple(),
        }


class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = ["nome"]


class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ["nome", "ativo"]

class AgendaMedicoForm(forms.ModelForm):
    class Meta:
        model = AgendaMedico
        fields = [
            "medico",
            "dia_semana",
            "hora_inicio",
            "hora_fim",
            "duracao_consulta",
            "vagas_particular",
            "vagas_convenio",
            "ativo",
        ]
        widgets = {
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fim": forms.TimeInput(attrs={"type": "time"}),
        }

class AgendaSemanalMedicoForm(forms.Form):
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.filter(ativo=True).order_by("nome"),
        label="Médico"
    )

    # SEGUNDA
    segunda_ativa = forms.BooleanField(required=False, label="Segunda-feira")
    segunda_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    segunda_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    segunda_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    segunda_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    segunda_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    segunda_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    segunda_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    segunda_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    segunda_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    segunda_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    # TERÇA
    terca_ativa = forms.BooleanField(required=False, label="Terça-feira")
    terca_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    terca_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    terca_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    terca_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    terca_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    terca_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    terca_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    terca_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    terca_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    terca_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    # QUARTA
    quarta_ativa = forms.BooleanField(required=False, label="Quarta-feira")
    quarta_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quarta_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quarta_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    quarta_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    quarta_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    quarta_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quarta_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quarta_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    quarta_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    quarta_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    # QUINTA
    quinta_ativa = forms.BooleanField(required=False, label="Quinta-feira")
    quinta_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quinta_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quinta_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    quinta_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    quinta_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    quinta_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quinta_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    quinta_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    quinta_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    quinta_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    # SEXTA
    sexta_ativa = forms.BooleanField(required=False, label="Sexta-feira")
    sexta_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sexta_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sexta_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    sexta_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    sexta_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    sexta_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sexta_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sexta_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    sexta_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    sexta_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    # SÁBADO
    sabado_ativa = forms.BooleanField(required=False, label="Sábado")
    sabado_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sabado_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sabado_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    sabado_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    sabado_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    sabado_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sabado_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    sabado_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    sabado_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    sabado_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    # DOMINGO
    domingo_ativa = forms.BooleanField(required=False, label="Domingo")
    domingo_1_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    domingo_1_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    domingo_1_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    domingo_1_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    domingo_1_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    domingo_2_hora_inicio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    domingo_2_hora_fim = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    domingo_2_duracao = forms.IntegerField(required=False, initial=20, min_value=1)
    domingo_2_vagas_convenio = forms.IntegerField(required=False, initial=0, min_value=0)
    domingo_2_vagas_particular = forms.IntegerField(required=False, initial=0, min_value=0)

    def clean(self):
        cleaned_data = super().clean()

        dias = [
            ("segunda", "Segunda-feira"),
            ("terca", "Terça-feira"),
            ("quarta", "Quarta-feira"),
            ("quinta", "Quinta-feira"),
            ("sexta", "Sexta-feira"),
            ("sabado", "Sábado"),
            ("domingo", "Domingo"),
        ]

        marcou_algum = False

        for prefixo, nome_dia in dias:
            ativo = cleaned_data.get(f"{prefixo}_ativa")
            if not ativo:
                continue

            marcou_algum = True
            tem_alguma_faixa = False

            for faixa in (1, 2):
                hora_inicio = cleaned_data.get(f"{prefixo}_{faixa}_hora_inicio")
                hora_fim = cleaned_data.get(f"{prefixo}_{faixa}_hora_fim")
                duracao = cleaned_data.get(f"{prefixo}_{faixa}_duracao")
                vagas_convenio = cleaned_data.get(f"{prefixo}_{faixa}_vagas_convenio")
                vagas_particular = cleaned_data.get(f"{prefixo}_{faixa}_vagas_particular")

                preencheu_algo = any([
                    hora_inicio, hora_fim,
                    duracao not in (None, ""),
                    vagas_convenio not in (None, ""),
                    vagas_particular not in (None, "")
                ])

                if preencheu_algo:
                    tem_alguma_faixa = True

                    if not hora_inicio:
                        self.add_error(f"{prefixo}_{faixa}_hora_inicio", f"Informe a hora inicial da faixa {faixa} em {nome_dia}.")
                    if not hora_fim:
                        self.add_error(f"{prefixo}_{faixa}_hora_fim", f"Informe a hora final da faixa {faixa} em {nome_dia}.")
                    if duracao in (None, ""):
                        self.add_error(f"{prefixo}_{faixa}_duracao", f"Informe a duração da faixa {faixa} em {nome_dia}.")
                    if vagas_convenio in (None, ""):
                        self.add_error(f"{prefixo}_{faixa}_vagas_convenio", f"Informe as vagas de convênio da faixa {faixa} em {nome_dia}.")
                    if vagas_particular in (None, ""):
                        self.add_error(f"{prefixo}_{faixa}_vagas_particular", f"Informe as vagas particulares da faixa {faixa} em {nome_dia}.")

                    if hora_inicio and hora_fim and hora_fim <= hora_inicio:
                        self.add_error(f"{prefixo}_{faixa}_hora_fim", f"A hora final deve ser maior que a hora inicial na faixa {faixa} de {nome_dia}.")

            if not tem_alguma_faixa:
                raise forms.ValidationError(f"Você marcou {nome_dia}, mas não preencheu nenhuma faixa de horário.")

            # conflito entre faixa 1 e faixa 2
            inicio1 = cleaned_data.get(f"{prefixo}_1_hora_inicio")
            fim1 = cleaned_data.get(f"{prefixo}_1_hora_fim")
            inicio2 = cleaned_data.get(f"{prefixo}_2_hora_inicio")
            fim2 = cleaned_data.get(f"{prefixo}_2_hora_fim")

            if inicio1 and fim1 and inicio2 and fim2:
                if inicio2 < fim1 and fim2 > inicio1:
                    self.add_error(f"{prefixo}_2_hora_inicio", f"As faixas de {nome_dia} não podem se sobrepor.")
                    self.add_error(f"{prefixo}_2_hora_fim", f"As faixas de {nome_dia} não podem se sobrepor.")

        if not marcou_algum:
            raise forms.ValidationError("Marque pelo menos um dia da semana para cadastrar a agenda.")

        return cleaned_data