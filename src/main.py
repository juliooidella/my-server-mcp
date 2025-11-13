"""
Módulo principal da aplicação.

Este módulo inicializa e configura o servidor MCP,
seguindo o princípio de Inversão de Dependência.
"""
from fastmcp import FastMCP
from .config.settings import Settings
from .services.jira_service import JiraService
from .tools.jira_tools import register_jira_tools


def create_app() -> FastMCP:
    """
    Factory function para criar e configurar a aplicação.
    
    Returns:
        Instância configurada do FastMCP
        
    Raises:
        ValueError: Se as configurações forem inválidas
    """
    # Carrega configurações
    settings = Settings.from_env()
    settings.validate()
    
    # Cria instância do servidor MCP
    mcp = FastMCP("MyServer")
    
    # Cria serviço Jira
    jira_service = JiraService(
        url=settings.jira_url,
        username=settings.atlassian_username,
        api_token=settings.atlassian_api_token,
        cloud=True
    )
    
    # Registra ferramentas
    register_jira_tools(mcp, jira_service)
    
    return mcp, settings


def main() -> None:
    """
    Função principal que inicia o servidor.
    """
    mcp, settings = create_app()
    
    # Inicia o servidor
    mcp.run(
        transport="http",
        host=settings.server_host,
        port=settings.server_port
    )


if __name__ == "__main__":
    main()
