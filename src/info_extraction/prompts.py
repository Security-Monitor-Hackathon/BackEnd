construct_prompt_cpted = (
    lambda descricao: f"""
    Aja como um especialista em CPTED (Crime Prevention Through Environmental Design). Analise a seguinte descrição de um local
    e preencha o schema JSON com base nos princípios de CPTED. Fundamente sua análise nos conceitos teóricos de vigilância,
    controle de acesso/territorialidade, manutenção (janelas quebradas) e suporte a atividades.

    Descrição do Local:
    {descricao}
    """)