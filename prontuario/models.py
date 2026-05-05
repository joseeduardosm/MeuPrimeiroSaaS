from django.db import models


class Prontuario(models.Model):
    """
    Representa um registro clínico do paciente.
    Cada registro pertence a uma clínica e a um paciente.
    """

    paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.CASCADE,
        related_name='prontuarios'
    )

    clinica = models.ForeignKey(
        'clinicas.Clinica',
        on_delete=models.CASCADE,
        related_name='prontuarios'
    )

    descricao = models.TextField()

    # auditoria (IMPORTANTE)
    criado_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        related_name='prontuarios_criados'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'

    def __str__(self):
        return f"{self.paciente} - {self.clinica}"