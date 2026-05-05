from django.db import models


class Especialista(models.Model):
    """
    Representa um profissional de saúde (médico, psicólogo, etc.)
    Está vinculado a um usuário do sistema.
    """

    usuario = models.OneToOneField(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='especialista'
    )

    registro_profissional = models.CharField(
        max_length=50,
        unique=True,
        help_text='CRM, CRP, CRO, etc.'
    )

    especialidade = models.CharField(
        max_length=100
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['especialidade']
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'

    def __str__(self):
        return f"{self.usuario} - {self.especialidade}"