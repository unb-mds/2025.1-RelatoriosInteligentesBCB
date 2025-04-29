# main.py (versão para multipage app)
import streamlit as st
import sys
import os
import subprocess

# Importar diretamente os outros scripts
try:
    from data_collector import BCBDataCollector
    from database_manager import DatabaseManager
except ImportError:
    st.error("Erro ao importar módulos necessários. Verifique as dependências.")
    st.stop()

# Interface principal
st.set_page_config(
    page_title="Sistema de Análise Econômica - BCB",
    page_icon="📊",
    layout="wide"
)

st.title("Sistema de Análise Econômica com Dados do Banco Central do Brasil")
st.markdown("""
Este sistema permite coletar, visualizar e analisar dados econômicos do Banco Central do Brasil,
além de criar modelos de machine learning para previsão de indicadores.
""")

# Função para coletar dados
def collect_data():
    with st.spinner("Coletando dados..."):
        collector = BCBDataCollector()
        data = collector.collect_all_data(last_n_years=5)
        db = DatabaseManager()
        results = db.save_all_data(data)
        if all(results.values()):
            st.success("Dados coletados e salvos com sucesso!")
        else:
            st.warning("Alguns dados não puderam ser salvos.")

# Organizar o layout de navegação
page = st.sidebar.selectbox(
    "Selecione uma opção:",
    ["Página Inicial", "Dashboard Econômico", "Previsões com ML"]
)

# Página inicial
if page == "Página Inicial":
    # Menu principal
    st.header("Escolha uma opção:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Coleta de Dados")
        st.markdown("Atualiza a base de dados com os últimos dados disponíveis nas APIs do BCB.")
        if st.button("Coletar Dados"):
            collect_data()
    
    with col2:
        st.subheader("Dashboard Econômico")
        st.markdown("Visualize os indicadores econômicos e suas tendências.")
        if st.button("Abrir Dashboard"):
            st.sidebar.selectbox(
                "Selecione uma opção:",
                ["Dashboard Econômico"],
                key="force_dashboard"
            )
            st.experimental_rerun()
    
    with col3:
        st.subheader("Previsões com ML")
        st.markdown("Use machine learning para prever tendências futuras dos indicadores.")
        if st.button("Abrir Previsões"):
            st.sidebar.selectbox(
                "Selecione uma opção:",
                ["Previsões com ML"],
                key="force_ml"
            )
            st.experimental_rerun()
    
    # Informações adicionais
    st.header("Documentação")
    st.markdown("""
    ### Como usar este sistema
    
    1. **Coleta de Dados**: Primeiro, colete os dados mais recentes das APIs do Banco Central do Brasil.
    2. **Dashboard Econômico**: Visualize os indicadores e suas relações.
    3. **Previsões com ML**: Treine modelos preditivos e visualize previsões futuras.
    """)

# Dashboard Econômico
elif page == "Dashboard Econômico":
    # Importar o app.py aqui
    try:
        import app
    except ImportError:
        st.error("Não foi possível carregar o dashboard econômico.")
        if st.button("Voltar"):
            st.sidebar.selectbox(
                "Selecione uma opção:",
                ["Página Inicial"],
                key="back_home"
            )
            st.experimental_rerun()

# Previsões com ML
elif page == "Previsões com ML":
    # Importar o ml_app.py aqui
    try:
        import ml_app
    except ImportError:
        st.error("Não foi possível carregar o dashboard de previsões.")
        if st.button("Voltar"):
            st.sidebar.selectbox(
                "Selecione uma opção:",
                ["Página Inicial"],
                key="back_home"
            )
            st.experimental_rerun()