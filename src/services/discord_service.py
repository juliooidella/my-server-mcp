import requests
import json

class DiscordService:
    """
    Serviço para interagir com o Discord via Webhooks.
    """
    
    def __init__(self, webhook_url: str):
        """
        Inicializa o serviço Discord.
        
        Args:
            webhook_url: URL do webhook do Discord
        """
        self.webhook_url = webhook_url
    
    def enviar_mensagem(self, mensagem: str) -> str:
        """
        Envia uma mensagem para o canal do Discord via webhook.
        
        Args:
            mensagem: A mensagem a ser enviada
            
        Returns:
            Confirmação de envio
        """
        payload = {
            "content": mensagem
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 204:
            return "Mensagem enviada com sucesso ao Discord!"
        else:
            return f"Falha ao enviar mensagem. Código de status: {response.status_code}, Resposta: {response.text}"