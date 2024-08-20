import streamlit as st
from IndiceX import app as indiceX_app
from IndiceY import app as indiceY_app

# Configurando a largura da página
st.set_page_config(layout="wide")

# Barra lateral para navegação
st.sidebar.title("Insper Quantitative Finance")
paginas = st.sidebar.radio("Índices", ["índice X", "índice Y"])

# Lógica para carregar a página correta
if paginas == "índice X":
    indiceX_app()
elif paginas == "índice Y":
    indiceY_app()