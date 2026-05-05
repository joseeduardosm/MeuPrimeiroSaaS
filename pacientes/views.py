from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.crypto import get_random_string
from accounts.decorators import gerenciar_pacientes_required

from .models import Paciente


@gerenciar_pacientes_required
@login_required
def lista_pacientes(request):
    busca = request.GET.get('pesquisa')
    incluir_inativos = request.GET.get('incluir_inativos') == 'on'

    pacientes = Paciente.objects.select_related('usuario').order_by('nome_completo')

    if not incluir_inativos:
        pacientes = pacientes.filter(ativo=True)

    if busca:
        pacientes = pacientes.filter(nome_completo__icontains=busca)

    return render(request, 'pacientes/lista.html', {
        'pacientes': pacientes,
        'busca': busca,
        'incluir_inativos': incluir_inativos,
    })

@gerenciar_pacientes_required
@login_required
def criar_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        data_nascimento = request.POST.get('data_nascimento') or None
        telefone = request.POST.get('telefone')

        if Paciente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Já existe um paciente cadastrado com este CPF')
            return render(request, 'pacientes/form.html', {
                'titulo': 'Novo Paciente'
            })
        
        Usuario = get_user_model()

        if Usuario.objects.filter(username=email).exists():
            messages.error(request, 'Já existe um usuário cadastrado com este email')
            return render(request, 'pacientes/form.html', {
                'titulo': 'Novo Paciente'
            })
        
        senha_temporaria = data_nascimento

        
        usuario = Usuario.objects.create_user(
            username=email,
            email=email,
            password=senha_temporaria,
            tipo=Usuario.TipoUsuario.PACIENTE
        )

        Paciente.objects.create(
            usuario=usuario,
            nome_completo=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone=telefone
        )

        messages.success(
            request,
            f'Paciente criado com sucesso. Senha temporária: {senha_temporaria}'
        )

        return redirect('pacientes_lista')

    return render(request, 'pacientes/form.html', {
        'titulo': 'Novo Paciente'
    })

@gerenciar_pacientes_required
@login_required
def editar_paciente(request, paciente_id):
    #paciente = get_object_or_404(Paciente, id=paciente_id, ativo=True)
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        data_nascimento = request.POST.get('data_nascimento') or None
        telefone = request.POST.get('telefone')
        status = request.POST.get('ativo') == 'on'

        cpf_ja_cadastrado = Paciente.objects.filter(cpf=cpf).exclude(id=paciente.id).exists()

        if cpf_ja_cadastrado:
            messages.error(request, 'Já existe outro paciente cadastrado com este CPF')
            return render(request, 'pacientes/form.html', {
                'paciente': paciente,
                'titulo': 'Editar Paciente'
            })

        paciente.nome_completo = nome
        paciente.cpf = cpf
        paciente.data_nascimento = data_nascimento
        paciente.telefone = telefone
        paciente.ativo = status
        paciente.save()

        paciente.usuario.username = email
        paciente.usuario.email = email
        paciente.usuario.save()
        

        messages.success(request, 'Paciente atualizado com sucesso')
        return redirect('pacientes_lista')

    return render(request, 'pacientes/form.html', {
        'paciente': paciente,
        'titulo': 'Editar Paciente'
    })



@gerenciar_pacientes_required
@login_required
def excluir_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id, ativo=True)

    if request.method == 'POST':
        paciente.ativo = False
        paciente.save()

        paciente.usuario.is_active = False
        paciente.usuario.save()

        messages.success(request, 'Paciente removido com sucesso')

    return redirect('pacientes_lista')
