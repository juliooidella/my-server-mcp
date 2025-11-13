"""
Módulo principal da aplicação.

Este módulo inicializa e configura o servidor MCP,
seguindo o princípio de Inversão de Dependência.
"""
from fastmcp import FastMCP
from .config.settings import Settings
from .services.jira_service import JiraService
from .tools.jira_tools import register_jira_tools
from dotenv import load_dotenv
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

load_dotenv()

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
    
    token_secreto = settings.mcp_prod_token
    
    auth_verifier = StaticTokenVerifier(
        tokens={
            token_secreto: {
                "client_id": "admin_user", # Identificador de quem está usando
                "scopes": ["admin"]        # Permissões (opcional)
            }
        }
    )
    # ------------------------------------------------------

    # NEW: Passamos o parametro 'auth' para o FastMCP
    # Outras formas de autenticação deve consultar a documentação https://gofastmcp.com/servers/auth/authentication
    mcp = FastMCP("MyServer", auth=auth_verifier)
    
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
