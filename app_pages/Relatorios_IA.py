# app_pages/Relatorios_IA.py
"""
Página de Relatórios com IA
Funcionalidades avançadas de análise econômica com inteligência artificial
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Adicionar path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Imports do ml_core/interpreter
try:
    from ml_core.interpreter import interpreter, analyze_economic_scenario
    from ml_core.interpreter.economic_analyzer import EconomicAnalyzer, quick_economic_analysis
    from ml_core.interpreter.config import get_indicator_name, CUSTOM_CSS
    from database_manager import DatabaseManager
    ML_INTERPRETER_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Erro ao carregar ML Interpreter: {e}")
    ML_INTERPRETER_AVAILABLE = False

def main():
    """Função principal da página Relatórios com IA"""
    
    # Configuração da página apenas se executado diretamente
    if __name__ == "__main__":
        st.set_page_config(
            page_title="Relatórios com IA",
            page_icon="🤖",
            layout="wide"
        )
    
    # CSS customizado
    if ML_INTERPRETER_AVAILABLE:
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Título principal
    st.title("🤖 Relatórios Econômicos com Inteligência Artificial")
    st.markdown("---")
    
    # Verificar disponibilidade do sistema
    if not ML_INTERPRETER_AVAILABLE:
        st.error("❌ Sistema de IA não disponível. Verifique a instalação dos componentes.")
        return
    
    # Sidebar - Configurações
    with st.sidebar:
        st.header("⚙️ Configurações de Análise")
        
        # Obter indicadores disponíveis
        db = DatabaseManager()
        stats = db.get_stats()
        available_indicators = [k for k in stats.keys() if k != 'db_size']
        
        if not available_indicators:
            st.error("❌ Nenhum indicador disponível no banco de dados")
            return
        
        # Seleção de indicadores
        selected_indicators = st.multiselect(
            "📈 Selecione os Indicadores:",
            available_indicators,
            default=available_indicators[:3] if available_indicators else [],
            format_func=get_indicator_name,
            help="Escolha os indicadores econômicos para análise"
        )
        
        # Período de análise
        period_months = st.slider(
            "📅 Período de Análise (meses):",
            min_value=3,
            max_value=36,
            value=12,
            step=1,
            help="Período histórico para análise de correlações e tendências"
        )
        
        # Períodos de previsão
        forecast_periods = st.slider(
            "🔮 Períodos de Previsão:",
            min_value=3,
            max_value=24,
            value=6,
            step=1,
            help="Número de períodos futuros para previsão"
        )
        
        st.markdown("---")
        
        # Status do sistema
        if st.button("📊 Status do Sistema"):
            status = interpreter.get_status()
            st.json(status)
    
    # Verificar se indicadores foram selecionados
    if not selected_indicators:
        st.warning("⚠️ Selecione pelo menos um indicador para análise.")
        show_welcome_section()
        return
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🤖 Relatório Completo",
        "📊 Visão Geral", 
        "🔗 Correlações", 
        "📈 Tendências", 
        "🔮 Previsões",
        "📄 Exportação"
    ])
    
    with tab1:
        show_ai_report_tab(selected_indicators, period_months, forecast_periods)
    
    with tab2:
        show_overview_tab(selected_indicators, stats)
    
    with tab3:
        show_correlation_tab(selected_indicators, period_months)
    
    with tab4:
        show_trends_tab(selected_indicators)
    
    with tab5:
        show_forecasts_tab(selected_indicators, forecast_periods)
    
    with tab6:
        show_export_tab(selected_indicators, period_months, forecast_periods)

def show_welcome_section():
    """Seção de boas-vindas quando nenhum indicador está selecionado"""
    
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
    
    st.info("👈 Selecione os indicadores na barra lateral para começar a análise!")

def show_ai_report_tab(selected_indicators, period_months, forecast_periods):
    """Tab principal com relatório completo de IA"""
    
    st.header("🤖 Relatório Econômico Inteligente")
    
    # Botão para gerar análise completa
    if st.button("🚀 Gerar Relatório Completo com IA", type="primary"):
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔄 Carregando dados...")
            progress_bar.progress(20)
            
            # Executar análise completa
            with st.spinner("🧠 Analisando dados e gerando insights..."):
                results = quick_economic_analysis(selected_indicators, period_months)
            
            progress_bar.progress(60)
            status_text.text("📊 Gerando visualizações...")
            
            if results:
                # Salvar na sessão
                st.session_state['ai_analysis_results'] = results
                st.session_state['analysis_timestamp'] = datetime.now()
                
                progress_bar.progress(100)
                status_text.text("✅ Análise concluída!")
                
                # Mostrar resultados
                show_complete_analysis_results(results, context="main_tab")
                
            else:
                st.error("❌ Falha na geração do relatório")
                
        except Exception as e:
            st.error(f"❌ Erro na análise: {str(e)}")
        finally:
            progress_bar.empty()
            status_text.empty()
    
    # Mostrar último relatório se existir
    if 'ai_analysis_results' in st.session_state:
        st.subheader("📋 Último Relatório Gerado")
        timestamp = st.session_state.get('analysis_timestamp', 'Desconhecido')
        st.caption(f"Gerado em: {timestamp}")
        
        with st.expander("Ver Relatório Completo", expanded=True):
            show_complete_analysis_results(st.session_state['ai_analysis_results'], context="expander")

def show_complete_analysis_results(results, context="default"):
    """Mostra os resultados completos da análise"""
    
    # Relatório de IA em texto
    if 'ai_report' in results and results['ai_report']:
        st.subheader("📄 Relatório Textual")
        st.markdown(results['ai_report'])
        
        # Download do relatório
        st.download_button(
            label="📥 Download Relatório (Markdown)",
            data=results['ai_report'],
            file_name=f"relatorio_ia_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            key=f"download_ai_report_{context}_{datetime.now().strftime('%H%M%S')}"
        )
    
    # Gráficos
    if 'charts' in results:
        charts = results['charts']
        
        # Gráfico multi-indicadores
        if charts.get('multi_indicator_chart'):
            st.subheader("📈 Evolução dos Indicadores")
            st.plotly_chart(
                charts['multi_indicator_chart'], 
                use_container_width=True,
                key=f"multi_indicator_chart_{context}_{datetime.now().timestamp()}"
            )
        
        # Heatmap de correlação
        if charts.get('correlation_heatmap'):
            st.subheader("🔥 Mapa de Correlações")
            st.plotly_chart(
                charts['correlation_heatmap'], 
                use_container_width=True,
                key=f"correlation_heatmap_{context}_{datetime.now().timestamp()}"
            )
        
        # Comparação de previsões
        if charts.get('forecast_comparison'):
            st.subheader("🔮 Previsões Comparativas")
            st.plotly_chart(
                charts['forecast_comparison'], 
                use_container_width=True,
                key=f"forecast_comparison_{context}_{datetime.now().timestamp()}"
            )

def show_overview_tab(selected_indicators, stats):
    """Tab de visão geral dos dados"""
    
    st.header("📊 Visão Geral dos Dados")
    
    # Métricas resumo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Indicadores", len(selected_indicators))
    
    with col2:
        total_records = sum([stats[ind]['count'] for ind in selected_indicators if ind in stats])
        st.metric("📋 Registros", f"{total_records:,}")
    
    with col3:
        if selected_indicators:
            oldest = min([stats[ind]['period'].split(' a ')[0] for ind in selected_indicators if ind in stats])
            st.metric("📅 Início", oldest)
    
    with col4:
        if selected_indicators:
            newest = max([stats[ind]['period'].split(' a ')[1] for ind in selected_indicators if ind in stats])
            st.metric("📅 Fim", newest)
    
    # Tabela detalhada
    st.subheader("📋 Detalhes dos Indicadores")
    
    details_data = []
    for indicator in selected_indicators:
        if indicator in stats:
            details_data.append({
                'Indicador': get_indicator_name(indicator),
                'Código': indicator,
                'Registros': stats[indicator]['count'],
                'Período': stats[indicator]['period'],
                'Status': '✅ Ativo' if stats[indicator]['count'] > 0 else '❌ Inativo'
            })
    
    if details_data:
        df_details = pd.DataFrame(details_data)
        st.dataframe(df_details, use_container_width=True)

def show_correlation_tab(selected_indicators, period_months):
    """Tab de análise de correlações"""
    
    st.header("🔗 Análise de Correlações")
    
    if len(selected_indicators) < 2:
        st.warning("⚠️ Selecione pelo menos 2 indicadores para análise de correlação.")
        return
    
    if st.button("🔄 Calcular Correlações"):
        with st.spinner("Calculando correlações..."):
            try:
                analyzer = EconomicAnalyzer()
                analyzer.load_indicators(selected_indicators)
                correlation_matrix = analyzer.calculate_correlation_matrix(period_months)
                
                if correlation_matrix is not None:
                    # Heatmap
                    st.subheader("🔥 Mapa de Calor")
                    heatmap = analyzer.plot_correlation_heatmap()
                    st.plotly_chart(
                        heatmap, 
                        use_container_width=True,
                        key=f"correlation_heatmap_tab_{datetime.now().timestamp()}"
                    )
                    
                    # Matriz numérica
                    st.subheader("📊 Matriz de Correlação")
                    display_matrix = correlation_matrix.copy()
                    display_matrix.columns = [get_indicator_name(col) for col in display_matrix.columns]
                    display_matrix.index = [get_indicator_name(idx) for idx in display_matrix.index]
                    st.dataframe(display_matrix.round(3), use_container_width=True)
                    
                    # Análise de correlações fortes
                    show_correlation_insights(correlation_matrix)
                else:
                    st.error("❌ Não foi possível calcular a matriz de correlação")
                    
            except Exception as e:
                st.error(f"❌ Erro na análise: {e}")

def show_correlation_insights(correlation_matrix):
    """Mostra insights das correlações"""
    
    st.subheader("💡 Insights de Correlação")
    
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
        df_corr = pd.DataFrame(strong_correlations)
        df_corr = df_corr.sort_values('Correlação', key=abs, ascending=False)
        st.dataframe(df_corr, use_container_width=True)
    else:
        st.info("ℹ️ Nenhuma correlação forte (>0.5) encontrada no período analisado.")

def show_trends_tab(selected_indicators):
    """Tab de análise de tendências"""
    
    st.header("📈 Análise de Tendências")
    
    try:
        analyzer = EconomicAnalyzer()
        analyzer.load_indicators(selected_indicators)
        
        for indicator in selected_indicators:
            if indicator in analyzer.indicators_data:
                st.subheader(f"📊 {get_indicator_name(indicator)}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Gráfico
                    data = analyzer.indicators_data[indicator]
                    fig = px.line(
                        data.tail(200),
                        x='date',
                        y='value',
                        title=f'Evolução - {get_indicator_name(indicator)}'
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(
                        fig, 
                        use_container_width=True,
                        key=f"trend_chart_{indicator}_{datetime.now().timestamp()}"
                    )
                
                with col2:
                    # Análise de tendência
                    trend_analysis = analyzer.analyze_indicator_trends(indicator)
                    
                    if trend_analysis:
                        st.markdown("**📊 Análise:**")
                        
                        # Trend com cores
                        trend_text = trend_analysis['trend']
                        if "Alta" in trend_text:
                            st.success(trend_text)
                        elif "Baixa" in trend_text:
                            st.error(trend_text)
                        else:
                            st.warning(trend_text)
                        
                        # Métricas
                        st.metric("Valor Atual", f"{trend_analysis['current_value']:.2f}")
                        st.metric("Variação", f"{trend_analysis['pct_change']:+.2f}%")
                        st.metric("Volatilidade", f"{trend_analysis['volatility']:.2f}")
                        
    except Exception as e:
        st.error(f"❌ Erro na análise de tendências: {e}")

def show_forecasts_tab(selected_indicators, forecast_periods):
    """Tab de previsões"""
    
    st.header("🔮 Previsões Econômicas")
    
    if st.button("🚀 Gerar Previsões"):
        with st.spinner("Gerando previsões..."):
            try:
                analyzer = EconomicAnalyzer()
                analyzer.load_indicators(selected_indicators)
                
                forecasts = analyzer.generate_forecast_comparison(selected_indicators, forecast_periods)
                
                if forecasts:
                    # Gráfico comparativo
                    st.subheader("📊 Previsões Comparativas")
                    forecast_chart = analyzer.plot_forecast_comparison(forecasts)
                    st.plotly_chart(
                        forecast_chart, 
                        use_container_width=True,
                        key=f"forecast_chart_tab_{datetime.now().timestamp()}"
                    )
                    
                    # Tabelas individuais
                    st.subheader("📋 Dados das Previsões")
                    
                    for indicator, forecast_data in forecasts.items():
                        with st.expander(f"📈 {get_indicator_name(indicator)}"):
                            st.dataframe(forecast_data, use_container_width=True)
                            
                            # Métricas da previsão
                            if not forecast_data.empty:
                                first_val = forecast_data['value'].iloc[0]
                                last_val = forecast_data['value'].iloc[-1]
                                trend_pct = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Primeira Previsão", f"{first_val:.2f}")
                                with col2:
                                    st.metric("Última Previsão", f"{last_val:.2f}")
                                with col3:
                                    st.metric("Tendência", f"{trend_pct:+.1f}%")
                else:
                    st.error("❌ Não foi possível gerar previsões")
                    
            except Exception as e:
                st.error(f"❌ Erro nas previsões: {e}")

def show_export_tab(selected_indicators, period_months, forecast_periods):
    """Tab de exportação de dados"""
    
    st.header("📄 Exportação de Relatórios")
    
    st.info("💡 Execute uma análise completa na primeira aba para ter dados para exportar.")
    
    if 'ai_analysis_results' in st.session_state:
        results = st.session_state['ai_analysis_results']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Relatórios Textuais")
            
            if 'ai_report' in results:
                # Download Markdown
                st.download_button(
                    label="📥 Download Relatório (MD)",
                    data=results['ai_report'],
                    file_name=f"relatorio_ia_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown",
                    key=f"download_ai_report_export_{datetime.now().strftime('%H%M%S')}"
                )
        
        with col2:
            st.subheader("📊 Dados Numéricos")
            
            if 'correlation_matrix' in results and results['correlation_matrix'] is not None:
                # Download CSV da matriz de correlação
                csv_data = results['correlation_matrix'].to_csv()
                st.download_button(
                    label="📥 Download Correlações (CSV)",
                    data=csv_data,
                    file_name=f"correlacoes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key=f"download_correlations_{datetime.now().strftime('%H%M%S')}"
                )
            
            if 'forecasts' in results:
                # Download das previsões
                for i, (indicator, forecast_data) in enumerate(results['forecasts'].items()):
                    csv_forecast = forecast_data.to_csv(index=False)
                    st.download_button(
                        label=f"📥 Previsão {get_indicator_name(indicator)} (CSV)",
                        data=csv_forecast,
                        file_name=f"previsao_{indicator}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        key=f"download_forecast_{indicator}_{i}_{datetime.now().strftime('%H%M%S')}"
                    )
    
    else:
        st.warning("⚠️ Nenhuma análise disponível para exportação. Execute uma análise completa primeiro.")

if __name__ == "__main__":
    main()