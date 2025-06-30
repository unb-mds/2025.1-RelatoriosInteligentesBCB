import streamlit as st
import plotly.express as px
import pandas as pd
import time
from components.indicadores import indicator_names, load_data
from ml_core.forecaster import simulate_forecast, calcular_estatisticas
from utils.report_generator import generate_downloadable_report
from datetime import datetime

def ml_page():
    st.title("Previsões de Indicadores Econômicos")
    
    indicator = st.selectbox(
        "Selecione o indicador para prever",
        list(indicator_names.keys()),
        format_func=lambda x: indicator_names.get(x, x)
    )


    # Atualizado: permite previsão entre 3 e 36 meses
    forecast_periods = st.slider("Número de meses para prever", min_value=3, max_value=36, value=6, step=1)

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
                    'Previsto': '#00529F'
                }
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
