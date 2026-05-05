# Importa o módulo base de models do Django (campos, ForeignKey, etc.)
from django.db import models

# Importa a classe base de usuário do Django, que já possui autenticação pronta
from django.contrib.auth.models import AbstractUser


# ================================
# MODEL DE USUÁRIO DO SISTEMA
# ================================
class Usuario(AbstractUser):
    """
    Representa o usuário do sistema.
    Herda de AbstractUser, que já possui:
    - username
    - senha (password)
    - email
    - permissões
    """

    # Enumeração de tipos de usuário (papéis no sistema)
    class TipoUsuario(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'           # Dono ou gestor da clínica
        ESPECIALISTA = 'ESPECIALISTA', 'Especialista'  # Médico ou profissional de saúde
        PACIENTE = 'PACIENTE', 'Paciente'          # Usuário final atendido
        RECEPCAO = 'RECEPCAO', 'Recepção'          # Funcionário administrativo

    # Campo que define o tipo do usuário
    tipo = models.CharField(
        max_length=20,                      # Tamanho máximo do valor salvo no banco
        choices=TipoUsuario.choices,        # Limita os valores aos definidos acima
        default=TipoUsuario.PACIENTE        # Valor padrão ao criar um usuário
    )

     # Define como o objeto será exibido como texto (ex: no admin)
    def __str__(self):
        return self.username


# ================================
# VÍNCULO USUÁRIO ↔ CLÍNICA
# ================================
class UsuarioClinica(models.Model):
    """
    Representa o vínculo entre usuário e clínica.
    Permite que um usuário pertença a várias clínicas.
    """
    class PapelClinica(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'           # Dono ou gestor da clínica
        ESPECIALISTA = 'ESPECIALISTA', 'Especialista'  # Médico ou profissional de saúde
        RECEPCAO = 'RECEPCAO', 'Recepção'          # Funcionário administrativo

    # Referência ao usuário
    usuario = models.ForeignKey(
        'accounts.Usuario',                 # Referência ao model Usuario
        on_delete=models.CASCADE,            # Se o usuário for deletado, o vínculo também será
        related_name='vinculos_clinica'
    )

    # Referência à clínica
    clinica = models.ForeignKey(
        'clinicas.Clinica',                 # Referência ao model Clinica
        on_delete=models.CASCADE,            # Se a clínica for deletada, o vínculo também será
        related_name='usuarios_vinculados'
    )

    papel = models.CharField(
        max_length=20,
        choices=PapelClinica.choices
    )

    # Indica se o vínculo está ativo
    ativo = models.BooleanField(
        default=True                        # Por padrão, o vínculo é ativo
    )

    # Define restrições e configurações do model
    class Meta:
    # evita duplicidade de vínculo usuário x clínica
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'clinica'],
                name='unique_usuario_clinica'
            )
        ]

        indexes = [
            models.Index (fields=['usuario']),
        ]

        # ordenação padrão (melhora admin e consultas)
        ordering = ['usuario', 'clinica']

        # nomes amigáveis no admin
        verbose_name = 'Vínculo Usuário-Clinica'
        verbose_name_plural = 'Vínculos Usuário-Clinica'

    # Representação textual do vínculo
    def __str__(self):
        return f"{self.usuario} - {self.clinica} ({self.papel})"