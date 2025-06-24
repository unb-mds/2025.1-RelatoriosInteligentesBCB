# app_pages/Relatorios_IA_integrated.py
"""
Versão integrada dos Relatórios com IA para funcionar dentro do main.py
SEM st.set_page_config e otimizada para contexto compartilhado
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Imports do ml_core/interpreter
ML_INTERPRETER_AVAILABLE = False
try:
    from ml_core.interpreter import interpreter, analyze_economic_scenario
    from ml_core.interpreter.economic_analyzer import EconomicAnalyzer, quick_economic_analysis
    from ml_core.interpreter.config import get_indicator_name, CUSTOM_CSS
    from database_manager import DatabaseManager
    ML_INTERPRETER_AVAILABLE = True
except ImportError as e:
    print(f"Erro ao carregar ML Interpreter: {e}")

def relatorios_ia_page():
    """Função principal adaptada para integração com main.py"""
    
    # Título da página (sem st.set_page_config)
    st.title("🤖 Relatórios Econômicos com Inteligência Artificial")
    st.markdown("---")
    
    # Verificar disponibilidade do sistema
    if not ML_INTERPRETER_AVAILABLE:
        st.error("❌ Sistema de IA não disponível. Verifique a instalação dos componentes.")
        st.info("💡 Tente executar: pip install prophet plotly")
        return
    
    # Configurações na sidebar (integrada com main.py)
    st.sidebar.markdown("### ⚙️ Configurações de Análise")
    
    # Obter indicadores disponíveis
    try:
        db = DatabaseManager()
        stats = db.get_stats()
        available_indicators = [k for k in stats.keys() if k != 'db_size']
    except Exception as e:
        st.error(f"❌ Erro ao conectar com banco de dados: {e}")
        return
    
    if not available_indicators:
        st.error("❌ Nenhum indicador disponível no banco de dados")
        st.info("💡 Execute primeiro a 'Coleta de Dados' no menu principal")
        return
    
    # Seleção de indicadores
    selected_indicators = st.sidebar.multiselect(
        "📈 Selecione os Indicadores:",
        available_indicators,
        default=available_indicators[:3] if len(available_indicators) >= 3 else available_indicators,
        format_func=get_indicator_name,
        help="Escolha os indicadores econômicos para análise"
    )
    
    # Período de análise
    period_months = st.sidebar.slider(
        "📅 Período de Análise (meses):",
        min_value=3,
        max_value=36,
        value=12,
        step=1,
        help="Período histórico para análise de correlações e tendências"
    )
    
    # Períodos de previsão
    forecast_periods = st.sidebar.slider(
        "🔮 Períodos de Previsão:",
        min_value=3,
        max_value=24,
        value=6,
        step=1,
        help="Número de períodos futuros para previsão"
    )
    
    # Status do sistema na sidebar
    if st.sidebar.button("📊 Status do Sistema"):
        with st.sidebar:
            try:
                status = interpreter.get_status()
                st.json(status)
            except Exception as e:
                st.error(f"Erro: {e}")
    
    # Verificar se indicadores foram selecionados
    if not selected_indicators:
        show_welcome_section()
        return
    
    # Interface principal com tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 Relatório IA",
        "🔗 Correlações", 
        "📈 Tendências", 
        "🔮 Previsões",
        "📄 Downloads"
    ])
    
    with tab1:
        show_ai_report_section(selected_indicators, period_months, forecast_periods)
    
    with tab2:
        show_correlation_section(selected_indicators, period_months)
    
    with tab3:
        show_trends_section(selected_indicators)
    
    with tab4:
        show_forecasts_section(selected_indicators, forecast_periods)
    
    with tab5:
        show_downloads_section(selected_indicators)

def show_welcome_section():
    """Seção de boas-vindas simplificada"""
    
    st.info("👈 Selecione pelo menos um indicador na barra lateral para começar a análise!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 Análise com IA
        - Relatórios automáticos
        - Insights inteligentes
        - Recomendações estratégicas
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Análise Multi-Indicadores
        - Correlações avançadas
        - Tendências comparativas
        - Visualizações interativas
        """)
    
    with col3:
        st.markdown("""
        ### 🔮 Previsões Avançadas
        - Machine Learning (Prophet)
        - Intervalos de confiança
        - Análise de cenários
        """)

def show_ai_report_section(selected_indicators, period_months, forecast_periods):
    """Seção principal de relatório IA simplificada"""
    
    st.header("🤖 Relatório Econômico Inteligente")
    
    # Botão principal
    if st.button("🚀 Gerar Relatório Completo com IA", type="primary", key="main_ai_report"):
        
        with st.spinner("🧠 Analisando dados e gerando insights..."):
            try:
                # Executar análise
                results = quick_economic_analysis(selected_indicators, period_months)
                
                if results:
                    # Salvar na sessão
                    st.session_state['ai_results'] = results
                    st.session_state['ai_timestamp'] = datetime.now()
                    st.success("✅ Análise concluída!")
                else:
                    st.error("❌ Falha na geração do relatório")
                    
            except Exception as e:
                st.error(f"❌ Erro na análise: {str(e)}")
    
    # Mostrar resultados se existir
    if 'ai_results' in st.session_state:
        results = st.session_state['ai_results']
        timestamp = st.session_state.get('ai_timestamp', 'Desconhecido')
        
        st.subheader("📋 Relatório Gerado")
        st.caption(f"Gerado em: {timestamp}")
        
        # Relatório de IA em texto
        if 'ai_report' in results and results['ai_report']:
            with st.expander("📄 Ver Relatório Completo", expanded=True):
                st.markdown(results['ai_report'])
        
        # Gráficos principais
        if 'charts' in results:
            charts = results['charts']
            
            if charts.get('multi_indicator_chart'):
                st.subheader("📈 Evolução dos Indicadores")
                st.plotly_chart(
                    charts['multi_indicator_chart'], 
                    use_container_width=True,
                    key=f"main_multi_chart_{datetime.now().timestamp()}"
                )
            
            if charts.get('correlation_heatmap'):
                st.subheader("🔥 Mapa de Correlações")
                st.plotly_chart(
                    charts['correlation_heatmap'], 
                    use_container_width=True,
                    key=f"main_corr_chart_{datetime.now().timestamp()}"
                )

def show_correlation_section(selected_indicators, period_months):
    """Seção de correlações simplificada"""
    
    st.header("🔗 Análise de Correlações")
    
    if len(selected_indicators) < 2:
        st.warning("⚠️ Selecione pelo menos 2 indicadores para análise de correlação.")
        return
    
    if st.button("🔄 Calcular Correlações", key="calc_corr"):
        with st.spinner("Calculando correlações..."):
            try:
                analyzer = EconomicAnalyzer()
                analyzer.load_indicators(selected_indicators)
                correlation_matrix = analyzer.calculate_correlation_matrix(period_months)
                
                if correlation_matrix is not None:
                    st.session_state['correlation_data'] = correlation_matrix
                    st.success("✅ Correlações calculadas!")
                else:
                    st.error("❌ Não foi possível calcular correlações")
                    
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    
    # Mostrar correlações se calculadas
    if 'correlation_data' in st.session_state:
        correlation_matrix = st.session_state['correlation_data']
        
        # Matriz numérica
        st.subheader("📊 Matriz de Correlação")
        display_matrix = correlation_matrix.copy()
        display_matrix.columns = [get_indicator_name(col) for col in display_matrix.columns]
        display_matrix.index = [get_indicator_name(idx) for idx in display_matrix.index]
        st.dataframe(display_matrix.round(3), use_container_width=True)

def show_trends_section(selected_indicators):
    """Seção de tendências simplificada"""
    
    st.header("📈 Análise de Tendências")
    
    try:
        analyzer = EconomicAnalyzer()
        analyzer.load_indicators(selected_indicators)
        
        for i, indicator in enumerate(selected_indicators):
            if indicator in analyzer.indicators_data:
                st.subheader(f"📊 {get_indicator_name(indicator)}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Gráfico simplificado
                    data = analyzer.indicators_data[indicator]
                    fig = px.line(
                        data.tail(100),  # Menos pontos para melhor performance
                        x='date',
                        y='value',
                        title=f'Últimos 100 registros - {get_indicator_name(indicator)}'
                    )
                    fig.update_layout(height=250)
                    st.plotly_chart(
                        fig, 
                        use_container_width=True,
                        key=f"trend_{indicator}_{i}_{datetime.now().timestamp()}"
                    )
                
                with col2:
                    # Análise de tendência
                    trend_analysis = analyzer.analyze_indicator_trends(indicator)
                    
                    if trend_analysis:
                        st.markdown("**📊 Análise:**")
                        
                        trend_text = trend_analysis['trend']
                        if "Alta" in trend_text:
                            st.success(trend_text)
                        elif "Baixa" in trend_text:
                            st.error(trend_text)
                        else:
                            st.warning(trend_text)
                        
                        st.metric("Valor Atual", f"{trend_analysis['current_value']:.2f}")
                        st.metric("Variação", f"{trend_analysis['pct_change']:+.2f}%")
                        
    except Exception as e:
        st.error(f"❌ Erro na análise de tendências: {e}")

def show_forecasts_section(selected_indicators, forecast_periods):
    """Seção de previsões simplificada"""
    
    st.header("🔮 Previsões Econômicas")
    
    if st.button("🚀 Gerar Previsões", key="gen_forecasts"):
        with st.spinner("Gerando previsões com Prophet..."):
            try:
                analyzer = EconomicAnalyzer()
                analyzer.load_indicators(selected_indicators)
                
                forecasts = analyzer.generate_forecast_comparison(selected_indicators, forecast_periods)
                
                if forecasts:
                    st.session_state['forecast_data'] = forecasts
                    st.success(f"✅ Previsões geradas para {len(forecasts)} indicadores!")
                else:
                    st.error("❌ Não foi possível gerar previsões")
                    
            except Exception as e:
                st.error(f"❌ Erro nas previsões: {e}")
    
    # Mostrar previsões se geradas
    if 'forecast_data' in st.session_state:
        forecasts = st.session_state['forecast_data']
        
        st.subheader("📋 Resumo das Previsões")
        
        for indicator, forecast_data in forecasts.items():
            with st.expander(f"📈 {get_indicator_name(indicator)}", expanded=False):
                if not forecast_data.empty:
                    col1, col2, col3 = st.columns(3)
                    
                    first_val = forecast_data['value'].iloc[0]
                    last_val = forecast_data['value'].iloc[-1]
                    trend_pct = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0
                    
                    with col1:
                        st.metric("Primeira Previsão", f"{first_val:.2f}")
                    with col2:
                        st.metric("Última Previsão", f"{last_val:.2f}")
                    with col3:
                        st.metric("Tendência", f"{trend_pct:+.1f}%")
                    
                    st.dataframe(forecast_data.head(), use_container_width=True)

def show_downloads_section(selected_indicators):
    """Seção de downloads simplificada"""
    
    st.header("📄 Downloads e Exportação")
    
    # Downloads dos resultados gerados
    if 'ai_results' in st.session_state:
        results = st.session_state['ai_results']
        
        st.subheader("📋 Relatórios Disponíveis")
        
        if 'ai_report' in results and results['ai_report']:
            st.download_button(
                label="📥 Download Relatório IA (Markdown)",
                data=results['ai_report'],
                file_name=f"relatorio_ia_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                key=f"download_report_{datetime.now().timestamp()}"
            )
    
    if 'correlation_data' in st.session_state:
        correlation_matrix = st.session_state['correlation_data']
        csv_data = correlation_matrix.to_csv()
        
        st.download_button(
            label="📥 Download Correlações (CSV)",
            data=csv_data,
            file_name=f"correlacoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key=f"download_corr_{datetime.now().timestamp()}"
        )
    
    if 'forecast_data' in st.session_state:
        forecasts = st.session_state['forecast_data']
        
        st.subheader("🔮 Previsões")
        for i, (indicator, forecast_data) in enumerate(forecasts.items()):
            csv_forecast = forecast_data.to_csv(index=False)
            st.download_button(
                label=f"📥 {get_indicator_name(indicator)} (CSV)",
                data=csv_forecast,
                file_name=f"previsao_{indicator}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key=f"download_forecast_{indicator}_{i}_{datetime.now().timestamp()}"
            )
    
    if not any(key in st.session_state for key in ['ai_results', 'correlation_data', 'forecast_data']):
        st.info("💡 Execute as análises nas outras abas para ter dados disponíveis para download.")

# Função principal para compatibilidade
def main():
    """Função principal para manter compatibilidade"""
    relatorios_ia_page()

if __name__ == "__main__":
    # Apenas para teste isolado
    import streamlit as st
    st.set_page_config(page_title="Relatórios IA", page_icon="🤖", layout="wide")
    main()