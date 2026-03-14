from django.db import models
from django.core.exceptions import ValidationError


class Agendamento(models.Model):
    TIPO_ATENDIMENTO_CHOICES = (
        ("particular", "Particular"),
        ("convenio", "Convênio"),
    )

    STATUS_CHOICES = (
        ("agendado", "Agendado"),
        ("confirmado", "Confirmado"),
        ("aguardando", "Aguardando"),
        ("em_atendimento", "Em atendimento"),
        ("finalizado", "Finalizado"),
        ("faltou", "Faltou"),
        ("cancelado", "Cancelado"),
    )

    paciente = models.ForeignKey(
        "pacientes.Paciente",
        on_delete=models.CASCADE,
        related_name="agendamentos"
    )
    medico = models.ForeignKey(
        "medicos.Medico",
        on_delete=models.PROTECT,
        related_name="agendamentos"
    )
    convenio = models.ForeignKey(
        "medicos.Convenio",
        on_delete=models.PROTECT,
        related_name="agendamentos",
        blank=True,
        null=True
    )
    tipo_atendimento = models.CharField(
        max_length=20,
        choices=TIPO_ATENDIMENTO_CHOICES
    )
    data_consulta = models.DateField()
    hora_consulta = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="agendado"
    )
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.tipo_atendimento == "particular" and self.convenio:
            raise ValidationError("Atendimento particular não deve ter convênio.")

        if self.tipo_atendimento == "convenio" and not self.convenio:
            raise ValidationError("Selecione o convênio para atendimento por convênio.")

        if self.tipo_atendimento == "convenio" and self.convenio:
            if not self.medico.convenios.filter(id=self.convenio.id).exists():
                raise ValidationError("Esse médico não atende o convênio selecionado.")

        existe_agendamento = Agendamento.objects.filter(
            medico=self.medico,
            data_consulta=self.data_consulta,
            hora_consulta=self.hora_consulta
        )

        if self.pk:
            existe_agendamento = existe_agendamento.exclude(pk=self.pk)

        if existe_agendamento.exists():
            raise ValidationError("Esse horário já está ocupado para esse médico.")

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["data_consulta", "hora_consulta"]
        constraints = [
            models.UniqueConstraint(
                fields=["medico", "data_consulta", "hora_consulta"],
                name="unique_agendamento_medico_data_hora"
            )
        ]

    def __str__(self):
        return f"{self.paciente.nome} - {self.medico.nome} - {self.data_consulta} {self.hora_consulta}"