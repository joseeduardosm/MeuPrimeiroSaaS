from django.urls import path
from .views import criar_paciente, editar_paciente, excluir_paciente, lista_pacientes

urlpatterns = [
    path('', lista_pacientes, name='pacientes_lista'),
    path('novo/', criar_paciente, name='pacientes_novo'),
    path('<int:paciente_id>/editar/', editar_paciente, name='pacientes_editar'),
    path('<int:paciente_id>/excluir/', excluir_paciente, name='pacientes_excluir'),
]
