"""
Serviço de integração com Jira.

Este módulo encapsula toda a lógica de interação com a API do Jira,
seguindo os princípios Single Responsibility e Dependency Inversion.
"""
from typing import Dict, Any, Optional
from atlassian import Jira


class JiraService:
    """
    Serviço para operações com Jira.
    
    Esta classe encapsula todas as operações relacionadas ao Jira,
    facilitando testes e manutenção do código.
    """
    
    def __init__(self, url: str, username: str, api_token: str, cloud: bool = True):
        """
        Inicializa o serviço Jira.
        
        Args:
            url: URL da instância do Jira
            username: Nome de usuário
            api_token: Token de API
            cloud: Se é uma instância cloud (padrão: True)
        """
        self._jira = Jira(
            url=url,
            username=username,
            password=api_token,
            cloud=cloud
        )
    
    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Busca uma issue do Jira.
        
        Args:
            issue_key: Chave da issue (ex: PROJ-123)
            
        Returns:
            Dict com os dados da issue
            
        Raises:
            Exception: Se houver erro ao buscar a issue
        """
        return self._jira.issue(issue_key)
    
    def get_issue_title_and_description(self, issue_key: str) -> tuple[str, str]:
        """
        Busca título e descrição de uma issue.
        
        Args:
            issue_key: Chave da issue
            
        Returns:
            Tupla (título, descrição)
        """
        issue = self.get_issue(issue_key)
        title = issue.get("fields", {}).get("summary", "")
        description = issue.get("fields", {}).get("description", "")
        return title, description
    
    def update_issue_fields(
        self, 
        issue_key: str, 
        fields: Dict[str, Any],
        notify_users: bool = True
    ) -> None:
        """
        Atualiza campos de uma issue.
        
        Args:
            issue_key: Chave da issue
            fields: Dicionário com os campos a atualizar
            notify_users: Se deve notificar usuários
            
        Raises:
            Exception: Se houver erro na atualização
        """
        self._jira.issue_update(
            issue_key=issue_key,
            fields=fields,
            notify_users=notify_users
        )
    
    def update_custom_fields(
        self,
        issue_key: str,
        info_tecnicas: Optional[str] = None,
        desc_implementacao: Optional[str] = None,
        plan_testes: Optional[str] = None,
        notify_users: bool = True
    ) -> None:
        """
        Atualiza campos customizados da issue.
        
        Args:
            issue_key: Chave da issue
            info_tecnicas: Informações técnicas (customfield_10051)
            desc_implementacao: Descrição da implementação (customfield_10059)
            plan_testes: Plano de testes (customfield_10049)
            notify_users: Se deve notificar usuários
            
        Raises:
            Exception: Se houver erro na atualização
        """
        fields_to_update = {}
        
        if info_tecnicas is not None:
            fields_to_update["customfield_10051"] = info_tecnicas
        if desc_implementacao is not None:
            fields_to_update["customfield_10059"] = desc_implementacao
        if plan_testes is not None:
            fields_to_update["customfield_10049"] = plan_testes
        
        if fields_to_update:
            self.update_issue_fields(issue_key, fields_to_update, notify_users)
    
    def update_description(
        self,
        issue_key: str,
        description: str,
        notify_users: bool = True
    ) -> None:
        """
        Atualiza a descrição de uma issue.
        
        Args:
            issue_key: Chave da issue
            description: Nova descrição
            notify_users: Se deve notificar usuários
            
        Raises:
            Exception: Se houver erro na atualização
        """
        self.update_issue_fields(
            issue_key=issue_key,
            fields={"description": description},
            notify_users=notify_users
        )
