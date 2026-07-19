import geopandas as gpd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pykrige.ok import OrdinaryKriging
import plotly.graph_objects as go


@st.cache_data
def calcular_krigagem(x, y, z, min_lon, max_lon, min_lat, max_lat):
    ok = OrdinaryKriging(
        x, y, z, 
        variogram_model='linear', 
        coordinates_type='geographic'
    )
    
    grid_lon = np.linspace(min_lon, max_lon, 100)
    grid_lat = np.linspace(min_lat, max_lat, 100)
    
    z_interpolado, variancia = ok.execute('grid', grid_lon, grid_lat)
    return z_interpolado, grid_lon, grid_lat

@st.fragment
def exibir_mapa_krigagem(dados_positivos, estacoes_unicas, mapa_rj):
    st.title("🌍 Análise de Krigagem")

    if not pd.api.types.is_datetime64_any_dtype(dados_positivos['Data_Hora']):
        dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])

    datas_disponiveis = sorted(dados_positivos['Data_Hora'].dt.date.unique(), reverse=True)
    dia_selecionado = st.selectbox("Selecione o Dia para Interpolação:", datas_disponiveis, key="krig_dia")

    df_dia = dados_positivos[dados_positivos['Data_Hora'].dt.date == dia_selecionado]

    if df_dia.empty:
        st.warning(f"Nenhum dado encontrado para o dia {dia_selecionado}.")
        return

    df_valores_dia = df_dia.groupby('ESTACAO')['Rajada_Máxima'].mean().reset_index()
    dados_mapa = pd.merge(df_valores_dia, estacoes_unicas, on='ESTACAO')

    x = dados_mapa['Longitude'].values
    y = dados_mapa['Latitude'].values
    z = dados_mapa['Rajada_Máxima'].values 

    # Limites do mapa
    min_lon, min_lat, max_lon, max_lat = mapa_rj.total_bounds

    # Chamada da função com cache
    with st.spinner("Processando Krigagem Geográfica..."):
        z_interpolado, _, _ = calcular_krigagem(x, y, z, min_lon, max_lon, min_lat, max_lat)

    # Plotagem
    fig, ax = plt.subplots(figsize=(12, 10))
    
  
    im = ax.imshow(z_interpolado, extent=[min_lon, max_lon, min_lat, max_lat],
                   origin='lower', cmap='viridis', alpha=0.8)

    mapa_rj.plot(ax=ax, color='none', edgecolor='black', linewidth=1.5)
    
    plt.colorbar(im, ax=ax, label='Rajada Média (km/h)')
    ax.scatter(x, y, c='red', s=30, edgecolors='black', label='Estações')

    plt.title(f"Interpolação de Rajadas - {dia_selecionado}")
    ax.legend()
    
    st.pyplot(fig)

def criar_mapa_interativo(dados_positivos, mapa_rj,estacoes_unicas):

    dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])
    st.title("🌍 Análise de Krigagem")
    dia_especifico = '2023-06-29'
    df_dia = dados_positivos[dados_positivos['Data_Hora'].dt.date == pd.to_datetime(dia_especifico).date()]

    if df_dia.empty:
        st.warning(f"Nenhum dado encontrado para o dia {dia_especifico}.")
        return

    df_valores_dia = df_dia.groupby('ESTACAO')['Velocidade_Vento'].mean().reset_index()
    dados_mapa = pd.merge(df_valores_dia, estacoes_unicas, on='ESTACAO')

    x = dados_mapa['Longitude'].values
    y = dados_mapa['Latitude'].values
    z = dados_mapa['Velocidade_Vento'].values

    ok = OrdinaryKriging(
        x, y, z, 
        variogram_model='linear', 
        coordinates_type='geographic'
    )

    min_lon, min_lat, max_lon, max_lat = mapa_rj.total_bounds
    grid_lon = np.linspace(min_lon, max_lon, 100)
    grid_lat = np.linspace(min_lat, max_lat, 100)

    z_interpolado, variancia = ok.execute('grid', grid_lon, grid_lat)

    fig = go.Figure(data=go.Contour(
            z=z_interpolado,
            x=grid_lon,
            y=grid_lat,
            colorscale='Viridis',
            contours=dict(showlines=False)
        ))
    fig.update_layout(
            title="Mapa Interativo de Velocidade do Vento",
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            hovermode="closest"
        )

    st.plotly_chart(fig)
   




