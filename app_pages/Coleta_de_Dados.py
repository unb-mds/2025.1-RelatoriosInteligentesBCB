import streamlit as st
from data_collector import BCBDataCollector
from database_manager import DatabaseManager


def coleta_page(last_n_years):
    st.header("Coleta de Dados")
    with st.spinner("Coletando dados..."):
        collector = BCBDataCollector()
        data = collector.collect_all_data(last_n_years)
        db = DatabaseManager()
        results = db.save_all_data(data)
        if all(results.values()):
            st.success("Dados coletados e salvos com sucesso!")
        else:
            st.warning("Alguns dados não puderam ser salvos.")