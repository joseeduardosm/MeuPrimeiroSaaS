from django.db import models

# Create your models here.
class Paciente(models.Model):
    """
    Representa o paciente do sistema
    esta vinculado a um usuario logado (login)
    """

    usuario = models.OneToOneField(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='paciente'
    )

    nome_completo = models.CharField(
        max_length=255
    )

    cpf = models.CharField(
        max_length=14,
        unique=True
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    #LGPD Controle Minimo
    ativo = models.BooleanField(
        default=True
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['nome_completo']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.nome_completo