from modulos import info_micro, paginainicial, conclusoes, micro_anual, micro_diario, krigagem, info_krig
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd

def aplicar_estilo():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1f2b 0%, #121722 100%);
            border-right: 2px solid #2b3445;
            box-shadow: 5px 0px 15px rgba(0,0,0,0.5);
        }
        
        [data-testid="stSidebar"] div {
            color: #e6e6e6 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Altera a fonte da sidebar */
        }
        .main {
            background-color: #0e1117; /* Garante o fundo escuro no centro */
            font-family: 'Helvetica', sans-serif; /* Define a fonte do centro */
        }

        /* Altera especificamente a cor e fonte de todos os textos do centro */
        .main div, .main p, .main span {
            color: #ffffff !important;
            font-family: 'Helvetica', sans-serif !important;
        }

        /* 3. BOTÕES (Já existente) */
        div.stButton > button {
            border-radius: 8px;
            border: 1px solid #2b3445;
            background-color: #1a1f2b;
            color: white;
            transition: 0.3s;
        }
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo()


@st.cache_data
def carregar_coordenadas():
    return pd.read_csv("estacoes_unicas.csv")
estacoes_unicas = carregar_coordenadas()


@st.cache_data
def carregar_mapa():
    mapa = gpd.read_file("mapario.json")
    return mapa
mapa_rj = carregar_mapa()

@st.cache_data
def carregar_dados_positivos():
    return pd.read_csv("DadoStreamlit_positivos.csv")
dados_positivos= carregar_dados_positivos()

@st.cache_data
def carregar_dados():
    return pd.read_csv("DadoStreamlit.csv")

dados = carregar_dados()



if "pagina" not in st.session_state:
    st.session_state.pagina = "Página Inicial"

with st.sidebar:
    st.header("Navegação")
    
    if st.button("🏠 Página Inicial"):
        st.session_state.pagina = "Página Inicial"

    # Expand de Análise 
    with st.expander("📊 Análise"):
        if st.button("📖 Guia"):
            st.session_state.pagina = "info_micro"
        if st.button("📅 Anual e Mensal"):
            st.session_state.pagina = "micro_anual"
       
        if st.button("🌡️ Heatmap - Diário"):
            st.session_state.pagina = "micro_diario" 

    with st.expander("🗺️ KRIGAGEM"):
        if st.button("📌 Informações"):
            st.session_state.pagina = "info_krig"
        if st.button("🗺️ Mapa diário"):
            st.session_state.pagina = "krigagem"

    if st.button("💡 Conlclusões e Insights"):
        st.session_state.pagina = "conclusao"

# Lógica de exibição da tela principal
if st.session_state.pagina == "Página Inicial":
    paginainicial.abertura(dados_positivos, estacoes_unicas, mapa_rj, dados)

elif st.session_state.pagina == "micro_anual":
    micro_anual.exibir_micro_anual(dados_positivos)
    micro_anual.exibir_micro_estatistica(dados_positivos)
    micro_anual.relacao_velocidade_rajada(dados_positivos)
    micro_anual.rajada_direcao(dados_positivos)
    micro_anual.rosa_dos_ventos(dados_positivos)


elif st.session_state.pagina == "micro_diario":
    st.title("Análise Micro - Visão diária")
    micro_diario.exibir_heatmap_diario(dados_positivos)


elif st.session_state.pagina == "krigagem":
    krigagem.exibir_mapa_krigagem(dados_positivos, estacoes_unicas, mapa_rj)

elif st.session_state.pagina == "conclusao":
    conclusoes.conclusao(dados_positivos)

elif st.session_state.pagina == "info_micro":
    info_micro.exibir_info_micro()

elif st.session_state.pagina == "info_krig":
    info_krig.exibir_info_krig()

