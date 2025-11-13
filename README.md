# Jira MCP Server

Servidor MCP (Model Context Protocol) para integração com Jira, desenvolvido seguindo os princípios SOLID.

> 📘 **[Guia Completo de Configuração com VS Code + GitHub Copilot](CONFIGURACAO_MCP.md)**  
> Aprenda como configurar este servidor MCP e integrá-lo com o GitHub Copilot no Visual Studio Code.

## 🏗️ Arquitetura

O projeto foi estruturado seguindo os princípios SOLID para melhor manutenibilidade e testabilidade:

```
src/
├── config/           # Gerenciamento de configurações
│   └── settings.py
├── services/         # Lógica de negócio
│   └── jira_service.py
├── tools/           # Ferramentas MCP
│   └── jira_tools.py
└── main.py          # Ponto de entrada
```

## 🚀 Quick Start

### 1. Obter Credenciais do Jira

Você precisará criar um **API Token** no Jira:

1. Acesse [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Clique em **"Create API token"**
3. Dê um nome (ex: "MCP Server")
4. Copie o token gerado (⚠️ não será mostrado novamente!)

> 📘 Para instruções detalhadas, veja a [seção de criação de token no guia completo](CONFIGURACAO_MCP.md#criar-token-de-api-do-jira)

### 2. Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```env
ATLASSIAN_USERNAME=seu_email@empresa.com
ATLASSIAN_API_TOKEN=seu_token_aqui
JIRA_URL=https://sua-empresa.atlassian.net/
SERVER_HOST=0.0.0.0
SERVER_PORT=8015
```

### 3. Execução Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python app.py
```

### 4. Execução com Docker (Recomendado)

```bash
# Build e execução
docker-compose up --build

# Execução em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servidor
docker-compose down
```

## � Integração com VS Code + GitHub Copilot

Para usar este servidor MCP com o GitHub Copilot no VS Code:

1. **Configure o servidor MCP no VS Code:**
   - Crie `.vscode/mcp.json` no seu projeto:
   
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

2. **Inicie o servidor** (se ainda não estiver rodando):
   ```bash
   docker-compose up -d
   ```

3. **Use no GitHub Copilot Chat:**
   ```
   Busque os detalhes da issue PROJ-123
   ```

> 📘 **[Ver Guia Completo de Integração](CONFIGURACAO_MCP.md)**  
> Inclui: configuração passo a passo, exemplos de uso, solução de problemas e mais.

## �🛠️ Ferramentas Disponíveis

### `hello`
Retorna uma saudação simples.
```python
hello(name: str) -> str
```

### `get_title_description_issue`
Busca título e descrição de uma issue do Jira.
```python
get_title_description_issue(key: str) -> str
```

### `update_infos_issue`
Atualiza campos customizados da issue.
```python
update_infos_issue(
    key: str,
    info_tecnicas: str,
    desc_implementacao: str,
    plan_testes: str
) -> str
```

### `update_description`
Atualiza a descrição da issue.
```python
update_description(key: str, description: str) -> str
```

## 📦 Dependências

- `fastmcp`: Framework para servidor MCP
- `atlassian-python-api`: Cliente Python para Atlassian/Jira
- `python`: 3.12+

## 🧪 Testes

```bash
# Testar conexão com servidor
curl http://localhost:8015

# Verificar logs
docker-compose logs -f jira-server
```

## 📝 Princípios SOLID Aplicados

- **Single Responsibility**: Cada módulo tem uma única responsabilidade
- **Open/Closed**: Extensível sem modificar código existente
- **Liskov Substitution**: Componentes substituíveis por mocks
- **Interface Segregation**: Interfaces enxutas e focadas
- **Dependency Inversion**: Dependências injetadas

Veja mais detalhes em [REFACTORING.md](REFACTORING.md).

## � Documentação Adicional

- 📘 **[Configuração MCP com VS Code](CONFIGURACAO_MCP.md)** - Guia completo de integração
- 🔧 **[REFACTORING.md](REFACTORING.md)** - Detalhes da arquitetura SOLID
- 🌐 **[Model Context Protocol](https://modelcontextprotocol.io/)** - Documentação oficial MCP
- 💬 **[GitHub Copilot Chat](https://code.visualstudio.com/docs/copilot/chat)** - Usando chat tools

## �📄 Licença

Este projeto é de uso interno.
