# ml_core/forecaster.py
import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta

def simulate_forecast(data: pd.DataFrame, periods: int) -> pd.DataFrame:
    """
    Simula uma previsão de dados com base nos últimos valores históricos.
    Esta é uma simulação simples e deve ser substituída por um modelo de ML real.

    Args:
        data (pd.DataFrame): DataFrame histórico com colunas 'date' e 'value'.
        periods (int): Número de meses para prever.

    Returns:
        pd.DataFrame: DataFrame contendo as datas e valores simulados da previsão.
    """

    if data.empty:
        return pd.DataFrame()

    history_df= data[['date', 'value']]
    history_df.rename(columns={'date':'ds', 'value':'y'}, inplace=True)
    
    forecaster = Prophet()

    forecaster.fit(history_df)
    forecasting_period = forecaster.make_future_dataframe(periods=periods, include_history=False, freq='ME')
    forecast_df = forecaster.predict(forecasting_period)

    future_df = pd.DataFrame({'date': forecast_df['ds'], 'value': forecast_df['yhat'], 'tipo': 'Previsão'})

    return future_df