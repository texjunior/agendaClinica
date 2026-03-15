from django.db import models


class Guiche(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Guichê"
        verbose_name_plural = "Guichês"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class SenhaAtendimento(models.Model):
    TIPO_PRIORIDADE_CHOICES = (
        ("preferencial", "Preferencial"),
        ("normal", "Normal"),
    )

    TIPO_ATENDIMENTO_CHOICES = (
        ("particular", "Particular"),
        ("convenio", "Convênio"),
    )

    STATUS_CHOICES = (
        ("aguardando", "Aguardando"),
        ("chamada", "Chamada"),
        ("em_atendimento", "Em atendimento"),
        ("finalizada", "Finalizada"),
        ("cancelada", "Cancelada"),
    )

    codigo = models.CharField(max_length=10, unique=True)
    tipo_prioridade = models.CharField(max_length=20, choices=TIPO_PRIORIDADE_CHOICES)
    tipo_atendimento = models.CharField(max_length=20, choices=TIPO_ATENDIMENTO_CHOICES)
    numero = models.PositiveIntegerField()
    data_emissao = models.DateField()
    hora_emissao = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="aguardando")

    class Meta:
        verbose_name = "Senha de Atendimento"
        verbose_name_plural = "Senhas de Atendimento"
        ordering = ["-data_emissao", "-hora_emissao"]

    def __str__(self):
        return self.codigo


class ChamadaSenha(models.Model):
    senha = models.ForeignKey(
        SenhaAtendimento,
        on_delete=models.CASCADE,
        related_name="chamadas"
    )
    guiche = models.ForeignKey(
        Guiche,
        on_delete=models.PROTECT,
        related_name="chamadas"
    )
    hora_chamada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chamada de Senha"
        verbose_name_plural = "Chamadas de Senha"
        ordering = ["-hora_chamada"]

    def __str__(self):
        return f"{self.senha.codigo} - {self.guiche.nome}"


class AtendimentoGuiche(models.Model):
    senha = models.OneToOneField(
        SenhaAtendimento,
        on_delete=models.CASCADE,
        related_name="atendimento_guiche"
    )
    guiche = models.ForeignKey(
        Guiche,
        on_delete=models.PROTECT,
        related_name="atendimentos"
    )
    paciente = models.ForeignKey(
        "pacientes.Paciente",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atendimentos_guiche"
    )
    convenio = models.ForeignKey(
        "medicos.Convenio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atendimentos_guiche"
    )
    observacao = models.TextField(blank=True, null=True)
    iniciado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Atendimento no Guichê"
        verbose_name_plural = "Atendimentos no Guichê"
        ordering = ["-iniciado_em"]

    def __str__(self):
        return f"{self.senha.codigo} - {self.guiche.nome}"