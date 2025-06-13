import streamlit as st
import plotly.express as px
import pandas as pd
import time
from components.indicadores import indicator_names, load_data
from ml_core.forecaster import simulate_forecast 

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
        fig = px.line(data, x='date', y='value')
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Simular Previsão"):
            with st.spinner("Calculando previsão..."):
                time.sleep(2)
                
                future_df = simulate_forecast(data, forecast_periods+1) 

                historical_df = pd.DataFrame({'date': data['date'].tail(12), 'value': data['value'].tail(12), 'tipo': 'Histórico'})
                combined_df = pd.concat([historical_df, future_df])
                fig = px.line(combined_df, x='date', y='value', color='tipo')
                st.plotly_chart(fig, use_container_width=True)
                st.success("Previsão concluída! (Simulação)")
    else:
        st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")