from django.contrib.auth.decorators import user_passes_test


def pode_gerenciar_pacientes(user):
    return user.is_authenticated and user.tipo in [
        user.TipoUsuario.ADMIN,
        user.TipoUsuario.ESPECIALISTA,
        user.TipoUsuario.RECEPCAO,
    ]

gerenciar_pacientes_required = user_passes_test(pode_gerenciar_pacientes)