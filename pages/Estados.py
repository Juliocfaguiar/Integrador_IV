import streamlit as st
import pandas as pd
from pandas import read_csv
# import geopandas as gpd
# from shapely.geometry import Point
# import matplotlib.pyplot as plt
import plotly.express as px
# import plotly.figure_factory as ff


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
    arquivo = st.file_uploader("Escolha um ou mais arquivos CSV", type=['csv'], accept_multiple_files=True, key="upload_csv")
    dfs = {}  # Utiliza um dicionário para armazenar os DataFrames com nomes de arquivo como chaves
    if arquivo:
        for i, arquivo in enumerate(arquivo):
            print(arquivo.type)
            match arquivo.type.split('/'):
                case 'text', 'csv':
                    df = pd.read_csv(arquivo, sep=",")
                    
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

                    # Utiliza um dicionário global para o mapeamento, se necessário
                    global bioma_mapeado, municipio_mapeado

                    if not dfs:
                        bioma_mapeado = {bioma: i + 1 for i, bioma in enumerate(df['bioma'].unique())}
                        municipio_mapeado = {municipio: i + 1 for i, municipio in enumerate(df['municipio'].unique())}
                    else:
                        biomas_existentes = list(bioma_mapeado.keys())
                        novos_biomas = [bioma for bioma in df['bioma'].unique() if bioma not in biomas_existentes]
                        for i, bioma in enumerate(novos_biomas):
                            bioma_mapeado[bioma] = len(bioma_mapeado) + i + 1

                        municipios_existentes = list(municipio_mapeado.keys())
                        novos_municipios = [municipio for municipio in df['municipio'].unique() if municipio not in municipios_existentes]
                        for i, municipio in enumerate(novos_municipios):
                            municipio_mapeado[municipio] = len(municipio_mapeado) + i + 1

                    df['id_bioma'] = df['bioma'].map(bioma_mapeado)
                    df['id_municipio'] = df['municipio'].map(municipio_mapeado)

                    dfs[arquivo.name] = df  # Armazena o DataFrame com o nome do arquivo como chave

        return dfs  # Retorna o dicionário de DataFrames

# Inicializa os mapeamentos globais
bioma_mapeado = {}
municipio_mapeado = {}
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Barra lateral
table = st.sidebar.checkbox("Tabela", False)
mapa = st.sidebar.checkbox("Gráfico Mapa",False)
barras = st.sidebar.checkbox("Grafico Barras",False) 
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# titulo

col01,col02,col03 = st.columns(3)
with col01:
    st.image('image/queimada.jpg',width=400)
with col02:
    st.title ('§:red[ P]rojeto :red[I]ntegrador :red[IV]')
    dfs = lerArquivo()

    if dfs:
        # Cria um selectbox para escolher o DataFrame
        opcao_df = st.selectbox("Selecione o DataFrame:", list(dfs.keys()))
 
        df_selecionado = dfs[opcao_df]

        municipios = df_selecionado['municipio'].unique()

        if mapa :
        # Cria o selectbox para filtrar por município
            opcao_municipio = st.selectbox("Selecione o Município:", municipios)
            # Acessa o DataFrame selecionado
            df_selecionado = dfs[opcao_df]
            # Filtra o DataFrame pelo município selecionado
            df_municipio = df_selecionado[df_selecionado['municipio'] == opcao_municipio]
            # st.write(df_municipio)
            # Cria uma coluna de geometria no DataFrame filtrado
            # geometry = [Point(xy) for xy in zip(df_municipio['lon'], df_municipio['lat'])]
            # crs={'proj': 'latlong', 'ellps':'WGS84', 'datum': 'WGS84','no_defs':True}
            # gdf = gpd.GeoDataFrame(df_municipio, geometry=geometry,crs=crs)

        # Define o sistema de coordenadas geográficas
        # gdf.set_crs(epsg=4326, inplace=True)


with col03:
    st.image('image/queimada.jpg',width=400)


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

if table:
    if dfs is not None: 
        st.dataframe(df_selecionado,width=2000,height=550)

if mapa:
     # Plota o gráfico com geopandas
    # fig, ax = plt.subplots(figsize=(20, 8))
    # gdf.plot(ax=ax, markersize=50, color='red', alpha=0.5,edgecolor='black')
    # ax.set_title(f"Localização das Ocorrências em {opcao_municipio}")
    # st.pyplot(fig)
    st.map(df_municipio, latitude='lat', longitude='lon')
# pip install streamlit-folium

if barras:
    options = st.radio("selecione a variável", ["id_bioma", "id_municipio"],
                        horizontal=True)

    if options == "id_bioma":
                col04,col05,col06,col07 = st.columns(4,gap = "large")
                with col04:
                    fig = px.bar(df_selecionado, x="data", y="id_bioma", color="bioma", 
                    width=900, height=720,
                    labels={"data": "Data", "id_bioma": "Tipo de Bioma"},
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
                    bioma_counts = df_selecionado['bioma'].value_counts()
                    st.write("**Quantidade de Focos por Bioma:**")
                    st.write(bioma_counts)

        

    if options == "id_municipio":
                        col08,col09,col10,col11 = st.columns(4,gap = "large")
                        with col08:
                        # Cria o gráfico com Plotly
                            fig = px.bar(df_selecionado, x="data", y="id_municipio", color="municipio", 
                            width=900, height=720,
                            barmode ='group',
                            labels={"data": "Data", "id_municipio": ""})
                            # color_discrete_map={"Pantanal": "green", "Mata Atlântica": "blue","Cerrado":"red"}) # Define cores personalizadas

                            # Exibe o gráfico no Streamlit
                            st.plotly_chart(fig)
                        with col09:
                             pass
                        with col10:
                             pass
                        with col11:
                            # Conta a quantidade de ocorrências de cada bioma
                            municipio_counts = df_selecionado['municipio'].value_counts()
                            st.write("**Quantidade de Focos por Municipio:**")
                            st.write(municipio_counts)
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #