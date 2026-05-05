import uuid
from django.db import models


# Create your models here.
class ModeloBase(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True
    )
    
    atualizado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
