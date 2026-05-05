Eu seguiria esta trilha em Pacientes:

1. **Organizar com `forms.py`**
   Trocar leitura manual de `request.POST.get(...)` por `PacienteForm`.
   Você aprende validação, erros no formulário e reaproveitamento.

2. **Melhorar validações**
   CPF duplicado, e-mail duplicado, campos obrigatórios, data de nascimento válida.

3. **Melhorar listagem**
   Pesquisa por nome, CPF e telefone.
   Filtro de ativos/inativos.
   Status mais bonito no template.

4. **Criar página de detalhe**
   `/pacientes/5/`
   Mostra dados completos do paciente e depois pode mostrar prontuários/agendamentos.

5. **Resetar senha temporária**
   Botão “Gerar nova senha” para paciente.
   Excelente para aprender POST separado em outra view.

6. **Troca obrigatória de senha**
   Campo no usuário tipo `deve_alterar_senha`.
   Depois do login, redireciona para trocar senha.

7. **Permissões mais refinadas**
   Admin/recepção podem criar.
   Especialista pode visualizar, talvez não excluir.
   Paciente só vê o próprio cadastro.

8. **Tenant/clínica**
   Associar paciente a uma clínica.
   A lista passa a mostrar só pacientes da clínica do usuário.