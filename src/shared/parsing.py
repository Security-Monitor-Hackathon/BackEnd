from src.info_extraction.schemas import AnaliseCptedDoLocal
from typing import Dict, Any


def achatar_analise_cpted(analise: AnaliseCptedDoLocal) -> Dict[str, Any]:
    """
    Converte um objeto de análise CPTED em um dicionário achatado,
    pronto para ser adicionado a um DataFrame.
    """
    separador_lista = "; "
    dados_achatados = {
        'titulo_analise': analise.titulo_analise,
        'indice_cpted_geral': analise.indice_cpted_geral.value,
        'resumo_executivo': analise.resumo_executivo,
        'vigilancia_nivel_natural': analise.vigilancia.nivel_vigilancia_natural.value,
        'vigilancia_iluminacao': analise.vigilancia.iluminacao.value,
        'vigilancia_pontos_cegos': separador_lista.join(analise.vigilancia.pontos_cegos_obstrucoes),
        'vigilancia_formal': separador_lista.join(analise.vigilancia.presenca_vigilancia_formal),
        'vigilancia_justificativa': analise.vigilancia.justificativa,
        'controle_acesso_clareza_fronteiras': analise.controle_de_acesso_e_territorialidade.clareza_das_fronteiras.value,
        'controle_acesso_barreiras_fisicas': separador_lista.join(analise.controle_de_acesso_e_territorialidade.barreiras_fisicas),
        'controle_acesso_barreiras_simbolicas': separador_lista.join(analise.controle_de_acesso_e_territorialidade.barreiras_simbolicas),
        'controle_acesso_justificativa': analise.controle_de_acesso_e_territorialidade.justificativa,
        'manutencao_percepcao_cuidado': analise.manutencao_e_zeladoria.percepcao_geral_de_cuidado.value,
        'manutencao_sinais_desordem': separador_lista.join(analise.manutencao_e_zeladoria.sinais_de_desordem_fisica),
        'manutencao_justificativa': analise.manutencao_e_zeladoria.justificativa,
        'suporte_atividades_legitimas': analise.suporte_de_atividades_e_uso_do_espaco.presenca_de_atividades_legitimas.value,
        'suporte_atividades_tipo_uso': separador_lista.join(analise.suporte_de_atividades_e_uso_do_espaco.tipo_de_uso_do_espaco),
        'suporte_atividades_areas_adjacentes': separador_lista.join(analise.suporte_de_atividades_e_uso_do_espaco.influencia_de_areas_adjacentes),
        'suporte_atividades_justificativa': analise.suporte_de_atividades_e_uso_do_espaco.justificativa,
        'recomendacoes': separador_lista.join(analise.recomendacoes_cpted)
    }
    return dados_achatados