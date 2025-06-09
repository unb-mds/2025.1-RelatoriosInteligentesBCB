import streamlit as st
import plotly.express as px
from components.indicadores import indicator_names, load_data

def dashboard_page():
    st.title("Dashboard Econômico - Dados do Banco Central do Brasil")

    # Slider e botão para atualização de dados
    st.sidebar.subheader("Atualização de Dados")
    years_to_fetch = st.sidebar.slider("Anos de dados para coletar", 1, 10, 5)
    update_button = st.sidebar.button("Atualizar Dados")
    if update_button:
        from Coleta_de_Dados import coleta_page
        coleta_page(years_to_fetch) 
        st.success(f"Dados dos últimos {years_to_fetch} anos atualizados!")


    st.sidebar.subheader("Indicadores")
    indicators = st.sidebar.multiselect(
        "Selecione os indicadores para visualizar",
        list(indicator_names.keys()),
        default=['ipca', 'selic', 'pib'],
        format_func=lambda x: indicator_names.get(x, x)
    )
    if not indicators:
        st.warning("Por favor, selecione pelo menos um indicador no menu lateral.")
    else:
        for indicator in indicators:
            data = load_data(indicator)
            if data is not None and not data.empty:
                st.subheader(indicator_names[indicator])
                fig = px.line(
                    data, x='date', y='value',
                    title=f'Evolução de {indicator_names[indicator]}',
                    labels={'date': 'Data', 'value': 'Valor'}
                )
                st.plotly_chart(fig, use_container_width=True)

                 # Adicione este bloco:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Estatísticas")
                    st.dataframe(data['value'].describe())
                with col2:
                    st.write("Dados Recentes")
                    st.dataframe(data.sort_values('date', ascending=False).head(5))
            else:
                st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")