"""
Ferramentas MCP para operações com Jira.

Este módulo define as ferramentas que serão expostas pelo servidor MCP,
seguindo o princípio Open/Closed - novas ferramentas podem ser adicionadas
sem modificar as existentes.
"""
from fastmcp import FastMCP
from ..services.jira_service import JiraService


def register_jira_tools(mcp: FastMCP, jira_service: JiraService) -> None:
    """
    Registra todas as ferramentas Jira no servidor MCP.
    
    Args:
        mcp: Instância do servidor FastMCP
        jira_service: Instância do serviço Jira
    """
    
    @mcp.tool
    def hello(name: str) -> str:
        """
        Retorna uma saudação simples.
        
        Args:
            name: Nome para saudar
            
        Returns:
            Mensagem de saudação
        """
        return f"Hello, {name}!"
    
    @mcp.tool
    def get_title_description_issue(key: str) -> str:
        """
        Útil para buscar informações do jira como titulo e descrição da tarefa.
        
        Args:
            key: Chave da issue do Jira (ex: PROJ-123)
            
        Returns:
            String formatada com título e descrição
        """
        try:
            title, description = jira_service.get_issue_title_and_description(key)
            return f"""Título: {title}\n\nDescrição da tarefa: {description}"""
        except Exception as e:
            return f"Erro ao buscar issue {key}: {str(e)}"
    
    @mcp.tool
    def update_infos_issue(
        key: str, 
        info_tecnicas: str, 
        desc_implementacao: str, 
        plan_testes: str
    ) -> str:
        """
        Útil para atualizar os campos do Jira.
        
        Args:
            key: Chave da issue
            info_tecnicas: Informações técnicas
            desc_implementacao: Descrição da implementação
            plan_testes: Plano de testes
            
        Returns:
            Mensagem de sucesso ou erro
        """
        try:
            jira_service.update_custom_fields(
                issue_key=key,
                info_tecnicas=info_tecnicas,
                desc_implementacao=desc_implementacao,
                plan_testes=plan_testes
            )
            return f"Issue {key} atualizada com sucesso!"
        except Exception as e:
            return f"Erro ao atualizar a issue {key}: {str(e)}"
    
    @mcp.tool
    def update_description(key: str, description: str) -> str:
        """
        Útil para atualizar a descrição da tarefa.
        
        Args:
            key: Chave da issue
            description: Nova descrição
            
        Returns:
            Mensagem de sucesso ou erro
        """
        try:
            jira_service.update_description(issue_key=key, description=description)
            return f"Issue {key} atualizada com sucesso!"
        except Exception as e:
            return f"Erro ao atualizar a issue {key}: {str(e)}"
