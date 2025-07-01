import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))

# Importa as funções necessárias dos nossos módulos organizados
from src.shared.clients import get_kluster_client
from src.image_to_text.service import generate_description_from_image

def main():
    """
    Script principal para gerar uma descrição textual de uma imagem
    usando a análise CPTED.
    """
    print("Inicializando o cliente da API Kluster/OpenAI...")
    client = get_kluster_client()
    
    # Se o cliente não puder ser criado (ex: falta de chave API), o programa para.
    if not client:
        print("Processo abortado devido à falha na inicialização do cliente.")
        return

    # --- Definição dos Dados de Entrada ---
    # A URL da imagem que queremos analisar.
    image_url = "https://avenidas.blogfolha.uol.com.br/files/2019/05/73541944dbb06a97f211873046377c77050af17208ee473f9395d3138ae49e71_5ae772e540a2f-768x512.jpg"
    
    # O prompt detalhado que guia a análise do modelo.
    cpted_question = (
        "Act as an expert in CPTED (Crime Prevention Through Environmental Design). "
        "Analyze the following image of a location and extract the main insights. "
        "Base your analysis on the theoretical concepts of surveillance, access "
        "control/territoriality, maintenance, and support for legitimate activities."
    )

    print(f"\nAnalisando a imagem da URL: {image_url}")
    print("Por favor, aguarde...")

    # --- Execução do Serviço ---
    # Chama a função do nosso módulo de serviço para fazer o trabalho pesado.
    description = generate_description_from_image(
        client=client, 
        image_url=image_url, 
        question=cpted_question
    )

    # --- Exibição do Resultado ---
    if description:
        print("\n--- DESCRIÇÃO GERADA PELA IA ---\n")
        print(description)
        print("\n---------------------------------\n")
        print("Dica: Copie esta descrição para usar como entrada no script 'run_info_extraction.py'.")
    else:
        print("\nNão foi possível gerar a descrição para a imagem.")

    return description

if __name__ == "__main__":
    main()