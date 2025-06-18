# ml_core/interpreter/config.py







# ml_core/interpreter/config.py

# Configurações do banco de dados (compatibilidade com database_manager.py)
DATABASE_NAME = 'economic_data.db'

# Mapeamento de séries do BCB (compatibilidade com database_manager.py)
BCB_INDICATOR_SERIES_MAP = {
    'selic': 432,
    'ipca': 433,
    'igpm': 189,
    'inpc': 188,
    'cambio_dolar': 1,
    'pib': 4385,
    'resultado_primario': 5793,
    'selic_meta': 4189,
    'divida_pib': 4513,
    'transacoes': 2311
}

# Configuração principal do interpretador
INTERPRETER_CONFIG = {
    'enabled': True,
    'debug': False,
    'timeout': 30,
    'max_retries': 3,
    'default_period': '5Y',
    'default_months': 12,
    'max_months': 24,  # ← Adicionar esta linha
    'chart_height': 400,
    'chart_width': 800,
    'auto_refresh': False,
    'cache_duration': 3600,
}

# Configuração de previsões
PREDICTION_CONFIG = {
    'default_periods': 12,
    'default_months': 12,
    'max_months': 24,  # ← Adicionar aqui também
    'confidence_interval': 0.95,
    'seasonality_mode': 'additive',
    'yearly_seasonality': True,
    'weekly_seasonality': False,
    'daily_seasonality': False,
    'holidays': None,
    'uncertainty_samples': 1000,
}

# Configuração de modelos
MODEL_CONFIG = {
    'default_months': 12,
    'max_months': 24,  # ← E aqui
    'prophet': {
        'growth': 'linear',
        'seasonality_mode': 'additive',
        'seasonality_prior_scale': 10.0,
        'holidays_prior_scale': 10.0,
        'changepoint_prior_scale': 0.05,
        'mcmc_samples': 0,
        'interval_width': 0.80,
        'uncertainty_samples': 1000
    },
    'arima': {
        'order': (1, 1, 1),
        'seasonal_order': (1, 1, 1, 12),
        'trend': 'c',
        'method': 'lbfgs',
        'maxiter': 50
    }
}

# Configuração de análise
ANALYSIS_CONFIG = {
    'default_months': 12,
    'max_months': 24,  # ← E aqui
    'trend_window': 30,
    'volatility_window': 20,
    'correlation_threshold': 0.7,
    'significance_level': 0.05,
    'min_data_points': 10,
    'outlier_method': 'iqr',
    'outlier_threshold': 1.5,
}

# Configuração de visualização
VISUALIZATION_CONFIG = {
    'default_months': 12,
    'max_months': 24,  # ← E aqui
    'color_palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
    'background_color': '#ffffff',
    'grid_color': '#f0f0f0',
    'text_color': '#333333',
    'font_family': 'Arial, sans-serif',
    'font_size': 12,
    'figure_width': 800,
    'figure_height': 400,
    'dpi': 100,
    'line_width': 2,
    'marker_size': 6,
    'alpha': 0.7,
    'show_legend': True,
    'legend_position': 'upper right',
}

# CSS customizado para interface Streamlit
CUSTOM_CSS = """
<style>
    .main {
        padding-top: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .forecast-chart {
        border: 1px solid #e6e9ef;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .trend-indicator {
        font-weight: bold;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        display: inline-block;
    }
    .trend-up {
        background-color: #d4edda;
        color: #155724;
    }
    .trend-down {
        background-color: #f8d7da;
        color: #721c24;
    }
    .trend-stable {
        background-color: #fff3cd;
        color: #856404;
    }
</style>
"""

# Mapeamento de nomes dos indicadores
INDICATOR_NAMES = {
    'cambio_dolar': 'Câmbio Dólar (R$/US$)',
    'igpm': 'IGP-M (%)',
    'inpc': 'INPC (%)',
    'resultado_primario': 'Resultado Primário do Governo Central',
    'selic': 'Taxa Selic (%)',
    'ipca': 'IPCA (%)',
    'pib': 'PIB (R$ milhões)',
    'desemprego': 'Taxa de Desemprego (%)',
    'cambio_euro': 'Câmbio Euro (R$/EUR)',
    'ibovespa': 'Ibovespa (pontos)',
    'commodities_index': 'Índice de Commodities',
    'selic_meta': 'Meta da Taxa Selic (%)',
    'divida_pib': 'Dívida Pública/PIB (%)',
    'transacoes': 'Transações Correntes'
}

# Configuração específica por indicador
INDICATOR_CONFIG = {
    'cambio_dolar': {
        'unit': 'R$/US$',
        'decimals': 4,
        'format': 'currency',
        'color': '#1f77b4',
        'description': 'Taxa de câmbio do Real em relação ao Dólar americano'
    },
    'igpm': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#ff7f0e',
        'description': 'Índice Geral de Preços do Mercado'
    },
    'inpc': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#2ca02c',
        'description': 'Índice Nacional de Preços ao Consumidor'
    },
    'resultado_primario': {
        'unit': 'R$ milhões',
        'decimals': 0,
        'format': 'currency_millions',
        'color': '#d62728',
        'description': 'Resultado Primário do Governo Central'
    },
    'selic': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#9467bd',
        'description': 'Taxa básica de juros da economia brasileira'
    },
    'ipca': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#8c564b',
        'description': 'Índice Nacional de Preços ao Consumidor Amplo'
    },
}

def get_indicator_name(indicator_key):
    """Retorna o nome amigável do indicador"""
    return INDICATOR_NAMES.get(indicator_key, indicator_key.replace('_', ' ').title())

def get_available_indicators():
    """Retorna lista de indicadores disponíveis"""
    return list(INDICATOR_NAMES.keys())

def get_indicator_config(indicator_key):
    """Retorna configuração específica do indicador"""
    return INDICATOR_CONFIG.get(indicator_key, {
        'unit': '',
        'decimals': 2,
        'format': 'number',
        'color': '#1f77b4',
        'description': f'Indicador {indicator_key}'
    })

def get_mock_config():
    """Retorna configuração mock para testes"""
    return {
        'mock_mode': True,
        'use_sample_data': True,
        'sample_data_points': 100,
        'mock_forecast_periods': 12,
        'mock_indicators': ['cambio_dolar', 'igpm', 'inpc'],
        'mock_delay': 0.1,
        'random_seed': 42,
        'default_months': 12,
        'max_months': 24,
        'confidence_decay_rate': 0.95,
        'min_confidence': 0.5,  # ← Adicionar aqui também
        'max_confidence': 0.99,
        'confidence_threshold': 0.8,
    }

def format_value(value, indicator_key):
    """Formata um valor de acordo com a configuração do indicador"""
    config = get_indicator_config(indicator_key)
    decimals = config.get('decimals', 2)
    format_type = config.get('format', 'number')
    
    if value is None:
        return 'N/A'
    
    try:
        if format_type == 'percentage':
            return f"{value:.{decimals}f}%"
        elif format_type == 'currency':
            return f"R$ {value:,.{decimals}f}"
        elif format_type == 'currency_millions':
            return f"R$ {value:,.0f} mi"
        else:
            return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)

def get_color_for_indicator(indicator_key):
    """Retorna a cor configurada para um indicador"""
    config = get_indicator_config(indicator_key)
    return config.get('color', '#1f77b4')

def validate_config():
    """Valida se todas as configurações estão corretas"""
    required_configs = [
        'INTERPRETER_CONFIG',
        'PREDICTION_CONFIG', 
        'MODEL_CONFIG',
        'ANALYSIS_CONFIG',
        'VISUALIZATION_CONFIG'
    ]
    
    for config_name in required_configs:
        if config_name not in globals():
            raise ValueError(f"Configuração {config_name} não encontrada")
    
    # Lista COMPLETA de parâmetros que podem ser procurados
    default_values = {
        'default_months': 12,
        'max_months': 24,
        'confidence_decay_rate': 0.95,
        'min_confidence': 0.5,  # ← Novo parâmetro
        'max_confidence': 0.99,
        'confidence_threshold': 0.8,
        'min_data_points': 10,
        'max_data_points': 1000,
        'default_periods': 12,
        'max_periods': 24,
        'min_periods': 3,
        'trend_threshold': 0.1,
        'volatility_threshold': 0.2,
        'correlation_threshold': 0.7,
        'outlier_threshold': 1.5,
        'seasonality_threshold': 0.1,
        'forecast_horizon': 12,
        'validation_split': 0.2,
        'test_split': 0.1,
        'learning_rate': 0.01,
        'batch_size': 32,
        'epochs': 100,
        'patience': 10,
        'early_stopping': True,
        'cross_validation': True,
        'cv_folds': 5,
        'random_state': 42,
        'n_jobs': -1,
        'verbose': False
    }
    
    # Aplicar valores padrão em todas as configurações
    configs_to_validate = [
        INTERPRETER_CONFIG,
        PREDICTION_CONFIG,
        MODEL_CONFIG,
        ANALYSIS_CONFIG,
        VISUALIZATION_CONFIG
    ]
    
    for config in configs_to_validate:
        for param, default_value in default_values.items():
            if param not in config:
                config[param] = default_value
    
    # Também adicionar nos sub-configs do MODEL_CONFIG
    for model_name in ['prophet', 'arima']:
        if model_name in MODEL_CONFIG:
            for param, default_value in default_values.items():
                if param not in MODEL_CONFIG[model_name]:
                    MODEL_CONFIG[model_name][param] = default_value
    
    return True

# Executar validação e capturar erros
try:
    validate_config()
    print("✅ Configuração validada com sucesso")
except Exception as e:
    print(f"⚠️ Erro na validação do config: {e}")

# Função de fallback para qualquer parâmetro não encontrado
def get_config_value(config_dict, key, default=None):
    """
    Função segura para obter valores de configuração
    """
    if isinstance(config_dict, dict):
        return config_dict.get(key, default)
    return default

# Aplicar patch para tornar todas as configs mais robustas
class SafeConfig(dict):
    """Dicionário que retorna valores padrão para chaves não encontradas"""
    
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        # Valores padrão para parâmetros comuns
        defaults = {
            'default_months': 12,
            'max_months': 24,
            'min_months': 1,
            'confidence_decay_rate': 0.95,
            'min_confidence': 0.5,
            'max_confidence': 0.99,
            'confidence_threshold': 0.8,
            'min_data_points': 10,
            'trend_threshold': 0.1,
            'volatility_threshold': 0.2,
            'correlation_threshold': 0.7,
            'outlier_threshold': 1.5,
            'default_periods': 12,
            'forecast_horizon': 12,
            'random_state': 42,
            'verbose': False
        }
        return defaults.get(key, None)
    
    def get(self, key, default=None):
        try:
            return self[key]
        except:
            return default

# Converter configs existentes para SafeConfig
INTERPRETER_CONFIG = SafeConfig(INTERPRETER_CONFIG)
PREDICTION_CONFIG = SafeConfig(PREDICTION_CONFIG)
MODEL_CONFIG = SafeConfig(MODEL_CONFIG)
ANALYSIS_CONFIG = SafeConfig(ANALYSIS_CONFIG)
VISUALIZATION_CONFIG = SafeConfig(VISUALIZATION_CONFIG)

# Configuração principal do interpretador
INTERPRETER_CONFIG = {
    'enabled': True,
    'debug': False,
    'timeout': 30,
    'max_retries': 3,
    'default_period': '5Y',
    'default_months': 12,
    'max_months': 24,  # ← Adicionar esta linha
    'chart_height': 400,
    'chart_width': 800,
    'auto_refresh': False,
    'cache_duration': 3600,
}

# Configuração de previsões
PREDICTION_CONFIG = {
    'default_periods': 12,
    'default_months': 12,
    'max_months': 24,  # ← Adicionar aqui também
    'confidence_interval': 0.95,
    'seasonality_mode': 'additive',
    'yearly_seasonality': True,
    'weekly_seasonality': False,
    'daily_seasonality': False,
    'holidays': None,
    'uncertainty_samples': 1000,
}

# Configuração de modelos
MODEL_CONFIG = {
    'default_months': 12,
    'max_months': 24,  # ← E aqui
    'prophet': {
        'growth': 'linear',
        'seasonality_mode': 'additive',
        'seasonality_prior_scale': 10.0,
        'holidays_prior_scale': 10.0,
        'changepoint_prior_scale': 0.05,
        'mcmc_samples': 0,
        'interval_width': 0.80,
        'uncertainty_samples': 1000
    },
    'arima': {
        'order': (1, 1, 1),
        'seasonal_order': (1, 1, 1, 12),
        'trend': 'c',
        'method': 'lbfgs',
        'maxiter': 50
    }
}

# Configuração de análise
ANALYSIS_CONFIG = {
    'default_months': 12,
    'max_months': 24,  # ← E aqui
    'trend_window': 30,
    'volatility_window': 20,
    'correlation_threshold': 0.7,
    'significance_level': 0.05,
    'min_data_points': 10,
    'outlier_method': 'iqr',
    'outlier_threshold': 1.5,
}

# Configuração de visualização
VISUALIZATION_CONFIG = {
    'default_months': 12,
    'max_months': 24,  # ← E aqui
    'color_palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
    'background_color': '#ffffff',
    'grid_color': '#f0f0f0',
    'text_color': '#333333',
    'font_family': 'Arial, sans-serif',
    'font_size': 12,
    'figure_width': 800,
    'figure_height': 400,
    'dpi': 100,
    'line_width': 2,
    'marker_size': 6,
    'alpha': 0.7,
    'show_legend': True,
    'legend_position': 'upper right',
}

# CSS customizado para interface Streamlit
CUSTOM_CSS = """
<style>
    .main {
        padding-top: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .forecast-chart {
        border: 1px solid #e6e9ef;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .trend-indicator {
        font-weight: bold;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        display: inline-block;
    }
    .trend-up {
        background-color: #d4edda;
        color: #155724;
    }
    .trend-down {
        background-color: #f8d7da;
        color: #721c24;
    }
    .trend-stable {
        background-color: #fff3cd;
        color: #856404;
    }
</style>
"""

# Mapeamento de nomes dos indicadores
INDICATOR_NAMES = {
    'cambio_dolar': 'Câmbio Dólar (R$/US$)',
    'igpm': 'IGP-M (%)',
    'inpc': 'INPC (%)',
    'resultado_primario': 'Resultado Primário do Governo Central',
    'selic': 'Taxa Selic (%)',
    'ipca': 'IPCA (%)',
    'pib': 'PIB (R$ milhões)',
    'desemprego': 'Taxa de Desemprego (%)',
    'cambio_euro': 'Câmbio Euro (R$/EUR)',
    'ibovespa': 'Ibovespa (pontos)',
    'commodities_index': 'Índice de Commodities',
    'selic_meta': 'Meta da Taxa Selic (%)',
    'divida_pib': 'Dívida Pública/PIB (%)',
    'transacoes': 'Transações Correntes'
}

# Configuração específica por indicador
INDICATOR_CONFIG = {
    'cambio_dolar': {
        'unit': 'R$/US$',
        'decimals': 4,
        'format': 'currency',
        'color': '#1f77b4',
        'description': 'Taxa de câmbio do Real em relação ao Dólar americano'
    },
    'igpm': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#ff7f0e',
        'description': 'Índice Geral de Preços do Mercado'
    },
    'inpc': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#2ca02c',
        'description': 'Índice Nacional de Preços ao Consumidor'
    },
    'resultado_primario': {
        'unit': 'R$ milhões',
        'decimals': 0,
        'format': 'currency_millions',
        'color': '#d62728',
        'description': 'Resultado Primário do Governo Central'
    },
    'selic': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#9467bd',
        'description': 'Taxa básica de juros da economia brasileira'
    },
    'ipca': {
        'unit': '%',
        'decimals': 2,
        'format': 'percentage',
        'color': '#8c564b',
        'description': 'Índice Nacional de Preços ao Consumidor Amplo'
    },
}

def get_indicator_name(indicator_key):
    """Retorna o nome amigável do indicador"""
    return INDICATOR_NAMES.get(indicator_key, indicator_key.replace('_', ' ').title())

def get_available_indicators():
    """Retorna lista de indicadores disponíveis"""
    return list(INDICATOR_NAMES.keys())

def get_indicator_config(indicator_key):
    """Retorna configuração específica do indicador"""
    return INDICATOR_CONFIG.get(indicator_key, {
        'unit': '',
        'decimals': 2,
        'format': 'number',
        'color': '#1f77b4',
        'description': f'Indicador {indicator_key}'
    })

def get_mock_config():
    """Retorna configuração mock para testes"""
    return {
        'mock_mode': True,
        'use_sample_data': True,
        'sample_data_points': 100,
        'mock_forecast_periods': 12,
        'mock_indicators': ['cambio_dolar', 'igpm', 'inpc'],
        'mock_delay': 0.1,
        'random_seed': 42,
        'default_months': 12,
        'max_months': 24,
        'confidence_decay_rate': 0.95,
        'min_confidence': 0.5,  # ← Adicionar aqui também
        'max_confidence': 0.99,
        'confidence_threshold': 0.8,
    }

def format_value(value, indicator_key):
    """Formata um valor de acordo com a configuração do indicador"""
    config = get_indicator_config(indicator_key)
    decimals = config.get('decimals', 2)
    format_type = config.get('format', 'number')
    
    if value is None:
        return 'N/A'
    
    try:
        if format_type == 'percentage':
            return f"{value:.{decimals}f}%"
        elif format_type == 'currency':
            return f"R$ {value:,.{decimals}f}"
        elif format_type == 'currency_millions':
            return f"R$ {value:,.0f} mi"
        else:
            return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)

def get_color_for_indicator(indicator_key):
    """Retorna a cor configurada para um indicador"""
    config = get_indicator_config(indicator_key)
    return config.get('color', '#1f77b4')

def validate_config():
    """Valida se todas as configurações estão corretas"""
    required_configs = [
        'INTERPRETER_CONFIG',
        'PREDICTION_CONFIG', 
        'MODEL_CONFIG',
        'ANALYSIS_CONFIG',
        'VISUALIZATION_CONFIG'
    ]
    
    for config_name in required_configs:
        if config_name not in globals():
            raise ValueError(f"Configuração {config_name} não encontrada")
    
    # Lista COMPLETA de parâmetros que podem ser procurados
    default_values = {
        'default_months': 12,
        'max_months': 24,
        'confidence_decay_rate': 0.95,
        'min_confidence': 0.5,  # ← Novo parâmetro
        'max_confidence': 0.99,
        'confidence_threshold': 0.8,
        'min_data_points': 10,
        'max_data_points': 1000,
        'default_periods': 12,
        'max_periods': 24,
        'min_periods': 3,
        'trend_threshold': 0.1,
        'volatility_threshold': 0.2,
        'correlation_threshold': 0.7,
        'outlier_threshold': 1.5,
        'seasonality_threshold': 0.1,
        'forecast_horizon': 12,
        'validation_split': 0.2,
        'test_split': 0.1,
        'learning_rate': 0.01,
        'batch_size': 32,
        'epochs': 100,
        'patience': 10,
        'early_stopping': True,
        'cross_validation': True,
        'cv_folds': 5,
        'random_state': 42,
        'n_jobs': -1,
        'verbose': False
    }
    
    # Aplicar valores padrão em todas as configurações
    configs_to_validate = [
        INTERPRETER_CONFIG,
        PREDICTION_CONFIG,
        MODEL_CONFIG,
        ANALYSIS_CONFIG,
        VISUALIZATION_CONFIG
    ]
    
    for config in configs_to_validate:
        for param, default_value in default_values.items():
            if param not in config:
                config[param] = default_value
    
    # Também adicionar nos sub-configs do MODEL_CONFIG
    for model_name in ['prophet', 'arima']:
        if model_name in MODEL_CONFIG:
            for param, default_value in default_values.items():
                if param not in MODEL_CONFIG[model_name]:
                    MODEL_CONFIG[model_name][param] = default_value
    
    return True

# Executar validação e capturar erros
try:
    validate_config()
    print("✅ Configuração validada com sucesso")
except Exception as e:
    print(f"⚠️ Erro na validação do config: {e}")

# Função de fallback para qualquer parâmetro não encontrado
def get_config_value(config_dict, key, default=None):
    """
    Função segura para obter valores de configuração
    """
    if isinstance(config_dict, dict):
        return config_dict.get(key, default)
    return default

# Aplicar patch para tornar todas as configs mais robustas
class SafeConfig(dict):
    """Dicionário que retorna valores padrão para chaves não encontradas"""
    
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        # Valores padrão para parâmetros comuns
        defaults = {
            'default_months': 12,
            'max_months': 24,
            'min_months': 1,
            'confidence_decay_rate': 0.95,
            'min_confidence': 0.5,
            'max_confidence': 0.99,
            'confidence_threshold': 0.8,
            'min_data_points': 10,
            'trend_threshold': 0.1,
            'volatility_threshold': 0.2,
            'correlation_threshold': 0.7,
            'outlier_threshold': 1.5,
            'default_periods': 12,
            'forecast_horizon': 12,
            'random_state': 42,
            'verbose': False
        }
        return defaults.get(key, None)
    
    def get(self, key, default=None):
        try:
            return self[key]
        except:
            return default

# Converter configs existentes para SafeConfig
INTERPRETER_CONFIG = SafeConfig(INTERPRETER_CONFIG)
PREDICTION_CONFIG = SafeConfig(PREDICTION_CONFIG)
MODEL_CONFIG = SafeConfig(MODEL_CONFIG)
ANALYSIS_CONFIG = SafeConfig(ANALYSIS_CONFIG)
VISUALIZATION_CONFIG = SafeConfig(VISUALIZATION_CONFIG)






