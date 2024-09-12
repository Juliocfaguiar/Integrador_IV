import streamlit as st
from pandas import read_csv


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #
# configurações da página

st.set_page_config(layout="wide",page_title="Focos de incêndio",page_icon=":fire:")
st.sidebar.header("Estados")

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
# Carrega arquivo


def lerArquivo():
    arquivo = st.file_uploader("Escolha um arquivo CSV",type=['csv'])
    if arquivo:
        print(arquivo.type)
        match arquivo.type.split('/'):
            case 'text','csv':
                df = read_csv(arquivo,sep =",")
                
                # Divide a coluna 'datahora' em duas colunas: 'data' e 'hora'
                df[['data', 'hora']] = df['datahora'].str.split(' ', expand=True)

                # Obtém a lista de todas as colunas do DataFrame
                cols = list(df.columns)

                # Obtém o índice (posição) das colunas 'data' e 'hora' na lista de colunas
                data_index = cols.index('data')
                hora_index = cols.index('hora')

                # Remove as colunas 'data' e 'hora' de suas posições originais na lista
                cols.pop(data_index)
                cols.pop(hora_index - 1)  # Ajusta o índice de 'hora' devido à remoção de 'data'

                # Insere as colunas 'data' e 'hora' no início da lista de colunas
                cols.insert(0, 'hora')
                cols.insert(0, 'data')

                # Reordena o DataFrame usando a nova ordem de colunas
                df = df[cols]

                # Remove a coluna original 'datahora' do DataFrame
                df = df.drop('datahora', axis=1)
                return df
    else:
        st.error('Arquivo ainda não foi importado')
        
df = lerArquivo()

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #

table = st.sidebar.checkbox("Tabela", False)
if df is not None:
    df_amostra = df.sample(n=60)
    if table:
        st.dataframe(df_amostra)
