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
    
    # Instanciar e treinar o modelo
    model = Prophet()
    model.fit(history_df)
    
    # Criar datas futuras com frequência mensal
    future_dates = model.make_future_dataframe(periods=periods, include_history=False, freq='MS')  # 'MS' = início do mês
    forecast = model.predict(future_dates)
    
    # Formatar a saída
    future_df = pd.DataFrame({
        'date': forecast['ds'],
        'value': forecast['yhat'],
        'tipo': 'Previsão'
    })

    return future_df
