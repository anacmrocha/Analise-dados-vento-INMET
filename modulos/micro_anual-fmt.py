import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import StrMethodFormatter
from matplotlib.colors import to_rgba


@st.fragment
def exibir_micro_anual(dados_positivos):
    st.title("Análise Micro - Anual")

    variaveis_opcoes = ["Rajada Máxima", "Velocidade do Vento"]
    variaveis_escolhidas = st.multiselect(
        "Selecione as variáveis para o gráfico:",
        options=variaveis_opcoes,default=["Rajada Máxima"] 
    )

    if not variaveis_escolhidas:
        st.warning("Por favor, selecione pelo menos uma variável para visualização.")
        st.stop()

    mapa_colunas = {
        "Rajada Máxima": "Rajada_Máxima",
        "Velocidade do Vento": "Velocidade_Vento"
        }
    colunas_foco = [mapa_colunas[v] for v in variaveis_escolhidas]


    st.title("📊 Distribuições")
    st.write(f"Analisando: Velocidade e Rajada")
    
    dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])

    estacoes = sorted(dados_positivos['ESTACAO'].unique())
    opcoes_estacoes = ["Todas as estações"] + list(estacoes)
    estacao = st.selectbox("Selecione a Estação:", opcoes_estacoes, key="estacao_micro_anual")
    
    anos = sorted(dados_positivos['Data_Hora'].dt.year.unique())
    opcoes_anos = ["Todos os anos"] + list(anos)
    ano = st.selectbox("Selecione o Ano:", opcoes_anos, key="ano_micro_anual")

    meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}
    mes_selecionado = st.selectbox("Selecione o Mês:", ["Todos os meses"] + meses_nomes, key="mes_micro_anual")

    df_foco = dados_positivos.copy()
    
    if estacao != "Todas as estações":
        df_foco = df_foco[df_foco['ESTACAO'] == estacao]
    
    if ano != "Todos os anos":
        df_foco = df_foco[df_foco['Data_Hora'].dt.year == int(ano)]

    if mes_selecionado != "Todos os meses":
        df_foco = df_foco[df_foco['Data_Hora'].dt.month == mapa_meses[mes_selecionado]]

    if ano == "Todos os anos" and mes_selecionado == "Todos os meses":
        titulo_temp = "Todos os anos e todos os meses"
    elif ano == "Todos os anos":
        titulo_temp = f"Todos os anos - {mes_selecionado}"
    elif mes_selecionado == "Todos os meses":
        titulo_temp = f"{ano} - Todos os meses"
    else:
        titulo_temp = f"{mes_selecionado}/{ano}"

    tipo_grafico = st.radio("Escolha a análise:", ["Histograma", "Sazonalidade", "Boxplot"])

    df_melted = df_foco.melt(
        id_vars=['ESTACAO', 'Data_Hora'], # Colunas que permanecem fixas
        value_vars=colunas_foco, # Colunas que serão "derretidas"
        var_name='Variável', 
        value_name='Valor'
        )

    if not df_foco.empty:
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 5))

        if tipo_grafico == "Histograma":
            bins = np.arange(0, 52, 2)
            sns.histplot(data=df_melted, x='Valor', hue='Variável', bins=bins, ax=ax, kde=True, element="step")
            ax.set_title(f"Distribuição: {estacao} ({titulo_temp})")

            formatter = ScalarFormatter(useOffset=False)
            formatter.set_scientific(False)
            ax.yaxis.set_major_formatter(formatter)
            ax.yaxis.get_offset_text().set_visible(False)


        elif tipo_grafico == "Sazonalidade":
            agregacao = st.radio("Escolha a métrica:", ["Média", "Máximo"], horizontal=True)
            metrica = 'mean' if agregacao == "Média" else 'max'

            if mes_selecionado != "Todos os meses":
                df_foco['Dia'] = df_foco['Data_Hora'].dt.day
                df_plot = df_foco.groupby('Dia')[colunas_foco].agg(metrica).reindex(range(1, 32), fill_value=0).reset_index()
                df_plot_melted = df_plot.melt(id_vars='Dia', var_name='Variável', value_name='Valor')
                sns.lineplot(data=df_plot_melted, x='Dia', y= 'Valor',  hue='Variável', ax=ax, marker='o')
            else:
                df_plot = df_foco.groupby(df_foco['Data_Hora'].dt.month)[colunas_foco].agg(metrica).reset_index()
                mapa_inverso = {v: k for k, v in mapa_meses.items()}
                df_plot['Mes'] = df_plot['Data_Hora'].map(mapa_inverso)
                df_plot_melted = df_plot.melt(id_vars='Mes', value_vars=colunas_foco, var_name='Variável', value_name='Valor')
                sns.lineplot(data=df_plot_melted, x='Mes', y='Valor',hue='Variável', ax=ax, marker='o')
            
            ax.set_title(f"Evolução Temporal ({agregacao}):  {estacao} - {titulo_temp}")
            plt.xticks(rotation=45)

        elif tipo_grafico == "Boxplot":
            if estacao == "Todas as estações":
                sns.boxplot(data=df_melted, x='Valor', y='ESTACAO', hue='ESTACAO', ax=ax, palette="viridis")
            else:
                sns.boxplot(data=df_melted, x='Variável', y='Valor', ax=ax, palette="Set2")
            ax.set_title(f"Dispersão: {estacao} ({titulo_temp})")
            ax.set_ylabel("m/s")
        st.subheader("Escolha exclusivamente uma única opção de análise para visualizar o gráfico correspondente.")")
        st.pyplot(fig, use_container_width=True)

@st.fragment
def exibir_micro_estatistica(dados_positivos):
    st.title("📊 Estatísticas Descritivas")
    st.write("Análise detalhada de velocidades e rajadas por estação e ano.")

    dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])
    col1, col2, col3 = st.columns(3)
    
    with col1:
        estacoes = sorted(dados_positivos['ESTACAO'].unique())
        opcoes_estacoes = ["Todas as estações"] + list(estacoes)
        estacao = st.selectbox("Selecione a Estação:", opcoes_estacoes, key="stat_estacao")
    
    with col2:
        anos = sorted(dados_positivos['Data_Hora'].dt.year.unique())
        opcoes_anos = ["Todos os anos"] + list(anos)
        ano = st.selectbox("Selecione o Ano:", opcoes_anos, key="stat_ano")

    with col3:
        meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}
        mes_selecionado = st.selectbox("Selecione o Mês:", ["Todos os meses"] + meses_nomes, key="stat_mes")
    

    df_foco = dados_positivos.copy()
    
    if estacao != "Todas as estações":
        df_foco = df_foco[df_foco['ESTACAO'] == estacao]
    
    if ano != "Todos os anos":
        df_foco = df_foco[df_foco['Data_Hora'].dt.year == int(ano)]

    if mes_selecionado != "Todos os meses":
        df_foco = df_foco[df_foco['Data_Hora'].dt.month == mapa_meses[mes_selecionado]]

    colunas_stats = ['Velocidade_Vento', 'Rajada_Máxima']

    # titulos dinamicos para os graficos
    if ano == "Todos os anos" and mes_selecionado == "Todos os meses":
        titulo_temp = "Todos os anos e todos os meses"
    elif ano == "Todos os anos":
        titulo_temp = f"Todos os anos - {mes_selecionado}"
    elif mes_selecionado == "Todos os meses":
        titulo_temp = f"{ano} - Todos os meses"
    else:
        titulo_temp = f"{mes_selecionado}/{ano}"
    
    if not df_foco.empty:
        stats = df_foco[colunas_stats].agg(['mean', 'max', lambda x: x.quantile(0.95), lambda x: x.quantile(0.99)])
        stats.index = ['Média', 'Máximo', 'Percentil 95', 'Percentil 99']
        
        st.subheader(f"Resumo Estatístico: {estacao} ({titulo_temp})")
        st.dataframe(stats.style.format("{:.2f}"), use_container_width=True)
        
        st.info("""
        **Entendendo os Percentis:**
        * **Percentil 95**: 95% das rajadas registradas neste ano foram inferiores a este valor.
        * **Percentil 99**: Indica o limite superior de eventos extremos (apenas 1% das rajadas superaram este valor).
        """)


@st.fragment
def rajada_direcao(dados_positivos):
    st.title("⇄ Relação: Rajada vs. Direção")

    dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])

    estacoes = sorted(dados_positivos['ESTACAO'].unique())
    opcoes_estacoes = ["Todas as estações"] + list(estacoes)
    estacao = st.selectbox("Selecione a Estação:", opcoes_estacoes, key="dir_raj_estacao")
    
    anos = sorted(dados_positivos['Data_Hora'].dt.year.unique())
    opcoes_anos = ["Todos os anos"] + list(anos)
    ano = st.selectbox("Selecione o Ano:", opcoes_anos, key="dir_raj_ano")

    meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}
    mes_selecionado = st.selectbox("Selecione o Mês:", ["Todos os meses"] + meses_nomes, key="dir_raj_mes")

    df_foco = dados_positivos.copy()
    
    
    if estacao != "Todas as estações":
        df_foco = df_foco[df_foco['ESTACAO'] == estacao]
    
    if ano != "Todos os anos":
        df_foco = df_foco[df_foco['Data_Hora'].dt.year == int(ano)]

    if mes_selecionado != "Todos os meses":
        df_foco = df_foco[df_foco['Data_Hora'].dt.month == mapa_meses[mes_selecionado]]

    # titulos dinamicos para os graficos
    if ano == "Todos os anos" and mes_selecionado == "Todos os meses":
        titulo_temp = "Todos os anos e todos os meses"
    elif ano == "Todos os anos":
        titulo_temp = f"Todos os anos - {mes_selecionado}"
    elif mes_selecionado == "Todos os meses":
        titulo_temp = f"{ano} - Todos os meses"
    else:
        titulo_temp = f"{mes_selecionado}/{ano}"
    
    if not df_foco.empty:
        limite = df_foco['Rajada_Máxima'].quantile(0.95)
        df_extremos = df_foco[df_foco['Rajada_Máxima'] >= limite].copy()
        
        radianos = np.deg2rad(df_extremos['Direção_Vento_gr'])

        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111, projection='polar')
        
        # plot com transparência
        sc = ax.scatter(radianos, df_extremos['Rajada_Máxima'], 
                        c=df_extremos['Rajada_Máxima'], cmap='Reds', alpha=0.5, edgecolors='none')
        
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        
        plt.colorbar(sc, label='Intensidade da Rajada (m/s)', pad=10)
        plt.title(f'Direção das Rajadas Extremas (P95+) - {estacao}: {titulo_temp}', pad=20)
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("Não há dados suficientes para este ano.")



@st.fragment
def relacao_velocidade_rajada(dados_positivos):
    st.title("🌪️ Relação: Velocidade vs. Rajada")
    dados_positivos['Data_Hora'] = pd.to_datetime(dados_positivos['Data_Hora'])

    col1, col2 = st.columns(2)
    with col1:
        anos = sorted(dados_positivos['Data_Hora'].dt.year.unique())
        opcoes_anos = ["Todos os anos"] + list(anos)
        ano = st.selectbox("Selecione o Ano:", opcoes_anos, key="relacao_ano")
    
    with col2:
        meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}
        mes_selecionado = st.selectbox("Selecione o Mês:", ["Todos os meses"] + meses_nomes, key="relacao_mes")
        
    estacoes_disponiveis = sorted(dados_positivos['ESTACAO'].unique())
    estacoes_selecionadas = st.multiselect("Selecione as Estações para comparação:", 
                                           estacoes_disponiveis, 
                                           default=estacoes_disponiveis[:2],
                                           key="rel_estacoes")

    df_foco = dados_positivos.copy()
    
    if ano != "Todos os anos":
        df_foco = df_foco[df_foco['Data_Hora'].dt.year == int(ano)]

    if mes_selecionado != "Todos os meses":
        df_foco = df_foco[df_foco['Data_Hora'].dt.month == mapa_meses[mes_selecionado]]

    if estacoes_selecionadas:
        df_foco = df_foco[df_foco['ESTACAO'].isin(estacoes_selecionadas)]

    # titulos dinamicos para os graficos
    if ano == "Todos os anos" and mes_selecionado == "Todos os meses":
        titulo_temp = "Todos os anos e todos os meses"
    elif ano == "Todos os anos":
        titulo_temp = f"Todos os anos - {mes_selecionado}"
    elif mes_selecionado == "Todos os meses":
        titulo_temp = f"{ano} - Todos os meses"
    else:
        titulo_temp = f"{mes_selecionado}/{ano}"

    if not df_foco.empty and len(estacoes_selecionadas) > 0:
        fig = sns.lmplot(
            x='Velocidade_Vento', 
            y='Rajada_Máxima', 
            hue='ESTACAO', 
            data=df_foco, 
            scatter_kws={'alpha': 0.3},
            height=6, 
            aspect=1.5
        )
        plt.title(f"Relação Vento Médio vs Rajada - {titulo_temp}")
        plt.xlabel("Velocidade Horária (m/s)")
        plt.ylabel("Rajada Máxima (m/s)")
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("Selecione pelo menos uma estação e verifique se há dados para o período.")


@st.fragment
def rosa_dos_ventos(dados_positivos):
    st.title("🧭 Rosa dos Ventos")

    estacoes = sorted(dados_positivos['ESTACAO'].unique())
    opcoes_estacoes = ["Todas as estações"] + list(estacoes)
    estacao = st.selectbox("Selecione a Estação:", opcoes_estacoes, key="rosa_estacao")
    
    anos = sorted(dados_positivos['Data_Hora'].dt.year.unique())
    opcoes_anos = ["Todos os anos"] + list(anos)
    ano = st.selectbox("Selecione o Ano:", opcoes_anos, key="rosa_ano")

    meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}
    mes_selecionado = st.selectbox("Selecione o Mês:", ["Todos os meses"] + meses_nomes, key="rosa_mes")
    
    df_foco = dados_positivos.copy()
    
    if estacao != "Todas as estações":
        df_foco = df_foco[df_foco['ESTACAO'] == estacao]
    
    if ano != "Todos os anos":
        df_foco = df_foco[df_foco['Data_Hora'].dt.year == int(ano)]

    if mes_selecionado != "Todos os meses":
        df_foco = df_foco[df_foco['Data_Hora'].dt.month == mapa_meses[mes_selecionado]]

    # titulos dinamicos para os graficos
    if ano == "Todos os anos" and mes_selecionado == "Todos os meses":
        titulo_temp = "Todos os anos e todos os meses"
    elif ano == "Todos os anos":
        titulo_temp = f"Todos os anos - {mes_selecionado}"
    elif mes_selecionado == "Todos os meses":
        titulo_temp = f"{ano} - Todos os meses"
    else:
        titulo_temp = f"{mes_selecionado}/{ano}"

    if not df_foco.empty:
        radianos = np.deg2rad(df_foco['Direção_Vento_gr'])
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
        ax.hist(radianos, bins=16, edgecolor='black', color='skyblue', alpha=0.7)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        
        ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        
        plt.title(f'Direção do Vento - {estacao}\n({titulo_temp})', pad=40)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    else:
        st.warning("Não há dados de direção disponíveis para esta seleção.")