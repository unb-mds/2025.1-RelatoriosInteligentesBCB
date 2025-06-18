# ml_core/interpreter/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Adicionar o diretório raiz ao path para imports absolutos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Imports absolutos em vez de relativos
from ml_core.interpreter.economic_analyzer import EconomicAnalyzer, quick_economic_analysis
from ml_core.interpreter.config import CUSTOM_CSS, get_indicator_name
from database_manager import DatabaseManager

# Configuração da página
st.set_page_config(
    page_title="Dashboard Econômico",
    page_icon="📊",
    layout="wide"
)

# CSS customizado
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def main():
    st.title("📊 Dashboard de Análise Econômica")
    st.markdown("---")
    
    # Sidebar - Configurações
    st.sidebar.header("⚙️ Configurações de Análise")
    
    # Obter indicadores disponíveis
    db = DatabaseManager()
    stats = db.get_stats()
    available_indicators = [k for k in stats.keys() if k != 'db_size']
    
    # Seleção de indicadores
    selected_indicators = st.sidebar.multiselect(
        "📈 Selecione os Indicadores:",
        available_indicators,
        default=available_indicators[:4] if available_indicators else [],
        format_func=get_indicator_name
    )
    
    # Período de análise
    period_months = st.sidebar.slider(
        "📅 Período de Análise (meses):",
        min_value=3,
        max_value=24,
        value=12,
        step=1
    )
    
    # Períodos de previsão
    forecast_periods = st.sidebar.slider(
        "🔮 Períodos de Previsão:",
        min_value=3,
        max_value=24,
        value=6,
        step=1
    )
    
    if not selected_indicators:
        st.warning("⚠️ Selecione pelo menos um indicador para análise.")
        return
    
    # Botão de análise
    if st.sidebar.button("🚀 Executar Análise Completa"):
        run_complete_analysis(selected_indicators, period_months, forecast_periods)
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", 
        "🔗 Correlações", 
        "📈 Tendências", 
        "🔮 Previsões",
        "🤖 Relatório IA"
    ])
    
    with tab1:
        show_overview_tab(selected_indicators, stats)
    
    with tab2:
        show_correlation_tab(selected_indicators, period_months)
    
    with tab3:
        show_trends_tab(selected_indicators)
    
    with tab4:
        show_forecasts_tab(selected_indicators, forecast_periods)
    
    with tab5:
        show_ai_report_tab(selected_indicators)

def run_complete_analysis(indicators, period_months, forecast_periods):
    """Executa análise completa com progress bar"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔄 Carregando dados...")
        progress_bar.progress(20)
        
        # Executar análise completa
        analysis_results = quick_economic_analysis(indicators, period_months)
        
        progress_bar.progress(60)
        status_text.text("📊 Gerando visualizações...")
        
        # Salvar resultados na sessão
        st.session_state['analysis_results'] = analysis_results
        st.session_state['last_analysis_time'] = datetime.now()
        
        progress_bar.progress(100)
        status_text.text("✅ Análise concluída!")
        
        st.success("🎉 Análise completa finalizada! Navegue pelas abas para ver os resultados.")
        
    except Exception as e:
        st.error(f"❌ Erro na análise: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def show_overview_tab(selected_indicators, stats):
    """Tab de visão geral"""
    st.header("📊 Visão Geral dos Dados")
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Indicadores Selecionados", len(selected_indicators))
    
    with col2:
        total_records = sum([stats[ind]['count'] for ind in selected_indicators if ind in stats])
        st.metric("📋 Total de Registros", f"{total_records:,}")
    
    with col3:
        if selected_indicators:
            oldest_date = min([stats[ind]['period'].split(' a ')[0] for ind in selected_indicators if ind in stats])
            st.metric("📅 Início dos Dados", oldest_date)
    
    with col4:
        if selected_indicators:
            newest_date = max([stats[ind]['period'].split(' a ')[1] for ind in selected_indicators if ind in stats])
            st.metric("📅 Último Registro", newest_date)
    
    # Tabela de detalhes
    st.subheader("📋 Detalhes dos Indicadores")
    
    details_data = []
    for indicator in selected_indicators:
        if indicator in stats:
            details_data.append({
                'Indicador': get_indicator_name(indicator),
                'Registros': stats[indicator]['count'],
                'Período': stats[indicator]['period'],
                'Status': '✅ Ativo' if stats[indicator]['count'] > 0 else '❌ Sem dados'
            })
    
    if details_data:
        df_details = pd.DataFrame(details_data)
        st.dataframe(df_details, use_container_width=True)
    
    # Gráfico de evolução temporal (se dados carregados)
    if 'analysis_results' in st.session_state:
        st.subheader("📈 Evolução Temporal dos Indicadores")
        multi_chart = st.session_state['analysis_results']['charts']['multi_indicator_chart']
        if multi_chart:
            st.plotly_chart(multi_chart, use_container_width=True)

def show_correlation_tab(selected_indicators, period_months):
    """Tab de análise de correlações"""
    st.header("🔗 Análise de Correlações")
    
    if len(selected_indicators) < 2:
        st.warning("⚠️ Selecione pelo menos 2 indicadores para análise de correlação.")
        return
    
    if st.button("🔄 Calcular Matriz de Correlação"):
        with st.spinner("Calculando correlações..."):
            analyzer = EconomicAnalyzer()
            analyzer.load_indicators(selected_indicators)
            correlation_matrix = analyzer.calculate_correlation_matrix(period_months)
            
            if correlation_matrix is not None:
                # Heatmap
                st.subheader("🔥 Mapa de Calor - Correlações")
                heatmap = analyzer.plot_correlation_heatmap()
                st.plotly_chart(heatmap, use_container_width=True)
                
                # Tabela de correlações
                st.subheader("📊 Matriz de Correlação")
                # Renomear colunas e índices para nomes amigáveis
                display_matrix = correlation_matrix.copy()
                display_matrix.columns = [get_indicator_name(col) for col in display_matrix.columns]
                display_matrix.index = [get_indicator_name(idx) for idx in display_matrix.index]
                st.dataframe(display_matrix.round(3), use_container_width=True)
                
                # Análise de correlações fortes
                st.subheader("💡 Correlações Mais Relevantes")
                strong_correlations = []
                
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr_value = correlation_matrix.iloc[i, j]
                        if not pd.isna(corr_value) and abs(corr_value) > 0.5:
                            strong_correlations.append({
                                'Par': f"{get_indicator_name(correlation_matrix.columns[i])} × {get_indicator_name(correlation_matrix.columns[j])}",
                                'Correlação': corr_value,
                                'Força': 'Forte' if abs(corr_value) > 0.7 else 'Moderada',
                                'Tipo': 'Positiva' if corr_value > 0 else 'Negativa'
                            })
                
                if strong_correlations:
                    df_correlations = pd.DataFrame(strong_correlations)
                    df_correlations = df_correlations.sort_values('Correlação', key=abs, ascending=False)
                    st.dataframe(df_correlations, use_container_width=True)
                else:
                    st.info("ℹ️ Nenhuma correlação forte encontrada (>0.5) no período analisado.")

def show_trends_tab(selected_indicators):
    """Tab de análise de tendências"""
    st.header("📈 Análise de Tendências")
    
    analyzer = EconomicAnalyzer()
    analyzer.load_indicators(selected_indicators)
    
    # Análise individual de cada indicador
    for indicator in selected_indicators:
        if indicator in analyzer.indicators_data:
            st.subheader(f"📊 {get_indicator_name(indicator)}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico do indicador
                data = analyzer.indicators_data[indicator]
                
                fig = px.line(
                    data.tail(200),  # Últimos 200 pontos
                    x='date',
                    y='value',
                    title=f'Evolução - {get_indicator_name(indicator)}'
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Análise de tendência
                trend_analysis = analyzer.analyze_indicator_trends(indicator)
                
                if trend_analysis:
                    st.markdown("**📊 Análise Atual:**")
                    
                    # Trend indicator com cores
                    trend_text = trend_analysis['trend']
                    if "Alta" in trend_text:
                        st.markdown(f'<p class="trend-up">{trend_text}</p>', unsafe_allow_html=True)
                    elif "Baixa" in trend_text:
                        st.markdown(f'<p class="trend-down">{trend_text}</p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="trend-stable">{trend_text}</p>', unsafe_allow_html=True)
                    
                    # Métricas
                    st.metric("Valor Atual", f"{trend_analysis['current_value']:.2f}")
                    st.metric("Variação (%)", f"{trend_analysis['pct_change']:+.2f}%")
                    st.metric("Volatilidade", f"{trend_analysis['volatility']:.2f}")

def show_forecasts_tab(selected_indicators, forecast_periods):
    """Tab de previsões"""
    st.header("🔮 Previsões Econômicas")
    
    if st.button("🚀 Gerar Previsões"):
        with st.spinner("Gerando previsões..."):
            analyzer = EconomicAnalyzer()
            analyzer.load_indicators(selected_indicators)
            
            forecasts = analyzer.generate_forecast_comparison(selected_indicators, forecast_periods)
            
            if forecasts:
                # Gráfico de comparação
                st.subheader("📊 Comparação de Previsões")
                forecast_chart = analyzer.plot_forecast_comparison(forecasts)
                st.plotly_chart(forecast_chart, use_container_width=True)
                
                # Tabela de previsões
                st.subheader("📋 Dados das Previsões")
                
                for indicator, forecast_data in forecasts.items():
                    with st.expander(f"📈 {get_indicator_name(indicator)}"):
                        st.dataframe(forecast_data, use_container_width=True)
                        
                        # Download CSV
                        csv = forecast_data.to_csv(index=False)
                        st.download_button(
                            label=f"📥 Download {get_indicator_name(indicator)}.csv",
                            data=csv,
                            file_name=f"previsao_{indicator}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )

def show_ai_report_tab(selected_indicators):
    """Tab do relatório de IA"""
    st.header("🤖 Relatório de Análise por IA")
    
    if st.button("🧠 Gerar Relatório Inteligente"):
        with st.spinner("Analisando dados e gerando insights..."):
            analyzer = EconomicAnalyzer()
            analyzer.load_indicators(selected_indicators)
            
            ai_report = analyzer.generate_ai_analysis_report(selected_indicators)
            
            if ai_report:
                st.markdown(ai_report)
                
                # Download do relatório
                st.download_button(
                    label="📥 Download Relatório (MD)",
                    data=ai_report,
                    file_name=f"relatorio_economico_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
                
                # Salvar na sessão para reutilização
                st.session_state['last_ai_report'] = ai_report
            else:
                st.error("❌ Não foi possível gerar o relatório.")
    
    # Mostrar último relatório se existir
    if 'last_ai_report' in st.session_state:
        st.subheader("📋 Último Relatório Gerado")
        with st.expander("Ver Relatório Anterior", expanded=False):
            st.markdown(st.session_state['last_ai_report'])

if __name__ == "__main__":
    main()