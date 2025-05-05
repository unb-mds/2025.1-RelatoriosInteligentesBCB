# Arquivo: ml_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from database_manager import DatabaseManager
from ml_models import EconomicPredictor
import os
import joblib

# Configuração da página
st.set_page_config(
    page_title="Previsão Econômica - Machine Learning",
    page_icon="🤖",
    layout="wide"
)

# Função para carregar dados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data(table_name, start_date=None, end_date=None):
    db_manager = DatabaseManager()
    return db_manager.load_data(table_name, start_date, end_date)

# Mapeamento de nomes para exibição
indicator_names = {
    'ipca': 'Inflação (IPCA)',
    'pib': 'PIB Real',
    'divida_pib': 'Dívida/PIB',
    'selic': 'Taxa SELIC Diária',
    'selic_meta': 'Meta da Taxa SELIC',
    'transacoes': 'Saldo em Transações Correntes',
    'cambio_dolar': 'Taxa de Câmbio do Dólar Diária',
    'igpm': 'Índice geral de preços do mercado (IGP-M)',
    'inpc': 'Índice nacional de preços ao consumidor (INPC)',
    'resultado_primario': 'Resultado Primário'
}

# Interface principal
st.title("Previsão de Indicadores Econômicos com Machine Learning")

# Sidebar
st.sidebar.title("Configurações")

# Verificar quais indicadores têm dados
db_manager = DatabaseManager()
available_indicators = {}

for ind in indicator_names.keys():
    data = db_manager.load_data(ind)
    if data is not None and len(data) > 0:
        available_indicators[ind] = indicator_names[ind]

# Seleção de indicador
indicator = st.sidebar.selectbox(
    "Selecione o indicador para prever",
    list(available_indicators.keys()),
    format_func=lambda x: available_indicators[x]
)

# Seleção de modelo
model_type = st.sidebar.selectbox(
    "Selecione o modelo",
    ["Linear Regression", "Ridge Regression", "Lasso Regression", "Random Forest"],
    index=3
)

# Mapeamento de modelos
model_map = {
    "Linear Regression": "linear",
    "Ridge Regression": "ridge",
    "Lasso Regression": "lasso",
    "Random Forest": "random_forest"
}

selected_model = model_map[model_type]

# Número de períodos futuros para prever
forecast_periods = st.sidebar.slider(
    "Número de meses para prever",
    min_value=1,
    max_value=24,
    value=12
)

# Inicializar preditor
predictor = EconomicPredictor()

# Verificar se existem modelos salvos
model_dir = 'models'
model_path = f"{model_dir}/{indicator}_{selected_model}_model.pkl"
scaler_path = f"{model_dir}/{indicator}_scaler.pkl"

model_exists = os.path.exists(model_path) and os.path.exists(scaler_path)

# Avisar ao usuário sobre o status do modelo
if model_exists:
    st.sidebar.success(f"Modelo existente encontrado para {indicator_names[indicator]}")
else:
    st.sidebar.warning(f"Nenhum modelo encontrado para {indicator_names[indicator]}. Por favor, treine o modelo.")

# Botão para treinar modelo
train_button = st.sidebar.button("Treinar Modelo")

# Criar guias
tab1, tab2, tab3 = st.tabs(["Previsões", "Análise do Modelo", "Dados Históricos"])

with tab1:
    # Treinar modelo se solicitado
    if train_button or not model_exists:
        with st.spinner(f"Treinando modelo {model_type} para {indicator_names[indicator]}..."):
            metrics = predictor.train_model(indicator, selected_model)
            
            if metrics:
                st.success("Modelo treinado com sucesso!")
                
                # Exibir métricas
                st.subheader("Métricas de Avaliação")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("MSE", f"{metrics['mse']:.4f}")
                col2.metric("RMSE", f"{metrics['rmse']:.4f}")
                col3.metric("MAE", f"{metrics['mae']:.4f}")
                col4.metric("R²", f"{metrics['r2']:.4f}")
                
                # Exibir gráfico de previsão vs real
                st.subheader("Previsão vs Valores Reais (Conjunto de Teste)")
                st.image(f"{model_dir}/{indicator}_prediction.png")
            else:
                st.error("Falha ao treinar o modelo. Verifique os dados.")
    elif model_exists:
        # Carregar modelo existente
        try:
            predictor.models[indicator] = joblib.load(model_path)
            predictor.scalers[indicator] = joblib.load(scaler_path)
        except Exception as e:
            st.error(f"Erro ao carregar modelo: {e}")
    
    # Fazer previsões
    if indicator in predictor.models or model_exists:
        st.header(f"Previsão de {indicator_names[indicator]} para os próximos {forecast_periods} meses")
        
        with st.spinner("Gerando previsões..."):
            # Tentar carregar o modelo novamente se necessário
            if indicator not in predictor.models and model_exists:
                try:
                    predictor.models[indicator] = joblib.load(model_path)
                    predictor.scalers[indicator] = joblib.load(scaler_path)
                except Exception as e:
                    st.error(f"Erro ao carregar modelo: {e}")
            
            future_preds = predictor.predict_future(indicator, steps=forecast_periods)
            
            if future_preds is not None:
                # Carregar dados históricos para comparação
                historical_data = load_data(indicator)
                
                if historical_data is not None:
                    # Limitar aos últimos 24 meses para visualização
                    historical_data = historical_data.sort_values('date').tail(24)
                    
                    # Preparar dados para gráfico
                    historical_df = pd.DataFrame({
                        'date': historical_data['date'],
                        'value': historical_data['value'],
                        'tipo': 'Histórico'
                    })
                    
                    future_df = pd.DataFrame({
                        'date': future_preds['date'],
                        'value': future_preds['value'],
                        'tipo': 'Previsão'
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
                        line_dash='tipo',
                        color_discrete_map={'Histórico': 'blue', 'Previsão': 'red'}
                    )
                    
                    # Adicionar intervalo de confiança (simplificado)
                    if selected_model == 'random_forest':
                        # Para Random Forest, podemos estimar a incerteza
                        std_dev = historical_data['value'].std() * 0.5
                        
                        upper_bound = future_df['value'] + std_dev
                        lower_bound = future_df['value'] - std_dev
                        
                        fig.add_trace(
                            go.Scatter(
                                x=future_df['date'].tolist() + future_df['date'].iloc[::-1].tolist(),
                                y=upper_bound.tolist() + lower_bound.iloc[::-1].tolist(),
                                fill='toself',
                                fillcolor='rgba(255,0,0,0.2)',
                                line=dict(color='rgba(255,0,0,0)'),
                                name='Intervalo de Confiança'
                            )
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Exibir tabela de previsões
                    st.subheader("Valores Previstos")
                    st.dataframe(future_preds)
                    
                    # Análise de tendência
                    trend = "ascendente" if future_preds['value'].iloc[-1] > future_preds['value'].iloc[0] else "descendente"
                    variation = ((future_preds['value'].iloc[-1] / future_preds['value'].iloc[0]) - 1) * 100
                    
                    st.info(f"Tendência {trend} com variação de {variation:.2f}% no período previsto.")
                else:
                    st.error("Não foi possível carregar os dados históricos para comparação.")
            else:
                st.error("Falha ao gerar previsões. Verifique se o modelo foi treinado corretamente.")
    else:
        st.warning("Por favor, treine o modelo primeiro usando o botão no menu lateral.")

with tab2:
    st.header("Análise do Modelo")
    
    if indicator in predictor.models or model_exists:
        # Tentar carregar o modelo novamente se necessário
        if indicator not in predictor.models and model_exists:
            try:
                predictor.models[indicator] = joblib.load(model_path)
                predictor.scalers[indicator] = joblib.load(scaler_path)
            except Exception as e:
                st.error(f"Erro ao carregar modelo: {e}")
        
        # Importância das features
        importance = predictor.get_feature_importance(indicator)
        
        if importance is not None:
            st.subheader("Importância das Features")
            
            # Para modelos lineares
            if 'coefficient' in importance.columns:
                fig = px.bar(
                    importance.head(15), 
                    x='coefficient', 
                    y='feature',
                    orientation='h',
                    title='Coeficientes do Modelo',
                    labels={'coefficient': 'Coeficiente', 'feature': 'Feature'},
                    color='coefficient',
                    color_continuous_scale='RdBu',
                    range_color=[-abs(importance['coefficient']).max(), abs(importance['coefficient']).max()]
                )
            else:  # Para Random Forest
                fig = px.bar(
                    importance.head(15),
                    x='importance',
                    y='feature',
                    orientation='h',
                    title='Top 15 Features Mais Importantes',
                    labels={'importance': 'Importância', 'feature': 'Feature'}
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Explicação
            st.subheader("Interpretação")
            
            if selected_model == 'random_forest':
                st.markdown("""
                **Como interpretar a importância das features:**
                
                - Valores mais altos indicam que a feature tem maior influência nas previsões.
                - Features com valores históricos (lag) do próprio indicador mostram a importância da tendência recente.
                - Features de outros indicadores revelam relações entre diferentes variáveis econômicas.
                
                Por exemplo, se 'ipca_lag_1' (valor do IPCA no mês anterior) tem alta importância para prever a Selic,
                isso sugere uma forte relação entre inflação e decisões de política monetária.
                """)
            else:
                st.markdown("""
                **Como interpretar os coeficientes:**
                
                - Valores positivos: um aumento na feature leva a um aumento no indicador previsto.
                - Valores negativos: um aumento na feature leva a uma diminuição no indicador previsto.
                - O tamanho do coeficiente indica a magnitude do efeito.
                
                Observe que os coeficientes são calculados sobre dados padronizados (mesma escala),
                então podem ser comparados diretamente entre si.
                """)
            
            # Tabela completa
            st.subheader("Tabela Completa de Importância das Features")
            st.dataframe(importance)
        else:
            st.warning("Não foi possível calcular a importância das features para este modelo.")
            
        # Explicação do modelo
        st.subheader("Sobre o Modelo")
        
        if selected_model == 'linear':
            st.markdown("""
            **Regressão Linear Simples**
            
            Este modelo procura uma relação linear entre as features e o target. Ele é bom para entender relações simples
            e diretas entre variáveis econômicas, mas pode não capturar relações complexas e não-lineares.
            
            É um modelo facilmente interpretável, onde cada coeficiente representa o efeito de uma variável sobre o resultado previsto.
            """)
        elif selected_model in ['ridge', 'lasso']:
            st.markdown("""
            **Regressão Regularizada**
            
            Estes modelos são semelhantes à regressão linear, mas incluem penalidades que ajudam a evitar o overfitting,
            especialmente quando há muitas features correlacionadas, como é comum em dados econômicos.
            
            - Ridge: Reduz os coeficientes, mas raramente os torna zero (bom para variáveis correlacionadas)
            - Lasso: Pode reduzir coeficientes a zero (bom para seleção de features)
            """)
        else:  # Random Forest
            st.markdown("""
            **Random Forest**
            
            Este é um modelo conjunto baseado em árvores de decisão. Ele é capaz de capturar relações não-lineares
            e interações complexas entre variáveis econômicas.
            
            Vantagens:
            - Captura relações não-lineares
            - Robusto a outliers
            - Não requer suposições sobre a distribuição dos dados
            - Geralmente tem boa performance sem muita necessidade de ajustes
            
            Desvantagens:
            - Menos interpretável que modelos lineares
            - Pode ser mais lento para treinar com muitos dados
            """)
    else:
        st.warning("Nenhum modelo treinado disponível. Por favor, treine um modelo primeiro.")

with tab3:
    st.header("Dados Históricos")
    
    # Carregar dados
    data = load_data(indicator)
    
    if data is not None and not data.empty:
        # Estatísticas básicas
        st.subheader(f"Estatísticas de {indicator_names[indicator]}")
        
        # Período dos dados
        min_date = data['date'].min().strftime('%d/%m/%Y')
        max_date = data['date'].max().strftime('%d/%m/%Y')
        
        st.markdown(f"**Período dos dados:** {min_date} a {max_date}")
        st.markdown(f"**Total de registros:** {len(data)}")
        
        # Estatísticas dos últimos 12 meses
        st.subheader("Dados dos Últimos 12 Meses")
        recent_data = data.sort_values('date', ascending=False).head(12).sort_values('date')
        
        # Gráfico recente
        fig = px.line(
            recent_data,
            x='date',
            y='value',
            title=f'Valores Recentes de {indicator_names[indicator]} (Últimos 12 Meses)',
            labels={'date': 'Data', 'value': 'Valor'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de dados recentes
        recent_data['date'] = recent_data['date'].dt.strftime('%d/%m/%Y')
        st.dataframe(recent_data[['date', 'value']])
        
        # Gráfico histórico completo
        st.subheader("Série Histórica Completa")
        fig2 = px.line(
            data,
            x='date',
            y='value',
            title=f'Série Histórica Completa de {indicator_names[indicator]}',
            labels={'date': 'Data', 'value': 'Valor'}
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Decomposição de tendência (simplificado)
        if len(data) >= 24:
            st.subheader("Análise de Tendência")
            
            # Calcular médias móveis
            data['MA_3m'] = data['value'].rolling(window=3).mean()
            data['MA_6m'] = data['value'].rolling(window=6).mean()
            data['MA_12m'] = data['value'].rolling(window=12).mean()
            
            # Gráfico com médias móveis
            fig3 = px.line(
                data,
                x='date',
                y=['value', 'MA_3m', 'MA_6m', 'MA_12m'],
                title='Análise de Tendência com Médias Móveis',
                labels={'date': 'Data', 'value': 'Valor', 'variable': 'Métrica'},
                color_discrete_map={
                    'value': 'blue',
                    'MA_3m': 'green',
                    'MA_6m': 'orange',
                    'MA_12m': 'red'
                }
            )
            fig3.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.error(f"Não há dados disponíveis para {indicator_names[indicator]}.")

# Rodapé
st.markdown("---")
st.caption("Análise de Machine Learning desenvolvida com dados do Banco Central do Brasil")
