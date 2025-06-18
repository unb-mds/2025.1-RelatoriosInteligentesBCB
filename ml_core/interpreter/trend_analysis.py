# ml_core/interpreter/trend_analysis.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .config import ANALYSIS_CONFIG, get_indicator_name

class TrendAnalyzer:
    """
    Analisador de tendências para indicadores econômicos
    """
    
    def __init__(self):
        # Configuração segura - usar ANALYSIS_CONFIG diretamente ou valores padrão
        self.config = ANALYSIS_CONFIG if ANALYSIS_CONFIG else {}
        
        # Parâmetros com valores padrão seguros
        self.min_data_points = self._get_config_value('min_data_points', 10)
        self.trend_window = self._get_config_value('trend_window', 30)
        self.volatility_window = self._get_config_value('volatility_window', 20)
        self.significance_level = self._get_config_value('significance_level', 0.05)
        self.outlier_threshold = self._get_config_value('outlier_threshold', 1.5)
        self.correlation_threshold = self._get_config_value('correlation_threshold', 0.7)
    
    def _get_config_value(self, key, default_value):
        """
        Método seguro para obter valores de configuração
        """
        try:
            if self.config and isinstance(self.config, dict):
                return self.config.get(key, default_value)
            else:
                return default_value
        except Exception:
            return default_value
    
    def analyze_trend(self, data, indicator_name, window_days=None):
        """
        Analisa tendência de um indicador específico
        
        Args:
            data: DataFrame com colunas 'date' e 'value'
            indicator_name: Nome do indicador
            window_days: Janela de análise em dias (opcional)
        
        Returns:
            Dicionário com análise de tendência
        """
        if data is None or data.empty:
            return None
        
        try:
            # Usar janela configurada ou padrão
            window = window_days or self.trend_window
            
            # Dados recentes para análise
            recent_data = data.tail(min(window, len(data))).copy()
            
            if len(recent_data) < self.min_data_points:
                return {
                    'indicator': indicator_name,
                    'trend': '📊 Dados Insuficientes',
                    'error': f'Menos de {self.min_data_points} pontos disponíveis'
                }
            
            # Calcular tendência linear
            x = np.arange(len(recent_data))
            y = recent_data['value'].values
            
            # Regressão linear simples
            if len(y) > 1:
                slope = np.polyfit(x, y, 1)[0]
            else:
                slope = 0
            
            # Calcular volatilidade
            volatility = recent_data['value'].std()
            
            # Variação percentual no período
            if len(recent_data) >= 2:
                first_value = recent_data['value'].iloc[0]
                last_value = recent_data['value'].iloc[-1]
                if first_value != 0:
                    pct_change = ((last_value - first_value) / first_value) * 100
                else:
                    pct_change = 0
            else:
                pct_change = 0
            
            # Determinar tendência
            threshold = volatility * 0.1 if volatility > 0 else 0.01
            
            if slope > threshold:
                trend = "📈 Tendência de Alta"
                trend_strength = "Forte" if abs(slope) > threshold * 2 else "Moderada"
            elif slope < -threshold:
                trend = "📉 Tendência de Baixa"
                trend_strength = "Forte" if abs(slope) > threshold * 2 else "Moderada"
            else:
                trend = "📊 Tendência Estável"
                trend_strength = "Estável"
            
            # Calcular estatísticas adicionais
            stats = self._calculate_additional_stats(recent_data)
            
            return {
                'indicator': indicator_name,
                'trend': trend,
                'trend_strength': trend_strength,
                'slope': slope,
                'volatility': volatility,
                'pct_change': pct_change,
                'current_value': recent_data['value'].iloc[-1],
                'period_start': recent_data['date'].iloc[0],
                'period_end': recent_data['date'].iloc[-1],
                'data_points': len(recent_data),
                'stats': stats
            }
            
        except Exception as e:
            return {
                'indicator': indicator_name,
                'trend': '❌ Erro na Análise',
                'error': str(e)
            }
    
    def _calculate_additional_stats(self, data):
        """
        Calcula estatísticas adicionais para a análise
        """
        try:
            values = data['value']
            
            return {
                'mean': values.mean(),
                'median': values.median(),
                'std': values.std(),
                'min': values.min(),
                'max': values.max(),
                'range': values.max() - values.min(),
                'quartile_25': values.quantile(0.25),
                'quartile_75': values.quantile(0.75)
            }
        except Exception:
            return {}
    
    def detect_outliers(self, data, method='iqr'):
        """
        Detecta outliers nos dados
        
        Args:
            data: DataFrame com dados
            method: Método de detecção ('iqr', 'zscore', 'modified_zscore')
        
        Returns:
            DataFrame com outliers marcados
        """
        if data is None or data.empty:
            return None
        
        try:
            data_copy = data.copy()
            values = data_copy['value']
            
            if method == 'iqr':
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - self.outlier_threshold * IQR
                upper_bound = Q3 + self.outlier_threshold * IQR
                
                outliers_mask = (values < lower_bound) | (values > upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs((values - values.mean()) / values.std())
                outliers_mask = z_scores > 3
                
            else:  # modified_zscore
                median = values.median()
                mad = np.median(np.abs(values - median))
                modified_z_scores = 0.6745 * (values - median) / mad
                outliers_mask = np.abs(modified_z_scores) > 3.5
            
            data_copy['is_outlier'] = outliers_mask
            data_copy['outlier_score'] = outliers_mask.astype(int)
            
            return data_copy
            
        except Exception as e:
            print(f"Erro na detecção de outliers: {e}")
            return data
    
    def analyze_seasonality(self, data, indicator_name):
        """
        Analisa sazonalidade nos dados
        
        Args:
            data: DataFrame com dados temporais
            indicator_name: Nome do indicador
        
        Returns:
            Dicionário com análise de sazonalidade
        """
        if data is None or data.empty:
            return None
        
        try:
            # Verificar se há dados suficientes para análise sazonal
            if len(data) < 24:  # Menos de 2 anos de dados mensais
                return {
                    'indicator': indicator_name,
                    'seasonality': 'Dados insuficientes para análise sazonal',
                    'seasonal_strength': 0
                }
            
            data_copy = data.copy()
            data_copy['month'] = data_copy['date'].dt.month
            data_copy['year'] = data_copy['date'].dt.year
            
            # Análise por mês
            monthly_stats = data_copy.groupby('month')['value'].agg(['mean', 'std']).reset_index()
            
            # Calcular força da sazonalidade
            overall_mean = data_copy['value'].mean()
            monthly_variance = monthly_stats['mean'].var()
            seasonal_strength = monthly_variance / data_copy['value'].var() if data_copy['value'].var() > 0 else 0
            
            # Identificar padrões sazonais
            if seasonal_strength > 0.1:
                peak_month = monthly_stats.loc[monthly_stats['mean'].idxmax(), 'month']
                trough_month = monthly_stats.loc[monthly_stats['mean'].idxmin(), 'month']
                
                seasonality_description = f"Sazonalidade detectada (pico: mês {peak_month}, vale: mês {trough_month})"
            else:
                seasonality_description = "Sazonalidade fraca ou inexistente"
            
            return {
                'indicator': indicator_name,
                'seasonality': seasonality_description,
                'seasonal_strength': seasonal_strength,
                'monthly_stats': monthly_stats.to_dict('records'),
                'peak_month': peak_month if seasonal_strength > 0.1 else None,
                'trough_month': trough_month if seasonal_strength > 0.1 else None
            }
            
        except Exception as e:
            return {
                'indicator': indicator_name,
                'seasonality': f'Erro na análise: {e}',
                'seasonal_strength': 0
            }
    
    def compare_indicators(self, data_dict, correlation_threshold=None):
        """
        Compara múltiplos indicadores e analisa correlações
        
        Args:
            data_dict: Dicionário {indicator_name: dataframe}
            correlation_threshold: Limite para correlação significativa
        
        Returns:
            Dicionário com análise comparativa
        """
        threshold = correlation_threshold or self.correlation_threshold
        
        if not data_dict or len(data_dict) < 2:
            return None
        
        try:
            # Preparar dados para correlação
            correlation_data = {}
            
            for indicator, data in data_dict.items():
                if data is not None and not data.empty:
                    # Usar dados dos últimos 12 meses
                    recent_data = data.tail(12)
                    correlation_data[indicator] = recent_data['value'].values[:len(recent_data)]
            
            if len(correlation_data) < 2:
                return None
            
            # Calcular matriz de correlação
            df_corr = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in correlation_data.items()]))
            correlation_matrix = df_corr.corr()
            
            # Encontrar correlações significativas
            strong_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if not pd.isna(corr_value) and abs(corr_value) > threshold:
                        strong_correlations.append({
                            'indicator_1': correlation_matrix.columns[i],
                            'indicator_2': correlation_matrix.columns[j],
                            'correlation': corr_value,
                            'strength': 'Forte' if abs(corr_value) > 0.7 else 'Moderada',
                            'direction': 'Positiva' if corr_value > 0 else 'Negativa'
                        })
            
            return {
                'correlation_matrix': correlation_matrix,
                'strong_correlations': strong_correlations,
                'indicators_analyzed': list(data_dict.keys()),
                'correlation_threshold': threshold
            }
            
        except Exception as e:
            return {
                'error': f'Erro na comparação: {e}',
                'indicators_analyzed': list(data_dict.keys())
            }
    
    def get_trend_summary(self, trends_list):
        """
        Gera resumo de múltiplas análises de tendência
        
        Args:
            trends_list: Lista de resultados de analyze_trend
        
        Returns:
            Dicionário com resumo
        """
        if not trends_list:
            return None
        
        try:
            valid_trends = [t for t in trends_list if t and 'error' not in t]
            
            if not valid_trends:
                return {'error': 'Nenhuma tendência válida encontrada'}
            
            # Contar tipos de tendência
            trend_counts = {}
            for trend in valid_trends:
                trend_type = trend.get('trend', 'Desconhecido')
                trend_counts[trend_type] = trend_counts.get(trend_type, 0) + 1
            
            # Calcular estatísticas gerais
            volatilities = [t.get('volatility', 0) for t in valid_trends if 'volatility' in t]
            pct_changes = [t.get('pct_change', 0) for t in valid_trends if 'pct_change' in t]
            
            return {
                'total_indicators': len(trends_list),
                'valid_analyses': len(valid_trends),
                'trend_distribution': trend_counts,
                'avg_volatility': np.mean(volatilities) if volatilities else 0,
                'avg_pct_change': np.mean(pct_changes) if pct_changes else 0,
                'most_common_trend': max(trend_counts, key=trend_counts.get) if trend_counts else None
            }
            
        except Exception as e:
            return {'error': f'Erro no resumo: {e}'}