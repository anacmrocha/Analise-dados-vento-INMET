import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def exibir_info_micro():
        st.title("📖 Guia de Análises")

        tab1, tab2 = st.tabs(["📖 Informações", "📊 Tipos de Gráficos"])


        with tab1:
            st.warning("⚠️ Os gráficos podem se apresentar no formato minimizado, clique com o mouse para maximizar")
            st.markdown(''' 
            ''')
            

        with tab2:
            st.subheader("Análises Disponíveis")
        
            col1, col2 = st.columns(2)
        
            with col1:
                with st.expander("📊Histogramas", expanded=True):
                    st.write("""
                **O que é:** Mostra a frequência com que determinadas intensidades de vento ocorrem.
                **Utilidade:** Identifica a predominância das diferentes faixas de intensidade de vento.
                """)
            
                with st.expander("📦 Boxplots"):
                    st.write("""
                **O que é:** Representa a variação dos dados.
                **Utilidade:** Excelente para identificar eventos extremos atípicos (outliers).
                """)

                with st.expander("📈 Sazonalidade"):
                    st.write("""
                **O que é:** Agrupa os dados em intervalos temporais definidos.
                **Utilidade:** Permite observar comportamentos cíclicos ao longo do tempo.
                """)

            with col2:
              

                with st.expander(" ⇄  Relação: Rajada vs. Direção"):
                    st.write("""
                **O que é:** Um gráfico polar que cruza a direção de onde o vento vem com sua intensidade.
                **Utilidade:** Permite visualizar a procedência das rajadas mais perigosas em relação às direções predominantes.
                """)

                with st.expander("🧭 Rosa dos Ventos"):
                    st.write("""    **O que é:** Gráfico polar que detalha a frequência das rajadas em diferentes direções. 
                 **Utilidade:** Indica as direções com maior incidência de registros de vento. """)

                with st.expander("💨 Velocidade vs. Rajada"):
                    st.write("""    **O que é:** Gráfico que relaciona a velocidade média do vento com a velocidade máxima das rajadas.
                **Utilidade:** Revela a correlação entre a velocidade constante e os picos de rajada. Ao plotar múltiplas estações simultaneamente
               permite comparar a relação entre os perfis de vento de diferentes locais """)

       





