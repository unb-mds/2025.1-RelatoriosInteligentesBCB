import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
from components.indicadores import indicator_names, load_data
from ml_core.forecaster import simulate_forecast, calcular_estatisticas
from utils.report_generator import generate_downloadable_report
from utils.ai_report_generator import AIReportGenerator
from datetime import datetime


def ml_page():
    st.title("Previsões de Indicadores Econômicos")
    indicator = st.selectbox(
        "Selecione o indicador para prever",
        list(indicator_names.keys()),
        format_func=lambda x: indicator_names.get(x, x)
    )
    forecast_periods = st.slider("Número de meses para prever", 1, 12, 6)
    
    data = load_data(indicator)

    if data is not None and not data.empty:
        st.subheader(f"Dados históricos de {indicator_names[indicator]}")
        fig_hist = px.line(data, x='date', y='value')
        st.plotly_chart(fig_hist, use_container_width=True)

        if st.button("Simular Previsão"):
            with st.spinner("Calculando previsão..."):
                time.sleep(2) # Simulação de processamento
                
                future_df = simulate_forecast(data, forecast_periods)
                future_df['tipo'] = 'Previsto'
                future_df['date_str'] = future_df['date'].dt.strftime('%d/%b/%Y')

                historical_df = pd.DataFrame({
                    'date': data['date'].tail(12),
                    'value': data['value'].tail(12),
                    'tipo': 'Histórico'
                })
                combined_df = pd.concat([historical_df, future_df])

                combined_df['date_str'] = combined_df['date'].dt.strftime('%d/%b/%Y')
                print("Valores únicos na coluna 'tipo':", combined_df['tipo'].unique())
                fig_forecast = px.line(
                    combined_df,
                    x='date_str',
                    y='value',
                    color='tipo',
                    title=f"Previsão vs Histórico para {indicator_names[indicator]}",
                    labels={'date_str': 'Data', 'value': 'Valor'},
                    color_discrete_map={
                        'Histórico': '#63a9e9',
                        'Previsto': '#00529F',
                    }, # <-- Comma here, 'markers=True' is outside the dictionary
                    markers=True # <-- Moved to here, as a direct argument to px.line
            )

                fig_forecast.update_xaxes(tickangle=90)
                
                fig_forecast.add_trace(go.Scatter(
                    x=future_df['date_str'],
                    y=future_df['upper_bound'],
                    name='upper_bound',
                    mode='lines',
                    line=dict(color='rgba(0,50,100,0.2)'),
                    showlegend=False
                ))

                fig_forecast.add_trace(go.Scatter(
                    x=future_df['date_str'],
                    y=future_df['lower_bound'],
                    name='lower_bound',
                    mode='lines',
                    line=dict(color='rgba(0,50,100,0.2)'),
                    fill='tonexty',
                    fillcolor='rgba(0,50,100,0.2)',
                    showlegend=False
                ))

                estat_hist = calcular_estatisticas(historical_df, 'Histórico')
                estat_prev = calcular_estatisticas(future_df, 'Previsto')
                tabela_estatisticas = pd.concat([estat_hist, estat_prev], axis=1)

                interpretative_text = (
                    f"Análise de previsão para o indicador {indicator_names[indicator]} para os próximos {forecast_periods} meses.\n\n"
                    "O modelo projetou os valores futuros com base nos dados históricos. "
                    "A tabela de estatísticas resume as principais métricas do período histórico em comparação com o período previsto. "
                    "Observe as mudanças na média e no desvio padrão para entender a tendência e a volatilidade esperadas."
                )

                st.session_state['forecast_results'] = {
                    'fig': fig_forecast,
                    'stats_table': tabela_estatisticas,
                    'text': interpretative_text,
                    'combined_df': combined_df, # Guardando o DF completo para o relatório
                    'indicator_name': indicator_names[indicator]
                }
                st.success("Previsão concluída!")

        if 'forecast_results' in st.session_state:
            results = st.session_state['forecast_results']
            
            # Exibe os resultados na tela
            st.plotly_chart(results['fig'], use_container_width=True)
            st.write("Tabela Estatística: Histórico vs Previsão")
            st.table(results['stats_table'])
            st.info(results['text']) # Exibindo o texto interpretativo


            # NOVA SEÇÃO: RELATÓRIOS PERSONALIZADOS COM IA
            st.markdown("---")
            st.header("🤖 Relatórios Personalizados com IA")
            
            # Container único para evitar duplicação
            with st.container():
                # Inicializar estado se não existir
                if 'ai_button_clicked' not in st.session_state:
                    st.session_state['ai_button_clicked'] = False
                    st.session_state['ai_button_type'] = None
                
                # Só mostrar interface se não estiver processando
                if not st.session_state['ai_button_clicked']:
                    ai_generator = AIReportGenerator()
                    
                    st.markdown("""
                    **Escolha o tipo de relatório que melhor atende suas necessidades:**
                    
                    - **📊 Técnico**: Análise econômica detalhada com termos especializados
                    - **📖 Parábolas**: Explicação dos dados usando histórias e analogias didáticas  
                    - **👥 Cidadãos**: Linguagem simples e acessível para todos
                    """)
                    
                    # Usar form para evitar duplicação
                    with st.form("ai_report_form", clear_on_submit=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            tech_clicked = st.form_submit_button("📊 Relatório Técnico", use_container_width=True)
                        
                        with col2:
                            parab_clicked = st.form_submit_button("📖 Parábolas", use_container_width=True)
                        
                        with col3:
                            simple_clicked = st.form_submit_button("👥 Para Cidadãos", use_container_width=True)
                    
                    # Processar cliques
                    if tech_clicked:
                        st.session_state['ai_button_clicked'] = True
                        st.session_state['ai_button_type'] = 'technical'
                        st.rerun()
                    elif parab_clicked:
                        st.session_state['ai_button_clicked'] = True
                        st.session_state['ai_button_type'] = 'parables'
                        st.rerun()
                    elif simple_clicked:
                        st.session_state['ai_button_clicked'] = True
                        st.session_state['ai_button_type'] = 'simple'
                        st.rerun()
                
                # Processar geração de relatório
                elif st.session_state['ai_button_clicked']:
                    ai_generator = AIReportGenerator()
                    report_type = st.session_state['ai_button_type']
                    
                    type_names = {
                        'technical': '📊 Técnico',
                        'parables': '📖 Parábolas',
                        'simple': '👥 Para Cidadãos'
                    }
                    
                    # Mostrar apenas o spinner durante processamento
                    with st.spinner(f"🔄 Gerando relatório {type_names[report_type]}..."):
                        try:
                            report_content = ai_generator.generate_report_content(
                                results['combined_df'], 
                                results['stats_table'], 
                                results['indicator_name'], 
                                report_type
                            )
                            
                            # Salvar resultado
                            st.session_state['ai_report'] = {
                                'content': report_content,
                                'type': report_type,
                                'type_name': type_names[report_type]
                            }
                            
                            # Resetar estado de clique
                            st.session_state['ai_button_clicked'] = False
                            st.session_state['ai_button_type'] = None
                            
                        except Exception as e:
                            st.error(f"Erro ao gerar relatório: {e}")
                            st.session_state['ai_button_clicked'] = False
                            st.session_state['ai_button_type'] = None
                    
                    # Forçar rerun após processamento
                    st.rerun()
            
            # Exibir relatório gerado (fora do container principal)
            if 'ai_report' in st.session_state and not st.session_state.get('ai_button_clicked', False):
                ai_report = st.session_state['ai_report']
                
                st.markdown("---")
                st.subheader(f"📝 Relatório Gerado: {ai_report['type_name']}")
                
                # Exibir conteúdo
                with st.container():
                    st.markdown("**Conteúdo do Relatório:**")
                    st.text_area(
                        label="",
                        value=ai_report['content'],
                        height=400,
                        disabled=True,
                        label_visibility="collapsed",
                        key="report_display"
                    )
                
                # Botões de ação
                with st.container():
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        if st.button("📋 Copiar Texto", use_container_width=True):
                            st.code(ai_report['content'], language="text")
                            st.success("✅ Texto disponível acima para cópia!")
                    
                    with col2:
                        if st.button("📄 Download PDF", use_container_width=True):
                            with st.spinner("📄 Gerando PDF..."):
                                ai_generator = AIReportGenerator()
                                pdf_bytes = ai_generator.generate_pdf_report(
                                    ai_report['content'],
                                    ai_report['type'],
                                    results['indicator_name']
                                )
                                
                                if pdf_bytes:
                                    st.download_button(
                                        label="⬇️ Baixar Relatório PDF",
                                        data=pdf_bytes,
                                        file_name=f"relatorio_ia_{ai_report['type']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                else:
                                    st.error("❌ Erro ao gerar PDF")
                    
                    with col3:
                        if st.button("🔄 Gerar Outro Tipo de Relatório", use_container_width=True):
                            if 'ai_report' in st.session_state:
                                del st.session_state['ai_report']
                            st.rerun()







            st.markdown("---")
            st.header("📥 Download do Relatório Completo")

            if st.button("Gerar Relatório para Download"):
                with st.spinner("Gerando seu relatório em PDF... Por favor, aguarde."):
                    
                    report_bytes = generate_downloadable_report(
                        interpretative_text=results['text'],
                        forecast_df=results['combined_df'], # Passando o DF combinado
                        metrics_df=results['stats_table'],  # Passando a tabela de estatísticas
                        fig_plot=results['fig']
                    )

                    st.download_button(
                        label="✅ Clique aqui para baixar o Relatório",
                        data=report_bytes,
                        file_name=f"relatorio_previsao_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
    else:
        st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")