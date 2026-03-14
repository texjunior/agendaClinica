from django.db import models
from django.core.exceptions import ValidationError

class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Convenio(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Convênio"
        verbose_name_plural = "Convênios"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=150)
    crm = models.CharField(max_length=30, unique=True)
    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.PROTECT,
        related_name="medicos"
    )
    convenios = models.ManyToManyField(
        Convenio,
        blank=True,
        related_name="medicos"
    )
    sala = models.CharField(max_length=50, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.especialidade.nome}"
 
class AgendaMedico(models.Model):
    DIAS_SEMANA = (
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    )

    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="agendas"
    )
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    duracao_consulta = models.PositiveIntegerField(
        default=20,
        help_text="Duração da consulta em minutos"
    )
    vagas_particular = models.PositiveIntegerField(default=0)
    vagas_convenio = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    def clean(self):
        if self.hora_fim <= self.hora_inicio:
            raise ValidationError("A hora final deve ser maior que a hora inicial.")

        if self.duracao_consulta <= 0:
            raise ValidationError("A duração da consulta deve ser maior que zero.")

    class Meta:
        verbose_name = "Agenda do Médico"
        verbose_name_plural = "Agendas dos Médicos"
        ordering = ["medico__nome", "dia_semana", "hora_inicio"]

    def __str__(self):
        return f"{self.medico.nome} - {self.get_dia_semana_display()} - {self.hora_inicio} às {self.hora_fim}"