# Estrutura Refatorada - Princípios SOLID

## Estrutura de Diretórios

```
my-server-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Gerenciamento de configurações
│   ├── services/
│   │   ├── __init__.py
│   │   └── jira_service.py     # Lógica de negócio do Jira
│   └── tools/
│       ├── __init__.py
│       └── jira_tools.py       # Ferramentas MCP
├── app.py                      # Compatibilidade (delega para src/main.py)
├── requirements.txt
└── README.md
```

## Princípios SOLID Aplicados

### 1. **Single Responsibility Principle (SRP)**
Cada módulo tem uma única responsabilidade:
- `settings.py`: Gerenciar configurações e variáveis de ambiente
- `jira_service.py`: Operações com a API do Jira
- `jira_tools.py`: Definição das ferramentas MCP
- `main.py`: Inicialização e orquestração da aplicação

### 2. **Open/Closed Principle (OCP)**
- Novas ferramentas podem ser adicionadas em `jira_tools.py` sem modificar código existente
- Novos serviços podem ser criados sem alterar `JiraService`

### 3. **Liskov Substitution Principle (LSP)**
- `JiraService` pode ser substituído por implementações mock para testes
- Interface consistente permite substituição sem quebrar o código

### 4. **Interface Segregation Principle (ISP)**
- Cada serviço expõe apenas métodos relevantes
- Clientes não dependem de métodos que não usam

### 5. **Dependency Inversion Principle (DIP)**
- Módulos de alto nível (`main.py`) não dependem de implementações específicas
- Dependências são injetadas via parâmetros de função
- Fácil substituição de implementações para testes

## Benefícios da Refatoração

1. **Testabilidade**: Cada componente pode ser testado isoladamente
2. **Manutenibilidade**: Código organizado e fácil de localizar
3. **Escalabilidade**: Fácil adicionar novos serviços e ferramentas
4. **Reutilização**: Componentes podem ser reusados em outros projetos
5. **Separação de Responsabilidades**: Cada arquivo tem um propósito claro

## Como Usar

Execute a aplicação normalmente:
```bash
python app.py
```

Ou use o módulo diretamente:
```bash
python -m src.main
```
