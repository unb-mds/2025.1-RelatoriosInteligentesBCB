import streamlit as st
from data_collector import BCBDataCollector
from database_manager import DatabaseManager

def coleta_page(last_n_years):
    st.title("🔄 Coleta de Dados")
    
    st.markdown("### Funcionalidades Planejadas:")
    st.markdown("""
    - Conexão com APIs do Banco Central do Brasil
    - Atualização automática de dados
    - Validação e limpeza de dados
    - Armazenamento em banco de dados
    """)
    
    if st.button("Coleta de Dados"):
        with st.spinner("Coletando dados..."):
            collector = BCBDataCollector()
            data = collector.collect_all_data(last_n_years)
            db = DatabaseManager()
            results = db.save_all_data(data)
            if all(results.values()):
                st.success("Dados coletados e salvos com sucesso!")
            else:
                st.warning("Alguns dados não puderam ser salvos.")
