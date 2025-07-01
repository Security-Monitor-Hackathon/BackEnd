from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Enums para controlar as saídas ---

class NivelControleEnum(str, Enum):
    """Nível de controle ou qualidade de um princípio CPTED."""
    ALTO = "Alto / Forte"
    MODERADO = "Moderado"
    BAIXO = "Baixo / Fraco"
    INEXISTENTE = "Inexistente"

class TipoIluminacaoEnum(str, Enum):
    """Qualidade da iluminação no local."""
    BOA = "Boa e uniforme"
    MODERADA = "Moderada com pontos de sombra"
    FRACA = "Fraca / Mal Iluminada"
    INEXISTENTE = "Inexistente"

class PercepcaoCuidadoEnum(str, Enum):
    """Percepção geral de manutenção e zeladoria."""
    BEM_CUIDADO = "Bem-Cuidado / Zelado"
    SINAIS_DE_NEGLIGENCIA = "Sinais de Negligência"
    ABANDONADO = "Abandonado / Degradado"

# --- Modelos Pydantic baseados nos princípios CPTED ---

class Vigilancia(BaseModel):
    """Avalia a capacidade de ver e ser visto no local."""
    nivel_vigilancia_natural: NivelControleEnum = Field(description="Capacidade dos moradores ou transeuntes de observar o ambiente naturalmente. ")
    iluminacao: TipoIluminacaoEnum = Field(description="Qualidade da iluminação artificial para visibilidade noturna. ")
    pontos_cegos_obstrucoes: List[str] = Field(description="Lista de elementos que obstruem a visão (ex: 'vegetação densa', 'muros altos', 'esquinas sem visibilidade').")
    presenca_vigilancia_formal: List[str] = Field(description="Lista de mecanismos de vigilância formais presentes (ex: 'Câmeras de CFTV', 'Guardas de segurança', 'Policiamento visível'). ")
    justificativa: str = Field(description="Breve explicação sobre a avaliação da vigilância no local.")

class ControleDeAcessoTerritorialidade(BaseModel):
    """Avalia a clareza das fronteiras entre espaços públicos e privados."""
    clareza_das_fronteiras: NivelControleEnum = Field(description="Clareza na distinção entre espaços públicos, semiprivados e privados. ")
    barreiras_fisicas: List[str] = Field(description="Lista de barreiras físicas que delimitam o território (ex: 'Muros', 'Portões', 'Cercas', 'Arame farpado'). ")
    barreiras_simbolicas: List[str] = Field(description="Lista de barreiras simbólicas que indicam transição de espaço (ex: 'Jardins frontais', 'Mudança de pavimento', 'Pequenos degraus'). ")
    justificativa: str = Field(description="Breve explicação sobre a avaliação do controle de acesso e territorialidade.")

class ManutencaoEzeladoria(BaseModel):
    """Avalia a percepção de cuidado e manutenção, baseado na teoria das 'Janelas Quebradas'."""
    percepcao_geral_de_cuidado: PercepcaoCuidadoEnum = Field(description="Impressão geral de manutenção do local. ")
    sinais_de_desordem_fisica: List[str] = Field(description="Lista de sinais visíveis de negligência ou vandalismo (ex: 'Pichações', 'Lixo acumulado', 'Janelas quebradas', 'Edifícios danificados'). ")
    justificativa: str = Field(description="Breve explicação sobre a avaliação da manutenção e zeladoria.")

class SuporteDeAtividades(BaseModel):
    """Avalia a presença de atividades legítimas que desencorajam o crime."""
    presenca_de_atividades_legitimas: NivelControleEnum = Field(description="Nível de uso do espaço por pessoas em atividades lícitas e comunitárias. ")
    tipo_de_uso_do_espaco: List[str] = Field(description="Lista dos tipos de atividades predominantes (ex: 'Residencial', 'Comercial', 'Lazer', 'Trânsito de passagem').")
    influencia_de_areas_adjacentes: List[str] = Field(description="Descreve como áreas vizinhas (escolas, shoppings, parques) impactam a segurança do local. ")
    justificativa: str = Field(description="Breve explicação sobre como o uso do espaço suporta ou não a segurança.")

# --- Modelo Principal para a Análise CPTED Completa ---

class AnaliseCptedDoLocal(BaseModel):
    """Schema para uma análise de segurança completa de um local, baseada nos princípios do CPTED."""
    titulo_analise: str = Field(description="Um título descritivo para a análise do local.")
    indice_cpted_geral: NivelControleEnum = Field(description="Uma avaliação consolidada do quão bem o local aplica os princípios CPTED.")
    resumo_executivo: str = Field(description="Um parágrafo que resume os principais pontos fortes e fracos de segurança do ambiente, justificando o índice geral.")
    
    vigilancia: Vigilancia
    controle_de_acesso_e_territorialidade: ControleDeAcessoTerritorialidade
    manutencao_e_zeladoria: ManutencaoEzeladoria
    suporte_de_atividades_e_uso_do_espaco: SuporteDeAtividades
    
    recomendacoes_cpted: List[str] = Field(description="Lista de ações e melhorias práticas sugeridas para aumentar a segurança do local com base nos princípios CPTED.")