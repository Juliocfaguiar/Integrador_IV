import streamlit as st
from pandas import read_csv
import plotly.express as px



# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações da página

st.set_page_config(layout="wide",page_title="Focos de incêndio",page_icon=":fire:")

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# funções


def barras_graf():
    columns = ['id_bioma','id_municipio']
    return columns
def colunas():
    columns =  ['data','hora','municipio','bioma','estado','id_bdq','foco_id','lat','lon']
    return columns


def lerArquivo():
    arquivo = st.file_uploader("Escolha um arquivo CSV",type=['csv'])
    if arquivo:
        print(arquivo.type)
        match arquivo.type.split('/'):
            case 'text','csv':
                df = read_csv(arquivo,sep =",")
                # Separa a coluna 'data_pas' em duas colunas: 'data' e 'hora'
                df[['data', 'hora']] = df['data_pas'].str.split(' ', expand=True)
                # Apaga a coluna "data_pas"
                df = df.drop('data_pas', axis=1)

                # Obtém a lista de colunas do DataFrame
                cols = list(df.columns)

                # Obtém o índice das colunas 'data' e 'hora' na lista de colunas
                data_index = cols.index('data')
                hora_index = cols.index('hora')

                # Remove as colunas 'data' e 'hora' de suas posições atuais na lista
                cols.pop(data_index)
                cols.pop(hora_index - 1)  # Ajusta o índice da coluna 'hora' após a remoção de 'data'

                # Insere as colunas 'data' e 'hora' no início da lista
                cols.insert(0, 'hora')
                cols.insert(0, 'data')

                # Reordena o DataFrame usando a nova ordem de colunas
                df = df[cols]
                

                # atribui número a cada bioma único começando com 1
                bioma_mapeado = {bioma: i + 1 for i, bioma in enumerate(df['bioma'].unique())}

                # cria uma nova coluna id_bioma
                df['id_bioma'] = df['bioma'].map(bioma_mapeado)

                # atribui número a cada municípios único começando com 1
                municipio_mapeado = {municipio: i + 1 for i, municipio in enumerate(df['municipio'].unique())}

                # Create a new column with the município IDs
                df['id_municipio'] = df['municipio'].map(municipio_mapeado)

                return df
    else:
        st.error('Arquivo ainda não foi importado')
        return None

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# titulo

col01,col02,col03 = st.columns(3)
with col01:
    st.image('image/queimada.jpg',width=400)
with col02:
    st.title ('§:red[ P]rojeto :red[I]ntegrador :red[IV]')
    df = lerArquivo()
with col03:
    st.image('image/queimada.jpg',width=400)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Barra lateral
table = st.sidebar.checkbox("Tabela", False)
mapa = st.sidebar.checkbox("Gráfico Mapa",False)
barras = st.sidebar.checkbox("Grafico Barras",False) 
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

if table:
    if df is not None: 
        st.dataframe(df,width=2000,height=550)

if mapa:
    st.map(df, latitude='lat', longitude='lon')
# pip install streamlit-folium

if barras:
    options = st.radio("selecione a variável", ["id_bioma", "id_municipio"],
                        horizontal=True)

    if options == "id_bioma":
                col04,col05,col06,col07 = st.columns(4)
                with col04:
                    # Agrupa por data e bioma, contando as ocorrências
                    df_agrupado = df.groupby(['data', 'bioma']).count().reset_index()
                    # Cria o gráfico com Plotly
                    fig = px.bar(df_agrupado, x="data", y="id_bioma", color="bioma", 
                    width=1000, height=720,
                    labels={"data": "Data", "id_bioma": " "},
                    barmode ='group',

                    color_discrete_map={"Pantanal": "green", "Mata Atlântica": "blue","Cerrado":"red"}) # Define cores personalizadas
                    # Exibe o gráfico no Streamlit
                    st.plotly_chart(fig)
                with col05:
                    pass
                with col06:
                    pass
                with col07:

                    # Conta a quantidade de ocorrências de cada bioma
                    bioma_counts = df['bioma'].value_counts()
                    st.write("**Quantidade de Focos por Bioma:**")
                    st.write(bioma_counts)

        


    if options == "id_municipio":
                col08,col09,col10,col11 = st.columns(4)
                with col08:
                            
                            # Agrupa por data e municipio, contando as ocorrências
                            df_agrupado = df.groupby(['data','municipio']).count().reset_index()
                            # Cria o gráfico com Plotly
                            fig = px.bar(df_agrupado, x="data", y="id_municipio", color="municipio", 
                            width=1000, height=720,
                            barmode ='group',
                            labels={"data": "Data", "id_municipio": ""})

                            # Exibe o gráfico no Streamlit
                            st.plotly_chart(fig)
                with col09:
                    pass
                with col10:
                    pass
                with col11:

                    # Conta a quantidade de ocorrências de cada bioma
                    municipio_counts = df['municipio'].value_counts()
                    st.write("**Quantidade de Focos por Municipio:**")
                    st.write(municipio_counts)
# # # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #