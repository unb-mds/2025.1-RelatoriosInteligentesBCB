# main.py (versão unificada)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time
import sys
import os

# Configuração da página (deve ser a primeira chamada Streamlit)
st.set_page_config(
    page_title="Sistema de Análise Econômica - BCB",
    page_icon="📊",
    layout="wide"
)

# Função para tentar importar os módulos necessários
def load_modules():
    try:
        global BCBDataCollector, DatabaseManager
        from data_collector import BCBDataCollector
        from database_manager import DatabaseManager
        return True
    except ImportError as e:
        st.error(f"Erro ao importar módulos necessários: {e}")
        return False

# Função para a página inicial
def home_page():
    st.title("Sistema de Análise Econômica com Dados do Banco Central do Brasil")
    st.markdown("""
    Este sistema permite coletar, visualizar e analisar dados econômicos do Banco Central do Brasil,
    além de criar modelos de machine learning para previsão de indicadores.
    """)
    
    # Menu principal
    st.header("Escolha uma opção:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Coleta de Dados")
        st.markdown("Atualiza a base de dados com os últimos dados disponíveis nas APIs do BCB.")
        if st.button("Coletar Dados"):
            if load_modules():
                collect_data()
    
    with col2:
        st.subheader("Dashboard Econômico")
        st.markdown("Visualize os indicadores econômicos e suas tendências.")
        if st.button("Abrir Dashboard"):
            st.session_state.page = "dashboard"
            st.experimental_rerun()
    
    with col3:
        st.subheader("Previsões com ML")
        st.markdown("Use machine learning para prever tendências futuras dos indicadores.")
        if st.button("Abrir Previsões"):
            st.session_state.page = "ml"
            st.experimental_rerun()
    
    # Informações adicionais
    st.header("Documentação")
    st.markdown("""
    ### Como usar este sistema
    
    1. **Coleta de Dados**: Primeiro, colete os dados mais recentes das APIs do Banco Central do Brasil.
    2. **Dashboard Econômico**: Visualize os indicadores e suas relações.
    3. **Previsões com ML**: Treine modelos preditivos e visualize previsões futuras.
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

# Função para carregar dados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data(table_name, start_date=None, end_date=None):
    if load_modules():
        db_manager = DatabaseManager()
        return db_manager.load_data(table_name, start_date, end_date)
    return None

# Função para o Dashboard Econômico
def dashboard_page():
    st.title("Dashboard Econômico - Dados do Banco Central do Brasil")
    
    if not load_modules():
        st.error("Não foi possível carregar os módulos necessários.")
        if st.button("Voltar para a página inicial"):
            st.session_state.page = "home"
            st.experimental_rerun()
        return
    
    # Mapeamento de nomes para exibição
    indicator_names = {
        'ipca': 'Inflação (IPCA)',
        'pib': 'PIB Real',
        'divida_pib': 'Dívida/PIB',
        'selic': 'Taxa SELIC Diária',
        'selic_meta': 'Meta da Taxa SELIC',
        'transacoes': 'Saldo em Transações Correntes',
        'resultado_primario': 'Resultado Primário'
    }
    
    # Sidebar
    st.sidebar.title("Opções")
    
    # Atualização de dados
    st.sidebar.subheader("Atualização de Dados")
    years_to_fetch = st.sidebar.slider("Anos de dados para coletar", 1, 10, 5)
    update_button = st.sidebar.button("Atualizar Dados")
    
    if update_button:
        collect_data()
    
    # Seleção de indicadores
    st.sidebar.subheader("Indicadores")
    indicators = st.sidebar.multiselect(
        "Selecione os indicadores para visualizar",
        list(indicator_names.keys()),
        default=['ipca', 'selic', 'pib'],
        format_func=lambda x: indicator_names.get(x, x)
    )
    
    # Exibir dados conforme seleção
    if not indicators:
        st.warning("Por favor, selecione pelo menos um indicador no menu lateral.")
    else:
        # Para cada indicador selecionado
        for indicator in indicators:
            data = load_data(indicator)
            
            if data is not None and not data.empty:
                st.subheader(indicator_names[indicator])
                
                # Gráfico interativo com Plotly
                fig = px.line(
                    data, 
                    x='date', 
                    y='value',
                    title=f'Evolução de {indicator_names[indicator]}',
                    labels={'date': 'Data', 'value': 'Valor'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Estatísticas básicas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("Estatísticas")
                    st.dataframe(data['value'].describe())
                
                with col2:
                    st.write("Dados Recentes")
                    st.dataframe(data.sort_values('date', ascending=False).head(5))
            else:
                st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")
    
    # Botão para voltar
    if st.button("Voltar para a página inicial"):
        st.session_state.page = "home"
        st.experimental_rerun()

# Função para a página de Machine Learning
def ml_page():
    st.title("Previsões de Indicadores Econômicos")
    
    if not load_modules():
        st.error("Não foi possível carregar os módulos necessários.")
        if st.button("Voltar para a página inicial"):
            st.session_state.page = "home"
            st.experimental_rerun()
        return
    
    # Versão simplificada da página de ML
    st.info("Esta é uma versão simplificada da página de Machine Learning.")
    
    # Mapeamento de nomes para exibição
    indicator_names = {
        'ipca': 'Inflação (IPCA)',
        'pib': 'PIB Real',
        'divida_pib': 'Dívida/PIB',
        'selic': 'Taxa SELIC Diária',
        'selic_meta': 'Meta da Taxa SELIC',
        'transacoes': 'Saldo em Transações Correntes',
        'resultado_primario': 'Resultado Primário'
    }
    
    # Seleção de indicador
    indicator = st.selectbox(
        "Selecione o indicador para prever",
        list(indicator_names.keys()),
        format_func=lambda x: indicator_names.get(x, x)
    )
    
    # Número de períodos futuros para prever
    forecast_periods = st.slider(
        "Número de meses para prever",
        min_value=1,
        max_value=12,
        value=6
    )
    
    # Carregar dados do indicador
    data = load_data(indicator)
    
    if data is not None and not data.empty:
        # Exibir dados históricos
        st.subheader(f"Dados históricos de {indicator_names[indicator]}")
        
        fig = px.line(
            data, 
            x='date', 
            y='value',
            title=f'Histórico de {indicator_names[indicator]}',
            labels={'date': 'Data', 'value': 'Valor'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Simulação de previsão (versão simplificada)
        if st.button("Simular Previsão"):
            with st.spinner("Calculando previsão..."):
                # Simular um tempo de processamento
                time.sleep(2)
                
                # Criar dados de previsão fictícios
                last_date = data['date'].max()
                last_value = data.loc[data['date'] == last_date, 'value'].values[0]
                
                # Criar tendência simples
                trend = 0.05  # 5% de variação
                future_dates = pd.date_range(start=last_date, periods=forecast_periods+1, freq='M')[1:]
                future_values = [last_value * (1 + trend * i) for i in range(1, forecast_periods+1)]
                
                future_df = pd.DataFrame({
                    'date': future_dates,
                    'value': future_values,
                    'tipo': 'Previsão'
                })
                
                # Preparar dados para gráfico
                historical_df = pd.DataFrame({
                    'date': data['date'].tail(12),
                    'value': data['value'].tail(12),
                    'tipo': 'Histórico'
                })
                
                combined_df = pd.concat([historical_df, future_df])
                
                # Criar gráfico
                fig = px.line(
                    combined_df, 
                    x='date', 
                    y='value', 
                    color='tipo',
                    title=f'Previsão de {indicator_names[indicator]} (Próximos {forecast_periods} meses)',
                    labels={'date': 'Data', 'value': 'Valor', 'tipo': 'Tipo'},
                    color_discrete_map={'Histórico': 'blue', 'Previsão': 'red'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.success("Previsão concluída! (Nota: Esta é uma simulação para demonstração)")
    else:
        st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")
    
    # Botão para voltar
    if st.button("Voltar para a página inicial"):
        st.session_state.page = "home"
        st.experimental_rerun()

# Principal
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Seletor de página via sidebar
page = st.sidebar.radio(
    "Navegação",
    ["Página Inicial", "Dashboard Econômico", "Previsões com ML"],
    key="sidebar_nav"
)

# Mapear seleção para o estado da página
if page == "Página Inicial":
    st.session_state.page = "home"
elif page == "Dashboard Econômico":
    st.session_state.page = "dashboard"
elif page == "Previsões com ML":
    st.session_state.page = "ml"

# Exibir a página selecionada
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "ml":
    ml_page()