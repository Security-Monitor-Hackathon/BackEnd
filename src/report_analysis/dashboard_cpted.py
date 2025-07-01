import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# Configuração da página do dashboard
st.set_page_config(
    page_title="Dashboard de Análise CPTED",
    page_icon="🛡️",
    layout="wide"
)

# Título do Dashboard
st.title("🛡️ Dashboard de Análise de Segurança CPTED")
st.markdown("Este dashboard apresenta uma análise visual dos dados de segurança de locais, com base nos princípios do CPTED.")

# --- Carregamento dos Dados ---
@st.cache_data
def carregar_dados(caminho_arquivo):
    """Função para carregar os dados do arquivo CSV."""
    try:
        df = pd.read_csv(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado. Por favor, verifique se ele está no mesmo diretório que o script.")
        return None

# Carrega o DataFrame
df = carregar_dados('../data/reports/relatorio_cpted_multiplas_analises1.csv')

if df is not None:
    # --- Barra Lateral de Filtros ---
    st.sidebar.header("Filtros do Relatório")
    
    # Filtro por Índice CPTED Geral
    indice_selecionado = st.sidebar.multiselect(
        "Filtrar por Índice CPTED Geral:",
        options=df['indice_cpted_geral'].unique(),
        default=df['indice_cpted_geral'].unique()
    )

    # Filtro por Nível de Iluminação
    iluminacao_selecionada = st.sidebar.multiselect(
        "Filtrar por Nível de Iluminação:",
        options=df['vigilancia_iluminacao'].unique(),
        default=df['vigilancia_iluminacao'].unique()
    )

    # Aplicando os filtros ao DataFrame
    df_filtrado = df[
        df['indice_cpted_geral'].isin(indice_selecionado) &
        df['vigilancia_iluminacao'].isin(iluminacao_selecionada)
    ]

    # --- Corpo Principal do Dashboard ---

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados. Por favor, ajuste os filtros na barra lateral.")
    else:
        # Linha de KPIs (Key Performance Indicators)
        st.markdown("### Visão Geral")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Análises", f"{len(df_filtrado)}")
        col2.metric("Índice de Risco Mais Comum", df_filtrado['indice_cpted_geral'].mode()[0])
        col3.metric("Percepção de Cuidado Mais Comum", df_filtrado['manutencao_percepcao_cuidado'].mode()[0])

        st.markdown("---")

        # Linha com Gráficos de Distribuição
        col_graf_1, col_graf_2 = st.columns(2)

        with col_graf_1:
            st.subheader("Distribuição do Índice CPTED Geral")
            fig_indice = px.bar(
                df_filtrado['indice_cpted_geral'].value_counts().reset_index(),
                x='indice_cpted_geral',
                y='count',
                title="Contagem por Nível de Risco",
                labels={'count': 'Quantidade de Locais', 'indice_cpted_geral': 'Índice CPTED'},
                color='indice_cpted_geral',
                text_auto=True,
                category_orders={"indice_cpted_geral": ["Baixo / Fraco", "Moderado", "Alto / Forte"]}
            )
            fig_indice.update_layout(showlegend=False)
            st.plotly_chart(fig_indice, use_container_width=True)

        with col_graf_2:
            st.subheader("Qualidade da Iluminação nos Locais")
            fig_iluminacao = px.pie(
                df_filtrado,
                names='vigilancia_iluminacao',
                title="Proporção por Nível de Iluminação",
                hole=0.3,
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            st.plotly_chart(fig_iluminacao, use_container_width=True)

        st.markdown("---")

        # --- Análise de Fatores e Recomendações ---
        st.subheader("Fatores Mais Comuns (Riscos e Recomendações)")

        def extrair_e_contar_fatores(series, top_n=5):
            """Função para separar strings, contar e retornar os mais comuns."""
            series = series.dropna()
            if series.empty:
                return pd.DataFrame(columns=['Fator', 'Contagem'])
            
            todos_os_fatores = series.str.split('; ').explode().str.strip()
            contagem = Counter(todos_os_fatores)
            
            contagem.pop('', None)
            
            df_contagem = pd.DataFrame(contagem.items(), columns=['Fator', 'Contagem']).sort_values('Contagem', ascending=False)
            return df_contagem.head(top_n)

        col_risco, col_rec = st.columns(2)

        with col_risco:
            st.markdown("##### Top 5 Fatores de Risco (Sinais de Desordem)")
            df_riscos = extrair_e_contar_fatores(df_filtrado['manutencao_sinais_desordem'])
            if not df_riscos.empty:
                fig_riscos = px.bar(
                    df_riscos.sort_values('Contagem', ascending=True),
                    x='Contagem',
                    y='Fator',
                    orientation='h',
                    text_auto=True
                )
                st.plotly_chart(fig_riscos, use_container_width=True)
            else:
                st.info("Nenhum fator de risco a ser exibido para a seleção atual.")

        with col_rec:
            st.markdown("##### Top 5 Recomendações")
            df_recomendacoes = extrair_e_contar_fatores(df_filtrado['recomendacoes'])
            if not df_recomendacoes.empty:
                fig_recomendacoes = px.bar(
                    df_recomendacoes.sort_values('Contagem', ascending=True),
                    x='Contagem',
                    y='Fator',
                    orientation='h',
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,
                    text_auto=True
                )
                st.plotly_chart(fig_recomendacoes, use_container_width=True)
            else:
                st.info("Nenhuma recomendação a ser exibida para a seleção atual.")

        # --- Visualização dos Dados Brutos ---
        with st.expander("Visualizar Tabela de Dados Completa"):
            st.dataframe(df_filtrado)