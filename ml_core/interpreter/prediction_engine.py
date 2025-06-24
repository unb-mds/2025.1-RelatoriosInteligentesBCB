"""
ML Core Interpreter - Prediction Engine
Módulo responsável pelas previsões com machine learning

Author: Assistant
Version: 1.1.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

from .config import PREDICTION_CONFIG, MODEL_CONFIG

class PredictionEngine:
    """
    Classe responsável pelas previsões econômicas
    """
    
    def __init__(self):
        self.config = PREDICTION_CONFIG
        self.model_config = MODEL_CONFIG
        self.default_months = self.config['default_months']
        self.max_months = self.config['max_months']
        self.confidence_decay_rate = self.config['confidence_decay_rate']
        self.min_confidence = self.config['min_confidence']
        
    def predict(self, data: pd.DataFrame, months_ahead: int = None, 
                method: str = 'auto') -> Optional[Dict[str, any]]:
        """
        Executa previsão usando o método especificado
        
        Args:
            data: DataFrame com dados históricos
            months_ahead: Número de meses para prever
            method: Método de previsão ('auto', 'linear', 'exponential', 'moving_average')
            
        Returns:
            Dict: Resultado da previsão ou None se não possível
        """
        # Validar parâmetros
        if months_ahead is None:
            months_ahead = self.default_months
        
        months_ahead = max(1, min(self.max_months, months_ahead))
        
        # Validar dados
        if data.empty or len(data) < 2:
            return self._create_fallback_prediction(data, months_ahead)
        
        # Preparar dados
        clean_data = self._prepare_data(data)
        
        if len(clean_data) < 2:
            return self._create_fallback_prediction(data, months_ahead)
        
        # Escolher método automaticamente se necessário
        if method == 'auto':
            method = self._select_best_method(clean_data)
        
        # Executar previsão baseada no método
        try:
            if method == 'linear':
                result = self._predict_linear_regression(clean_data, months_ahead)
            elif method == 'exponential':
                result = self._predict_exponential_smoothing(clean_data, months_ahead)
            elif method == 'moving_average':
                result = self._predict_moving_average(clean_data, months_ahead)
            else:
                result = self._predict_linear_regression(clean_data, months_ahead)
            
            if result is None:
                return self._create_fallback_prediction(clean_data, months_ahead)
            
            return result
            
        except Exception as e:
            print(f"Erro na previsão: {e}")
            return self._create_fallback_prediction(clean_data, months_ahead)
    
    def _prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara dados para previsão
        
        Args:
            data: DataFrame bruto
            
        Returns:
            pd.DataFrame: Dados limpos e ordenados
        """
        # Criar cópia e ordenar
        clean_data = data.copy().sort_values('date').reset_index(drop=True)
        
        # Remover valores nulos e infinitos
        clean_data = clean_data.dropna(subset=['value'])
        clean_data = clean_data[~np.isinf(clean_data['value'])]
        
        # Filtrar outliers extremos (mais de 5 desvios padrão)
        if len(clean_data) > 5:
            mean_val = clean_data['value'].mean()
            std_val = clean_data['value'].std()
            if std_val > 0:
                outlier_mask = np.abs(clean_data['value'] - mean_val) < 5 * std_val
                clean_data = clean_data[outlier_mask]
        
        return clean_data
    
    def _select_best_method(self, data: pd.DataFrame) -> str:
        """
        Seleciona automaticamente o melhor método baseado nos dados
        
        Args:
            data: DataFrame com dados limpos
            
        Returns:
            str: Método recomendado
        """
        n_points = len(data)
        
        # Analisar características dos dados
        values = data['value'].values
        volatility = np.std(values) / np.mean(values) if np.mean(values) != 0 else 0
        
        # Analisar tendência
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        y_pred = slope * x + np.polyfit(x, values, 1)[1]
        r_squared = 1 - (np.sum((values - y_pred) ** 2) / np.sum((values - np.mean(values)) ** 2))
        
        # Lógica de seleção
        if n_points < 6:
            return 'moving_average'
        elif n_points < 12:
            return 'exponential' if volatility < 0.2 else 'moving_average'
        else:
            if r_squared > 0.6 and volatility < 0.15:
                return 'linear'
            elif volatility < 0.25:
                return 'exponential'
            else:
                return 'moving_average'
    
    def _predict_linear_regression(self, data: pd.DataFrame, months_ahead: int) -> Optional[Dict[str, any]]:
        """
        Previsão usando regressão linear
        
        Args:
            data: DataFrame com dados limpos
            months_ahead: Número de meses para prever
            
        Returns:
            Dict: Resultado da previsão ou None
        """
        config = self.model_config['linear_regression']
        
        if len(data) < config['min_data_points']:
            return None
        
        # Preparar variáveis
        x = np.arange(len(data))
        y = data['value'].values
        
        # Validação cruzada simples
        split_idx = max(1, int(len(x) * config['validation_split']))
        x_train, x_test = x[:split_idx], x[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Treinar modelo
        slope, intercept = np.polyfit(x_train, y_train, 1)
        
        # Avaliar modelo se há dados de teste
        if len(x_test) > 0:
            y_pred_test = slope * x_test + intercept
            rmse = np.sqrt(np.mean((y_test - y_pred_test) ** 2))
        else:
            # Usar dados de treino para estimar erro
            y_pred_train = slope * x_train + intercept
            rmse = np.sqrt(np.mean((y_train - y_pred_train) ** 2))
        
        # Calcular R²
        y_pred_all = slope * x + intercept
        ss_res = np.sum((y - y_pred_all) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 1e-10 else 0
        r_squared = max(0, min(1, r_squared))
        
        # Gerar previsões futuras
        future_x = np.arange(len(x), len(x) + months_ahead)
        future_values = slope * future_x + intercept
        
        # Gerar datas futuras
        future_dates = self._generate_future_dates(data['date'].max(), months_ahead)
        
        # Calcular intervalos de confiança
        confidence_intervals = self._calculate_confidence_intervals(
            future_values, rmse, months_ahead, 'linear'
        )
        
        # Calcular scores de confiança decrescente
        confidence_scores = self._calculate_confidence_scores(months_ahead, r_squared)
        
        return {
            'dates': future_dates,
            'values': future_values.tolist(),
            'confidence_intervals': confidence_intervals,
            'confidence_scores': confidence_scores,
            'method': 'Regressão Linear',
            'rmse': rmse,
            'r_squared': r_squared,
            'model_params': {
                'slope': slope,
                'intercept': intercept,
                'train_size': len(x_train)
            }
        }
    
    def _predict_exponential_smoothing(self, data: pd.DataFrame, months_ahead: int) -> Optional[Dict[str, any]]:
        """
        Previsão usando suavização exponencial (Holt)
        
        Args:
            data: DataFrame com dados limpos
            months_ahead: Número de meses para prever
            
        Returns:
            Dict: Resultado da previsão ou None
        """
        config = self.model_config['exponential_smoothing']
        
        if len(data) < config['min_data_points']:
            return None
        
        values = data['value'].values
        alpha = config['alpha']
        beta = config['beta']
        
        # Inicialização
        level = values[0]
        trend = values[1] - values[0] if len(values) > 1 else 0
        
        # Lista para armazenar previsões históricas (para calcular erro)
        historical_forecasts = []
        
        # Aplicar suavização exponencial dupla
        for i in range(1, len(values)):
            # Previsão para este ponto
            forecast = level + trend
            historical_forecasts.append(forecast)
            
            # Atualizar componentes
            prev_level = level
            level = alpha * values[i] + (1 - alpha) * (level + trend)
            trend = beta * (level - prev_level) + (1 - beta) * trend
        
        # Calcular erro histórico
        if len(historical_forecasts) > 0:
            actual_values = values[1:]  # Valores reais correspondentes
            errors = [abs(actual - forecast) for actual, forecast in zip(actual_values, historical_forecasts)]
            rmse = np.sqrt(np.mean([e**2 for e in errors]))
        else:
            rmse = np.std(values) * 0.1
        
        # Gerar previsões futuras
        future_values = []
        for i in range(1, months_ahead + 1):
            pred_value = level + trend * i
            future_values.append(pred_value)
        
        # Gerar datas futuras
        future_dates = self._generate_future_dates(data['date'].max(), months_ahead)
        
        # Calcular intervalos de confiança
        confidence_intervals = self._calculate_confidence_intervals(
            future_values, rmse, months_ahead, 'exponential'
        )
        
        # Calcular scores de confiança
        base_confidence = 0.8  # Ligeiramente menor que regressão linear
        confidence_scores = self._calculate_confidence_scores(months_ahead, base_confidence)
        
        return {
            'dates': future_dates,
            'values': future_values,
            'confidence_intervals': confidence_intervals,
            'confidence_scores': confidence_scores,
            'method': 'Suavização Exponencial',
            'rmse': rmse,
            'model_params': {
                'alpha': alpha,
                'beta': beta,
                'final_level': level,
                'final_trend': trend
            }
        }
    
    def _predict_moving_average(self, data: pd.DataFrame, months_ahead: int) -> Optional[Dict[str, any]]:
        """
        Previsão usando média móvel adaptativa
        
        Args:
            data: DataFrame com dados limpos
            months_ahead: Número de meses para prever
            
        Returns:
            Dict: Resultado da previsão ou None
        """
        config = self.model_config['moving_average']
        
        if len(data) < config['min_data_points']:
            return None
        
        values = data['value'].values
        alpha = config['alpha']
        
        # Determinar janela ótima
        max_window = min(config['max_window'], len(values))
        optimal_window = min(max(3, len(values) // 4), max_window)
        
        # Pesos exponenciais para média móvel ponderada
        weights = np.array([alpha * (1 - alpha)**i for i in range(optimal_window)])
        weights = weights / weights.sum()
        
        # Calcular média móvel ponderada
        recent_values = values[-optimal_window:]
        ma_value = np.average(recent_values, weights=weights)
        
        # Estimar tendência usando regressão nos dados recentes
        recent_window = min(len(values), optimal_window)
        recent_x = np.arange(recent_window)
        recent_y = values[-recent_window:]
        
        if len(recent_y) >= 2:
            trend, _ = np.polyfit(recent_x, recent_y, 1)
        else:
            trend = 0
        
        # Calcular volatilidade para intervalos de confiança
        volatility = np.std(values[-min(12, len(values)):])
        
        # Gerar previsões com decay da tendência
        future_values = []
        current_level = ma_value
        
        for i in range(months_ahead):
            # Aplicar decay na tendência para evitar extrapolação excessiva
            trend_factor = np.exp(-0.1 * i)
            pred_value = current_level + trend * trend_factor
            future_values.append(pred_value)
            
            # Atualizar nível com suavização
            current_level = alpha * pred_value + (1 - alpha) * current_level
        
        # Gerar datas futuras
        future_dates = self._generate_future_dates(data['date'].max(), months_ahead)
        
        # Calcular intervalos de confiança baseados na volatilidade
        confidence_intervals = []
        for i, pred in enumerate(future_values):
            margin = volatility * (1 + 0.25 * i) * 1.5
            confidence_intervals.append((pred - margin, pred + margin))
        
        # Calcular scores de confiança
        base_confidence = 0.75  # Menor que outros métodos
        confidence_scores = self._calculate_confidence_scores(months_ahead, base_confidence)
        
        return {
            'dates': future_dates,
            'values': future_values,
            'confidence_intervals': confidence_intervals,
            'confidence_scores': confidence_scores,
            'method': 'Média Móvel Adaptativa',
            'rmse': volatility,
            'model_params': {
                'window_size': optimal_window,
                'alpha': alpha,
                'trend': trend,
                'ma_value': ma_value
            }
        }
    
    def _generate_future_dates(self, last_date: pd.Timestamp, months_ahead: int) -> List[datetime]:
        """
        Gera lista de datas futuras
        
        Args:
            last_date: Última data dos dados históricos
            months_ahead: Número de meses à frente
            
        Returns:
            List[datetime]: Lista de datas futuras
        """
        future_dates = []
        current_date = last_date
        
        for i in range(months_ahead):
            # Adicionar um mês
            if current_date.month == 12:
                next_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_date = current_date.replace(month=current_date.month + 1)
            
            future_dates.append(next_date.to_pydatetime())
            current_date = next_date
        
        return future_dates
    
    def _calculate_confidence_intervals(self, predictions: List[float], rmse: float, 
                                      months_ahead: int, method: str) -> List[Tuple[float, float]]:
        """
        Calcula intervalos de confiança para as previsões
        
        Args:
            predictions: Lista de valores previstos
            rmse: Erro quadrático médio do modelo
            months_ahead: Número de meses previstos
            method: Método de previsão usado
            
        Returns:
            List[Tuple[float, float]]: Lista de intervalos (inferior, superior)
        """
        intervals = []
        
        # Fator base baseado no método
        if method == 'linear':
            base_factor = 1.96  # 95% de confiança
        elif method == 'exponential':
            base_factor = 2.0
        else:
            base_factor = 1.5
        
        for i, pred in enumerate(predictions):
            # Margem cresce com o tempo e inclui incerteza do modelo
            time_factor = 1 + 0.15 * i  # Cresce 15% por mês
            margin = rmse * base_factor * time_factor
            
            intervals.append((pred - margin, pred + margin))
        
        return intervals
    
    def _calculate_confidence_scores(self, months_ahead: int, base_confidence: float = 0.9) -> List[float]:
        """
        Calcula scores de confiança decrescente
        
        Args:
            months_ahead: Número de meses previstos
            base_confidence: Confiança inicial (0-1)
            
        Returns:
            List[float]: Lista de scores de confiança
        """
        scores = []
        
        for i in range(months_ahead):
            # Decay exponencial da confiança
            confidence = base_confidence * np.exp(-self.confidence_decay_rate * i)
            confidence = max(confidence, self.min_confidence)
            scores.append(confidence)
        
        return scores
    
    def _create_fallback_prediction(self, data: pd.DataFrame, months_ahead: int) -> Dict[str, any]:
        """
        Cria previsão de fallback para casos de erro ou dados insuficientes
        
        Args:
            data: DataFrame com dados (pode estar vazio)
            months_ahead: Número de meses para prever
            
        Returns:
            Dict: Previsão de fallback
        """
        # Usar último valor disponível ou zero
        if not data.empty and 'value' in data.columns:
            last_value = data['value'].iloc[-1]
            last_date = data['date'].max()
        else:
            last_value = 0
            last_date = pd.Timestamp.now()
        
        # Gerar datas futuras
        future_dates = self._generate_future_dates(last_date, months_ahead)
        
        # Previsões constantes (último valor)
        future_values = [last_value] * months_ahead
        
        # Intervalos de confiança amplos
        confidence_intervals = [(val * 0.8, val * 1.2) for val in future_values]
        
        # Confiança baixa
        confidence_scores = [0.3] * months_ahead
        
        return {
            'dates': future_dates,
            'values': future_values,
            'confidence_intervals': confidence_intervals,
            'confidence_scores': confidence_scores,
            'method': 'Fallback Simples',
            'rmse': None,
            'model_params': {
                'fallback_reason': 'Dados insuficientes ou erro no modelo',
                'base_value': last_value
            }
        }
    
    def evaluate_prediction_quality(self, data: pd.DataFrame, prediction_result: Dict[str, any]) -> Dict[str, any]:
        """
        Avalia a qualidade da previsão baseada nos dados históricos
        
        Args:
            data: DataFrame com dados históricos
            prediction_result: Resultado da previsão
            
        Returns:
            Dict: Métricas de qualidade da previsão
        """
        if data.empty or not prediction_result:
            return {
                'quality_score': 0,
                'reliability': 'Baixa',
                'factors': []
            }
        
        # Fatores que influenciam a qualidade
        factors = []
        quality_points = 0
        max_points = 0
        
        # 1. Quantidade de dados históricos
        n_points = len(data)
        max_points += 20
        if n_points >= 24:
            quality_points += 20
            factors.append("✅ Dados históricos suficientes (24+ pontos)")
        elif n_points >= 12:
            quality_points += 15
            factors.append("⚠️ Dados históricos moderados (12-23 pontos)")
        else:
            quality_points += 5
            factors.append("❌ Poucos dados históricos (<12 pontos)")
        
        # 2. Qualidade do modelo (R² se disponível)
        max_points += 25
        r_squared = prediction_result.get('r_squared', 0)
        if r_squared > 0.7:
            quality_points += 25
            factors.append("✅ Modelo com alta precisão (R² > 0.7)")
        elif r_squared > 0.5:
            quality_points += 18
            factors.append("⚠️ Modelo com precisão moderada (R² > 0.5)")
        elif r_squared > 0.3:
            quality_points += 10
            factors.append("⚠️ Modelo com baixa precisão (R² > 0.3)")
        else:
            quality_points += 5
            factors.append("❌ Modelo com precisão muito baixa (R² ≤ 0.3)")
        
        # 3. Volatilidade dos dados
        max_points += 20
        volatility = np.std(data['value']) / np.mean(data['value']) * 100 if np.mean(data['value']) != 0 else 100
        if volatility < 10:
            quality_points += 20
            factors.append("✅ Baixa volatilidade (<10%)")
        elif volatility < 25:
            quality_points += 15
            factors.append("⚠️ Volatilidade moderada (10-25%)")
        elif volatility < 50:
            quality_points += 8
            factors.append("⚠️ Alta volatilidade (25-50%)")
        else:
            quality_points += 3
            factors.append("❌ Volatilidade muito alta (>50%)")
        
        # 4. Método usado
        max_points += 15
        method = prediction_result.get('method', '')
        if 'Linear' in method:
            quality_points += 15
            factors.append("✅ Método robusto (Regressão Linear)")
        elif 'Exponential' in method:
            quality_points += 12
            factors.append("✅ Método adaptativo (Suavização Exponencial)")
        elif 'Moving' in method:
            quality_points += 8
            factors.append("⚠️ Método conservador (Média Móvel)")
        else:
            quality_points += 3
            factors.append("❌ Método de fallback")
        
        # 5. Consistência da tendência
        max_points += 20
        values = data['value'].values
        if len(values) >= 6:
            # Analisar consistência dividindo dados em duas metades
            mid_point = len(values) // 2
            first_half = values[:mid_point]
            second_half = values[mid_point:]
            
            # Tendência da primeira metade
            x1 = np.arange(len(first_half))
            slope1 = np.polyfit(x1, first_half, 1)[0] if len(first_half) >= 2 else 0
            
            # Tendência da segunda metade
            x2 = np.arange(len(second_half))
            slope2 = np.polyfit(x2, second_half, 1)[0] if len(second_half) >= 2 else 0
            
            # Verificar consistência
            if np.sign(slope1) == np.sign(slope2) and abs(slope1) > 1e-10 and abs(slope2) > 1e-10:
                quality_points += 20
                factors.append("✅ Tendência consistente ao longo do tempo")
            elif abs(slope1) < 1e-10 and abs(slope2) < 1e-10:
                quality_points += 15
                factors.append("✅ Comportamento estável consistente")
            else:
                quality_points += 8
                factors.append("⚠️ Mudança de tendência detectada")
        else:
            quality_points += 10
            factors.append("⚠️ Dados insuficientes para avaliar consistência")
        
        # Calcular score final
        quality_score = (quality_points / max_points) * 100
        
        # Classificar confiabilidade
        if quality_score >= 80:
            reliability = 'Alta'
        elif quality_score >= 60:
            reliability = 'Moderada'
        elif quality_score >= 40:
            reliability = 'Baixa'
        else:
            reliability = 'Muito Baixa'
        
        return {
            'quality_score': round(quality_score, 1),
            'reliability': reliability,
            'factors': factors,
            'details': {
                'data_points': n_points,
                'model_accuracy': r_squared,
                'volatility': round(volatility, 1),
                'method': method,
                'max_possible_score': max_points,
                'achieved_score': quality_points
            }
        }
    
    def compare_prediction_methods(self, data: pd.DataFrame, months_ahead: int = 6) -> Dict[str, any]:
        """
        Compara diferentes métodos de previsão no mesmo dataset
        
        Args:
            data: DataFrame com dados históricos
            months_ahead: Número de meses para prever
            
        Returns:
            Dict: Comparação entre métodos
        """
        methods = ['linear', 'exponential', 'moving_average']
        results = {}
        
        # Executar cada método
        for method in methods:
            try:
                result = self.predict(data, months_ahead, method)
                if result:
                    quality = self.evaluate_prediction_quality(data, result)
                    results[method] = {
                        'prediction': result,
                        'quality': quality
                    }
            except Exception as e:
                results[method] = {
                    'prediction': None,
                    'quality': {'quality_score': 0, 'reliability': 'Erro'},
                    'error': str(e)
                }
        
        # Encontrar melhor método
        best_method = None
        best_score = 0
        
        for method, data_method in results.items():
            if data_method['prediction'] and data_method['quality']['quality_score'] > best_score:
                best_score = data_method['quality']['quality_score']
                best_method = method
        
        # Recomendação
        recommendation = self._generate_method_recommendation(results, best_method)
        
        return {
            'results': results,
            'best_method': best_method,
            'best_score': best_score,
            'recommendation': recommendation,
            'summary': self._generate_comparison_summary(results)
        }
    
    def _generate_method_recommendation(self, results: Dict, best_method: str) -> str:
        """Gera recomendação de método baseada nos resultados"""
        if not best_method:
            return "Dados insuficientes para fazer recomendação confiável. Use dados adicionais."
        
        best_result = results[best_method]
        score = best_result['quality']['quality_score']
        
        method_names = {
            'linear': 'Regressão Linear',
            'exponential': 'Suavização Exponencial',
            'moving_average': 'Média Móvel'
        }
        
        recommendation = f"Recomendamos usar {method_names.get(best_method, best_method)} "
        
        if score >= 80:
            recommendation += f"(qualidade alta: {score:.1f}%). Este método apresenta excelente adequação aos dados."
        elif score >= 60:
            recommendation += f"(qualidade moderada: {score:.1f}%). Este método é adequado, mas monitore a precisão."
        else:
            recommendation += f"(qualidade baixa: {score:.1f}%). Use com cautela e considere coletar mais dados."
        
        return recommendation
    
    def _generate_comparison_summary(self, results: Dict) -> List[str]:
        """Gera resumo da comparação entre métodos"""
        summary = []
        
        valid_results = {k: v for k, v in results.items() if v['prediction'] is not None}
        
        if not valid_results:
            return ["Nenhum método conseguiu gerar previsões válidas com os dados fornecidos."]
        
        # Ordenar por qualidade
        sorted_methods = sorted(valid_results.items(), 
                              key=lambda x: x[1]['quality']['quality_score'], 
                              reverse=True)
        
        method_names = {
            'linear': 'Regressão Linear',
            'exponential': 'Suavização Exponencial', 
            'moving_average': 'Média Móvel'
        }
        
        # Melhor método
        best_method, best_data = sorted_methods[0]
        summary.append(f"🥇 {method_names[best_method]}: melhor performance ({best_data['quality']['quality_score']:.1f}%)")
        
        # Outros métodos
        for method, data in sorted_methods[1:]:
            score = data['quality']['quality_score']
            if score >= 60:
                summary.append(f"✅ {method_names[method]}: boa alternativa ({score:.1f}%)")
            elif score >= 40:
                summary.append(f"⚠️ {method_names[method]}: adequado com limitações ({score:.1f}%)")
            else:
                summary.append(f"❌ {method_names[method]}: não recomendado ({score:.1f}%)")
        
        return summary
    
    def get_prediction_explanation(self, prediction_result: Dict[str, any]) -> Dict[str, any]:
        """
        Gera explicação detalhada sobre como a previsão foi gerada
        
        Args:
            prediction_result: Resultado da previsão
            
        Returns:
            Dict: Explicação detalhada
        """
        if not prediction_result:
            return {
                'method_explanation': 'Não foi possível gerar previsão',
                'confidence_explanation': 'N/A',
                'limitations': ['Dados insuficientes']
            }
        
        method = prediction_result.get('method', 'Desconhecido')
        
        # Explicações por método
        method_explanations = {
            'Regressão Linear': {
                'description': 'Identifica tendência linear nos dados históricos e projeta para o futuro',
                'assumptions': ['Tendência linear continua', 'Sem mudanças estruturais', 'Padrão histórico se mantém'],
                'best_for': 'Dados com tendência clara e constante',
                'limitations': ['Não captura sazonalidade', 'Sensível a outliers', 'Assume linearidade']
            },
            'Suavização Exponencial': {
                'description': 'Usa média ponderada dando mais peso aos dados recentes e captura tendência',
                'assumptions': ['Dados recentes são mais relevantes', 'Tendência pode mudar gradualmente'],
                'best_for': 'Dados com tendência variável e mudanças graduais',
                'limitations': ['Não captura mudanças abruptas', 'Requer calibração de parâmetros']
            },
            'Média Móvel Adaptativa': {
                'description': 'Calcula média dos valores recentes com pesos decrescentes',
                'assumptions': ['Futuro próximo similar ao passado recente', 'Mudanças graduais'],
                'best_for': 'Dados estáveis ou com alta volatilidade',
                'limitations': ['Reativo a mudanças', 'Não prevê reversões de tendência']
            }
        }
        
        # Explicação da confiança
        avg_confidence = np.mean(prediction_result.get('confidence_scores', [0]))
        
        if avg_confidence > 0.7:
            confidence_explanation = "Alta confiança: dados históricos mostram padrão claro e consistente"
        elif avg_confidence > 0.5:
            confidence_explanation = "Confiança moderada: alguns padrões identificados, mas com incertezas"
        elif avg_confidence > 0.3:
            confidence_explanation = "Baixa confiança: padrões pouco claros ou dados voláteis"
        else:
            confidence_explanation = "Confiança muito baixa: dados insuficientes ou muito irregulares"
        
        return {
            'method_explanation': method_explanations.get(method, {
                'description': f'Método {method} aplicado aos dados',
                'assumptions': ['Padrões históricos se mantêm'],
                'best_for': 'Casos gerais',
                'limitations': ['Baseado apenas em dados históricos']
            }),
            'confidence_explanation': confidence_explanation,
            'confidence_decay': 'Confiança diminui exponencialmente com o tempo (15% por mês)',
            'interval_explanation': 'Intervalos de confiança mostram faixa provável de valores reais',
            'general_limitations': [
                'Baseado apenas em dados históricos',
                'Não prevê eventos extraordinários',
                'Assume continuidade de padrões',
                'Não considera fatores externos',
                'Precisão diminui com horizonte temporal'
            ]
        }