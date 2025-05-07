# Arquivo: streamlit_app.py (novo arquivo)
import streamlit as st

st.title("Análise de Dados Econômicos")
st.write("Versão de teste para Streamlit Cloud")

# Botão simples que não depende de outros módulos
if st.button("Testar conexão"):
    st.success("Funcionou! A aplicação está rodando no Streamlit Cloud!")