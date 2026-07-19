import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def conclusao(dados_positivos):
    st.subheader("💡 Conclusões e Insights")

    col1, col2 = st.columns(2)
    
    max_rajada = dados_positivos['Rajada_Máxima'].max()
    total_estacoes = dados_positivos['ESTACAO'].nunique()
    
    col1.metric("Rajada Máxima Registrada", f"{max_rajada:.1f} m/s")
    col2.metric("Estações Ativas", total_estacoes)
    
    st.markdown("---")
    
    st.subheader(" 💡 Conclusão - Qualidade dos dados")
    st.markdown(''' Considerando o histograma de todas as estações ao longo dos anos, observamos uma Distribuição Assimétrica à Direita. ''')
    st.image("histogramatudo1.png", width=700)
    st.markdown(''' Essa é a forma esperada para velocidade de vento, uma vez que a física do vento em condições normais tende a velocidades baixas/moderadas, enquanto os eventos extremos (tempestades, frentes frias) são as 
    exceções que formam essa cauda à direita. Portanto, isso evidencia um certo nível de qualidade dos dados.''')
    st.markdown(''' Ao mudar para o histograma de todas as estações  anualmente, podemos observar coerentemente 
    a mesma distribuição com variações em seu grau de curtose ''')

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
    st.markdown(''' De acordo com os protocolos do NHC (Nacional Hurricane Center), podemos concluir que a partir da estrutura dos dados do INMET (ver Glossário), as rajadas máximas atuam como indicadores do potencial de impacto imediato, enquanto a 
    velocidade média do vento (sustentado) valida a magnitude e a organização do fenômeno. ''')

    st.markdown( '''Por exemplo, considerando a estação Pico do Couto em março de 2018, identificamos picos de magnitude extrema. Na ocasião, a rajada máxima atingiu 49 m/s (aprox. 176 km/h), valor que, segundo a Escala Modificada de Beaufort, 
    situa-se no Grau 12, caracterizando um evento de potencial impacto devastador.''')

    st.image("sazonalidadepicodocouto1.png", width=700)

    st.markdown('''Assim, como ferramenta de validação, foi adotado o gráfico de correlação entre a 
    velocidade média e a rajada máxima.   ''')

    st.image("relacaovel-raj.png", width=700)

    st.markdown(''' Com base no gráfico acima e nas fontes consultadas, 
    descartamos a possibilidade de eventos citados anteriormente. ''')

    st.subheader("💡Conclusões - Sazonalidade")
    st.markdown(''' Para uma análise coerente da sazonalidade, vamos considerar a **média** das rajadas/velocidades no contexto macro (todas as estações). A justificativa é clara; se considerarmos o **máximo**, é evidente que distorções ocorrerão. Por exemplo, considerando a
estação Pico do Couto, que mencionada acima apresenta a característica de rajadas intensas em comparação com outras estações, a análise da sazonalidade no contexto macro se resumiria a analisar especificamente o comportamento dos dados desta.
 ''')
    st.image("sazonalidade-tudo.png", width=900)
    st.markdown('''Uma conclusão possível que podemos extrair do gráfico acima é:
* Existe uma menor intensidade no vento nos meses;
	* Abril
	* Maio
	* Junho
* Existe uma maior intensidade no vento nos meses;
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
Também podemos observar tais variações em uma mesma estação, considerando diferentes anos. Abaixo consideramos a estação de Campo dos Goytacazes, que apresentou períodos de baixa intensidade de vento em 2019 e 2024.
 ''')
    imagens_2 = ["sazo-goy19.png", "sazo-goy24.png"]
    legendas_2 = ["Campo dos Goytacazes 2019", "Campo dos Goytacazes 2024"]
    cols = st.columns(2)
    for i, img in enumerate(imagens_2):
        cols[i % 2].image(img, caption=legendas_2[i], use_container_width=True)
    st.markdown(''' Note que o período de baixa em 2019 foi entre março a julho, enquanto em 2024 foi somente em abril. 
   Adiante, a estação de Carmo apresentou períodos de altas e baixas semelhantes nos anos de 2019 à 2022, 
   entretanto, no ano de 2024 houveram alterações significativas.
    ''')

    imagens_3 = ["sazo-carmo19.png", "sazo-carmo22.png", "sazo-carmo24.png"]
    legendas_3 = ["Carmo 2019", "Carmo 2022", "Carmo 2024"]
    cols = st.columns(2)
    for i, img in enumerate(imagens_3):
        cols[i % 2].image(img, caption=legendas_3[i], use_container_width=True)

    st.markdown(''' a ''')
    imagens_4 = ["sazo-goy19.png", "sazo-goy24.png"]
    legendas_4 = ["Descrição 1", "Descrição 2"]
    cols = st.columns(2)
    for i, img in enumerate(imagens_4):
        cols[i % 2].image(img, caption=legendas_4[i], use_container_width=True)
    st.markdown(''' a ''')
    imagens_5 = ["sazo-rioclaro23.png", "sazo-rioclaro25.png"]
    legendas_5 = ["Descrição 1", "Descrição 2"]
    cols = st.columns(2)
    for i, img in enumerate(imagens_5):
        cols[i % 2].image(img, caption=legendas_5[i], use_container_width=True)

    st.subheader("💡Conclusões - Direção versus Rajada")



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


