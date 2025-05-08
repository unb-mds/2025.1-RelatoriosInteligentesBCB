# Arquivo: app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from database_manager import DatabaseManager
from data_collector import BCBDataCollector
from datetime import datetime, timedelta

# ========================== CONFIGURAÇÕES INICIAIS ==========================

# Configuração da página
st.set_page_config(
    page_title="Dashboard Econômico - Dados BCB",
    page_icon="📊",
    layout="wide"
)

# Inicialização do banco e coletor (evita múltiplas criações desnecessárias)
db_manager = DatabaseManager()
collector = BCBDataCollector()

# ========================== FUNÇÕES AUXILIARES ==========================

# Função para atualizar os dados
def update_data(years=5):
    with st.spinner("Atualizando dados..."):
        data = collector.collect_all_data(last_n_years=years)
        results = db_manager.save_all_data(data)

        success = all(results.values())
        if success:
            st.success("Dados atualizados com sucesso!")
        else:
            st.error("Houve problemas na atualização de alguns indicadores.")
        return success

# Função para carregar dados com cache
@st.cache_data(ttl=3600)
def load_data(table_name: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    return db_manager.load_data(table_name, start_date, end_date)

# ========================== CONSTANTES ==========================

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

# ========================== INTERFACE PRINCIPAL ==========================

st.title("Dashboard Econômico - Dados do Banco Central do Brasil")

# Sidebar
st.sidebar.title("Opções")

# Atualização de dados
st.sidebar.subheader("Atualização de Dados")
years_to_fetch = st.sidebar.slider("Anos de dados para coletar", 1, 10, 5)
update_button = st.sidebar.button("Atualizar Dados")
if update_button:
    update_data(years=years_to_fetch)

# Seleção de indicadores
st.sidebar.subheader("Indicadores")
indicators = st.sidebar.multiselect(
    "Selecione os indicadores para visualizar",
    list(indicator_names.keys()),
    default=['ipca', 'selic', 'pib']
)

# Seleção de período
st.sidebar.subheader("Período")
current_year = datetime.now().year
years_range = list(range(2000, current_year + 1))
start_year, end_year = st.sidebar.select_slider(
    "Selecione o período",
    options=years_range,
    value=(current_year - 5, current_year)
)
start_date = f"{start_year}-01-01"
end_date = f"{end_year}-12-31"

# ========================== CONTEÚDO PRINCIPAL ==========================

if not indicators:
    st.warning("Por favor, selecione pelo menos um indicador no menu lateral.")
else:
    tab1, tab2, tab3 = st.tabs(["Séries Temporais", "Análise Comparativa", "Estatísticas"])

    # ===================== SÉRIES TEMPORAIS =====================
    with tab1:
        st.header("Séries Temporais")
        for indicator in indicators:
            data = load_data(indicator, start_date, end_date)

            if data is not None and not data.empty:
                st.subheader(indicator_names[indicator])
                
                fig = px.line(
                    data,
                    x='date',
                    y='value',
                    title=f'Evolução de {indicator_names[indicator]}',
                    labels={'date': 'Data', 'value': 'Valor'}
                )
                st.plotly_chart(fig, use_container_width=True)

                col1, col2, col3, col4 = st.columns(4)

                latest = data.iloc[-1]
                previous = data.iloc[-2] if len(data) > 1 else latest

                col1.metric(
                    "Valor Mais Recente",
                    f"{latest['value']:.2f}",
                    f"{latest['value'] - previous['value']:.2f}" if previous is not latest else "0.00"
                )

                col2.metric("Média do Período", f"{data['value'].mean():.2f}")

                max_val = data['value'].max()
                max_date = data.loc[data['value'].idxmax(), 'date'].strftime('%d/%m/%Y')
                col3.metric("Máximo", f"{max_val:.2f}", f"em {max_date}")

                min_val = data['value'].min()
                min_date = data.loc[data['value'].idxmin(), 'date'].strftime('%d/%m/%Y')
                col4.metric("Mínimo", f"{min_val:.2f}", f"em {min_date}")

                st.markdown("---")
            else:
                st.error(f"Não há dados disponíveis para {indicator_names[indicator]} no período selecionado.")

    # ===================== ANÁLISE COMPARATIVA =====================
    with tab2:
        st.header("Análise Comparativa")

        if len(indicators) > 1:
            dfs = []
            for indicator in indicators:
                data = load_data(indicator, start_date, end_date)
                if data is not None and not data.empty:
                    data = data.copy()
                    data['indicator'] = indicator_names[indicator]
                    data['normalized'] = (data['value'] - data['value'].min()) / (data['value'].max() - data['value'].min())
                    dfs.append(data)

            if dfs:
                combined = pd.concat(dfs)

                st.subheader("Comparação de Indicadores (Normalizados)")
                fig1 = px.line(
                    combined,
                    x='date',
                    y='normalized',
                    color='indicator',
                    title='Comparação de Indicadores (Valores Normalizados)',
                    labels={'date': 'Data', 'normalized': 'Valor Normalizado', 'indicator': 'Indicador'}
                )
                st.plotly_chart(fig1, use_container_width=True)

                st.subheader("Matriz de Correlação")
                pivot = combined.pivot_table(index='date', columns='indicator', values='value', aggfunc='mean')
                corr = pivot.corr()

                fig2, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
                plt.title('Correlação entre Indicadores')
                st.pyplot(fig2)

                st.subheader("Análise Temporal")
                combined['year'] = combined['date'].dt.year
                combined['month'] = combined['date'].dt.month

                time_option = st.radio("Selecione o tipo de análise temporal:", ["Média Anual", "Variação Anual"])
                if time_option == "Média Anual":
                    annual_avg = combined.groupby(['year', 'indicator'])['value'].mean().reset_index()
                    fig3 = px.line(
                        annual_avg,
                        x='year',
                        y='value',
                        color='indicator',
                        title='Média Anual por Indicador',
                        labels={'year': 'Ano', 'value': 'Valor Médio', 'indicator': 'Indicador'}
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    pivoted = combined.pivot_table(index='year', columns='indicator', values='value', aggfunc='mean')
                    annual_change = pivoted.pct_change() * 100
                    annual_change = annual_change.reset_index().melt(id_vars='year', var_name='indicator', value_name='change')
                    fig3 = px.bar(
                        annual_change,
                        x='year',
                        y='change',
                        color='indicator',
                        barmode='group',
                        title='Variação Percentual Anual por Indicador',
                        labels={'year': 'Ano', 'change': 'Variação (%)', 'indicator': 'Indicador'}
                    )
                    st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Selecione pelo menos dois indicadores para análise comparativa.")

    # ===================== ESTATÍSTICAS =====================
    with tab3:
        st.header("Estatísticas Detalhadas")
        for indicator in indicators:
            data = load_data(indicator, start_date, end_date)
            if data is not None and not data.empty:
                st.subheader(indicator_names[indicator])

                stats = data['value'].describe()
                stats_df = pd.DataFrame({'Estatística': stats.index, 'Valor': stats.values})

                last_obs = data.sort_values('date', ascending=False).head(5).copy()
                last_obs['date'] = last_obs['date'].dt.strftime('%d/%m/%Y')

                col1, col2 = st.columns(2)
                with col1:
                    st.write("Estatísticas do Período")
                    st.dataframe(stats_df)

                with col2:
                    st.write("Últimas Observações")
                    st.dataframe(last_obs[['date', 'value']])

                col3, col4 = st.columns(2)
                with col3:
                    fig_hist = px.histogram(
                        data,
                        x='value',
                        nbins=20,
                        title=f'Distribuição de {indicator_names[indicator]}',
                        labels={'value': 'Valor', 'count': 'Frequência'}
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)

                with col4:
                    fig_box = px.box(
                        data,
                        y='value',
                        title=f'Boxplot de {indicator_names[indicator]}',
                        labels={'value': 'Valor'}
                    )
                    st.plotly_chart(fig_box, use_container_width=True)

                st.markdown("---")
            else:
                st.error(f"Não há dados disponíveis para {indicator_names[indicator]} no período selecionado.")

# Rodapé
st.markdown("---")
st.caption("Dashboard desenvolvido com dados do Banco Central do Brasil")
