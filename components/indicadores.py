from database_manager import DatabaseManager

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

def load_data(table_name, start_date=None, end_date=None):
    db_manager = DatabaseManager()
    return db_manager.load_data(table_name, start_date, end_date)