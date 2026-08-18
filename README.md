# Site Prospector

Prospecção semiautomática de clientes com site fraco: encontra negócios com alto potencial no Google Maps, cria um redesign premium, publica na HostGator e envia a proposta por e-mail — tudo comandado pelo assistente de IA em linguagem natural.

**Neutro em relação a agente.** É um toolkit portátil de skills + MCP, não um plugin preso a nenhum fornecedor. Funciona em qualquer agente/IDE de IA que suporte **servidores MCP** e **skills** (Claude Code / Claude Cowork, Gemini CLI / Antigravity, Cursor, Codex, opencode e outros). O CRM, o painel e as templates são Python/SQLite/HTML puros, sem nenhuma dependência específica de agente.

A busca de negócios roda no **navegador** (MCP Playwright) — sem API key do Google, sem vínculo com fornecedor. O navegador entra só para avaliar o site de cada lead e achar o e-mail.

## Feito para o DeepSeek Harness (creator mode)

Este projeto foi pensado para rodar como um **modo** (agent preset) do [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), criado pelo **creator mode**. O prompt abaixo é o que você cola no creator mode para transformar o assistente no Site Prospector.

O preset pronto fica em `deepseek-harness/`:

```
deepseek-harness/
├── PROMPT.md           ← o prompt do modo (em inglês)
├── preset.yml          ← nome e descrição do preset
└── agent.cordis.yml    ← composição do agente (persona + tools + skills)
```

### O prompt do modo

Cole o conteúdo de `deepseek-harness/PROMPT.md` no campo de persona/system prompt do creator mode:

> <!-- PROMPT: cole aqui o conteúdo de deepseek-harness/PROMPT.md -->

> ⚠️ **Funciona em qualquer harness.** Este mesmo conteúdo é teoricamente independente de fornecedor: funciona em Claude Code, Gemini CLI, Cursor, opencode etc. Basta pedir a um LLM para adaptar os trechos específicos do harness (nomes de ferramentas, forma de carregar as skills, local da config MCP). A lógica do pipeline, as skills e as templates não mudam.

## Estrutura do toolkit

```
deepseek-harness/              ← o modo pronto para o DeepSeek Harness (creator mode)
├── PROMPT.md                  o prompt do modo (em inglês)
├── preset.yml                 nome e descrição do preset
└── agent.cordis.yml           persona + tools + skills

site-prospector/               ← esta pasta é o toolkit
├── mcp_config.json            define os servidores MCP (CRM + navegador Playwright)
├── prospector_mcp.py          servidor MCP do CRM (SQLite)
├── dashboard/                 painel local (Python/SQLite) — pronto para copiar
└── skills/                    as 7 skills (SKILL.md)
    ├── setup/
    ├── maps-prospecting/
    ├── premium-redesign/
    ├── email-proposal/
    ├── hostgator-deploy/
    ├── leads-dashboard/
    └── service-contract/
```

## Instalação

### 1. Registrar os servidores MCP

Registre os dois servidores MCP do `mcp_config.json` na configuração de MCP do seu agente:

- **prospector-crm** — o servidor local do CRM (`prospector_mcp.py`). Aponte `--folder` para a pasta do seu projeto (onde ficam `prospector.db`, os leads e os sites).
- **playwright** — o servidor de automação de navegador (`@playwright/mcp`), usado para prospectar no Google Maps, avaliar sites de clientes e achar e-mails.

Cada agente tem seu próprio local de config de MCP (veja a documentação do seu). O schema JSON é o padrão MCP, então é o mesmo para todos.

### 2. Instalar as skills

Copie a pasta `skills/` para o diretório de skills do seu agente, para que o assistente consiga carregá-las sob demanda:

- **DeepSeek Harness:** `.dsh/skills/` na raiz do projeto (ou use o preset de `deepseek-harness/`)
- **Claude Code:** `~/.claude/skills/`
- **Gemini / Antigravity:** `~/.gemini/skills/` (ou `.agents/skills/` no projeto)
- **opencode:** `.opencode/skills/` na raiz do workspace
- **Cursor:** consulte a documentação de skills/rules da sua versão

As skills são `SKILL.md` em markdown com frontmatter YAML — o mesmo formato que a maioria dos agentes usa. Se o seu agente usar outra convenção, adapte apenas a estrutura de pastas; o conteúdo é a lógica.

### 3. Configurar o Prospector

Abra a pasta do projeto e diga ao assistente **"configurar o prospector"**. A skill `setup` coleta seus dados, a conexão HostGator e instala o painel local.

## Como usar (linguagem natural)

1. **"prospecta nutricionistas em São Paulo"** → navega no Google Maps, qualifica (nota alta + site ruim + e-mail) e alimenta o dashboard.
2. **"redesenha os 5 melhores"** → redesign premium + editor visual + comparador antes/depois.
3. **"publica na HostGator"** → sobe as páginas e a página-capa, verifica HTTPS.
4. **"manda a proposta"** → rascunho de e-mail anti-spam pronto para revisar.
5. Depois: contrato, e o `dashboard.html` administra tudo (kanban + financeiro).

## Como ele se mantém neutro

- **Sem arquivos de plugin de fornecedor** — só config MCP padrão, Python, SQLite, HTML e `SKILL.md`.
- **Sem caminhos de agente fixos** — os caminhos são placeholders que você preenche para a sua máquina e pasta do projeto.
- **Busca no Google Maps via navegador** — sem API key do Google Maps Platform.
- **CRM + dashboard locais** — todos os dados ficam no seu computador, no `prospector.db`; nada depende de conector em nuvem.
- **Qualquer provedor de e-mail** — a skill de proposta gera o rascunho via seu MCP/conector de e-mail ou por um link de compose simples.

## Observações

- A moeda aparece como `R$` (BRL) — o fluxo mira o mercado brasileiro (hospedagem HostGator, WhatsApp como canal de contato principal). Ajuste as templates se operar em outro país.
- O `dashboard.html` é um painel único autocontido: kanban com drag & drop, edição, funil, contratos e financeiro. Duplo clique em `start-dashboard.bat` (Windows) / `start-dashboard.command` (macOS) roda com o banco de dados conectado.
