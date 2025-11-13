# Configuração do Servidor MCP Jira com GitHub Copilot no VS Code

Este guia completo mostra como configurar e usar o servidor MCP Jira como ferramenta no Visual Studio Code com GitHub Copilot.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Criar Token de API do Jira](#criar-token-de-api-do-jira)
3. [Configurar o Servidor MCP](#configurar-o-servidor-mcp)
4. [Integrar com VS Code](#integrar-com-vs-code)
5. [Usar Ferramentas no Chat](#usar-ferramentas-no-chat)
6. [Solução de Problemas](#solução-de-problemas)

---

## Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ **Visual Studio Code** (versão 1.102 ou superior) - [Download](https://code.visualstudio.com/download)
- ✅ **GitHub Copilot** habilitado - [Configurar Copilot](/docs/copilot/setup.md)
- ✅ **Docker** e **Docker Compose** instalados
- ✅ Conta no **Atlassian Jira Cloud**

---

## Criar Token de API do Jira

### Passo 1: Acessar Configurações da Conta Atlassian

1. Acesse [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Faça login com sua conta Atlassian

### Passo 2: Criar Novo Token de API

1. Clique no botão **"Create API token"**

   ![Criar Token API](https://support.atlassian.com/cloud-administration/docs/manage-api-tokens-for-your-atlassian-account/)

2. Digite um nome descritivo para o token (ex: "MCP Server - VS Code")

3. Clique em **"Create"**

4. **IMPORTANTE**: Copie o token gerado imediatamente e guarde em local seguro
   - ⚠️ Você não poderá visualizar o token novamente após fechar a janela
   - 💡 Recomenda-se usar um gerenciador de senhas

### Passo 3: Identificar seu Nome de Usuário

Seu nome de usuário é o **endereço de e-mail** que você usa para fazer login no Jira.

**Exemplo:**
- Username: `joao.silva@empresa.com`
- URL do Jira: `https://sua-empresa.atlassian.net/`

---

## Configurar o Servidor MCP

### Opção 1: Executar com Docker (Recomendado)

#### 1. Clonar ou Baixar o Projeto

```bash
cd ~/projetos
git clone <repository-url> my-server-mcp
cd my-server-mcp
```

#### 2. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# Credenciais do Jira (OBRIGATÓRIO)
ATLASSIAN_USERNAME=seu_email@empresa.com
ATLASSIAN_API_TOKEN=seu_token_aqui

# URL da sua instância Jira
JIRA_URL=https://sua-empresa.atlassian.net/

# Configurações do Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8015
```

**⚠️ IMPORTANTE:**
- Substitua `seu_email@empresa.com` pelo seu email do Jira
- Substitua `seu_token_aqui` pelo token gerado no passo anterior
- Substitua `sua-empresa` pelo identificador da sua organização no Jira

#### 3. Iniciar o Servidor

```bash
# Build e iniciar em modo background
docker-compose up --build -d

# Verificar logs
docker-compose logs -f jira-server

# Parar o servidor
docker-compose down
```

#### 4. Verificar se o Servidor está Funcionando

```bash
# Testar conexão
curl http://localhost:8015

# Deve retornar informações sobre o servidor MCP
```

### Opção 2: Executar Localmente (Python)

#### 1. Instalar Dependências

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

#### 2. Configurar Variáveis de Ambiente

```bash
export ATLASSIAN_USERNAME="seu_email@empresa.com"
export ATLASSIAN_API_TOKEN="seu_token_aqui"
export JIRA_URL="https://sua-empresa.atlassian.net/"
```

#### 3. Executar o Servidor

```bash
python app.py
```

---

## Integrar com VS Code

### Passo 1: Habilitar Suporte a MCP no VS Code

1. Abra **VS Code**
2. Vá em **Settings** (`Ctrl+,` ou `Cmd+,`)
3. Procure por `chat.mcp.access`
4. Certifique-se de que está configurado como `all` (padrão)

### Passo 2: Adicionar o Servidor MCP ao VS Code

Você tem **duas opções** para adicionar o servidor:

#### Opção A: Configuração Global (Disponível em todos os projetos)

1. Abra o **Command Palette** (`Ctrl+Shift+P` ou `Cmd+Shift+P`)
2. Digite e selecione: **MCP: Add Server**
3. Escolha o tipo: **HTTP**
4. Configure os campos:
   - **Server Name**: `jira-mcp`
   - **URL**: `http://localhost:8015`
5. Selecione **Global** para adicionar à configuração de usuário

#### Opção B: Configuração por Workspace (Específico do projeto)

1. No seu projeto, crie o arquivo `.vscode/mcp.json`
2. Adicione a seguinte configuração:

```json
{
    "servers": {
        "jira-mcp": {
            "type": "http",
            "url": "http://localhost:8015"
        }
    }
}
```

**💡 Dica**: Use a configuração global se quiser usar o servidor em múltiplos projetos. Use a configuração por workspace para compartilhar com a equipe via Git.

### Passo 3: Confiar no Servidor MCP

Na primeira vez que iniciar o servidor:

1. VS Code mostrará um diálogo pedindo para **confirmar que você confia no servidor**
2. Clique em **Trust** para permitir que o servidor seja executado

![MCP Trust Dialog](https://code.visualstudio.com/assets/docs/copilot/mcp-servers/mcp-server-trust-dialog.png)

### Passo 4: Iniciar o Servidor MCP

1. Abra o **Command Palette** (`Ctrl+Shift+P`)
2. Digite: **MCP: List Servers**
3. Selecione **jira-mcp**
4. Clique em **Start Server**

Alternativamente, o servidor pode iniciar automaticamente se você habilitar:
- **Settings** → `chat.mcp.autostart` → `true` (Experimental)

### Passo 5: Verificar se o Servidor está Conectado

1. Abra a **Chat View** do Copilot (`Ctrl+Alt+I` ou ícone de chat)
2. Clique no ícone **Tools** (🔧) no canto superior direito
3. Você deve ver as ferramentas do Jira listadas:
   - `jira-mcp.hello`
   - `jira-mcp.get_title_description_issue`
   - `jira-mcp.update_infos_issue`
   - `jira-mcp.update_description`

![Tools Picker](https://code.visualstudio.com/assets/docs/copilot/mcp-servers/agent-mode-select-tools.png)

---

## Usar Ferramentas no Chat

### Modo Agente (Automático)

No modo agente, o Copilot invoca automaticamente as ferramentas conforme necessário:

1. Abra o **Chat** (`Ctrl+Alt+I`)
2. Certifique-se de estar em **Agent Mode** (ícone de varinha mágica ativo)
3. Digite sua pergunta naturalmente:

**Exemplos:**

```
Busque as informações da issue PROJ-123
```

```
Atualize a descrição da issue PROJ-456 com as informações que discutimos
```

```
Quais são os detalhes técnicos da tarefa DEV-789?
```

O Copilot automaticamente:
- Identifica a ferramenta necessária
- Solicita aprovação (se configurado)
- Executa a ferramenta
- Apresenta os resultados

### Invocar Ferramentas Explicitamente

Você pode referenciar ferramentas diretamente usando `#`:

1. No chat, digite `#`
2. Selecione a ferramenta desejada da lista
3. Forneça os parâmetros necessários

**Exemplo:**

```
#jira-mcp.get_title_description_issue key:PROJ-123
```

### Aprovar Invocações de Ferramentas

Quando uma ferramenta é invocada pela primeira vez, o VS Code pode pedir aprovação:

![Tool Confirmation](https://code.visualstudio.com/assets/docs/copilot/mcp-servers/mcp-tool-confirmation.png)

Você pode configurar o comportamento de aprovação em:
- **Settings** → `chat.tools.confirmationBehavior`

---

## Ferramentas Disponíveis

### 1. `hello`

Retorna uma saudação simples (útil para testar a conexão).

**Exemplo:**
```
#jira-mcp.hello name:João
```

**Resposta:**
```
Hello, João!
```

---

### 2. `get_title_description_issue`

Busca título e descrição de uma issue do Jira.

**Parâmetros:**
- `key` (string): Chave da issue (ex: PROJ-123)

**Exemplo:**
```
Busque os detalhes da issue PROJ-123
```

ou

```
#jira-mcp.get_title_description_issue key:PROJ-123
```

**Resposta:**
```
Título: Implementar autenticação OAuth2

Descrição da tarefa: Adicionar suporte para autenticação OAuth2 
no sistema, permitindo login via Google e Microsoft.
```

---

### 3. `update_infos_issue`

Atualiza campos customizados da issue (informações técnicas, descrição da implementação e plano de testes).

**Parâmetros:**
- `key` (string): Chave da issue
- `info_tecnicas` (string): Informações técnicas
- `desc_implementacao` (string): Descrição da implementação
- `plan_testes` (string): Plano de testes

**Exemplo:**
```
Atualize a issue PROJ-123 com:
- Informações técnicas: Usar biblioteca oauth2-client v3.5
- Implementação: Criar endpoints /auth/google e /auth/microsoft
- Testes: Testar com contas de teste de ambas plataformas
```

**Resposta:**
```
Issue PROJ-123 atualizada com sucesso!
```

---

### 4. `update_description`

Atualiza apenas a descrição da issue.

**Parâmetros:**
- `key` (string): Chave da issue
- `description` (string): Nova descrição

**Exemplo:**
```
Atualize a descrição da issue PROJ-456 para incluir os 
requisitos de segurança discutidos na reunião
```

**Resposta:**
```
Issue PROJ-456 atualizada com sucesso!
```

---

## Gerenciar Ferramentas

### Visualizar Ferramentas Disponíveis

1. Abra o **Chat View**
2. Clique no ícone **Tools** (🔧)
3. Veja todas as ferramentas disponíveis e seu status

### Habilitar/Desabilitar Ferramentas

No **Tools Picker**, você pode:
- ✅ Marcar/desmarcar ferramentas individuais
- 🔧 Habilitar/desabilitar servidores inteiros
- 📋 Criar conjuntos de ferramentas personalizados

### Criar Tool Sets (Conjuntos de Ferramentas)

Para agrupar ferramentas relacionadas:

1. Abra **Command Palette**
2. Digite: **Chat: Create Tool Set**
3. Selecione as ferramentas do Jira
4. Nomeie o conjunto (ex: "Jira Tasks")

Agora você pode habilitar/desabilitar todo o conjunto de uma vez!

---

## Solução de Problemas

### Problema: Servidor não conecta

**Sintomas:**
- Ferramentas não aparecem no Tools Picker
- Erro ao tentar usar ferramentas do Jira

**Soluções:**

1. **Verificar se o servidor está rodando:**
   ```bash
   docker-compose ps
   # ou
   curl http://localhost:8015
   ```

2. **Verificar logs do servidor:**
   ```bash
   docker-compose logs -f jira-server
   ```

3. **Reiniciar o servidor:**
   ```bash
   docker-compose restart
   ```

4. **Reiniciar o servidor MCP no VS Code:**
   - Command Palette → **MCP: List Servers**
   - Selecione `jira-mcp` → **Restart Server**

---

### Problema: Erro de autenticação no Jira

**Sintomas:**
- Erro: "401 Unauthorized"
- Mensagem sobre credenciais inválidas

**Soluções:**

1. **Verificar credenciais no `.env`:**
   - Username correto (email completo)
   - Token de API válido e ativo
   - URL do Jira correta

2. **Regenerar token de API:**
   - Acesse [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
   - Revogue o token antigo
   - Crie um novo token
   - Atualize o `.env`
   - Reinicie o servidor

3. **Testar credenciais manualmente:**
   ```bash
   curl -u "seu_email@empresa.com:seu_token" \
        https://sua-empresa.atlassian.net/rest/api/3/myself
   ```

---

### Problema: "Cannot have more than 128 tools"

**Sintomas:**
- Erro ao iniciar chat com muitas ferramentas ativas

**Solução:**

1. Abra o **Tools Picker** no Chat View
2. Desabilite ferramentas ou servidores que não está usando
3. Ou habilite **Virtual Tools** em Settings:
   - `github.copilot.chat.virtualTools.threshold` → `true`

---

### Problema: Ferramentas não aparecem após atualização

**Solução:**

1. Limpar cache de ferramentas:
   - Command Palette → **MCP: Reset Cached Tools**

2. Reiniciar o servidor MCP:
   - Command Palette → **MCP: List Servers** → **Restart**

---

### Verificar Logs do MCP no VS Code

1. Command Palette → **MCP: List Servers**
2. Selecione `jira-mcp`
3. Clique em **Show Output**

Ou acesse diretamente:
- **View** → **Output** → Selecione **MCP** no dropdown

---

## Configurações Avançadas

### Adicionar Autenticação (Headers)

Se seu servidor MCP requer autenticação adicional:

```json
{
    "inputs": [
        {
            "type": "promptString",
            "id": "jira-api-token",
            "description": "Jira API Token",
            "password": true
        }
    ],
    "servers": {
        "jira-mcp": {
            "type": "http",
            "url": "http://localhost:8015",
            "headers": {
                "Authorization": "Bearer ${input:jira-api-token}"
            }
        }
    }
}
```

### Usar em Dev Container

Adicione ao `.devcontainer/devcontainer.json`:

```json
{
    "name": "Meu Projeto",
    "image": "mcr.microsoft.com/devcontainers/typescript-node:latest",
    "customizations": {
        "vscode": {
            "mcp": {
                "servers": {
                    "jira-mcp": {
                        "type": "http",
                        "url": "http://localhost:8015"
                    }
                }
            }
        }
    }
}
```

### Sincronizar entre Dispositivos

Habilite **Settings Sync**:

1. Command Palette → **Settings Sync: Configure**
2. Certifique-se de que **MCP Servers** está marcado
3. Suas configurações de MCP serão sincronizadas entre dispositivos

---

## Recursos Adicionais

- 📖 [Documentação Oficial MCP](https://modelcontextprotocol.io/)
- 🔧 [Repositório de Servidores MCP](https://github.com/modelcontextprotocol/servers)
- 💬 [GitHub Copilot no VS Code](/docs/copilot/chat/copilot-chat.md)
- 🛠️ [Usando Ferramentas no Chat](/docs/copilot/chat/chat-tools.md)

---

## Exemplos de Uso Prático

### Exemplo 1: Revisar Issue antes de começar tarefa

```
Copilot, busque os detalhes da issue PROJ-123 e me dê um resumo 
do que precisa ser feito
```

### Exemplo 2: Atualizar issue após implementação

```
Acabei de implementar a funcionalidade OAuth2 para a issue PROJ-123.
Atualize os campos técnicos com:
- Tecnologia: oauth2-client v3.5 + Passport.js
- Implementação: Endpoints /auth/google e /auth/microsoft criados
- Testes: Testes unitários e integração incluídos
```

### Exemplo 3: Buscar múltiplas issues

```
Liste os detalhes das issues PROJ-123, PROJ-124 e PROJ-125
```

### Exemplo 4: Workflow completo

```
1. Busque PROJ-123
2. Com base nos requisitos, me sugira uma arquitetura de solução
3. Depois que eu implementar, atualize a issue com os detalhes técnicos
```

---

## Segurança

⚠️ **IMPORTANTE - Boas Práticas de Segurança:**

1. **Nunca commite credenciais:**
   - Adicione `.env` ao `.gitignore`
   - Use `.env.example` apenas com placeholders

2. **Rotacione tokens periodicamente:**
   - Crie novos tokens a cada 90 dias
   - Revogue tokens antigos

3. **Use permissões mínimas:**
   - O token deve ter apenas as permissões necessárias no Jira

4. **Confie apenas em servidores conhecidos:**
   - Revise a configuração antes de confiar em um servidor MCP

5. **Use HTTPS em produção:**
   - Para servidores remotos, sempre use HTTPS

---

## Suporte

Se encontrar problemas:

1. ✅ Verifique os logs do servidor (`docker-compose logs`)
2. ✅ Verifique os logs do MCP no VS Code (Output → MCP)
3. ✅ Consulte a seção [Solução de Problemas](#solução-de-problemas)
4. ✅ Revise a [documentação oficial do MCP](https://modelcontextprotocol.io/)

---

**Última atualização:** 11 de novembro de 2025
