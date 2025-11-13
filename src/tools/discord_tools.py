from fastmcp import FastMCP
from ..services.discord_service import DiscordService

def registrar_ferramentas_discord(mcp: FastMCP, discord_service: DiscordService) -> None:
    """
    Registra outras ferramentas no servidor MCP.
    
    Args:
        mcp: Instância do servidor FastMCP
    """
    @mcp.tool
    def enviar_mensagem_discord(mensagem: str) -> str:
        """
        Envia uma mensagem para um canal do Discord via webhook.
        
        Args:
            mensagem: A mensagem a ser enviada
            
        Returns:
            Confirmação de envio
        """
        return discord_service.enviar_mensagem(mensagem)
        
    
    @mcp.tool
    def outra_ferramenta(param: str) -> str:
        """
        Exemplo de outra ferramenta.
        
        Args:
            param: Parâmetro de entrada
            
        Returns:
            Resposta da ferramenta
        """
        return f"Outra ferramenta recebeu: {param}"