# run_info_extraction.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))

import pandas as pd
from src.shared.clients import get_genai_client
from src.info_extraction.agent import extrair_dados_cpted
from src.shared.parsing import achatar_analise_cpted

def main():
    """
    Script principal para extrair dados CPTED de uma lista de descrições
    e salvar os resultados em um arquivo CSV.
    """
    print("Inicializando o cliente Google GenAI...")
    client = get_genai_client()
    if not client:
        print("Processo abortado devido à falha na inicialização do cliente.")
        return

    # Dados de entrada (poderia ser lido de um arquivo CSV)
    descricoes_de_locais = [
        """The image depicts a street scene at night with several individuals walking along the sidewalk. Here's an analysis based on the four key components of Crime Prevention Through Environmental Design (CPTED):

1. **Surveillance:**
   - The presence of streetlights provides ambient lighting, which can deter criminal activity by making the area more visible to potential offenders. However, the image shows that the streetlights are not positioned to provide direct surveillance over the entire area. There is no clear indication of cameras or other forms of active surveillance.
   - The lack of visible security personnel or cameras suggests that the area may rely solely on natural surveillance provided by pedestrians and passersby.

2. **Access Control/Territoriality:**
   - The sidewalk appears to be relatively narrow, which could limit the number of people who can walk on it simultaneously, potentially reducing the likelihood of criminal activity due to the reduced opportunity for crime.
   - The presence of parked cars along the street might create a sense of territoriality, as vehicles can act as barriers and provide some level of protection for the occupants. However, the cars are parked close to the curb, which might make it easier for someone to quickly exit and commit a crime.
   - The street signs, such as the "No Parking" sign, indicate some form of access control but do not necessarily prevent unauthorized access. The effectiveness of these signs depends on their enforcement and the behavior of the community members.   

3. **Maintenance:**
   - The street appears to be well-maintained with clean sidewalks and properly functioning streetlights. This contributes to a positive environment that discourages criminal activity by maintaining a sense of order and cleanliness.
   - However, the presence of graffiti on the walls and the general appearance of the buildings suggest that there might be underlying issues with maintenance and community engagement. Graffiti can be a sign of neglect and may attract further criminal activity if left unchecked.

4. **Support for Legitimate Activities:**
   - The individuals walking on the sidewalk appear to be engaged in legitimate activities, such as walking or cycling. Their presence suggests that the area is being used for its intended purpose, which can deter criminal activity by creating a sense of normalcy and activity.
   - The presence of parked cars and the general layout of the street suggest that the area supports various legitimate activities, including transportation and commerce. However, the lack of active surveillance and the potential for unauthorized access through the parked cars could still pose risks.

In conclusion, while the image shows a generally well-maintained and active street, the lack of active surveillance and the potential for unauthorized access through the parked cars raise concerns about the effectiveness of the current CPTED measures. To improve the safety of this area, it would be beneficial to implement additional surveillance systems, enforce parking regulations, and engage the local community in maintaining the area.""",
    ]
    
    lista_de_resultados_achatados = []

    print(f"Iniciando processamento de {len(descricoes_de_locais)} descrições...")
    for i, descricao in enumerate(descricoes_de_locais, 1):
        print(f"\nProcessando Descrição #{i}...")
        
        analise_obj = extrair_dados_cpted(descricao, client)
        
        if analise_obj:
            dados_para_linha = achatar_analise_cpted(analise_obj)
            lista_de_resultados_achatados.append(dados_para_linha)
            print(f"Descrição #{i} processada com sucesso.")
        else:
            print(f"Falha no processamento da Descrição #{i}.")

    if not lista_de_resultados_achatados:
        print("\nNenhuma análise foi processada com sucesso. Nenhum arquivo CSV será gerado.")
        return

    # Salvar resultados em CSV
    print("\nProcessamento concluído. Salvando relatório...")
    df_final = pd.DataFrame(lista_de_resultados_achatados)

    reports_path = "tests/data/reports"
    os.makedirs(reports_path, exist_ok=True)
    nome_do_arquivo_csv = os.path.join(reports_path, 'relatorio_cpted_extraido1.csv')
    
    try:
        df_final.to_csv(nome_do_arquivo_csv, index=False, encoding='utf-8-sig')
        print(f"Arquivo '{nome_do_arquivo_csv}' salvo com sucesso com {len(df_final)} análises.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo CSV: {e}")

    return

if __name__ == "__main__":
    main()