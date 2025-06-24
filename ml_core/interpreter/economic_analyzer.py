# ml_core/interpreter/economic_analyzer.py
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from database_manager import DatabaseManager
from ml_core.forecaster import simulate_forecast
from .config import get_indicator_name, get_available_indicators, VISUALIZATION_CONFIG, ANALYSIS_CONFIG

class EconomicAnalyzer:
    """
    Classe para análise econômica avançada com múltiplos indicadores
    """
    
    def __init__(self):
        self.db = DatabaseManager()
        self.indicators_data = {}
        self.correlation_matrix = None
        
    def load_indicators(self, indicators, start_date=None, end_date=None):
        """
        Carrega dados de múltiplos indicadores
        
        Args:
            indicators: Lista de indicadores para carregar
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
        """
        self.indicators_data = {}
        
        for indicator in indicators:
            data = self.db.load_data(indicator, start_date, end_date)
            if data is not None and not data.empty:
                self.indicators_data[indicator] = data
                print(f"✅ {indicator}: {len(data)} registros carregados")
            else:
                print(f"❌ {indicator}: Sem dados disponíveis")
    
    def calculate_correlation_matrix(self, period_months=12):
        """
        Calcula matriz de correlação entre indicadores
        
        Args:
            period_months: Período em meses para análise de correlação
        """
        if not self.indicators_data:
            print("❌ Nenhum dado carregado. Use load_indicators() primeiro.")
            return None
        
        # Filtrar dados pelo período
        cutoff_date = datetime.now() - timedelta(days=period_months * 30)
        
        # Preparar dados para correlação
        correlation_data = {}
        
        for indicator, data in self.indicators_data.items():
            # Filtrar por período
            filtered_data = data[data['date'] >= cutoff_date].copy()
            
            if len(filtered_data) > 0:
                # Agrupar por mês para sincronizar frequências
                filtered_data['year_month'] = filtered_data['date'].dt.to_period('M')
                monthly_avg = filtered_data.groupby('year_month')['value'].mean()
                correlation_data[indicator] = monthly_avg
        
        # Criar DataFrame alinhado
        df_corr = pd.DataFrame(correlation_data)
        
        # Calcular correlação
        self.correlation_matrix = df_corr.corr()
        
        return self.correlation_matrix
    
    def plot_correlation_heatmap(self):
        """
        Cria heatmap da matriz de correlação
        """
        if self.correlation_matrix is None:
            print("❌ Calcule a matriz de correlação primeiro.")
            return None
        
        # Plotly heatmap
        fig = go.Figure(data=go.Heatmap(
            z=self.correlation_matrix.values,
            x=[get_indicator_name(col) for col in self.correlation_matrix.columns],
            y=[get_indicator_name(idx) for idx in self.correlation_matrix.index],
            colorscale='RdBu',
            zmid=0,
            text=np.round(self.correlation_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Matriz de Correlação - Indicadores Econômicos',
            xaxis_title='Indicadores',
            yaxis_title='Indicadores',
            width=VISUALIZATION_CONFIG['figure_width'],
            height=VISUALIZATION_CONFIG['figure_height']
        )
        
        return fig
    
    def analyze_indicator_trends(self, indicator, window_days=90):
        """
        Analisa tendências de um indicador específico
        
        Args:
            indicator: Nome do indicador
            window_days: Janela de análise em dias
        """
        if indicator not in self.indicators_data:
            return None
        
        data = self.indicators_data[indicator].copy()
        
        # Calcular estatísticas de tendência
        recent_data = data.tail(min(window_days, len(data)))
        
        # Tendência linear
        x = np.arange(len(recent_data))
        y = recent_data['value'].values
        slope = np.polyfit(x, y, 1)[0] if len(y) > 1 else 0
        
        # Volatilidade
        volatility = recent_data['value'].std()
        
        # Variação percentual
        if len(recent_data) >= 2:
            pct_change = ((recent_data['value'].iloc[-1] - recent_data['value'].iloc[0]) / 
                         recent_data['value'].iloc[0] * 100)
        else:
            pct_change = 0
        
        # Determinar tendência
        threshold = volatility * ANALYSIS_CONFIG.get('trend_window', 0.1) / 100
        if slope > threshold:
            trend = "📈 Tendência de Alta"
        elif slope < -threshold:
            trend = "📉 Tendência de Baixa" 
        else:
            trend = "📊 Tendência Estável"
        
        return {
            'indicator': indicator,
            'trend': trend,
            'slope': slope,
            'volatility': volatility,
            'pct_change': pct_change,
            'current_value': recent_data['value'].iloc[-1],
            'period_start': recent_data['date'].iloc[0],
            'period_end': recent_data['date'].iloc[-1],
            'data_points': len(recent_data)
        }
    
    def generate_multi_indicator_chart(self, indicators, normalize=True):
        """
        Gera gráfico com múltiplos indicadores
        
        Args:
            indicators: Lista de indicadores para plotar
            normalize: Se True, normaliza os dados para mesma escala
        """
        fig = go.Figure()
        
        colors = VISUALIZATION_CONFIG['color_palette']
        
        for i, indicator in enumerate(indicators):
            if indicator in self.indicators_data:
                data = self.indicators_data[indicator].copy()
                
                values = data['value'].values
                if normalize:
                    # Normalizar para escala 0-100
                    values = ((values - values.min()) / (values.max() - values.min())) * 100
                
                color = colors[i % len(colors)]
                
                fig.add_trace(go.Scatter(
                    x=data['date'],
                    y=values,
                    mode='lines',
                    name=get_indicator_name(indicator),
                    line=dict(width=VISUALIZATION_CONFIG['line_width'], color=color)
                ))
        
        fig.update_layout(
            title='Evolução dos Indicadores Econômicos',
            xaxis_title='Data',
            yaxis_title='Valor Normalizado (0-100)' if normalize else 'Valor',
            hovermode='x unified',
            width=VISUALIZATION_CONFIG['figure_width'],
            height=VISUALIZATION_CONFIG['figure_height'],
            font=dict(family=VISUALIZATION_CONFIG['font_family'], size=VISUALIZATION_CONFIG['font_size'])
        )
        
        return fig
    
    def generate_ai_analysis_report(self, indicators):
        """
        Gera relatório de análise econômica usando IA
        
        Args:
            indicators: Lista de indicadores para analisar
        """
        if not self.indicators_data:
            return "❌ Nenhum dado carregado para análise."
        
        # Calcular análises individuais
        trends_analysis = {}
        for indicator in indicators:
            if indicator in self.indicators_data:
                trends_analysis[indicator] = self.analyze_indicator_trends(indicator)
        
        # Calcular correlações
        correlation_matrix = self.calculate_correlation_matrix()
        
        # Gerar relatório
        report = self._build_analysis_report(trends_analysis, correlation_matrix)
        
        return report
    
    def _build_analysis_report(self, trends_analysis, correlation_matrix):
        """
        Constrói relatório de análise estruturado
        """
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        report = f"""
# 📊 RELATÓRIO DE ANÁLISE ECONÔMICA
**Data do Relatório:** {current_date}

## 🎯 RESUMO EXECUTIVO

### Indicadores Analisados
{len(trends_analysis)} indicadores econômicos foram analisados para identificar tendências, correlações e insights estratégicos.

## 📈 ANÁLISE INDIVIDUAL DOS INDICADORES

"""
        
        # Análise individual
        for indicator, analysis in trends_analysis.items():
            if analysis:
                indicator_name = get_indicator_name(indicator)
                report += f"""
### {indicator_name}
- **Tendência Atual:** {analysis['trend']}
- **Valor Atual:** {analysis['current_value']:.2f}
- **Variação do Período:** {analysis['pct_change']:+.2f}%
- **Volatilidade:** {analysis['volatility']:.2f}
- **Pontos de Dados:** {analysis['data_points']} registros
- **Período Analisado:** {analysis['period_start'].strftime('%d/%m/%Y')} a {analysis['period_end'].strftime('%d/%m/%Y')}

"""
        
        # Análise de correlações
        if correlation_matrix is not None:
            report += """
## 🔗 ANÁLISE DE CORRELAÇÕES

### Correlações Mais Fortes
"""
            
            # Encontrar correlações mais fortes (excluindo diagonal)
            correlation_pairs = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if not np.isnan(corr_value):
                        correlation_pairs.append({
                            'pair': f"{get_indicator_name(correlation_matrix.columns[i])} × {get_indicator_name(correlation_matrix.columns[j])}",
                            'correlation': corr_value
                        })
            
            # Ordenar por correlação absoluta
            correlation_pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
            
            for pair in correlation_pairs[:5]:  # Top 5 correlações
                corr = pair['correlation']
                strength = "Forte" if abs(corr) > 0.7 else "Moderada" if abs(corr) > 0.4 else "Fraca"
                direction = "Positiva" if corr > 0 else "Negativa"
                
                report += f"- **{pair['pair']}:** {corr:.3f} ({strength} {direction})\n"
        
        # Insights e recomendações
        report += """

## 💡 INSIGHTS E RECOMENDAÇÕES

### Principais Observações
"""
        
        # Análise automatizada de tendências
        high_trends = [ind for ind, analysis in trends_analysis.items() if analysis and "Alta" in analysis['trend']]
        low_trends = [ind for ind, analysis in trends_analysis.items() if analysis and "Baixa" in analysis['trend']]
        stable_trends = [ind for ind, analysis in trends_analysis.items() if analysis and "Estável" in analysis['trend']]
        
        if high_trends:
            high_names = [get_indicator_name(ind) for ind in high_trends]
            report += f"- **Indicadores em Alta:** {', '.join(high_names)}\n"
        
        if low_trends:
            low_names = [get_indicator_name(ind) for ind in low_trends]
            report += f"- **Indicadores em Baixa:** {', '.join(low_names)}\n"
        
        if stable_trends:
            stable_names = [get_indicator_name(ind) for ind in stable_trends]
            report += f"- **Indicadores Estáveis:** {', '.join(stable_names)}\n"
        
        report += """

### Recomendações Estratégicas
1. **Monitoramento Contínuo:** Acompanhar indicadores com alta volatilidade
2. **Análise de Correlações:** Utilizar correlações fortes para previsões cruzadas
3. **Diversificação:** Considerar indicadores com baixa correlação para reduzir riscos
4. **Atualização Regular:** Revisar análises mensalmente para capturar mudanças de tendência

---
*Relatório gerado automaticamente pelo Sistema de Análise Econômica*
"""
        
        return report
    
    def generate_forecast_comparison(self, indicators, periods=6):
        """
        Gera comparação de previsões para múltiplos indicadores
        """
        forecasts = {}
        
        for indicator in indicators:
            if indicator in self.indicators_data:
                try:
                    forecast = simulate_forecast(indicator, periods)
                    if forecast is not None and not forecast.empty:
                        forecasts[indicator] = forecast
                        print(f"✅ Previsão gerada para {indicator}")
                    else:
                        print(f"❌ Falha na previsão para {indicator}")
                except Exception as e:
                    print(f"❌ Erro na previsão para {indicator}: {e}")
        
        return forecasts
    
    def plot_forecast_comparison(self, forecasts):
        """
        Plota comparação de previsões
        """
        fig = make_subplots(
            rows=len(forecasts), 
            cols=1,
            subplot_titles=[get_indicator_name(ind) for ind in forecasts.keys()],
            vertical_spacing=0.05
        )
        
        colors = VISUALIZATION_CONFIG['color_palette']
        
        for i, (indicator, forecast_data) in enumerate(forecasts.items(), 1):
            color = colors[i % len(colors)]
            
            # Dados históricos recentes
            if indicator in self.indicators_data:
                historical = self.indicators_data[indicator].tail(30)
                fig.add_trace(
                    go.Scatter(
                        x=historical['date'],
                        y=historical['value'],
                        mode='lines',
                        name=f'{get_indicator_name(indicator)} (Histórico)',
                        line=dict(color=color, width=2),
                        showlegend=(i==1)
                    ),
                    row=i, col=1
                )
            
            # Previsões
            fig.add_trace(
                go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data['value'],
                    mode='lines+markers',
                    name=f'{get_indicator_name(indicator)} (Previsão)',
                    line=dict(color='red', width=2, dash='dash'),
                    marker=dict(size=6),
                    showlegend=(i==1)
                ),
                row=i, col=1
            )
        
        fig.update_layout(
            title='Comparação de Previsões Econômicas',
            height=300 * len(forecasts),
            showlegend=True,
            font=dict(family=VISUALIZATION_CONFIG['font_family'], size=VISUALIZATION_CONFIG['font_size'])
        )
        
        return fig

# Função de conveniência para análise rápida
def quick_economic_analysis(indicators, period_months=12):
    """
    Função para análise econômica rápida
    
    Args:
        indicators: Lista de indicadores
        period_months: Período de análise em meses
    
    Returns:
        Dicionário com análises e gráficos
    """
    analyzer = EconomicAnalyzer()
    analyzer.load_indicators(indicators)
    
    # Análises
    correlation_matrix = analyzer.calculate_correlation_matrix(period_months)
    ai_report = analyzer.generate_ai_analysis_report(indicators)
    forecasts = analyzer.generate_forecast_comparison(indicators)
    
    # Gráficos
    correlation_heatmap = analyzer.plot_correlation_heatmap()
    multi_chart = analyzer.generate_multi_indicator_chart(indicators)
    forecast_chart = analyzer.plot_forecast_comparison(forecasts) if forecasts else None
    
    return {
        'analyzer': analyzer,
        'correlation_matrix': correlation_matrix,
        'ai_report': ai_report,
        'forecasts': forecasts,
        'charts': {
            'correlation_heatmap': correlation_heatmap,
            'multi_indicator_chart': multi_chart,
            'forecast_comparison': forecast_chart
        }
    }