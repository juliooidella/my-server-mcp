# 🚀 MCP Server (Jira + Discord)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://docker.com)

Um servidor MCP (Model Context Protocol) para integração com Jira Cloud e Discord através do GitHub Copilot no VS Code.

> 📘 **[Guia Completo de Configuração com VS Code + GitHub Copilot](CONFIGURACAO_MCP.md)** > Aprenda como configurar este servidor MCP e integrá-lo com o GitHub Copilot no Visual Studio Code.

## 📑 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Ferramentas Disponíveis](#️-ferramentas-disponíveis)
- [📋 Pré-requisitos](#-pré-requisitos)
- [🚀 Instalação e Configuração](#-instalação-e-configuração)
- [🔐 Autenticação de Servidor MCP](#-autenticação-de-servidor-mcp)
- [💡 Exemplos de Uso](#-exemplos-de-uso)
- [🐳 Docker](#-docker)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🏗️ Arquitetura SOLID](#️-arquitetura-solid)
- [🔧 Solução de Problemas](#-solução-de-problemas)

## ✨ Funcionalidades

- 🔍 **Jira:** Buscar informações de issues (título e descrição).
- ✏️ **Jira:** Atualizar descrições, informações técnicas e planos de testes.
- 📢 **Discord:** Enviar mensagens para canais via Webhook.
- 🤖 **Integração nativa** com GitHub Copilot.
- 🐳 **Suporte completo** ao Docker.

## 🛠️ Ferramentas Disponíveis

### Ferramentas Jira
| Ferramenta | Descrição | Parâmetros |
|------------|-----------|------------|
| `hello` | Teste de conexão | `name` |
| `get_title_description_issue` | Buscar detalhes da issue | `key` |
| `update_infos_issue` | Atualizar campos técnicos | `key`, `info_tecnicas`, `desc_implementacao`, `plan_testes` |
| `update_description` | Atualizar descrição | `key`, `description` |

### Ferramentas Discord
| Ferramenta | Descrição | Parâmetros |
|------------|-----------|------------|
| `enviar_mensagem_discord` | Envia mensagem via webhook | `mensagem` |
| `outra_ferramenta` | Ferramenta de exemplo | `param` |

## 📋 Pré-requisitos

- Visual Studio Code (v1.102+)
- GitHub Copilot habilitado
- Docker e Docker Compose
- Conta Atlassian Jira Cloud
- Webhook do Discord (opcional)

## 🚀 Instalação e Configuração

### 1. Token de API do Jira

1. Aceda a [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Clique em **"Create API token"**.
3. Nomeie o token (ex: "MCP Server - VS Code").
4. **Copie e guarde o token com segurança**.

### 2. Configuração Rápida com Docker

```bash
# Clone o repositório
git clone [https://github.com/juliooidella/my-server-mcp.git](https://github.com/juliooidella/my-server-mcp.git)
cd my-server-mcp

# Configure as variáveis de ambiente
cp .env.example .env
````

Edite o ficheiro `.env` (certifique-se de usar `MCP_PROD_TOKEN`):

```env
# Credenciais do Jira
ATLASSIAN_USERNAME=seu_email@empresa.com
ATLASSIAN_API_TOKEN=seu_token_aqui
JIRA_URL=[https://sua-empresa.atlassian.net/](https://sua-empresa.atlassian.net/)

# Integração Discord (Opcional)
DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/](https://discord.com/api/webhooks/)...

# Segurança MCP (OBRIGATÓRIO)
MCP_PROD_TOKEN=seu_token_secreto_aqui_123456

# Configurações do Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8015
```

```bash
# Inicie o servidor
docker-compose up --build -d

# Verifique se está a funcionar
curl http://localhost:8015
```

### 3\. Configuração Alternativa (Python Local)

```bash
# Usando UV (recomendado)
uv sync
uv run app.py

# Ou usando Python tradicional
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

### 4\. Integração com VS Code

#### Opção A: Configuração Global

1.  Abra a **Command Palette** (`Ctrl+Shift+P`).
2.  Digite: **MCP: Add Server**.
3.  Configure:
      - **Server Name**: `jira-mcp`
      - **URL**: `http://localhost:8015`
      - **Scope**: Global

#### Opção B: Configuração por Workspace (`.vscode/mcp.json`)

```json
{
    "inputs": [
        {
            "type": "promptString",
            "id": "mcp-prod-token", 
            "description": "Insira o Token MCP (definido no .env como MCP_PROD_TOKEN)",
            "password": true
        }
    ],
    "servers": {
        "jira-mcp": {
            "type": "http",
            "url": "http://localhost:8015",
            "headers": {
                "Authorization": "Bearer ${input:mcp-prod-token}"
            }
        }
    }
}
```

### 5\. Iniciar e Verificar

1.  **Command Palette** → **MCP: List Servers**.
2.  Selecione **jira-mcp** → **Start Server**.
3.  No chat do Copilot, clique no ícone **Tools** (🔧).
4.  Verifique se as ferramentas do Jira e Discord aparecem.

## 🔐 Autenticação de Servidor MCP

Este projeto utiliza autenticação via Token Bearer. O token deve ser definido na variável de ambiente `MCP_PROD_TOKEN` no servidor. O cliente (VS Code) deve enviar este mesmo token no cabeçalho `Authorization`.

## 💡 Exemplos de Uso

### Jira

```
Busque os detalhes da issue PROJ-123
```

```
Atualize a issue PROJ-456 com:
- Informações técnicas: React 18 + TypeScript
- Implementação: Componentes funcionais com hooks
```

### Discord

```
Envie uma mensagem no Discord avisando que terminei a tarefa PROJ-123
```

## 🐳 Docker

### Executar em background

```bash
docker-compose up -d
```

### Ver logs

```bash
docker-compose logs -f jira-server
```

## 📁 Estrutura do Projeto

```
my-server-mcp/
├── app.py                  # Ponto de entrada
├── src/
│   ├── main.py            # Configuração do FastMCP e registo de ferramentas
│   ├── config/
│   │   └── settings.py    # Validação de variáveis de ambiente
│   ├── services/
│   │   ├── jira_service.py    # Lógica do Jira
│   │   └── discord_service.py # Lógica do Discord
│   └── tools/
│       ├── jira_tools.py      # Definições das ferramentas Jira
│       └── discord_tools.py   # Definições das ferramentas Discord
└── ...
```

## 🏗️ Arquitetura SOLID

O projeto foi estruturado seguindo os princípios SOLID, separando responsabilidades entre Configuração, Serviços e Ferramentas (Tools). Veja mais detalhes em [REFACTORING.md](https://www.google.com/search?q=REFACTORING.md).

## 🔧 Solução de Problemas

### Erro: "MCP\_PROD\_TOKEN não pode estar vazio"

Certifique-se de que definiu a variável `MCP_PROD_TOKEN` no seu ficheiro `.env` e não `MCP_AUTH_TOKEN`.

### Servidor não conecta

Verifique se o container Docker está a correr:

```bash
docker-compose ps
```

### Ferramentas não aparecem

1.  **Command Palette** → **MCP: Reset Cached Tools**
2.  **Command Palette** → **MCP: List Servers** → **Restart**

-----

**Desenvolvido para integração Jira + Discord + GitHub Copilot**

