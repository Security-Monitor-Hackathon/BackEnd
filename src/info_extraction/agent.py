from .schemas import AnaliseCptedDoLocal
from .prompts import construct_prompt_cpted
from src import config

def _get_model_structured_response(prompt: str, client, schema: dict):
    """Função de baixo nível para chamar a API. O '_' indica uso interno."""
    response = client.models.generate_content(
        model=config.GOOGLE_MODEL_NAME, 
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
        },
    )
    # O SDK mais recente retorna o dicionário diretamente em .text, que é um JSON string
    import json
    return json.loads(response.text)


def extrair_dados_cpted(descricao: str, client) -> AnaliseCptedDoLocal | None:
    """
    Orquestra o processo de extração de dados estruturados de uma descrição.
    
    Args:
        descricao (str): A descrição textual do local.
        client: O cliente GenAI configurado.

    Returns:
        Um objeto AnaliseCptedDoLocal validado ou None em caso de erro.
    """
    if not client:
        print("Erro: Cliente GenAI não inicializado.")
        return None
        
    try:
        # 1. Construir o prompt
        prompt = construct_prompt_cpted(descricao)
        
        # 2. Obter o schema Pydantic como dicionário
        schema_dict = AnaliseCptedDoLocal.model_json_schema()

        # 3. Chamar a API para obter a resposta estruturada
        resposta_bruta = _get_model_structured_response(prompt, client, schema_dict)
        
        # 4. Validar e retornar o objeto Pydantic
        analise_validada = AnaliseCptedDoLocal.model_validate(resposta_bruta)
        return analise_validada

    except Exception as e:
        print(f"Falha ao extrair dados da descrição: {e}")
        return None