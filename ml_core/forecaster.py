# ml_core/forecaster.py
import pandas as pd
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

    last_date = data['date'].max()
    last_value = data.loc[data['date'] == last_date, 'value'].values[0]

    # Trend fixo para a simulação.
    # Em um modelo real, isso viria da análise do modelo.
    trend = 0.05 

    future_dates = pd.date_range(start=last_date, periods=periods + 1, freq='M')[1:]
    future_values = [last_value * (1 + trend * i) for i in range(1, periods + 1)]

    future_df = pd.DataFrame({'date': future_dates, 'value': future_values, 'tipo': 'Previsão'})
    return future_df