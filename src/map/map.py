import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "../../../")))

import pandas as pd
import folium
from typing import Optional, Dict, Any
import database_manager as db

# --- NOVA FUNÇÃO AUXILIAR ---
def converter_url_imgur(url: Optional[str]) -> Optional[str]:
    """
    Converte uma URL de página do Imgur em uma URL de imagem direta.
    Ex: 'https://imgur.com/aBcDeF' -> 'https://i.imgur.com/aBcDeF.jpg'
    """
    if not url or not isinstance(url, str):
        return None
    
    # Se já for um link direto (i.imgur.com), apenas retorna
    if url.startswith("https://i.imgur.com"):
        return url
        
    # Se for um link de página, converte
    if url.startswith("https://imgur.com/"):
        image_id = url.split("/")[-1]
        return f"https://i.imgur.com/{image_id}.jpg" # .jpg é um padrão seguro

    return url # Retorna a URL original se não corresponder aos padrões conhecidos


def gerar_mapa_de_marcadores_html(zoom_start: int = 12) -> Optional[str]:
    """
    Gera um mapa Folium com marcadores, com popups responsivos que não saem da tela.
    """
    print("Buscando dados de análise do banco de dados...")
    dados_do_banco = db.get_all_analyses_for_map()

    if not dados_do_banco:
        print("Nenhum dado com coordenadas encontrado no banco de dados para gerar o mapa.")
        return None

    df = pd.DataFrame(dados_do_banco)
    df['lat'] = pd.to_numeric(df['lat'])
    df['lon'] = pd.to_numeric(df['lon'])

    def cor_icone(indice_str: Optional[str]) -> str:
        if not isinstance(indice_str, str): return 'gray'
        lower_indice = indice_str.lower()
        if any(keyword in lower_indice for keyword in ['baixo', 'fraco', 'inexistente']): return 'red'
        if 'moderado' in lower_indice or 'médio' in lower_indice: return 'orange'
        if 'forte' in lower_indice or 'alto' in lower_indice: return 'green'
        return 'gray'

    centro = [df.iloc[0]['lat'], df.iloc[0]['lon']]
    m = folium.Map(location=centro, zoom_start=zoom_start, tiles="cartodbpositron")

    print(f"Adicionando {len(df)} marcadores ao mapa...")
    for _, row in df.iterrows():
        indice_atual = row.get('indice_cpted_geral', 'N/A')
        original_url = row.get('capture_url')
        imagem_url_direta = converter_url_imgur(original_url)

        imagem_html = ""
        if imagem_url_direta:
            imagem_html = f"""
            <a href="{original_url}" target="_blank" title="Clique para ver no Imgur">
                <img src="{imagem_url_direta}" alt="Imagem da Análise" style="width:100%; border-radius:5px; margin-top:10px;">
            </a>
            """
        
        # --- POPUP COM CSS RESPONSIVO ---
        popup_html = f"""
        <div style="width: 280px; max-height: 250px; overflow-y: auto; word-wrap: break-word; font-family: sans-serif; font-size: 14px;">
          <h4 style="margin:0 0 10px 0;font-size:16px;">{row.get('titulo_analise', 'Análise Sem Título')}</h4>
          <b>Índice CPTED Geral:</b> {indice_atual}<br>
          <details style="margin-top:10px;">
            <summary style="cursor:pointer;color:blue;font-size:12px;">Ver detalhes</summary>
            <ul style="padding-left:20px;margin-top:5px; font-size:12px; list-style-type: square;">
              <li><b>Data:</b> {row.get('data_processamento').strftime('%d/%m/%Y %H:%M') if row.get('data_processamento') else 'N/A'}</li>
              <li><b>Resumo:</b> {row.get('resumo_executivo', 'N/A')}</li>
              <li><b>Recomendações:</b> {row.get('recomendacoes', 'N/A')}</li>
            </ul>
          </details>
          {imagem_html}
        </div>
        """
        
        folium.Marker(
            [row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row.get('titulo_analise', ''),
            icon=folium.Icon(color=cor_icone(indice_atual), icon='shield-alt', prefix='fa')
        ).add_to(m)

    print("Geração do mapa de marcadores concluída.")
    return m._repr_html_()

# Exemplo de uso:
if __name__ == "__main__":
    html_mapa = gerar_mapa_de_marcadores_html()

    if html_mapa:
        with open("mapa_de_marcadores_com_imagens.html", "w", encoding='utf-8') as f:
            f.write(html_mapa)
        print("\nMapa salvo com sucesso em 'mapa_de_marcadores_com_imagens.html'")
