import streamlit as st
import plotly.express as px
import pandas as pd
from components.indicadores import indicator_names, load_data

def dashboard_page():
    st.title("📈 Dashboard Econômico - Dados do Banco Central do Brasil")

    st.sidebar.subheader(":blue[Indicadores]")
    indicators = st.sidebar.multiselect(
        ":blue[Selecione os indicadores para visualizar]",
        list(indicator_names.keys()),
        default=['ipca'],
        format_func=lambda x: indicator_names.get(x, x)
    )
    if not indicators:
        st.warning("Por favor, selecione pelo menos um indicador no menu lateral.")
    else:
        for indicator in indicators:
            data = load_data(indicator)

            if data is not None and not data.empty:
                # Garante que as colunas de data sejam do tipo datetime
                data['date'] = pd.to_datetime(data['date'])
                data['created_at'] = pd.to_datetime(data['created_at'])

            if data is not None and not data.empty:
                st.subheader(indicator_names[indicator])
                fig = px.line(
                    data, x='date', y='value',
                    title=f'Evolução de {indicator_names[indicator]}',
                    labels={'date': 'Data', 'value': 'Valor'}
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")

                # Tabela 1: Estatísticas Principais
                st.markdown("##### Estatísticas")
                all_stats = data['value'].describe()
                desired_metrics_map = {
                    'mean': 'Média',
                    '50%': 'Mediana',
                    'std': 'Desvio Padrão',
                    'min': 'Mínimo',
                    'max': 'Máximo'
                }
                selected_stats = all_stats.loc[desired_metrics_map.keys()]
                final_stats_df = selected_stats.to_frame(name='Valor').rename(index=desired_metrics_map)
                st.table(final_stats_df)

                st.write("") 

                # Tabela 2: Dados Recentes (com todas as colunas e formatação)
                st.markdown("##### Dados Recentes")
                recent_data = data.sort_values('date', ascending=False).head(5).copy()
                
                recent_data['date'] = recent_data['date'].dt.strftime('%d/%m/%Y')
                recent_data['created_at'] = recent_data['created_at'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo').dt.strftime('%d/%m/%Y %H:%M')

                recent_data.rename(columns={
                    'date': 'Data do Valor',
                    'value': 'Valor',
                    'created_at': 'Data de Coleta'
                }, inplace=True)
                
                st.table(recent_data[[ 'Data do Valor', 'Valor', 'Data de Coleta']].reset_index(drop=True))
                

            else:
                st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")
