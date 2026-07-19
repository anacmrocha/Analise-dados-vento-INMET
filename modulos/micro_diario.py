import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def exibir_heatmap_diario(dados_positivos):
    st.title("🌡️ Heatmap: Intensidade Horária por Dia")
    
    estacoes = sorted(dados_positivos['ESTACAO'].unique())
    estacao = st.selectbox("Selecione a Estação:", estacoes, key="hm_estacao")
    
    dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])
    anos = sorted(dados_positivos['Data_Hora'].dt.year.unique())
    ano = st.selectbox("Selecione o Ano:", anos, key="hm_ano")
    
    meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_selecionado = st.selectbox("Selecione o Mês:", meses_nomes, key="hm_mes")
    mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}

    
    # 2. Filtragem
    df_foco = dados_positivos[
        (dados_positivos['ESTACAO'] == estacao) &
        (dados_positivos['Data_Hora'].dt.year == ano) &
        (dados_positivos['Data_Hora'].dt.month == mapa_meses[mes_selecionado])
    ].copy()
    
    df_foco['Dia'] = df_foco['Data_Hora'].dt.day
    df_foco['Hora'] = df_foco['Data_Hora'].dt.hour

    matriz_rajadas = df_foco.pivot_table(
        index='Hora',
        columns='Dia',
        values='Rajada_Máxima',
        aggfunc='mean'
    )
    
    # 4. Plotagem
    if not matriz_rajadas.empty:
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # O fmt=".0f" é melhor para rajadas médias, mas você pode usar .1f se preferir precisão
        sns.heatmap(matriz_rajadas, cmap='YlOrRd', annot=True, fmt=".1f", ax=ax, linewidths=.5)
        
        ax.set_title(f'Rajadas Máximas por Hora e Dia - {estacao} ({mes_selecionado}/{ano})')
        ax.set_xlabel('Dia do Mês')
        ax.set_ylabel('Hora do Dia (UTC)')
        
        st.pyplot(fig)
    else:
        st.warning("Não há dados suficientes para gerar o heatmap neste período.")




