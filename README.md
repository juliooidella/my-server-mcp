# 🚀 MCP Jira Server

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://docker.com)

Um servidor MCP (Model Context Protocol) para integração com Jira Cloud através do GitHub Copilot no VS Code.

> 📘 **[Guia Completo de Configuração com VS Code + GitHub Copilot](CONFIGURACAO_MCP.md)**  
> Aprenda como configurar este servidor MCP e integrá-lo com o GitHub Copilot no Visual Studio Code.

## 📑 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Ferramentas Disponíveis](#️-ferramentas-disponíveis)
- [📋 Pré-requisitos](#-pré-requisitos)
- [🚀 Instalação e Configuração](#-instalação-e-configuração)
- [� Autenticação de Servidor MCP](#-autenticação-de-servidor-mcp)
- [�💡 Exemplos de Uso](#-exemplos-de-uso)
- [🐳 Docker](#-docker)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🏗️ Arquitetura SOLID](#️-arquitetura-solid)
- [🔧 Configurando Novas Ferramentas MCP](#-configurando-novas-ferramentas-mcp)
- [🔧 Solução de Problemas](#-solução-de-problemas)
- [🔒 Segurança](#-segurança)
- [📖 Documentação Adicional](#-documentação-adicional)

## ✨ Funcionalidades

- 🔍 **Buscar informações** de issues do Jira
- ✏️ **Atualizar descrições** e campos customizados
- 🤖 **Integração nativa** com GitHub Copilot
- 🐳 **Suporte completo** ao Docker
- ⚡ **Interface simples** via chat do Copilot

## 🛠️ Ferramentas Disponíveis

| Ferramenta | Descrição | Parâmetros |
|------------|-----------|------------|
| `hello` | Teste de conexão | `name` |
| `get_title_description_issue` | Buscar detalhes da issue | `key` |
| `update_infos_issue` | Atualizar campos técnicos | `key`, `info_tecnicas`, `desc_implementacao`, `plan_testes` |
| `update_description` | Atualizar descrição | `key`, `description` |

## 📋 Pré-requisitos

- Visual Studio Code (v1.102+)
- GitHub Copilot habilitado
- Docker e Docker Compose
- Conta Atlassian Jira Cloud

## 🚀 Instalação e Configuração

### 1. Token de API do Jira

1. Acesse [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Clique em **"Create API token"**
3. Nomeie o token (ex: "MCP Server - VS Code")
4. **Copie e guarde o token com segurança**

### 2. Configuração Rápida com Docker

```bash
# Clone o repositório
git clone https://github.com/juliooidella/my-server-mcp.git
cd my-server-mcp

# Configure as variáveis de ambiente
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Credenciais do Jira
ATLASSIAN_USERNAME=seu_email@empresa.com
ATLASSIAN_API_TOKEN=seu_token_aqui
JIRA_URL=https://sua-empresa.atlassian.net/

# Configurações do Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8015
```

```bash
# Inicie o servidor
docker-compose up --build -d

# Verifique se está funcionando
curl http://localhost:8015
```

### 3. Configuração Alternativa (Python Local)

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

### 4. Integração com VS Code

#### Opção A: Configuração Global

1. Abra o **Command Palette** (`Ctrl+Shift+P`)
2. Digite: **MCP: Add Server**
3. Configure:
   - **Server Name**: `jira-mcp`
   - **URL**: `http://localhost:8015`
   - **Scope**: Global

#### Opção B: Configuração por Workspace

Crie `.vscode/mcp.json`:

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

### 5. Iniciar e Verificar

1. **Command Palette** → **MCP: List Servers**
2. Selecione **jira-mcp** → **Start Server**
3. No chat do Copilot, clique no ícone **Tools** (🔧)
4. Verifique se as ferramentas do Jira aparecem

## 🔐 Autenticação de Servidor MCP

### Por que Autenticação é Importante?

A autenticação em servidores MCP é **crucial** para:

- **🛡️ Segurança**: Previne acesso não autorizado às suas ferramentas e dados
- **🔒 Controle de Acesso**: Define quem pode usar quais funcionalidades
- **📊 Auditoria**: Rastreia quem está fazendo o quê em seus sistemas
- **🌐 Ambiente Produtivo**: Protege APIs e recursos empresariais
- **⚠️ Prevenção de Abusos**: Evita uso malicioso ou excessivo do servidor

### 🔧 Como Funciona no Projeto

Este projeto implementa autenticação por **Token Bearer** usando `StaticTokenVerifier`:

```python
# src/main.py
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

# Token de autenticação (em produção, use variável de ambiente!)
token_secreto = "d41d8cd98f00b204e9800998ecf8427e"

# Configurar autenticação
auth_verifier = StaticTokenVerifier(
    tokens={
        token_secreto: {
            "client_id": "admin_user",  # Identificador do usuário
            "scopes": ["admin"]         # Permissões (opcional)
        }
    }
)

# Aplicar ao servidor MCP
mcp = FastMCP("MyServer", auth=auth_verifier)
```

### 🔗 Configuração no GitHub Copilot

#### Com Autenticação (Recomendado para Produção)

Crie `.vscode/mcp.json` **com headers de autenticação**:

```json
{
    "servers": {
        "jira-mcp": {
            "description": "Servidor MCP JIRA com autenticação",
            "url": "http://localhost:8015/mcp",
            "type": "http",
            "headers": {
                "Authorization": "Bearer d41d8cd98f00b204e9800998ecf8427e"
            }
        }
    }
}
```

#### Sem Autenticação (Apenas Desenvolvimento Local)

```json
{
    "servers": {
        "jira-mcp": {
            "description": "Servidor MCP JIRA local",
            "url": "http://localhost:8015/mcp",
            "type": "http"
        }
    }
}
```

### 🔒 Configuração Segura para Produção

#### 1. **Use Variáveis de Ambiente**

```python
import os

# ❌ NUNCA hardcode tokens no código
token_secreto = "d41d8cd98f00b204e9800998ecf8427e"

# ✅ Use variáveis de ambiente
token_secreto = os.getenv("MCP_AUTH_TOKEN", "fallback-token")
```

#### 2. **Configure no `.env`**

```env
# Token de autenticação MCP
MCP_AUTH_TOKEN=seu_token_super_secreto_aqui_123456
```

#### 3. **Use Tokens Seguros**

```python
import secrets

# Gerar token seguro
token_seguro = secrets.token_urlsafe(32)
print(f"Novo token: {token_seguro}")
```

### 🌍 Configurações por Ambiente

#### Desenvolvimento Local
```json
{
    "servers": {
        "jira-mcp-dev": {
            "url": "http://localhost:8015/mcp",
            "type": "http"
            // Sem autenticação para facilitar desenvolvimento
        }
    }
}
```

#### Produção/Compartilhado
```json
{
    "servers": {
        "jira-mcp-prod": {
            "url": "https://mcp.empresa.com/mcp",
            "type": "http",
            "headers": {
                "Authorization": "Bearer ${env:MCP_PROD_TOKEN}"
            }
        }
    }
}
```

### 🔐 Tipos de Autenticação Disponíveis

O FastMCP suporta diferentes métodos de autenticação:

#### 1. **Static Token (Usado no projeto)**
```python
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

auth = StaticTokenVerifier(tokens={"token123": {"user": "admin"}})
```

#### 2. **JWT Tokens**
```python
from fastmcp.server.auth.providers.jwt import JWTVerifier

auth = JWTVerifier(
    secret_key="sua-chave-secreta",
    algorithm="HS256"
)
```

#### 3. **API Key**
```python
from fastmcp.server.auth.providers.apikey import APIKeyVerifier

auth = APIKeyVerifier(
    api_keys={"api_key_123": {"client": "app1"}}
)
```

### 🛡️ Melhores Práticas de Segurança

1. **✅ Use HTTPS em produção**
   ```json
   {
       "servers": {
           "jira-mcp": {
               "url": "https://mcp.empresa.com/mcp",
               "type": "http"
           }
       }
   }
   ```

2. **✅ Rotacione tokens regularmente**
   ```bash
   # Gerar novo token a cada 90 dias
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **✅ Use variáveis de ambiente**
   ```json
   {
       "servers": {
           "jira-mcp": {
               "url": "http://localhost:8015/mcp",
               "headers": {
                   "Authorization": "Bearer ${env:MCP_TOKEN}"
               }
           }
       }
   }
   ```

4. **✅ Configure diferentes tokens por ambiente**
   - **Desenvolvimento**: Token simples ou sem autenticação
   - **Teste**: Token de teste com permissões limitadas  
   - **Produção**: Token forte com auditoria completa

5. **✅ Monitore acessos**
   ```python
   import logging
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   # Log de autenticação
   logger.info(f"Usuário {client_id} acessou ferramenta {tool_name}")
   ```

### 📚 Recursos Adicionais

- **[FastMCP Auth Docs](https://gofastmcp.com/servers/auth/authentication)** - Documentação completa
- **[JWT.io](https://jwt.io/)** - Para validar e debugar tokens JWT
- **[Python Secrets](https://docs.python.org/3/library/secrets.html)** - Geração segura de tokens

## 💡 Exemplos de Uso

### Buscar informações de uma issue

```
Busque os detalhes da issue PROJ-123
```

### Atualizar campos técnicos

```
Atualize a issue PROJ-456 com:
- Informações técnicas: React 18 + TypeScript
- Implementação: Componentes funcionais com hooks
- Testes: Jest + Testing Library
```

### Atualizar apenas a descrição

```
Atualize a descrição da issue DEV-789 para incluir 
os novos requisitos discutidos na reunião
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

### Parar o servidor

```bash
docker-compose down
```

## 📁 Estrutura do Projeto

```
my-server-mcp/
├── app.py                  # Ponto de entrada
├── docker-compose.yml     # Configuração Docker
├── Dockerfile             # Imagem Docker
├── requirements.txt       # Dependências Python
├── pyproject.toml         # Configuração UV/Python
├── .env.example           # Exemplo de variáveis
├── src/
│   ├── main.py            # Servidor MCP principal
│   ├── config/
│   │   └── settings.py    # Configurações
│   ├── services/
│   │   └── jira_service.py # Lógica do Jira
│   └── tools/
│       └── jira_tools.py   # Definições das ferramentas
└── docs/                  # Documentação
```

## 🏗️ Arquitetura SOLID

O projeto foi estruturado seguindo os princípios SOLID:

- **Single Responsibility**: Cada módulo tem uma única responsabilidade
- **Open/Closed**: Extensível sem modificar código existente
- **Liskov Substitution**: Componentes substituíveis por mocks
- **Interface Segregation**: Interfaces enxutas e focadas
- **Dependency Inversion**: Dependências injetadas

Veja mais detalhes em [REFACTORING.md](REFACTORING.md).

## 🔧 Configurando Novas Ferramentas MCP

O servidor MCP é altamente extensível! Você pode facilmente adicionar novas ferramentas para integrar com diferentes APIs, bancos de dados, bibliotecas Python e muito mais.

### 🛠️ O que é Possível Implementar

- **🌐 APIs REST/GraphQL** - Integração com qualquer API web
- **🗄️ Bancos de Dados** - PostgreSQL, MySQL, MongoDB, Redis
- **☁️ Serviços Cloud** - AWS, Azure, GCP, Firebase
- **📊 Análise de Dados** - Pandas, NumPy, Matplotlib
- **🤖 IA/ML** - OpenAI, Anthropic, HuggingFace, scikit-learn
- **📧 Comunicação** - Email, Slack, Discord, Teams
- **📋 Gestão** - GitHub, GitLab, Trello, Notion
- **🔐 Autenticação** - OAuth, JWT, LDAP
- **📁 Arquivos** - Google Drive, Dropbox, S3
- **🚀 DevOps** - Docker, Kubernetes, CI/CD

### 🏗️ Estrutura de uma Nova Ferramenta

#### 1. Definir a Ferramenta (`src/tools/nova_tool.py`)

```python
from fastmcp import Tool
from typing import Dict, Any

# Definir parâmetros da ferramenta
def nova_ferramenta_tool() -> Tool:
    return Tool(
        name="nova_ferramenta",
        description="Descrição do que a ferramenta faz",
        parameters={
            "param1": {
                "type": "string",
                "description": "Descrição do parâmetro",
                "required": True
            },
            "param2": {
                "type": "integer", 
                "description": "Parâmetro opcional",
                "required": False,
                "default": 10
            }
        }
    )

# Implementar a lógica da ferramenta
async def nova_ferramenta_handler(arguments: Dict[str, Any]) -> str:
    param1 = arguments.get("param1")
    param2 = arguments.get("param2", 10)
    
    try:
        # Sua lógica aqui
        resultado = await processar_dados(param1, param2)
        return f"Resultado: {resultado}"
    except Exception as e:
        return f"Erro: {str(e)}"
```

#### 2. Criar o Serviço (`src/services/nova_service.py`)

```python
import httpx
import asyncpg
from typing import Optional, List, Dict, Any

class NovaService:
    def __init__(self, api_key: str, database_url: Optional[str] = None):
        self.api_key = api_key
        self.database_url = database_url
        self._client = httpx.AsyncClient()
        
    async def chamar_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Exemplo de chamada de API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = await self._client.post(
            f"https://api.exemplo.com/{endpoint}",
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    async def consultar_banco(self, query: str) -> List[Dict[str, Any]]:
        """Exemplo de consulta ao banco de dados"""
        if not self.database_url:
            raise ValueError("URL do banco não configurada")
            
        conn = await asyncpg.connect(self.database_url)
        try:
            rows = await conn.fetch(query)
            return [dict(row) for row in rows]
        finally:
            await conn.close()
    
    async def processar_dados(self, dados: List[Dict]) -> Dict[str, Any]:
        """Exemplo usando bibliotecas Python"""
        import pandas as pd
        import numpy as np
        
        df = pd.DataFrame(dados)
        resultado = {
            "total": len(df),
            "media": np.mean(df.select_dtypes(include=[np.number])).to_dict(),
            "resumo": df.describe().to_dict()
        }
        return resultado
```

#### 3. Registrar no Servidor Principal (`src/main.py`)

```python
from fastmcp import FastMCP
from src.tools.nova_tool import nova_ferramenta_tool, nova_ferramenta_handler
from src.services.nova_service import NovaService

# Inicializar servidor MCP
mcp = FastMCP("MCP Server")

# Configurar serviço
nova_service = NovaService(
    api_key=os.getenv("NOVA_API_KEY"),
    database_url=os.getenv("DATABASE_URL")
)

# Registrar ferramenta
mcp.add_tool(
    nova_ferramenta_tool(),
    nova_ferramenta_handler
)
```

### 📚 Exemplos Práticos de Ferramentas

#### Exemplo 1: Integração com OpenAI

```python
import openai
from fastmcp import Tool

def openai_tool() -> Tool:
    return Tool(
        name="gerar_texto_ai",
        description="Gera texto usando OpenAI GPT",
        parameters={
            "prompt": {"type": "string", "required": True},
            "max_tokens": {"type": "integer", "required": False, "default": 100}
        }
    )

async def openai_handler(arguments: Dict[str, Any]) -> str:
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": arguments["prompt"]}],
        max_tokens=arguments.get("max_tokens", 100)
    )
    
    return response.choices[0].message.content
```

#### Exemplo 2: Consulta em Banco PostgreSQL

```python
import asyncpg

def postgres_tool() -> Tool:
    return Tool(
        name="consultar_usuarios",
        description="Consulta usuários no banco PostgreSQL",
        parameters={
            "filtro": {"type": "string", "required": False},
            "limite": {"type": "integer", "required": False, "default": 10}
        }
    )

async def postgres_handler(arguments: Dict[str, Any]) -> str:
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    
    query = "SELECT * FROM usuarios"
    params = []
    
    if filtro := arguments.get("filtro"):
        query += " WHERE nome ILIKE $1"
        params.append(f"%{filtro}%")
    
    query += f" LIMIT {arguments.get('limite', 10)}"
    
    try:
        rows = await conn.fetch(query, *params)
        resultado = [dict(row) for row in rows]
        return f"Encontrados {len(resultado)} usuários: {resultado}"
    finally:
        await conn.close()
```

#### Exemplo 3: Análise de Dados com Pandas

```python
import pandas as pd
import io

def analise_dados_tool() -> Tool:
    return Tool(
        name="analisar_csv",
        description="Analisa dados de um arquivo CSV",
        parameters={
            "dados_csv": {"type": "string", "required": True},
            "colunas": {"type": "array", "required": False}
        }
    )

async def analise_dados_handler(arguments: Dict[str, Any]) -> str:
    dados_csv = arguments["dados_csv"]
    colunas = arguments.get("colunas")
    
    # Ler CSV do string
    df = pd.read_csv(io.StringIO(dados_csv))
    
    if colunas:
        df = df[colunas]
    
    analise = {
        "linhas": len(df),
        "colunas": list(df.columns),
        "estatisticas": df.describe().to_dict(),
        "valores_nulos": df.isnull().sum().to_dict(),
        "tipos": df.dtypes.to_dict()
    }
    
    return f"Análise completa:\n{analise}"
```

#### Exemplo 4: Integração com Slack

```python
import httpx

def slack_tool() -> Tool:
    return Tool(
        name="enviar_slack",
        description="Envia mensagem para o Slack",
        parameters={
            "canal": {"type": "string", "required": True},
            "mensagem": {"type": "string", "required": True},
            "usuario": {"type": "string", "required": False}
        }
    )

async def slack_handler(arguments: Dict[str, Any]) -> str:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    payload = {
        "channel": arguments["canal"],
        "text": arguments["mensagem"],
        "username": arguments.get("usuario", "MCP Bot")
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(webhook_url, json=payload)
        
    if response.status_code == 200:
        return "Mensagem enviada com sucesso!"
    else:
        return f"Erro ao enviar: {response.text}"
```

### 🔧 Configuração de Dependências

#### 1. Adicionar no `requirements.txt`

```txt
# Banco de dados
asyncpg==0.29.0
sqlalchemy==2.0.23
redis==5.0.1

# APIs e HTTP
httpx==0.25.2
aiohttp==3.9.1

# IA/ML
openai==1.3.8
anthropic==0.7.8
transformers==4.36.2
torch==2.1.2

# Análise de dados
pandas==2.1.4
numpy==1.25.2
matplotlib==3.8.2
plotly==5.17.0

# Cloud services
boto3==1.34.0  # AWS
azure-storage-blob==12.19.0  # Azure
google-cloud-storage==2.10.0  # GCP

# Comunicação
slack-sdk==3.26.1
discord.py==2.3.2
```

#### 2. Configurar variáveis de ambiente (`.env`)

```env
# APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=ant-...
SLACK_WEBHOOK_URL=https://hooks.slack.com/...

# Bancos de dados
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0

# Cloud
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AZURE_STORAGE_CONNECTION_STRING=...
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### 🚀 Exemplo Completo: Ferramenta de Weather API

```python
# src/tools/weather_tool.py
from fastmcp import Tool
import httpx
from typing import Dict, Any

def weather_tool() -> Tool:
    return Tool(
        name="consultar_clima",
        description="Consulta o clima atual de uma cidade",
        parameters={
            "cidade": {"type": "string", "required": True},
            "pais": {"type": "string", "required": False, "default": "BR"},
            "unidade": {"type": "string", "required": False, "default": "metric"}
        }
    )

async def weather_handler(arguments: Dict[str, Any]) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    cidade = arguments["cidade"]
    pais = arguments.get("pais", "BR")
    unidade = arguments.get("unidade", "metric")
    
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{cidade},{pais}",
        "appid": api_key,
        "units": unidade,
        "lang": "pt_br"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
        if response.status_code != 200:
            return f"Erro ao consultar clima: {response.text}"
        
        data = response.json()
        
        clima = {
            "cidade": data["name"],
            "temperatura": data["main"]["temp"],
            "sensacao": data["main"]["feels_like"],
            "umidade": data["main"]["humidity"],
            "descricao": data["weather"][0]["description"],
            "vento": data["wind"]["speed"]
        }
        
        return f"""🌤️ Clima em {clima['cidade']}:
        🌡️ Temperatura: {clima['temperatura']}°C (sensação: {clima['sensacao']}°C)
        💧 Umidade: {clima['umidade']}%
        💨 Vento: {clima['vento']} m/s
        ☁️ Condição: {clima['descricao']}"""
```

### 💡 Dicas Avançadas

#### 1. **Validação de Entrada**

```python
from pydantic import BaseModel, validator

class WeatherParams(BaseModel):
    cidade: str
    pais: str = "BR"
    unidade: str = "metric"
    
    @validator('unidade')
    def validate_unidade(cls, v):
        if v not in ['metric', 'imperial', 'kelvin']:
            raise ValueError('Unidade deve ser: metric, imperial ou kelvin')
        return v
```

#### 2. **Cache e Performance**

```python
import asyncio
from functools import lru_cache
import redis.asyncio as redis

# Cache em memória
@lru_cache(maxsize=100)
def cache_simples(key: str) -> str:
    return expensive_operation(key)

# Cache Redis
async def cache_redis(key: str, ttl: int = 3600):
    r = redis.from_url(os.getenv("REDIS_URL"))
    cached = await r.get(key)
    if cached:
        return cached.decode()
    
    result = await expensive_async_operation(key)
    await r.setex(key, ttl, result)
    return result
```

#### 3. **Tratamento de Erros Robusto**

```python
import logging
from functools import wraps

def handle_errors(func):
    @wraps(func)
    async def wrapper(arguments: Dict[str, Any]) -> str:
        try:
            return await func(arguments)
        except httpx.HTTPError as e:
            logging.error(f"Erro HTTP: {e}")
            return f"Erro de conexão: {e}"
        except ValueError as e:
            logging.error(f"Erro de validação: {e}")
            return f"Parâmetros inválidos: {e}"
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return f"Erro interno: {e}"
    return wrapper

@handle_errors
async def minha_ferramenta_handler(arguments: Dict[str, Any]) -> str:
    # Sua lógica aqui
    pass
```

### 📖 Recursos Úteis

- **[FastMCP Docs](https://github.com/jlowin/fastmcp)** - Framework usado
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - Especificação oficial
- **[httpx](https://www.python-httpx.org/)** - Cliente HTTP async
- **[asyncpg](https://magicstack.github.io/asyncpg/)** - PostgreSQL async
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados

Agora você pode criar ferramentas poderosas para praticamente qualquer integração que imaginar! 🚀

## 🔧 Solução de Problemas

### Servidor não conecta

```bash
# Verificar status
docker-compose ps

# Ver logs
docker-compose logs jira-server

# Reiniciar
docker-compose restart
```

### Erro de autenticação (401)

1. Verificar credenciais no `.env`
2. Regenerar token de API no Jira
3. Testar credenciais:

```bash
curl -u "email:token" \
     https://sua-empresa.atlassian.net/rest/api/3/myself
```

### Ferramentas não aparecem

1. **Command Palette** → **MCP: Reset Cached Tools**
2. **Command Palette** → **MCP: List Servers** → **Restart**

## 🔒 Segurança

⚠️ **Boas Práticas:**

- ✅ Nunca commite o arquivo `.env`
- ✅ Rotacione tokens a cada 90 dias
- ✅ Use permissões mínimas no Jira
- ✅ Revogue tokens antigos ao criar novos

## 🧪 Testes

```bash
# Testar conexão com servidor
curl http://localhost:8015

# Verificar logs
docker-compose logs -f jira-server
```

## 📖 Documentação Adicional

- [Configuração Completa](CONFIGURACAO_MCP.md) - Guia detalhado passo a passo
- [Refactoring SOLID](REFACTORING.md) - Detalhes da arquitetura
- [Documentação MCP](https://modelcontextprotocol.io/) - Protocolo oficial
- [GitHub Copilot Chat](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide) - Como usar o chat

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -am 'Add nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Encontrou algum problema? 

- 📝 [Abra uma issue](https://github.com/juliooidella/my-server-mcp/issues)
- 📧 Entre em contato: julio.oidella@exemplo.com

---

**Desenvolvido com ❤️ para integração Jira + GitHub Copilot**