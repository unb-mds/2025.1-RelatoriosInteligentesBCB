import pandas as pd

from datetime import datetime, timedelta

# Verificar disponibilidade do Prophet
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("⚠️ Prophet não disponível, usando método alternativo")

def simulate_forecast(indicator_or_data, periods: int) -> pd.DataFrame:
    """
    Gera previsão usando Prophet ou dados diretos.
    
    Args:
        indicator_or_data: Nome do indicador (str) ou DataFrame com dados históricos
        periods (int): Número de períodos para prever.

    Returns:
        pd.DataFrame: DataFrame contendo as datas e valores da previsão.
    """
    
    # Se recebeu string (nome do indicador), carregar dados
    if isinstance(indicator_or_data, str):
        from database_manager import DatabaseManager
        db = DatabaseManager()
        data = db.load_data(indicator_or_data)
        if data is None or data.empty:
            print(f"❌ Nenhum dado disponível para {indicator_or_data}")
            return pd.DataFrame()
    else:
        # Se recebeu DataFrame diretamente
        data = indicator_or_data
    
    if data.empty:
        print("❌ DataFrame vazio fornecido")
        return pd.DataFrame()

    if PROPHET_AVAILABLE:
        try:
            # Preparar dados para Prophet
            history_df = data[['date', 'value']].copy()
            history_df.rename(columns={'date': 'ds', 'value': 'y'}, inplace=True)
            
            # Remover valores nulos
            history_df = history_df.dropna()
            
            if len(history_df) < 10:
                print(f"❌ Dados insuficientes ({len(history_df)} pontos)")
                return create_simple_forecast(data, periods)
            
            print(f"📈 Gerando previsão Prophet ({len(history_df)} pontos, {periods} períodos)")
            
            # Criar e treinar modelo Prophet
            forecaster = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False
            )
            forecaster.fit(history_df)
            
            # Criar período futuro
            forecasting_period = forecaster.make_future_dataframe(
                periods=periods, 
                include_history=False, 
                freq='ME'  # Monthly End
            )
            
            # Fazer previsão
            forecast_df = forecaster.predict(forecasting_period)
            
            # Formatar resultado
            future_df = pd.DataFrame({
                'date': forecast_df['ds'], 
                'value': forecast_df['yhat'], 
                'lower_bound': forecast_df['yhat_lower'],
                'upper_bound': forecast_df['yhat_upper'],
                'tipo': 'Previsão'
            })
            
            print(f"✅ Previsão Prophet concluída: {len(future_df)} períodos")
            return future_df
            
        except Exception as e:
            print(f"❌ Erro no Prophet: {e}")
            print("🔄 Usando método alternativo...")
            return create_simple_forecast(data, periods)
    else:
        # Usar método alternativo se Prophet não disponível
        return create_simple_forecast(data, periods)

def create_simple_forecast(data: pd.DataFrame, periods: int) -> pd.DataFrame:
    """
    Método alternativo simples de previsão usando tendência linear.
    
    Args:
        data: DataFrame com colunas 'date' e 'value'
        periods: Número de períodos para prever
        
    Returns:
        DataFrame com previsões
    """
    import numpy as np
    
    if data is None or data.empty or len(data) < 2:
        print("❌ Dados insuficientes para previsão simples")
        return pd.DataFrame()
    
    try:
        # Usar últimos 30 pontos ou todos se menos de 30
        recent_data = data.tail(min(30, len(data))).copy()
        
        # Calcular tendência simples
        x = np.arange(len(recent_data))
        y = recent_data['value'].values
        
        # Regressão linear simples
        coeffs = np.polyfit(x, y, 1)
        slope, intercept = coeffs[0], coeffs[1]
        
        last_value = recent_data['value'].iloc[-1]
        last_date = recent_data['date'].iloc[-1]
        
        # Gerar datas futuras (assumindo frequência mensal)
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=periods,
            freq='M'
        )
        
        # Gerar previsões com tendência
        predictions = []
        for i in range(periods):
            predicted_value = last_value + slope * (i + 1)
            predictions.append(predicted_value)
        
        # Criar DataFrame resultado
        result = pd.DataFrame({
            'date': future_dates,
            'value': predictions,
            'lower_bound': [p * 0.95 for p in predictions],
            'upper_bound': [p * 1.05 for p in predictions],
            'tipo': 'Previsão Simples'
        })
        
        print(f"✅ Previsão simples concluída: {periods} períodos")
        return result
        
    except Exception as e:
        print(f"❌ Erro na previsão simples: {e}")
        return pd.DataFrame()
