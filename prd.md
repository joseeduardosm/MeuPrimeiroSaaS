
ClinicaOS
SaaS de Gestão de Clínicas e Consultórios

PRD — Product Requirements Document
Tech Spec — Especificação Técnica
Versão 1.0 — MVP
5 de maio de 2026

Parte 1 — Product Requirements Document (PRD)

1.1 Visão do Produto
O ClinicaOS é uma plataforma SaaS multi-tenant para gestão de clínicas e consultórios médicos, desenvolvida com foco em conformidade legal (LGPD e CFM), experiência do usuário e escalabilidade. Cada clínica opera em um ambiente isolado, com dados segregados e controle de acesso próprio.

1.2 Público-Alvo
Perfil	Quem é	O que precisa
Administrador da clínica	Dono ou gestor da clínica/consultório	Cadastrar equipe, configurar plano, ver relatórios
Especialista (médico)	Profissional de saúde vinculado à clínica	Ver agenda, registrar prontuário, emitir prescrições
Recepcionista	Funcionário da clínica	Agendar consultas, gerenciar fila, confirmar pacientes
Paciente	Usuário final do serviço	Confirmar/cancelar consultas, acessar histórico
Super Admin (SaaS)	Equipe ClinicaOS	Gerenciar tenants, planos, monitorar sistema

1.3 Funcionalidades do MVP — v1
1.3.1 Gestão de Clínicas (CRUD)
•	Cadastro da clínica: razão social, CNPJ, endereço, logotipo, contatos
•	Configuração de horários de funcionamento por dia da semana
•	Vinculação de especialistas à clínica
•	Gestão de salas/consultórios por clínica
•	Isolamento total de dados entre tenants (row-level ou schema separation)

1.3.2 Gestão de Especialistas (CRUD)
•	Cadastro completo: nome, CRM/CRO/número de registro, especialidade, foto
•	Vinculação a uma ou mais clínicas
•	Configuração de agenda semanal por especialista e por clínica
•	Duração padrão de atendimento por tipo (consulta, exame, procedimento)

1.3.3 Gestão de Pacientes (CRUD)
•	Cadastro: nome, CPF, data de nascimento, contatos, convênio
•	Consentimento LGPD explícito no momento do cadastro (aceite digital com timestamp)
•	Histórico de atendimentos por clínica (prontuário eletrônico básico)
•	Direito ao esquecimento: exclusão/anonimização de dados mediante solicitação
•	Exportação de dados do paciente (portabilidade LGPD)

1.3.4 Agendamentos (Consultas, Exames e Procedimentos)
•	CRUD completo para os três tipos de agendamento
•	Chaves estrangeiras: Clínica + Especialista + Paciente (obrigatórias)
•	Status do agendamento: Agendado / Confirmado / Cancelado / Realizado / Falta
•	Verificação de conflito de horário (mesmo especialista, mesmo horário)
•	Fila de espera automática quando horário está ocupado
•	Confirmação/cancelamento via WhatsApp (API) ou e-mail
•	Avaliação pós-atendimento (NPS simplificado: 1 a 5 estrelas + comentário)

1.3.5 Financeiro — Planos SaaS
•	Planos: Free (1 especialista, 50 agendamentos/mês), Pro, Enterprise
•	Controle de inadimplência: bloqueio de funcionalidades após vencimento
•	Histórico de pagamentos por clínica/tenant
•	Webhooks para integração com gateway de pagamento (Stripe ou Pagar.me)

1.3.6 Financeiro — Clínicas (Cobranças de Pacientes)
•	Registro de valor por consulta/exame/procedimento
•	Registro de convênio (particular, plano de saúde)
•	Controle de pagamento: Pendente / Pago / Parcial / Isento
•	Controle de inadimplência por paciente
•	Relatório financeiro por período, por especialista, por tipo

1.3.7 Prontuário Eletrônico Básico
•	Registro de atendimento: queixa principal, observações, CID-10
•	Histórico cronológico por paciente e por clínica
•	Acesso restrito: apenas especialistas da clínica onde o atendimento ocorreu
•	Log de acesso ao prontuário (LGPD — rastreabilidade)

1.3.8 Conformidade Legal (LGPD + CFM)
•	Aceite de termos e política de privacidade com versão e timestamp
•	Log de acesso a dados sensíveis de pacientes
•	Criptografia de campos sensíveis no banco (CPF, data de nascimento)
•	Retenção de dados: configurável por tenant, com política de purge
•	DPO (Data Protection Officer): campo de contato obrigatório no cadastro da clínica

1.4 Fora do Escopo v1 (próximas versões)
•	Telemedicina / videochamada integrada
•	Prescrição digital com assinatura ICP-Brasil
•	App mobile nativo
•	Integração com TISS/ANS (convênios)
•	Módulo de estoque/farmácia

Parte 2 — Tech Spec (Especificação Técnica Django)

2.1 Stack Tecnológica
Camada	Tecnologia	Justificativa
Backend	Django 5.x + Python 3.12	Framework principal, MTV, ORM
Banco de dados	PostgreSQL 16	Suporte a row-level security, JSON fields, UUID PKs
Cache / Filas	Redis + Celery	Notificações assíncronas, confirmações, e-mails
Frontend	Django Templates + HTMX + Alpine.js	Sem SPA — progressivo, baixo custo de manutenção
CSS	Tailwind CSS (via CDN no dev, build no prod)	UI moderna sem framework pesado
Arquivos estáticos	WhiteNoise (dev) + S3 (prod)	Mesma estratégia do SGI
E-mail	Django email + SendGrid	Confirmações e notificações
WhatsApp	Twilio API ou Evolution API	Confirmação/cancelamento de consultas
Autenticação	Django Auth + django-allauth	Login, convites, múltiplos perfis
Multi-tenancy	django-tenants ou tenant_id por model	Isolamento de dados entre clínicas
Pagamentos	Stripe ou Pagar.me (webhooks)	Planos SaaS + cobranças de pacientes
Deploy	Docker + Nginx + Gunicorn	Containerização e ambiente replicável

2.2 Estrutura de Apps Django
O projeto segue o princípio de separação de responsabilidades: cada app tem uma única área de domínio. Nenhum app importa diretamente de outro — a comunicação ocorre via signals ou services.

App	Responsabilidade	Models principais
core/	Configurações globais, base models, multi-tenancy	Tenant, Plano, Assinatura
accounts/	Autenticação, usuários, perfis, convites	User, PerfilUsuario, Convite
clinicas/	CRUD de clínicas e suas configurações	Clinica, Sala, HorarioFuncionamento
especialistas/	CRUD de especialistas e suas agendas	Especialista, AgendaSemanal, VinculoClinica
pacientes/	CRUD de pacientes, consentimento, LGPD	Paciente, ConsentimentoLGPD, LogAcessoDados
agendamentos/	Consultas, exames, procedimentos, fila	Agendamento, TipoAgendamento, FilaEspera
prontuario/	Prontuário eletrônico por atendimento	Prontuario, RegistroAtendimento, CID10
financeiro/	Cobranças, inadimplência, relatórios	Cobranca, Pagamento, StatusFinanceiro
planos/	Planos SaaS, assinaturas, limites	PlanoClinica, LimitePlano, HistoricoPlano
notificacoes/	E-mail, WhatsApp, filas Celery	Notificacao, TemplateMsg, LogEnvio
avaliacoes/	NPS pós-atendimento	Avaliacao, RespostaAvaliacao
auditoria/	Log de ações e acesso a dados sensíveis	AuditLog, LogAcessoProntuario

2.3 Estratégia Multi-Tenant
Cada Clinica é um tenant. A segregação de dados será feita via campo tenant_id (FK) em todos os models de domínio, com middleware que injeta o tenant atual em cada requisição.

•	TenantMiddleware: identifica o tenant pelo subdomínio (clinica.clinicaos.com.br) ou pelo usuário autenticado
•	BaseTenantModel: model abstrato com tenant (FK → Clinica) e campos de auditoria (criado_em, atualizado_em, criado_por)
•	TenantManager: manager customizado que filtra automaticamente por tenant em todo queryset
•	Validação: nenhuma view de domínio retorna dados de outro tenant — garantido no manager, não na view

2.4 Models Centrais — Esboço
Paciente
Campo	Tipo Django	Observação
id	UUIDField (PK)	Nunca expor ID sequencial — LGPD
clinica	ForeignKey → Clinica	Tenant do paciente
nome_completo	CharField	Dado pessoal — log de acesso obrigatório
cpf	CharField (criptografado)	Usar django-encrypted-model-fields
data_nascimento	DateField (criptografado)	Dado sensível LGPD
telefone	CharField	Para notificações WhatsApp
email	EmailField	Para confirmações por e-mail
convenio	CharField (nullable)	Particular ou nome do plano
consentimento_lgpd	OneToOneField → ConsentimentoLGPD	Obrigatório antes de salvar
ativo	BooleanField	Soft delete — nunca deletar fisicamente
criado_em / atualizado_em	DateTimeField (auto)	Rastreabilidade

Agendamento
Campo	Tipo Django	Observação
id	UUIDField (PK)	
clinica	ForeignKey → Clinica	Tenant
especialista	ForeignKey → Especialista	Profissional responsável
paciente	ForeignKey → Paciente	Paciente atendido
tipo	CharField (choices)	CONSULTA | EXAME | PROCEDIMENTO
data_hora_inicio	DateTimeField	Início do atendimento
data_hora_fim	DateTimeField	Calculado a partir da duração padrão
status	CharField (choices)	AGENDADO|CONFIRMADO|CANCELADO|REALIZADO|FALTA
valor	DecimalField	Valor cobrado neste atendimento
status_pagamento	CharField (choices)	PENDENTE|PAGO|PARCIAL|ISENTO
observacoes	TextField (nullable)	Notas internas
avaliacao	OneToOneField → Avaliacao	Preenchida pós-atendimento

2.5 Padrões de Desenvolvimento
Fat Views → Services
Toda lógica de negócio que não é I/O HTTP vai para services.py. A view recebe a requisição, valida o form e chama o service. O service não conhece request.

•	agendamentos/services.py → AgendamentoService.criar(), .cancelar(), .confirmar()
•	notificacoes/services.py → NotificacaoService.enviar_confirmacao(), .enviar_lembrete()
•	financeiro/services.py → FinanceiroService.registrar_pagamento(), .verificar_inadimplencia()

Regras de URLs
•	URLs raiz (urls.py): apenas inclui os apps — sem lógica
•	Cada app tem seu próprio urls.py com namespace declarado
•	Padrão de nomenclatura: {app}:{entidade}-{acao} (ex: agendamentos:consulta-criar)
•	UUIDs nas URLs — nunca IDs sequenciais expostos

Class-Based Views
•	Preferir CBVs com Mixins: LoginRequiredMixin + TenantRequiredMixin + PermissionRequiredMixin
•	TenantRequiredMixin: valida que o objeto acessado pertence ao tenant do usuário logado
•	Formulários customizados em forms.py — nunca lógica de validação na view

Testes
•	Cobertura mínima: 80% nos services e models
•	Usar pytest-django + factory_boy para fixtures
•	Todo novo model deve ter ao menos: test_criacao, test_str, test_tenant_isolation
•	Todo novo service deve ter: test_caminho_feliz, test_validacao, test_permissao

2.6 LGPD — Implementação Técnica
Requisito LGPD	Implementação Django
Consentimento explícito	Model ConsentimentoLGPD com versao_termos, ip_origem, timestamp, aceite=True/False
Direito ao esquecimento	Management command anonymize_paciente — substitui dados por hash anônimo, mantém registros médicos
Portabilidade de dados	View export_dados_paciente → gera JSON/PDF com todos os dados do paciente
Log de acesso	Signal post_read no prontuário → grava em LogAcessoProntuario (quem, quando, qual)
Criptografia em repouso	django-encrypted-model-fields nos campos CPF e data_nascimento
Retenção de dados	Configuração por tenant: prazo_retencao_anos → cron job de purge via Celery Beat
DPO	Campo obrigatório no cadastro da Clinica: nome_dpo e email_dpo

2.7 Roadmap de Desenvolvimento
Sprint	Tema	Entregáveis
1	Base e infraestrutura	Projeto Django, apps criados, BaseTenantModel, TenantMiddleware, autenticação
2	Clínicas e especialistas	CRUD Clinica, CRUD Especialista, vínculo, agenda semanal
3	Pacientes e LGPD	CRUD Paciente, ConsentimentoLGPD, LogAcesso, exportação
4	Agendamentos	CRUD Consulta/Exame/Procedimento, conflito de horário, fila de espera
5	Financeiro clínica	Cobranças por atendimento, status pagamento, inadimplência, relatórios
6	Notificações	E-mail de confirmação, WhatsApp API, cancelamento, avaliação pós-atendimento
7	Prontuário	Registro de atendimento, histórico, CID-10, controle de acesso
8	Planos SaaS	Modelos de plano, controle de limites, webhooks de pagamento, inadimplência
9	Testes e hardening	Cobertura 80%, auditoria de segurança, LGPD checklist, deploy Docker


ClinicaOS — Documento interno. Não distribuir.
