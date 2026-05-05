# Bom Atendimento / ClinicaOS

Sistema de estudo para construção de um SaaS de gestão de clínicas e consultórios com Django.

O projeto segue o PRD em `prd.md`, que descreve a visão de um produto multi-tenant para clínicas, com gestão de pacientes, especialistas, agendamentos, prontuário, financeiro, notificações e requisitos de conformidade LGPD/CFM.

## Progresso Da Trilha De Pacientes

O módulo `pacientes` está sendo usado como laboratório principal de aprendizado antes de replicar os padrões nos demais CRUDs.

| Etapa | Progresso estimado | Status |
| --- | ---: | --- |
| Organizar com `forms.py` | 20% | `PacienteForm` criado, mas ainda não integrado às views e templates. |
| Melhorar validações | 35% | Há validações manuais para CPF e e-mail duplicados, mas ainda falta centralizar no form e tratar melhor erros de campos. |
| Melhorar listagem | 60% | Já existe pesquisa por nome e filtro para incluir inativos; ainda faltam busca por CPF/telefone e status mais amigável. |
| Criar página de detalhe | 0% | Ainda não existe rota `/pacientes/<id>/` para visualização detalhada. |
| Resetar senha temporária | 0% | Ainda não existe ação separada para gerar nova senha temporária. |
| Troca obrigatória de senha | 0% | Ainda não existe campo/regra para forçar alteração de senha no primeiro login. |
| Permissões mais refinadas | 40% | CRUD já é restrito à equipe da clínica; ainda falta diferenciar permissões entre admin, recepção, especialista e paciente. |
| Tenant/clínica | 0% | Paciente ainda não está vinculado a uma clínica/tenant. |

## Objetivo do MVP

Construir uma base Django para gestão operacional de clínicas, começando pelos fundamentos:

- autenticação com usuário customizado;
- controle de perfis de usuário;
- CRUD de pacientes;
- controle de acesso por tipo de usuário;
- templates Django com Bootstrap;
- evolução gradual para multi-tenancy por clínica.

## Stack Atual

- Python 3.11
- Django 5.1
- MySQL
- Bootstrap via CDN
- Django Templates

## Apps Planejados

Conforme o PRD, a arquitetura prevê apps separados por domínio:

- `core`: dashboard e estrutura geral;
- `accounts`: usuários, perfis e permissões;
- `clinicas`: cadastro das clínicas/tenants;
- `pacientes`: cadastro de pacientes e regras LGPD iniciais;
- `especialistas`: profissionais de saúde;
- `agendamentos`: consultas, exames e procedimentos;
- `prontuario`: registros clínicos;
- `financeiro`: cobranças e pagamentos;
- `notificacoes`: e-mail, WhatsApp e logs;
- `auditoria`: rastreabilidade e acessos sensíveis.

## Estado Atual

O módulo mais avançado no momento é `pacientes`, usado como laboratório de aprendizado dos conceitos centrais do Django:

- roteamento com `urls.py`;
- views baseadas em função;
- `GET` e `POST`;
- templates com contexto;
- mensagens do Django;
- decorators de permissão;
- soft delete;
- filtros por query string;
- introdução a `forms.py`.

## Setup Local

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente em `.env`:

```env
DJANGO_SECRET_KEY=sua-chave
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

MYSQL_NAME=nome_do_banco
MYSQL_USER=usuario
MYSQL_PASSWORD=senha
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Execute as migrations:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Observações

Este repositório é um projeto de estudo em evolução. Algumas decisões ainda são deliberadamente simples para fins didáticos e serão refinadas com o avanço do aprendizado.

Pontos futuros importantes:

- mover validações para `forms.py`;
- criar vínculo real entre pacientes e clínicas;
- implementar isolamento por tenant;
- substituir senha temporária previsível por senha aleatória;
- melhorar regras LGPD, auditoria e prontuário.
