from django.db import models
from core.models import ModeloBase

# Create your models here.
class Clinica(ModeloBase):
    """
    Representa a unidade organizacional (tenant) do sistema
    Toda entidade de negócio estará vincula a uma clínica
    """

    #identificação básica
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome da Clínica'
    )

    razao_social = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Razão Social'
    )

    cnpj = models.CharField(
        max_length=18,
        unique=False,
        verbose_name='CNPJ'
    )

    #contato
    email = models.EmailField(
        blank=True, 
        null=True,
        verbose_name='E-mail'
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True, 
        verbose_name='Telefone'
    )

    #endereço

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    cidade = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    #LGPD
    nome_dpo=models.CharField(
        max_length=255,
        verbose_name='Responsável pela proteção de dados (DPO)'
    )

    email_dpo=models.EmailField(
        verbose_name='E-mail do DPO'
    )

    #configurações operacionais
    ativa = models.BooleanField(
        default=True,
        verbose_name='Clinica Ativa'
    )

    #controle de retenção de dados (LGPD)
    prazo_retencao_anos = models.PositiveBigIntegerField(
        default=5,
        verbose_name='Prazo de retenção de dados (anos)'
    )

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Clínica'
        verbose_name_plural = 'Clínicas'
        ordering = ['nome']