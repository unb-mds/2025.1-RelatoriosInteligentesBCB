# ml_core/interpreter/visualization.py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from .config import VISUALIZATION_CONFIG, get_indicator_name

class VisualizationEngine:
    """
    Engine de visualização para indicadores econômicos
    """
    
    def __init__(self):
        self.config = VISUALIZATION_CONFIG
        self.colors = self.config['color_palette']
    
    def create_line_chart(self, data, indicator_name, title=None):
        """
        Cria gráfico de linha simples
        
        Args:
            data: DataFrame com colunas 'date' e 'value'
            indicator_name: Nome do indicador
            title: Título personalizado (opcional)
        """
        if data is None or data.empty:
            return None
        
        title = title or f'Evolução - {get_indicator_name(indicator_name)}'
        
        fig = px.line(
            data,
            x='date',
            y='value',
            title=title,
            color_discrete_sequence=[self.colors[0]]
        )
        
        fig.update_layout(
            width=self.config['figure_width'],
            height=self.config['figure_height'],
            font=dict(
                family=self.config['font_family'],
                size=self.config['font_size']
            ),
            xaxis_title='Data',
            yaxis_title='Valor'
        )
        
        return fig
    
    def create_multi_line_chart(self, data_dict, normalize=True, title=None):
        """
        Cria gráfico com múltiplas linhas
        
        Args:
            data_dict: Dicionário {indicator: dataframe}
            normalize: Se True, normaliza os dados
            title: Título personalizado
        """
        fig = go.Figure()
        
        title = title or 'Comparação de Indicadores Econômicos'
        
        for i, (indicator, data) in enumerate(data_dict.items()):
            if data is not None and not data.empty:
                values = data['value'].values
                
                if normalize:
                    # Normalizar para escala 0-100
                    values = ((values - values.min()) / (values.max() - values.min())) * 100
                
                color = self.colors[i % len(self.colors)]
                
                fig.add_trace(go.Scatter(
                    x=data['date'],
                    y=values,
                    mode='lines',
                    name=get_indicator_name(indicator),
                    line=dict(width=self.config['line_width'], color=color)
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Data',
            yaxis_title='Valor Normalizado (0-100)' if normalize else 'Valor',
            width=self.config['figure_width'],
            height=self.config['figure_height'],
            font=dict(
                family=self.config['font_family'],
                size=self.config['font_size']
            ),
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def create_correlation_heatmap(self, correlation_matrix):
        """
        Cria heatmap de correlação
        
        Args:
            correlation_matrix: Matriz de correlação pandas
        """
        if correlation_matrix is None or correlation_matrix.empty:
            return None
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=[get_indicator_name(col) for col in correlation_matrix.columns],
            y=[get_indicator_name(idx) for idx in correlation_matrix.index],
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlation_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Matriz de Correlação - Indicadores Econômicos',
            xaxis_title='Indicadores',
            yaxis_title='Indicadores',
            width=self.config['figure_width'],
            height=self.config['figure_height']
        )
        
        return fig
    
    def create_forecast_chart(self, historical_data, forecast_data, indicator_name):
        """
        Cria gráfico de previsão
        
        Args:
            historical_data: Dados históricos
            forecast_data: Dados de previsão
            indicator_name: Nome do indicador
        """
        fig = go.Figure()
        
        # Dados históricos
        if historical_data is not None and not historical_data.empty:
            fig.add_trace(go.Scatter(
                x=historical_data['date'],
                y=historical_data['value'],
                mode='lines',
                name='Histórico',
                line=dict(color=self.colors[0], width=2)
            ))
        
        # Previsões
        if forecast_data is not None and not forecast_data.empty:
            fig.add_trace(go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['value'],
                mode='lines+markers',
                name='Previsão',
                line=dict(color='red', width=2, dash='dash'),
                marker=dict(size=6)
            ))
            
            # Intervalos de confiança se disponíveis
            if 'lower_bound' in forecast_data.columns and 'upper_bound' in forecast_data.columns:
                fig.add_trace(go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data['upper_bound'],
                    mode='lines',
                    line=dict(width=0),
                    name='Limite Superior',
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data['lower_bound'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.2)',
                    name='Intervalo de Confiança',
                    showlegend=True
                ))
        
        fig.update_layout(
            title=f'Previsão - {get_indicator_name(indicator_name)}',
            xaxis_title='Data',
            yaxis_title='Valor',
            width=self.config['figure_width'],
            height=self.config['figure_height'],
            font=dict(
                family=self.config['font_family'],
                size=self.config['font_size']
            )
        )
        
        return fig
    
    def create_trend_analysis_chart(self, data, trend_info, indicator_name):
        """
        Cria gráfico de análise de tendência
        
        Args:
            data: DataFrame com dados
            trend_info: Informações de tendência
            indicator_name: Nome do indicador
        """
        if data is None or data.empty:
            return None
        
        fig = go.Figure()
        
        # Linha principal
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['value'],
            mode='lines',
            name='Dados',
            line=dict(color=self.colors[0], width=2)
        ))
        
        # Linha de tendência se disponível
        if trend_info and 'slope' in trend_info:
            # Calcular linha de tendência
            x_vals = np.arange(len(data))
            trend_line = trend_info['slope'] * x_vals + data['value'].iloc[0]
            
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=trend_line,
                mode='lines',
                name='Tendência',
                line=dict(color='red', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=f'Análise de Tendência - {get_indicator_name(indicator_name)}',
            xaxis_title='Data',
            yaxis_title='Valor',
            width=self.config['figure_width'],
            height=self.config['figure_height'],
            font=dict(
                family=self.config['font_family'],
                size=self.config['font_size']
            )
        )
        
        return fig
    
    def create_comparison_subplots(self, data_dict, title="Comparação de Indicadores"):
        """
        Cria subplots para comparar múltiplos indicadores
        
        Args:
            data_dict: Dicionário {indicator: dataframe}
            title: Título principal
        """
        if not data_dict:
            return None
        
        num_indicators = len(data_dict)
        rows = (num_indicators + 1) // 2  # 2 colunas
        
        fig = make_subplots(
            rows=rows,
            cols=2,
            subplot_titles=[get_indicator_name(ind) for ind in data_dict.keys()],
            vertical_spacing=0.08,
            horizontal_spacing=0.05
        )
        
        for i, (indicator, data) in enumerate(data_dict.items()):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            if data is not None and not data.empty:
                color = self.colors[i % len(self.colors)]
                
                fig.add_trace(
                    go.Scatter(
                        x=data['date'],
                        y=data['value'],
                        mode='lines',
                        name=get_indicator_name(indicator),
                        line=dict(color=color, width=2),
                        showlegend=False
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            title=title,
            height=300 * rows,
            font=dict(
                family=self.config['font_family'],
                size=self.config['font_size']
            )
        )
        
        return fig
    
    def create_metrics_dashboard(self, metrics_dict):
        """
        Cria dashboard de métricas
        
        Args:
            metrics_dict: Dicionário com métricas
        """
        # Esta função pode ser expandida para criar um dashboard completo
        # Por enquanto, retorna None (placeholder)
        return None