
# Configurações da API do Banco Central do Brasil
BCB_API_BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"

# Mapeamento de indicadores do BCB e suas séries
BCB_INDICATOR_SERIES_MAP = {
    'ipca': 433,           # Inflação: IPCA
    'pib': 4380,           # Atividade Econômica: PIB Real
    'divida_pib': 13761,   # Dívida Pública: Relação Dívida/PIB
    'selic': 11,           # Taxa SELIC diária
    'selic_meta': 4189,    # Meta da taxa SELIC
    'transacoes': 22707,   # Balanço de Pagamentos: Saldo em Transações Correntes
    'cambio_dolar': 1,     # Taxa de Câmbio - Dólar (Diário)
    'igpm': 189,           # Índice geral de preços do mercado (IGP-M)
    'inpc': 188,           # Índice nacional de preços ao consumidor (INPC)
    'resultado_primario': 7547 # Indicadores Fiscais: Resultado Primário
}

# Configurações do Banco de Dados
DATABASE_NAME = 'economic_data.db'