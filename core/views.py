from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from prontuario.models import Prontuario


@login_required
def dashboard(request):
    total_pacientes = Paciente.objects.count()
    total_prontuarios = Prontuario.objects.count()

    return render(request, 'core/dashboard.html', {
        'total_pacientes': total_pacientes,
        'total_prontuarios': total_prontuarios,
    })