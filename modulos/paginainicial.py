import geopandas as gpd
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from modulos.conclusoes import conclusao, colorir_risco, mostrar_escala_beaufort


def plotar_mapa_estacoes(estacoes_unicas, mapa_rj):

    gdf_estacoes = gpd.GeoDataFrame(
    estacoes_unicas, 
    geometry=gpd.points_from_xy(estacoes_unicas.Longitude, estacoes_unicas.Latitude)
    )
    gdf_estacoes.set_crs(epsg=4326, inplace=True)

    mapa_rj = mapa_rj.to_crs(epsg=4326)
    fig, ax = plt.subplots(figsize=(12, 10))

    mapa_rj.plot(ax=ax, color='lightgray', edgecolor='white')
    gdf_estacoes.plot(ax=ax, color='red', markersize=50, label='Estações INMET')
    
    # Adicionar rótulos
    for _, row in gdf_estacoes.iterrows():
        ax.text(row['Longitude'], row['Latitude'], s=row['ESTACAO'], 
                fontsize=7, color='black', fontweight='bold')

    plt.title("Estações Meteorológicas - Estado do Rio de Janeiro")
    plt.legend()
    st.pyplot(fig)

def abertura(dados_positivos, estacoes_unicas, mapa_rj, dados):
    # 1. Título e Subtítulo com Emojis
    st.title("Análise de dados de Vento do INMET")
    st.subheader("Estações automáticas do estado do **Rio de Janeiro**")

    
    # 2. Layout em Colunas para a Seção de Introdução
    col1, col2 = st.columns([2, 3], vertical_alignment="center")
    
    with col1:
        st.markdown(f"""
        Bem-vindo ao nosso Dashboard de Análise de dados de Vento do INMET! 👋🏻
        """)
        st.markdown(''' Neste site apresentamos uma análise detalhada dos dados de vento do **INMET** (Instituto Nacional de Meteorologia). O período análisado é referente aos
anos de **2018** à **2025**. A análise será realizada utilizando técnicas de visualização de dados e estatísticas descritivas.
 ''')
    
    with col2:
        # Uso da "bala de prata" para ajuste automático de imagem
        st.image("inmet.png", use_container_width=True)

    st.markdown("---")

    # 3. Métricas em destaque para quebrar o "estilo PDF"
    m1, m2, m3= st.columns(3)
    m1.metric("Período Analisado", "2018 — 2025")
    m3.metric("Estações ativas", "27")
    m2.metric("Estado analisado", "Rio de Janeiro")

    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 🎯 Nosso Objetivo")
        st.write("""
        O principal **objetivo** da nossa análise é entender o comportamento dos dados,
       buscar **eventos extremos**, possíveis relações e oferecer insigts.
        """)

    st.markdown("---")

    pag1, pag2, pag3, pag4 = st.tabs(["Descrição", "Informações dos Dados", "Limpeza", "Links e Fontes"])
    with pag1:
        st.subheader(" 📌 Descrição")
        with st.expander(" Estrutura do Dashboard (clique para expandir)"):
            st.markdown(''' 
            * **Página Inicial**: informações gerais sobre os dados.
            * **Análise**: visualização interativa dos gráficos.
            * **Conclusões e insights**: síntese dos resultados e insights extraídos.
        ''')
        with st.expander("Sobre as seções "):
            st.markdown('''
            * A seção de Análise é proposta no formato interativo a fim de otimizar a exploração de dados. Note que além de estruturar as informações, tal ferramenta
           permite que outros usuários explorem e extraiam suas próprias conclusões e insights. 
            * Para auxiliar na interpretação, incluímos um Guia que detalha a função de cada gráfico, apresentando as 
            justificativas técnicas para a escolha de cada representação visual. 
            * A Conclusão é apresentada de forma objetiva, estruturada em duas seções: geral e detalhada.
            ''')
        
        estacoes = [
        "ANGRA DOS REIS", "CAMBUCI", "XEREM", "MARAMBAIA", "CAMPOS DOS GOYTACAZES",
        "PARATY", "TRES RIOS", "FORTE DE COPACABANA", "VALENCA", "SILVA JARDIM",
        "ARRAIAL DO CABO", "TERESOPOLIS-PARQUE NACIONAL", "MACAE", "RIO DE JANEIRO - VILA MILITAR",
        "RIO DE JANEIRO - JACAREPAGUA", "SEROPEDICA-ECOLOGIA AGRICOLA", "RIO CLARO",
        "PICO DO COUTO", "RESENDE", "NOVA FRIBURGO - SALINAS", "CAMPOS DOS GOYTACAZES - SAO TOME",
        "SAQUAREMA - SAMPAIO CORREIA", "NITEROI", "CARMO", "SANTA MARIA MADALENA",
        "ITATIAIA", "Paty do Alferes - Avelar"
    ]

        with st.expander(f"📊 {len(estacoes)} estações incluídas na análise (clique para expandir)"):
            st.write("Lista das estações automáticas:")
            st.columns(3) 
            for estacao in estacoes:
                st.markdown(f"- {estacao}")

        st.subheader(" 📍 Mapa do estado do Rio de Janeiro")
        plotar_mapa_estacoes(estacoes_unicas, mapa_rj)
        st.subheader("📋 Tabela de dados")
        st.dataframe(dados_positivos)

    with pag2:
        st.subheader(" 📊 Informações dos dados")
        st.markdown(''' Para garantir a coerência da análise, é fundamental considerar previamente os conceitos básicos do vento e a natureza dos dados observados.
       Ao utilizarmos a [Escala de Beaufort](https://pt.wikipedia.org/wiki/Escala_de_Beaufort) como referência,
       traduzimos significado físico aos registros numéricos de velocidade.
    
    ''')
        mostrar_escala_beaufort()
        st.subheader("🧐 Observações")
        st.markdown(''' Para fins de classificação meteorológica, deve-se priorizar o vento sustentado em detrimento de picos isolados. Segundo o [National Hurricane Center Product Description Document](https://www.nhc.noaa.gov/pdf/NHC_Product_Description.pdf), eventos extremos de vento, como ciclones ou furacões, são definidos pela força média do vento mantida (sustentada por 1 minuto), 
        e não apenas por marcações numéricas momentâneas ou rajadas  ''')
        st.subheader("📖 Registro dos dados")
        st.markdown(""" 
        * **DIREÇÃO DO VENTO:**
        Nas estações automáticas é a medida em graus angulares da direção do vento (de onde o vento vem). Este valor é a média dos últimos 10 minutos antes de cada hora, de envio da mensagem de dados.
        * **VELOCIDADE DO VENTO:**
        Nas estações automáticas é a medida da velocidade do vento. Este valor é a média dos últimos 10 minutos antes de cada hora, de envio da mensagem de dados.
        * **RAJADA MÁXIMA:**
        Nas estações automáticas é a medida máxima da velocidade do vento, ocorrida na última hora antes de cada mensagem de dados.
        """)

        st.markdown(
        "**Fonte:** [Glossário - INMET](https://portal.inmet.gov.br/glossario/glossario)"
    )

        st.markdown("---")



    with pag3:
        st.subheader("🧹 Limpeza dos dados")
        st.markdown('''
        * Os dados foram obtidos do site oficial do INMET, que disponibiliza informações meteorológicas de diversas regiões do Brasil.
        * Não foram realizados tratamento nos dados, apenas foram excluídos valores negativos para evitar distorções de análise
        ''')
        st.write("Percentual de registros removidos")
        total_por_estacao = dados['ESTACAO'].value_counts()
        validos_por_estacao = dados_positivos['ESTACAO'].value_counts()

        df_analise = pd.DataFrame({
        'Total_Registros': total_por_estacao,
        'Validos': validos_por_estacao}).dropna()

        df_analise['Porcentagem_Perdida'] = (
            (df_analise['Total_Registros'] - df_analise['Validos']) / df_analise['Total_Registros']) * 100

        df_display = df_analise.copy()
        df_display['Porcentagem_Perdida'] = df_display['Porcentagem_Perdida'].map('{:.2f}%'.format)
        st.dataframe(df_display, use_container_width=True)

        if df_analise['Porcentagem_Perdida'].max() > 20:
            st.warning("⚠️ Algumas estações apresentam uma perda superior a 20% dos dados.")

    with pag4:
        st.subheader("🔗 Lins")
        st.markdown("""
        * [Site INMET](https://portal.inmet.gov.br/)
        * [Site National Hurricane Center](https://www.nhc.noaa.gov/)
        """)
    





