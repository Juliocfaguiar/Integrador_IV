import streamlit as st
from pandas import read_csv
# import plotly.figure_factory as ff


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações da página

st.set_page_config(layout="wide",page_title="Focos de incêndio",page_icon=":fire:")

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# funções



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
# histograma = st.sidebar.checkbox("Histograma",False) 
mapa = st.sidebar.checkbox("Gráfico Mapa",False)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

if table:
    if df is not None: 
        st.dataframe(df,width=2000,height=550)

if mapa:
    st.map(df, latitude='lat', longitude='lon')
# pip install streamlit-folium

# if histograma:
#     col04,col05 = st.columns(2)
#     with col04:
#         selecao = st.multiselect('Selecione',colunas(),
#         ['municipio'])
#         legendas= [f'selecao']

#     with col05:
#         fig = ff.create_distplot(
#         selecao, legendas,bin_size=[.1, .25, .5])
#         st.plotly_chart(fig, use_container_width=True)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #



# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #



# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #