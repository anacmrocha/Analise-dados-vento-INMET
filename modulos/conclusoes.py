import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def conclusao(dados_positivos):
    st.subheader("💡 Conclusões e Insights")
    
    st.markdown("---")

    pag1, pag2= st.tabs(["Geral", "Detalhada"])
    
    with pag1:
        st.subheader(" 🌐 Visão Geral dos Dados")
   
        st.success("#### Qualidade dos Dados")
        st.write("Os dados apresentam um nível de qualidade adequado para a análise exploratória.")
   
        st.warning("#### Classificação de eventos")
        st.write("Não é possível confirmar a classificação de eventos extremos (furacões e ciclones tropicais) com base nos dados.")

        st.divider() 
    
        st.subheader("📅 Padrões Sazonais de Intensidade")
        c1, c2 = st.columns(2)
    
        with c1:
            st.info("#### 📉 Menor Intensidade")
            st.markdown("""
            * **Abril**
            * **Maio**
            * **Junho**
            """)
        
        with c2:
            st.error("#### 📈 Maior Intensidade")
            st.markdown("""
            * **Setembro**
            * **Outubro**
            * **Novembro**
            """)

        st.subheader(" ⇄ Relação - Direção versus Rajada")
        st.write(" As rajadas mais severas coincidem com as direções de maior incidência de ventos")

        ranking = (dados_positivos.groupby('ESTACAO')['Rajada_Máxima']
                   .max()
                   .sort_values(ascending=False)
                   .head(5)
                   .reset_index())
        ranking.columns = ['Estação', 'Rajada Máxima (m/s)']
        ranking.index = ranking.index + 1
        st.subheader("🏆 Top 5 Estações - Maiores Rajadas Registradas")

        st.dataframe(
            ranking, 
            use_container_width=True,
            hide_index=False
        )
    with pag2:
        st.subheader(" 💡 Conclusão - Qualidade dos dados")
        st.markdown(''' Considerando o histograma de todas as estações ao longo dos anos, observamos uma Distribuição Assimétrica à Direita. ''')
        st.image("histogramatudo1.png", width=700)
        st.markdown(''' Essa é a forma esperada para velocidade de vento, uma vez que a física do vento em condições normais tende a velocidades baixas/moderadas, enquanto os eventos extremos são as 
        exceções que formam essa cauda à direita. Portanto, isso evidencia um certo nível de qualidade dos dados.''')
        st.markdown(''' Ao mudar para o histograma de todas as estações  anualmente, podemos observar coerentemente 
        a mesma distribuição com variações em seu grau de [curtose](https://pt.wikipedia.org/wiki/Curtose]) ''')

        imagens = ["histo_angra.png", "histo_macae.png", "histo_marambaia.png"]
        legendas = ["ANGRA DOS REIS", "MACAE", "MARAMBAIA"]
        cols = st.columns(3)
        for i, img in enumerate(imagens):
            cols[i % 3].image(img, caption=legendas[i], use_container_width=True)

        st.subheader("💡Insight - Direcionamento das análises")
        st.markdown(''' Considerando a análise de todas as estações ao longo dos anos, 
        o boxplot comparativo permite visualizar a dispersão e a distribuição dos dados. ''')

        st.image("boxplottudo.png", width=700)

        st.markdown('''Em razão do nosso objetivo principal, se faz necessário a pontuação de conceitos para uma melhor interpretação dos dados. A partir da *Escala de Beaufort*, seria possível concluir que algumas
        estações sofreram fenômenos como furacões, entretanto, essa análise preliminar requer validação. 
             ''')
  

        st.markdown( '''Por exemplo, considerando a estação Pico do Couto em março de 2018, identificamos picos de magnitude extrema. Na ocasião, a rajada máxima atingiu 49 m/s (aprox. 176 km/h), valor que, segundo a Escala Modificada de Beaufort, 
         situa-se no Grau 12, caracterizando um evento de potencial impacto devastador.''')

        st.image("sazonalidadepicodocouto1.png", width=700)

        st.markdown(''' Entretanto, de acordo com os protocolos do NHC (Nacional Hurricane Center), para classificar um fenômeno intenso como um furacão, os ventos devem ser mantidos por um período de pelo menos 10 minutos. 
            Assim, podemos concluir que a partir da estrutura dos dados do INMET (Página Inicial), as rajadas máximas atuam como indicadores do potencial de impacto imediato, enquanto a velocidade média do vento valida **ou não** a magnitude e a organização do fenômeno, uma vez que a velocidade média é referente a média dos últimos 10 minutos antes de cada hora.
            ''')
        st.markdown('''Abaixo consideramos o gráfico de correlação entre a velocidade média e a rajada máxima.    ''')

        st.image("relacaovel-raj.png", width=700)

        st.markdown(''' Com base no gráfico acima, nas fontes consultadas e na estrutura de registro 
            dos dados, não é possível confirmar a classificação do fenômeno. ''')

        st.subheader("💡Conclusões - Sazonalidade")
        st.markdown(''' Para uma análise coerente da sazonalidade, vamos considerar a **média** das rajadas/velocidades no contexto macro (todas as estações). A justificativa é clara; se considerarmos o **máximo**, é evidente que distorções ocorrerão. Por exemplo, considerando a
        estação Pico do Couto, que mencionada acima apresenta a característica de rajadas intensas em comparação com outras estações, a análise da sazonalidade no contexto macro se resumiria a analisar especificamente o comportamento dos dados desta.
             ''')
        st.image("sazonalidade-tudo.png", width=900)
        st.markdown('''
        Uma conclusão possível que podemos extrair do gráfico acima é:

        * Existe uma **menor** intensidade no vento nos meses:
	        * Abril
	        * Maio
	        * Junho

        * Existe uma maior intensidade no vento nos meses:
	        * Setembro
	        * Outubro
	        * Novembro
        ''')
        st.markdown(''' Note que estamos considerando a média de 27 estações, sendo assim, devemos enfatizar que as conclusões 
            acima apenas nos oferecem um indicativo geral, distante de ser uma regra. ''')
        st.markdown(''' 
            Ao analisarmos individualmente as estações, nos deparamos com variações nos períodos citados acima, como por exemplo;
             ''')
        imagens_1 = ["sazo-arraial.png", "sazo-pico.png", "sazo-vila.png"]
        legendas_1 = ["Arraial do Cabo", "Pico do Couto", "Vila Militar 3"]
        cols = st.columns(3)
        for i, img in enumerate(imagens_1):
            cols[i % 3].image(img, caption=legendas_1[i], use_container_width=True)

        st.markdown(''' A partir da constatação que Pico do Couto teve um período
         encurtado de baixa intensidade de vento, essa variação também se reflete no histograma. ''')
        st.image("histo_pico.png", width=700)

        st.markdown(''' Note que a altura das rajadas e das velocidades estão mais próximas, diferente do histograma geral.
            Também podemos observar tais variações em uma mesma estação, considerando diferentes anos. Abaixo consideramos a estação de Campo dos Goytacazes.
             ''')
        imagens_2 = ["sazo-goy19.png", "sazo-goy24.png"]
        legendas_2 = ["Campo dos Goytacazes 2019", "Campo dos Goytacazes 2024"]
        cols = st.columns(2)
        for i, img in enumerate(imagens_2):
            cols[i % 2].image(img, caption=legendas_2[i], use_container_width=True)
        st.markdown(''' Note que o período de baixa na intensidade do vento em 2019 foi entre março a julho, enquanto em 2024 foi somente em abril. 
           Adiante, a estação de Carmo apresentou períodos de altas e baixas semelhantes nos anos de 2019 à 2022, 
           entretanto, no ano de 2024 houveram alterações significativas.
            ''')

        imagens_3 = ["sazo-carmo19.png", "sazo-carmo22.png", "sazo-carmo24.png"]
        legendas_3 = ["Carmo 2019", "Carmo 2022", "Carmo 2024"]
        cols = st.columns(3)
        for i, img in enumerate(imagens_3):
            cols[i % 3].image(img, caption=legendas_3[i], use_container_width=True)


        st.markdown(''' Por fim, é interessante considerar a estação de Rio Claro, que apresentou um alto percentual de perda de dados (ver seção Limpeza de Dados, Página inicial)  ''')
        imagens_5 = ["sazo-rioclaro23.png", "sazo-rioclaro25.png"]
        legendas_5 = ["Rio Claro 2023", "Rio Claro 2025"]
        cols = st.columns(2)
        for i, img in enumerate(imagens_5):
            cols[i % 2].image(img, caption=legendas_5[i], use_container_width=True)

        st.markdown(''' Assim podemos concluir que a análise geral de sazonalidade de todas as estações ao longo dos anos nos oferece um **indicativo** de períodos de altas e baixas na intensidade do vento, sendo importante
       considerar a influência das perdas e variações do comportamento de cada estação. ''')

        st.subheader("💡Conclusões - Direção versus Rajada")

        st.markdown('''Ao observar o gráfico abaixo, que apresenta todas as estações ao longo dos anos, podemos constatar, 
        inicialmente, que as rajadas mais intensas vêm do **noroeste e do sudeste**.  ''')

        st.image("rajdir_tudo.png", width=700)

        st.markdown('''Em contrapartida, a rosa dos ventos indica
       que a maior quantidade de rajadas vieram das direções **nordeste e sudoeste** ''')
        st.image("rosa_tudo.png", width=500)

        st.markdown(''' Mais uma vez, a partir de uma análise menos profunda do gráfico, 
        seria possível concluir que as rajadas fortes ocorrem em direções que menos ventam. Entretanto, observe que o gráfico representa as rajadas máximas, o que enfatiza o comportamento de algumas estações específicas. Após analisar individualmente as estações, foi possível constatar que uma boa parte das 27 estações apresentam 
        comportamentos diferentes, as maiores rajadas não obedecem essa regra, como por exemplo;  ''')
    
        imagens_6 = ["rajdir_3rios.png", "rajdir_goy.png", "rajdir_arraial.png"]
        legendas_6 = ["Três Rios", "Campo dos Goytacazes", "Arraial do Cabo"]
        cols = st.columns(3)
        for i, img in enumerate(imagens_6):
            cols[i % 3].image(img, caption=legendas_6[i], use_container_width=True)

        st.markdown('''Sendo assim, é possível afirmar que essa
       interpretação superficial oferece principalmente o reflexo da estação Pico do Couto. ''')
        st.image("rajdir_pico.png", width=700)

        st.markdown('''Em geral, a maioria das estações teve as maiores rajadas nas direções de maior quantidade 
        de registros, ou em direções opostas, como:''')

        st.markdown("""
            <style>
            /* Força a altura em qualquer imagem dentro da nossa classe personalizada */
            .galeria-estacoes img {
                height: 250px !important;
                width: 100% !important;
                object-fit: cover !important;
                border-radius: 10px;
            }
    
            /* Garante que o contêiner da imagem não tente se expandir além dos 250px */
            .galeria-estacoes [data-testid="stImage"] {
                height: 250px !important;
                overflow: hidden;
            }
            </style>
            """, unsafe_allow_html=True)

        imagens_7 = ["raj-carmo.png", "rosa-carmo.png" , "raj-itatiaia.png", "rosa-itatiaia.png","raj-nova.png" , "nova-rosa.png", "raj-cambuci.png", "rosa-cambuci.png" ]
        legendas_7 = ["Carmo", "Carmo", "Itatiaia", "Itatiaia" , "Nova Friburgo - Salinas" , "Nova Friburgo - Salinas", "Cambuci", "Cambuci" ]
        cols = st.columns(2)
        for i in range(0, len(imagens_7), 2):
            col1, col2 = st.columns(2)
    
            with col1:
                st.markdown('<div class="galeria-estacoes">', unsafe_allow_html=True)
                st.image(imagens_7[i], caption=legendas_7[i], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                if i + 1 < len(imagens_7):
                    st.markdown('<div class="galeria-estacoes">', unsafe_allow_html=True)
                    st.image(imagens_7[i+1], caption=legendas_7[i+1], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(''' Assim podemos concluir que em geral, as rajadas mais severas coincidem com as direções de maior incidência de ventos, confirmando 
        que a direção predominante também é a principal fonte de eventos extremos. ''')
        st.markdown("---")

        


def colorir_risco(row):
    return ['background-color: #ffcccc' if row['Grau'] >= 9 else '' for _ in row]


def mostrar_escala_beaufort():
    st.subheader("Escala Modificada de Beaufort")
    
    data = [
        [0, "Calmaria", "Menos de 1,8", "Menos de 0,5", "Nada se move. Fumaça sobe verticalmente."],
        [1, "Bafagem", "1,8 – 6,0", "0,5 – 1,67", "Fumaça indica sentido, catavento não."],
        [2, "Brisa leve", "7,0 – 11,0", "1,94 – 3,06", "Vento na face, folhas agitam-se."],
        [3, "Vento fresco", "12,0 – 19,0", "3,33 – 5,28", "Folhas e arbustos movem-se."],
        [4, "Vento moderado", "20,0 – 30,0", "5,56 – 8,33", "Levanta poeira, move galhos pequenos."],
        [5, "Vento regular", "31,0 – 40,0", "8,61 – 11,11", "Oscila arbustos, cristas em rios."],
        [6, "Vento meio forte", "41,0 – 51,0", "11,39 – 14,17", "Zune fios, dificulta guarda-chuva."],
        [7, "Vento forte", "52,0 – 61,0", "14,44 – 16,94", "Troncos movem-se, difícil caminhar."],
        [8, "Vento muito forte", "62,0 – 74,0", "17,22 – 20,56", "Quebra galhos, impossível andar."],
        [9, "Vento duro", "75,0 – 87,0", "20,83 – 24,17", "Danos em casas, arranca telhas."],
        [10, "Vento muito duro", "88,0 – 102,0", "24,44 – 28,33", "Derruba árvores, danos consideráveis."],
        [11, "Tempestuoso", "103,0 – 119,0", "28,61 – 33,06", "Grande destruição, derruba fiação."],
        [12, "Furacão", "Acima de 120,0", "Acima de 33,33", "Efeitos devastadores."]
    ]

   
    df_beaufort = pd.DataFrame(data, columns=[
        "Grau", "Nomenclatura", "Vel. (km/h)", "Vel. (m/s)", "Caracterização"
    ])
    
    st.dataframe(df_beaufort.style.apply(colorir_risco, axis=1))
    st.markdown(
        "**Fonte:** [CEMTEC - Escala Modificada de Beaufort](https://www.cemtec.ms.gov.br/wp-content/uploads/2019/02/ESCALA-MODIFICADA-DE-BEAUFORT-INTENSIDADE-DO-VENTO-2.pdf)"
    )
    st.markdown("---")


