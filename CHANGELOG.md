# Changelog

Todas as mudanças relevantes deste projeto de estudo serão registradas aqui.

## 2026-05-05

### Adicionado

- Criado projeto Django base do SaaS de clínicas.
- Criado usuário customizado em `accounts.Usuario` com tipos:
  - `ADMIN`
  - `ESPECIALISTA`
  - `PACIENTE`
  - `RECEPCAO`
- Criado vínculo `UsuarioClinica` para futura relação entre usuários e clínicas.
- Criado model `Clinica` com campos de identificação, contato, DPO e retenção de dados.
- Criado model `Paciente` com vínculo para usuário, CPF, data de nascimento, telefone e status `ativo`.
- Criado model inicial de `Especialista`.
- Criado model inicial de `Prontuario`.
- Criada autenticação via `LoginView` e `LogoutView`.
- Criado dashboard inicial em `core`.
- Criado CRUD básico de pacientes:
  - listagem;
  - criação;
  - edição;
  - exclusão lógica.
- Criada geração de usuário para paciente cadastrado pela recepção.
- Adicionadas mensagens do Django para feedback de criação, edição e exclusão.
- Adicionado modal Bootstrap para exibir mensagens do sistema.
- Adicionado controle visual da navbar para esconder o menu de pacientes quando o usuário logado é do tipo `PACIENTE`.
- Criado decorator `gerenciar_pacientes_required` em `accounts/decorators.py`.
- Aplicado controle de acesso ao CRUD de pacientes para equipe da clínica.
- Adicionada pesquisa de pacientes por nome.
- Adicionado filtro para incluir ou ocultar pacientes inativos.
- Criado `pacientes/forms.py` com `PacienteForm` como início da migração para Django Forms.
- Criado `proximos-passos.md` para organizar a trilha de aprendizado.
- Criado `README.md` com visão do projeto, stack e setup local.

### Alterado

- `base.html` passou a ser um template HTML completo com Bootstrap, navbar, bloco de conteúdo e modal de mensagens.
- O login do paciente passou a usar e-mail como `username` durante a criação.
- A exclusão de paciente passou a ser soft delete:
  - `Paciente.ativo = False`;
  - `Usuario.is_active = False`.
- A listagem de pacientes passou a permitir alternar entre apenas ativos e ativos/inativos.
- O formulário de pacientes passou a exibir checkbox de status no modo edição.

### Corrigido

- Corrigida view de criação de pacientes para sempre retornar uma resposta HTTP.
- Corrigido problema de checkbox `ativo` enviando `"on"` em vez de booleano.
- Corrigidos imports do decorator de permissão.
- Corrigida validação de e-mail duplicado para consultar `Usuario` em vez de `Paciente`.

### Notas Técnicas

- O módulo de pacientes ainda usa validações parcialmente manuais em `views.py`.
- `PacienteForm` foi criado, mas ainda não foi integrado às views/templates.
- A senha temporária atual ainda precisa ser revisada para voltar a ser aleatória e mais segura.
- O sistema ainda não implementa tenant real por clínica.
