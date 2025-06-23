import pandas as pd
from prophet import Prophet


def simulate_forecast(data: pd.DataFrame, periods: int) -> pd.DataFrame:
    """
    Gera uma previsão de valores futuros com base em dados históricos usando o Prophet.
    
    Args:
        data (pd.DataFrame): DataFrame histórico com colunas 'date' e 'value'.
        periods (int): Número de meses para prever (de 3 a 36).

    Returns:
        pd.DataFrame: DataFrame contendo as datas e valores previstos.
    """
    if data.empty or periods < 3 or periods > 36:
        return pd.DataFrame()

    # Preparar os dados
    history_df = data[['date', 'value']].rename(columns={'date': 'ds', 'value': 'y'})
    
    forecaster = Prophet()

    forecaster.fit(history_df)
    forecasting_period = forecaster.make_future_dataframe(periods=periods, include_history=False, freq='ME')
    forecast_df = forecaster.predict(forecasting_period)

    future_df = pd.DataFrame({'date': forecast_df['ds'], 'value': forecast_df['yhat'], 'tipo': 'Previsão'})

    return future_df

def calcular_estatisticas(df, nome):
    """
    Calcula estatísticas descritivas básicas para uma série temporal.

    Args:
        df (pd.DataFrame): DataFrame contendo uma coluna 'value' com os dados numéricos.
        nome (str): Nome para identificar a série de estatísticas (usado como nome da Series retornada).

    Returns:
        pd.Series: Série contendo média, mediana, desvio padrão, mínimo e máximo dos valores.
    """
    return pd.Series({
        'Média': df['value'].mean(),
        'Mediana': df['value'].median(),
        'Desvio Padrão': df['value'].std(),
        'Mínimo': df['value'].min(),
        'Máximo': df['value'].max()
    }, name=nome)

