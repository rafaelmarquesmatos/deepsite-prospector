# Site Prospector

Prospecção semiautomática de clientes com site fraco: encontra negócios com alto potencial no Google Maps, cria um redesign premium, publica no seu hosting e envia a proposta por e-mail — tudo comandado pelo assistente de IA em linguagem natural.

**Neutro em relação a agente.** É um toolkit portátil de skills + MCP, não um plugin preso a nenhum fornecedor. Funciona em qualquer agente/IDE de IA que suporte **servidores MCP** e **skills** (Claude Code / Claude Cowork, Gemini CLI / Antigravity, Cursor, Codex, opencode e outros). O CRM, o painel e as templates são Python/SQLite/HTML puros, sem nenhuma dependência específica de agente.

A busca de negócios roda no **navegador** (MCP Playwright) — sem API key do Google, sem vínculo com fornecedor. O navegador entra só para avaliar o site de cada lead e achar o e-mail.

## Feito para o DeepSeek Harness (creator mode)

Este projeto foi pensado para rodar como um **modo** (agent preset) do [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), criado pelo **creator mode**. A instalação é só colar o `PROMPT.md` no creator mode: o agente **clona este repo e instala o preset a partir dele** (não re-escreve o toolkit).

O preset pronto fica em `deepseek-harness/`:

```
deepseek-harness/
├── PROMPT.md           ← a spec que você cola no creator mode (em inglês)
├── preset.yml          ← nome e descrição do preset
├── agent.cordis.yml    ← composição do agente (persona + tools + MCP + skills)
└── self-update.js      ← plugin de auto-update (roda no início de cada sessão)
```

### O prompt do modo

Cole o conteúdo de `deepseek-harness/PROMPT.md` no **creator mode** do DeepSeek Harness (ao criar o modo):

> <!-- PROMPT: cole aqui o conteúdo de deepseek-harness/PROMPT.md -->

> ⚠️ **Funciona em qualquer harness.** Este mesmo conteúdo é teoricamente independente de fornecedor: funciona em Claude Code, Gemini CLI, Cursor, opencode etc. Basta pedir a um LLM para adaptar os trechos específicos do harness (nomes de ferramentas, forma de carregar as skills, local da config MCP). A lógica do pipeline, as skills e as templates não mudam.

## Estrutura do toolkit

```
deepseek-harness/              ← o modo pronto para o DeepSeek Harness (creator mode)
├── PROMPT.md                  a spec que você cola no creator mode (em inglês)
├── preset.yml                 nome e descrição do preset
├── agent.cordis.yml           persona + tools + MCP + skills
└── self-update.js             plugin de auto-update (roda no início de cada sessão)

site-prospector/               ← esta pasta é o toolkit (fonte única da verdade)
├── mcp_config.json            define os servidores MCP (CRM + navegador Playwright)
├── prospector_mcp.py          servidor MCP do CRM (SQLite)
├── dashboard/                 painel local (Python/SQLite) — pronto para copiar
└── skills/                    as 7 skills (SKILL.md)
    ├── setup/
    ├── maps-prospecting/
    ├── premium-redesign/
    ├── email-proposal/
    ├── deploy/
    ├── leads-dashboard/
    └── service-contract/
```

## Configuração

Abra a pasta do projeto e diga ao assistente **"configurar o prospector"**. A skill `setup` coleta seus dados, o domínio de hosting (opcional) e instala o painel local. Os servidores MCP e as skills já vêm ativos no modo — o empacotamento está descrito no prompt (`deepseek-harness/PROMPT.md`).

## Como usar (linguagem natural)

1. **"prospecta nutricionistas em São Paulo"** → navega no Google Maps, qualifica (nota alta + site ruim + e-mail) e alimenta o dashboard.
2. **"redesenha os 5 melhores"** → redesign premium + editor visual + comparador antes/depois.
3. **"publica o site"** → prepara os arquivos, orienta o upload manual (qualquer hosting) e verifica HTTPS.
4. **"manda a proposta"** → rascunho de e-mail anti-spam pronto para revisar.
5. Depois: contrato, e o `dashboard.html` administra tudo (kanban + financeiro).

## Observações

- A moeda aparece como `R$` (BRL) — o fluxo mira o mercado brasileiro (WhatsApp como canal de contato principal, hosting próprio do usuário). Ajuste as templates se operar em outro país.
- O `dashboard.html` é um painel único autocontido: kanban com drag & drop, edição, funil, contratos e financeiro. Duplo clique em `start-dashboard.bat` (Windows) / `start-dashboard.command` (macOS) roda com o banco de dados conectado.
