
import streamlit as st
import pandas as pd
from pandas import read_csv


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações da página

st.set_page_config(layout="wide",page_title="Focos de incêndio",page_icon=":fire:")

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# funções

def variaveis_municipios():
    municipios = ['RIO VERDE DE MATO GROSSO', 'CASSILÂNDIA', 'AQUIDAUANA',
       'INOCÊNCIA', 'RIBAS DO RIO PARDO', 'PARANAÍBA', 'CAMPO GRANDE',
       'SIDROLÂNDIA', 'IGUATEMI', 'ÁGUA CLARA', 'NAVIRAÍ', 'CORUMBÁ',
       'PONTA PORÃ', 'ITAPORÃ', 'RIO BRILHANTE', 'ARAL MOREIRA',
       'NOVA ALVORADA DO SUL', 'PORTO MURTINHO', 'LADÁRIO', 'MARACAJU',
       'NOVA ANDRADINA', 'NOVO HORIZONTE DO SUL', 'MIRANDA',
       'TRÊS LAGOAS', 'BRASILÂNDIA', 'SANTA RITA DO PARDO', 'BODOQUENA',
       'BONITO', 'BELA VISTA', 'DOURADOS', 'SELVÍRIA', 'BATAGUASSU',
       'PARAÍSO DAS ÁGUAS', 'TERENOS', 'JARDIM', 'GUIA LOPES DA LAGUNA',
       'BANDEIRANTES', 'AMAMBAI', 'CARACOL', 'JUTI', 'NIOAQUE',
       'ANASTÁCIO', 'COSTA RICA', 'ITAQUIRAÍ', 'TACURU',
       'SÃO GABRIEL DO OESTE', 'PEDRO GOMES', 'FIGUEIRÃO', 'ALCINÓPOLIS',
       'CAMAPUÃ', 'SONORA', 'APARECIDA DO TABOADO', 'CORONEL SAPUCAIA',
       'CORGUINHO', 'COXIM', 'BATAYPORÃ', 'IVINHEMA', 'JAPORÃ',
       'TAQUARUSSU', 'CAARAPÓ', 'ANAURILÂNDIA', 'ANGÉLICA', 'MUNDO NOVO',
       'SETE QUEDAS', 'PARANHOS', 'JATEÍ', 'CHAPADÃO DO SUL',
       'DOIS IRMÃOS DO BURITI', 'DOURADINA', 'LAGUNA CARAPÃ', 'ELDORADO',
       'ROCHEDO', 'JARAGUARI', 'VICENTINA', 'FÁTIMA DO SUL', 'DEODÁPOLIS',
       'ANTÔNIO JOÃO', 'GLÓRIA DE DOURADOS', 'RIO NEGRO']
    return municipios


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# titulo

col01,col02,col03 = st.columns(3)
with col01:
    pass
with col02:
    st.title (':red[§] P:red[rojeto] I:red[ntegrador] IV')
    st.image('image/queimadas.jpg',width=600)
with col03:
    pass
# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Barra lateral
table = st.sidebar.checkbox("Tabela", False)
mapa = st.sidebar.checkbox("Gráfico Mapa",False)

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# Carrega arquivo


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
                    df[['data', 'hora']] = df['datahora'].str.split(' ', expand=True)
                    
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

                    # Remove a coluna original 'datahora' do DataFrame
                    df = df.drop('datahora', axis=1)
                    dfs[arquivo.name] = df  # Armazena o DataFrame com o nome do arquivo como chave
        return dfs

        
dfs = lerArquivo()

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

if dfs:
    # Cria um selectbox para escolher o DataFrame
    opcao_df = st.selectbox("Selecione o DataFrame:", list(dfs.keys()))

    df_selecionado = dfs[opcao_df]

    municipios = df_selecionado['municipio'].unique()

if dfs is not None:
    
    if table:
        df_amostra = df_selecionado.sample(n=60)
        st.dataframe(df_amostra)

# if mapa:

# # Cria o selectbox para filtrar por município
#     opcao_municipio = st.selectbox("Selecione o Município:", municipios)
#     # Acessa o DataFrame selecionado
#     df_selecionado = dfs[opcao_df]
#     # Filtra o DataFrame pelo município selecionado
#     df_municipio = df_selecionado[df_selecionado['municipio'] == opcao_municipio]

#     st.map(df_selecionado, latitude='latitude', longitude='longitude')
