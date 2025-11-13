"""
Gerenciamento de configurações e variáveis de ambiente.

Este módulo centraliza todas as configurações da aplicação,
seguindo o princípio Single Responsibility.
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """
    Classe de configurações da aplicação.
    
    Attributes:
        atlassian_username: Nome de usuário do Atlassian/Jira
        atlassian_api_token: Token de API do Atlassian/Jira
        jira_url: URL da instância do Jira
        server_host: Host do servidor MCP
        server_port: Porta do servidor MCP
    """
    atlassian_username: str
    atlassian_api_token: str
    jira_url: str = "https://nimitz.atlassian.net/"
    server_host: str = "0.0.0.0"
    server_port: int = 8015
    mcp_prod_token: str = ""
    discord_webhook_url: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "Settings":
        """
        Cria uma instância de Settings a partir de variáveis de ambiente.
        
        Returns:
            Settings: Instância configurada
            
        Raises:
            ValueError: Se variáveis obrigatórias não estiverem definidas
        """
        username = os.environ.get("ATLASSIAN_USERNAME")
        api_token = os.environ.get("ATLASSIAN_API_TOKEN")
        mcp_prod_token = os.environ.get("MCP_PROD_TOKEN")
        
        if not username or not api_token or not mcp_prod_token:
            raise ValueError(
                "As variáveis de ambiente ATLASSIAN_USERNAME, "
                "ATLASSIAN_API_TOKEN e MCP_PROD_TOKEN precisam ser definidas."
            )
        
        return cls(
            atlassian_username=username,
            atlassian_api_token=api_token,
            jira_url=os.environ.get("JIRA_URL", cls.jira_url),
            server_host=os.environ.get("SERVER_HOST", cls.server_host),
            server_port=int(os.environ.get("SERVER_PORT", cls.server_port)),
            mcp_prod_token=mcp_prod_token,
            discord_webhook_url=os.environ.get("DISCORD_WEBHOOK_URL", "")
        )
    
    def validate(self) -> None:
        """
        Valida as configurações.
        
        Raises:
            ValueError: Se alguma configuração for inválida
        """
        if not self.atlassian_username:
            raise ValueError("Username não pode estar vazio")
        if not self.atlassian_api_token:
            raise ValueError("API Token não pode estar vazio")
        if not self.jira_url:
            raise ValueError("Jira URL não pode estar vazio")
        if self.server_port <= 0 or self.server_port > 65535:
            raise ValueError("Porta deve estar entre 1 e 65535")
        if not self.mcp_prod_token:
            raise ValueError("MCP_PROD_TOKEN não pode estar vazio")
        
