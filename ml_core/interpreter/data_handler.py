"""
ML Core Interpreter - Data Handler
Módulo responsável pela gestão, validação e preparação de dados

Author: Assistant
Version: 1.1.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

from .config import get_mock_config, get_available_indicators, INDICATOR_NAMES

class DataHandler:
    """
    Classe responsável pela gestão de dados do interpreter
    """
    
    def __init__(self):
        self.indicator_names = INDICATOR_NAMES
        
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Valida se os dados estão no formato correto
        
        Args:
            data: DataFrame com dados para validar
            
        Returns:
            bool: True se dados válidos, False caso contrário
        """
        if data is None or data.empty:
            return False
        
        # Verificar colunas obrigatórias
        required_columns = ['date', 'value']
        if not all(col in data.columns for col in required_columns):
            return False
        
        # Verificar se há dados suficientes
        if len(data) < 2:
            return False
        
        # Verificar tipos de dados
        try:
            pd.to_datetime(data['date'])
            pd.to_numeric(data['value'])
        except:
            return False
        
        return True
    
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa e prepara os dados para análise
        
        Args:
            data: DataFrame com dados brutos
            
        Returns:
            pd.DataFrame: Dados limpos e preparados
        """
        if not self.validate_data(data):
            raise ValueError("Dados inválidos fornecidos para limpeza")
        
        # Criar cópia para não modificar original
        clean_data = data.copy()
        
        # Converter tipos
        clean_data['date'] = pd.to_datetime(clean_data['date'])
        clean_data['value'] = pd.to_numeric(clean_data['value'], errors='coerce')
        
        # Remover duplicatas por data
        clean_data = clean_data.drop_duplicates(subset=['date'], keep='last')
        
        # Ordenar por data
        clean_data = clean_data.sort_values('date').reset_index(drop=True)
        
        # Remover valores nulos na coluna value
        clean_data = clean_data.dropna(subset=['value'])
        
        # Remover valores infinitos
        clean_data = clean_data[~np.isinf(clean_data['value'])]
        
        # Filtrar valores extremamente outliers (mais de 10 desvios padrão)
        if len(clean_data) > 5:
            mean_val = clean_data['value'].mean()
            std_val = clean_data['value'].std()
            if std_val > 0:
                outlier_mask = np.abs(clean_data['value'] - mean_val) < 10 * std_val
                clean_data = clean_data[outlier_mask]
        
        return clean_data
    
    def generate_realistic_mock_data(self, indicator: str, months: int = 48) -> pd.DataFrame:
        """
        Gera dados mock realistas para um indicador específico
        
        Args:
            indicator: Nome do indicador
            months: Número de meses de dados para gerar
            
        Returns:
            pd.DataFrame: Dados mock realistas
        """
        np.random.seed(42)  # Para reprodutibilidade
        
        # Data final é hoje
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        dates = pd.date_range(start=start_date, end=end_date, freq='M')
        
        # Obter configuração mock para o indicador
        mock_config = get_mock_config(indicator)
        base = mock_config['base']
        trend_factor = mock_config['trend_factor']
        noise_factor = mock_config['noise_factor']
        min_value = mock_config['min_value']
        max_value = mock_config['max_value']
        
        # Padrões específicos por indicador
        if indicator == 'ipca':
            # IPCA: Simular ciclos inflacionários realistas
            # Período normal → inflação alta → normalização
            trend = np.concatenate([
                np.linspace(0, 2, len(dates)//3),
                np.linspace(2, 6, len(dates)//3),
                np.linspace(6, 1, len(dates) - 2*len(dates)//3)
            ])
            seasonal = np.sin(np.linspace(0, 4*np.pi, len(dates))) * 0.8
            noise = np.random.normal(0, noise_factor, len(dates))
            values = base + trend + seasonal + noise
            
        elif indicator == 'selic':
            # SELIC: Ciclo de política monetária
            # Juros baixos → alta → estabilização
            trend = np.concatenate([
                np.linspace(-11, -8, len(dates)//3),
                np.linspace(-8, 0, len(dates)//3),
                np.linspace(0, -1, len(dates) - 2*len(dates)//3)
            ])
            noise = np.random.normal(0, noise_factor, len(dates))
            values = base + trend + noise
            
        elif indicator == 'pib':
            # PIB: Ciclo econômico com recessão e recuperação
            trend = np.concatenate([
                np.linspace(0, -3, len(dates)//4),      # Recessão
                np.linspace(-3, -1, len(dates)//4),     # Fundo
                np.linspace(-1, 2, len(dates)//4),      # Recuperação
                np.linspace(2, 1, len(dates) - 3*len(dates)//4)
            ])
            seasonal = np.sin(np.linspace(0, 3*np.pi, len(dates))) * 0.5
            noise = np.random.normal(0, noise_factor, len(dates))
            values = base + trend + seasonal + noise
            
        elif indicator == 'cambio_dolar':
            # Câmbio: Volatilidade com choques pontuais
            trend = np.cumsum(np.random.normal(0, 0.08, len(dates)))
            # Adicionar choques pontuais
            shocks = np.zeros(len(dates))
            shock_indices = np.random.choice(len(dates), size=3, replace=False)
            shocks[shock_indices] = np.random.normal(0, 0.5, 3)
            noise = np.random.normal(0, noise_factor, len(dates))
            values = base + trend + shocks + noise
            
        elif indicator == 'divida_pib':
            # Dívida/PIB: Tendência crescente com estabilização
            trend = np.linspace(0, 10, len(dates))
            noise = np.random.normal(0, noise_factor * 2, len(dates))
            values = base + trend + noise
            
        else:
            # Padrão genérico para outros indicadores
            trend = np.cumsum(np.random.normal(0, trend_factor/10, len(dates)))
            seasonal = np.sin(np.linspace(0, 2*np.pi, len(dates))) * trend_factor/4
            noise = np.random.normal(0, noise_factor, len(dates))
            values = base + trend + seasonal + noise
        
        # Aplicar limites
        values = np.clip(values, min_value, max_value)
        values = np.round(values, 3)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    def generate_mock_data_dict(self, months: int = 48) -> Dict[str, pd.DataFrame]:
        """
        Gera dicionário completo de dados mock para todos os indicadores
        
        Args:
            months: Número de meses de dados para gerar
            
        Returns:
            Dict[str, pd.DataFrame]: Dicionário com dados mock
        """
        mock_data = {}
        available_indicators = get_available_indicators()
        
        for indicator in available_indicators:
            try:
                mock_data[indicator] = self.generate_realistic_mock_data(indicator, months)
            except Exception as e:
                # Fallback para dados genéricos
                mock_data[indicator] = self._generate_generic_mock_data(indicator, months)
        
        return mock_data
    
    def _generate_generic_mock_data(self, indicator: str, months: int) -> pd.DataFrame:
        """
        Gera dados mock genéricos como fallback
        
        Args:
            indicator: Nome do indicador
            months: Número de meses
            
        Returns:
            pd.DataFrame: Dados mock genéricos
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        dates = pd.date_range(start=start_date, end=end_date, freq='M')
        
        # Valores genéricos
        base = 100
        trend = np.cumsum(np.random.normal(0, 0.5, len(dates)))
        noise = np.random.normal(0, 2, len(dates))
        values = base + trend + noise
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    def detect_outliers(self, data: pd.DataFrame, factor: float = 1.5) -> List[Dict]:
        """
        Detecta outliers usando método IQR
        
        Args:
            data: DataFrame com dados
            factor: Fator multiplicativo para IQR
            
        Returns:
            List[Dict]: Lista de outliers detectados
        """
        if data.empty or len(data) < 4:
            return []
        
        values = data['value'].dropna()
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)
        IQR = Q3 - Q1
        
        # Se IQR muito pequeno, usar método baseado em desvio padrão
        if IQR < 1e-10:
            mean_val = values.mean()
            std_val = values.std()
            lower_bound = mean_val - 2 * std_val
            upper_bound = mean_val + 2 * std_val
        else:
            lower_bound = Q1 - factor * IQR
            upper_bound = Q3 + factor * IQR
        
        outliers = []
        median_value = values.median()
        std_value = values.std()
        
        for idx, row in data.iterrows():
            value = row['value']
            if pd.notna(value) and (value < lower_bound or value > upper_bound):
                outlier_type = 'Alto' if value > upper_bound else 'Baixo'
                deviation = abs(value - median_value) / std_value if std_value > 1e-10 else 0
                
                outliers.append({
                    'date': row['date'],
                    'value': value,
                    'type': outlier_type,
                    'deviation': deviation,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                })
        
        return sorted(outliers, key=lambda x: x['deviation'], reverse=True)
    
    def get_data_quality_score(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calcula score de qualidade dos dados
        
        Args:
            data: DataFrame com dados
            
        Returns:
            Dict[str, float]: Métricas de qualidade
        """
        if data.empty:
            return {
                'completeness': 0.0,
                'consistency': 0.0,
                'validity': 0.0,
                'overall_score': 0.0
            }
        
        # Completude (% de valores não nulos)
        completeness = (1 - data['value'].isnull().sum() / len(data)) * 100
        
        # Consistência (baixa variação relativa)
        if data['value'].std() > 0 and data['value'].mean() != 0:
            cv = data['value'].std() / abs(data['value'].mean())
            consistency = max(0, 100 - cv * 10)  # Penalizar alta variação
        else:
            consistency = 50  # Score neutro para dados constantes
        
        # Validade (% de valores dentro de limites razoáveis)
        Q1 = data['value'].quantile(0.25)
        Q3 = data['value'].quantile(0.75)
        IQR = Q3 - Q1
        
        if IQR > 0:
            lower_limit = Q1 - 3 * IQR
            upper_limit = Q3 + 3 * IQR
            valid_count = ((data['value'] >= lower_limit) & (data['value'] <= upper_limit)).sum()
            validity = (valid_count / len(data)) * 100
        else:
            validity = 100  # Se não há variação, todos são válidos
        
        # Score geral (média ponderada)
        overall_score = (completeness * 0.4 + consistency * 0.3 + validity * 0.3)
        
        return {
            'completeness': round(completeness, 2),
            'consistency': round(consistency, 2),
            'validity': round(validity, 2),
            'overall_score': round(overall_score, 2)
        }
    
    def prepare_data_for_analysis(self, data: pd.DataFrame, months_filter: Optional[int] = None) -> pd.DataFrame:
        """
        Prepara dados para análise (limpa + filtra período)
        
        Args:
            data: DataFrame com dados brutos
            months_filter: Número de meses para filtrar (None = todos)
            
        Returns:
            pd.DataFrame: Dados preparados para análise
        """
        # Limpar dados
        clean_data = self.clean_data(data)
        
        # Filtrar período se especificado
        if months_filter:
            cutoff_date = datetime.now() - timedelta(days=30 * months_filter)
            filtered_data = clean_data[clean_data['date'] >= cutoff_date].copy()
            
            if filtered_data.empty:
                # Se filtro resulta em dados vazios, usar todos os dados
                return clean_data
            else:
                return filtered_data
        
        return clean_data
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, any]:
        """
        Retorna resumo estatístico dos dados
        
        Args:
            data: DataFrame com dados
            
        Returns:
            Dict: Resumo estatístico
        """
        if data.empty:
            return {
                'count': 0,
                'period': 'N/A',
                'mean': 0,
                'std': 0,
                'min': 0,
                'max': 0,
                'quality_score': 0
            }
        
        quality = self.get_data_quality_score(data)
        
        return {
            'count': len(data),
            'period': f"{data['date'].min().strftime('%m/%Y')} - {data['date'].max().strftime('%m/%Y')}",
            'mean': round(data['value'].mean(), 3),
            'std': round(data['value'].std(), 3),
            'min': round(data['value'].min(), 3),
            'max': round(data['value'].max(), 3),
            'quality_score': quality['overall_score']
        }
    
    def export_data_to_dict(self, data: pd.DataFrame) -> Dict[str, any]:
        """
        Exporta dados para dicionário (útil para APIs)
        
        Args:
            data: DataFrame com dados
            
        Returns:
            Dict: Dados em formato dicionário
        """
        if data.empty:
            return {
                'dates': [],
                'values': [],
                'metadata': self.get_data_summary(data)
            }
        
        return {
            'dates': data['date'].dt.strftime('%Y-%m-%d').tolist(),
            'values': data['value'].round(3).tolist(),
            'metadata': self.get_data_summary(data)
        }
    
    def merge_indicator_data(self, data_dict: Dict[str, pd.DataFrame], 
                           indicators: List[str]) -> pd.DataFrame:
        """
        Combina dados de múltiplos indicadores em um DataFrame
        
        Args:
            data_dict: Dicionário com dados dos indicadores
            indicators: Lista de indicadores para combinar
            
        Returns:
            pd.DataFrame: Dados combinados
        """
        if not indicators or not data_dict:
            return pd.DataFrame()
        
        # Filtrar apenas indicadores disponíveis
        available_indicators = [ind for ind in indicators if ind in data_dict and not data_dict[ind].empty]
        
        if not available_indicators:
            return pd.DataFrame()
        
        # Começar com o primeiro indicador
        merged_data = data_dict[available_indicators[0]].copy()
        merged_data = merged_data.rename(columns={'value': available_indicators[0]})
        
        # Adicionar outros indicadores
        for indicator in available_indicators[1:]:
            indicator_data = data_dict[indicator].copy()
            indicator_data = indicator_data.rename(columns={'value': indicator})
            
            merged_data = pd.merge(
                merged_data, 
                indicator_data, 
                on='date', 
                how='outer'
            )
        
        # Ordenar por data
        merged_data = merged_data.sort_values('date').reset_index(drop=True)
        
        return merged_data