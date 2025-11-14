
Vamos rodar o Jupyter Lab para desenvolvimento interativo:

```bash
uv run --with jupyter jupyter lab
```

Após o Jupyter Lab abrir no navegador, crie um novo notebook Python 3 e cole o código abaixo para testar a conexão com o servidor MCP remoto.


```python
import asyncio
from fastmcp import Client

# 1. Coloque o URL do seu servidor aqui
SERVER_URL = "http://127.0.0.1:8007/mcp"  # ou https://api.exemplo.com/mcp

config = {
    "mcpServers": {
        "jira_server": {
            "url": "http://127.0.0.1:8015/mcp",
            # O token deve ser passado como Bearer
            "headers": {"Authorization": "Bearer d41d8cd98f00b204e9800998ecf8427e"}
        }
    }
}
async def test_remote():
    print(f"🔌 Conectando a: {SERVER_URL} ...")
    
    # O cliente detecta automaticamente que é transporte HTTP/SSE pelo URL
    client = Client(config)

    async with client:
        # 1. Teste de Conectividade Básica (Ping)
        try:
            await client.ping()
            print("✅ Ping: Sucesso! Servidor acessível.")
        except Exception as e:
            print(f"❌ Erro no Ping: {e}")
            return

        # 2. Informações do Servidor (Obtidas no Handshake)
        info = client.initialize_result.serverInfo
        print(f"\nℹ️ Servidor: {info.name} (v{info.version})")

        # 3. Listar Ferramentas Disponíveis (Discovery)
        print("\n🛠️ Listando Ferramentas...")
        tools = await client.list_tools()
        
        if not tools:
            print("   (Nenhuma ferramenta encontrada)")
        else:
            for t in tools:
                print(f"   - {t.name}: {t.description or 'Sem descrição'}")

        # 4. (Opcional) Teste de Chamada de Ferramenta
        # Descomente as linhas abaixo se quiser testar uma ferramenta específica
        
        tool_name = "enviar_mensagem_discord"
        params = {"mensagem": "Olá Mundo",
                  
                 }
        print(f"\n🚀 Testando ferramenta '{tool_name}'...")
        result = await client.call_tool(tool_name, params)
        print(f"   Resultado: {result.data}")

# No Jupyter, você pode chamar await diretamente
await test_remote()
```
