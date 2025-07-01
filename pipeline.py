import json

# Importa os criadores de cliente
from src.shared.clients import get_kluster_client, get_genai_client
# Importa o serviço que gera descrição da imagem
from src.image_to_text.service import generate_description_from_image
# Importa o agente que extrai informações da descrição
from src.info_extraction.agent import extrair_dados_cpted

def run_full_pipeline(image_url: str) -> dict | None:
    """
    Executa o pipeline completo: de URL de imagem a dados estruturados CPTED.

    Args:
        image_url: A URL da imagem a ser analisada.

    Returns:
        Um dicionário com os dados extraídos ou None em caso de falha.
    """
    print("--- INICIANDO PIPELINE DE ANÁLISE CPTED ---")

    # --- Inicialização dos Clientes ---
    print("Inicializando clientes de API...")
    kluster_client = get_kluster_client()
    genai_client = get_genai_client()

    if not all([kluster_client, genai_client]):
        print("ERRO: Falha ao inicializar um ou mais clientes de API. Verifique suas chaves no arquivo .env")
        return None
    print("Clientes inicializados com sucesso.")

    # --- ETAPA 1: Imagem para Texto ---
    print("\n[ETAPA 1/2] Gerando descrição da imagem...")
    
    # Pergunta que guia o modelo de visão
    cpted_question = (
        "Act as an expert in CPTED (Crime Prevention Through Environmental Design). "
        "Analyze the following image of a location and extract the main insights. "
        "Base your analysis on the theoretical concepts of surveillance, access "
        "control/territoriality, maintenance, and support for legitimate activities."
    )

    description = generate_description_from_image(
        client=kluster_client,
        image_url=image_url,
        question=cpted_question
    )

    if not description:
        print("ERRO: Falha ao gerar a descrição da imagem. Pipeline interrompido.")
        return None
    
    print("Descrição da imagem gerada com sucesso.")
    # print(f"Descrição parcial: '{description[:100]}...'") # Descomente para depurar

    # --- ETAPA 2: Extração de Informação ---
    print("\n[ETAPA 2/2] Extraindo dados estruturados da descrição...")

    # A função `extrair_dados_cpted` já retorna um objeto Pydantic
    analise_cpted_obj = extrair_dados_cpted(description, genai_client)

    if not analise_cpted_obj:
        print("ERRO: Falha ao extrair dados estruturados. Pipeline interrompido.")
        return None

    print("Dados estruturados extraídos com sucesso!")

    # Retorna o objeto Pydantic como um dicionário Python
    return analise_cpted_obj.model_dump()


if __name__ == "__main__":
    # --- Ponto de Entrada do Pipeline ---
    # Defina a URL da imagem que você quer analisar aqui
    URL_DA_IMAGEM_PARA_ANALISE = "https://avenidas.blogfolha.uol.com.br/files/2019/05/73541944dbb06a97f211873046377c77050af17208ee473f9395d3138ae49e71_5ae772e540a2f-768x512.jpg"

    # Executa a função principal do pipeline
    resultado_final = run_full_pipeline(URL_DA_IMAGEM_PARA_ANALISE)

    print("\n--- RESULTADO FINAL DO PIPELINE ---")
    if resultado_final:
        # Usa json.dumps para imprimir o dicionário como uma string JSON formatada
        # ensure_ascii=False garante que caracteres como 'ç' e 'ã' sejam exibidos corretamente
        print(json.dumps(resultado_final, indent=2, ensure_ascii=False))
    else:
        print("O pipeline falhou e não produziu um resultado.")