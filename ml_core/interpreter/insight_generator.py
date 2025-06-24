"""
ML Core Interpreter - Insight Generator
Módulo responsável pela geração inteligente de insights econômicos

Author: Assistant
Version: 1.1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from .config import get_indicator_name, get_indicator_config, ANALYSIS_CONFIG

class InsightGenerator:
    """
    Classe responsável pela geração inteligente de insights
    """
    
    def __init__(self):
        self.config = ANALYSIS_CONFIG['insights']
        self.max_insights = self.config['max_insights']
        self.min_confidence = self.config['min_confidence']
        
    def generate(self, indicator: str, data: pd.DataFrame, 
                trend_analysis: Dict[str, any]) -> List[str]:
        """
        Gera insights inteligentes para um indicador específico
        
        Args:
            indicator: Nome do indicador
            data: DataFrame com dados históricos
            trend_analysis: Resultado da análise de tendência
            
        Returns:
            List[str]: Lista de insights formatados
        """
        if data.empty:
            return ["📊 Dados insuficientes para gerar insights abrangentes."]
        
        insights = []
        indicator_name = get_indicator_name(indicator)
        
        # 1. Insights sobre tendência principal
        insights.extend(self._generate_trend_insights(indicator, indicator_name, trend_analysis))
        
        # 2. Insights sobre volatilidade
        insights.extend(self._generate_volatility_insights(indicator_name, trend_analysis))
        
        # 3. Insights específicos por indicador
        insights.extend(self._generate_indicator_specific_insights(indicator, trend_analysis, data))
        
        # 4. Insights sobre padrões sazonais
        insights.extend(self._generate_seasonal_insights(indicator_name, trend_analysis))
        
        # 5. Insights sobre outliers
        insights.extend(self._generate_outlier_insights(indicator_name, data))
        
        # 6. Insights de contexto econômico
        insights.extend(self._generate_economic_context_insights(indicator, trend_analysis))
        
        # Limitar número de insights e ordenar por relevância
        return self._prioritize_insights(insights)[:self.max_insights]
    
    def _generate_trend_insights(self, indicator: str, indicator_name: str, 
                                trend_analysis: Dict[str, any]) -> List[str]:
        """Gera insights sobre a tendência principal"""
        insights = []
        
        direction = trend_analysis.get('direction', 'N/A')
        confidence = trend_analysis.get('confidence', 0)
        strength = trend_analysis.get('trend_strength', 'Indefinida')
        change_pct = trend_analysis.get('change_pct', 0)
        significance = trend_analysis.get('trend_significance', 'Baixa')
        
        # Insight principal sobre tendência
        if confidence > 0.7:
            if direction == 'Crescente':
                insights.append(
                    f"📈 **Tendência Ascendente {strength}:** {indicator_name} apresenta crescimento "
                    f"consistente ({change_pct:+.2f}%) com {significance.lower()} confiabilidade "
                    f"({confidence:.1%}). Padrão bem estabelecido para planejamento estratégico."
                )
            elif direction == 'Decrescente':
                insights.append(
                    f"📉 **Tendência Descendente {strength}:** {indicator_name} em trajetória de queda "
                    f"({change_pct:+.2f}%) com {significance.lower()} confiabilidade "
                    f"({confidence:.1%}). Requer atenção e possíveis intervenções."
                )
            else:  # Estável
                insights.append(
                    f"📊 **Estabilidade Confirmada:** {indicator_name} mantém comportamento estável "
                    f"({change_pct:+.2f}%) com {significance.lower()} confiabilidade. "
                    f"Cenário favorável para previsibilidade."
                )
        elif confidence > 0.4:
            insights.append(
                f"⚠️ **Tendência Incerta:** {indicator_name} apresenta sinais mistos "
                f"(confiança: {confidence:.1%}). Período de transição ou influências externas "
                f"podem estar afetando o comportamento do indicador."
            )
        else:
            insights.append(
                f"❓ **Comportamento Irregular:** {indicator_name} sem padrão claro "
                f"(confiança: {confidence:.1%}). Análise adicional necessária para "
                f"compreender as forças que influenciam este indicador."
            )
        
        # Insight sobre consistência da tendência
        consistency = trend_analysis.get('trend_consistency', 'N/A')
        recent_direction = trend_analysis.get('recent_direction', 'N/A')
        
        if consistency == 'Reversão' and confidence > 0.5:
            insights.append(
                f"🔄 **Mudança de Direção:** {indicator_name} mostra sinais de reversão "
                f"recente. Tendência geral {direction.lower()}, mas movimento recente "
                f"{recent_direction.lower()}. Monitoramento intensivo recomendado."
            )
        elif consistency == 'Consistente' and confidence > 0.6:
            insights.append(
                f"✅ **Padrão Consistente:** {indicator_name} mantém direção {direction.lower()} "
                f"tanto no período geral quanto recentemente. Alta previsibilidade."
            )
        
        return insights
    
    def _generate_volatility_insights(self, indicator_name: str, 
                                    trend_analysis: Dict[str, any]) -> List[str]:
        """Gera insights sobre volatilidade"""
        insights = []
        
        volatility = trend_analysis.get('volatility', 0)
        volatility_level = trend_analysis.get('volatility_level', 'N/A')
        volatility_trend = trend_analysis.get('volatility_trend', 'N/A')
        
        if volatility > 25:
            insights.append(
                f"🌊 **Volatilidade Extrema:** {indicator_name} com variações de {volatility:.1f}%. "
                f"Período excepcional que dificulta planejamento e requer gestão ativa de risco. "
                f"Considere fatores externos que podem estar causando instabilidade."
            )
        elif volatility > 15:
            insights.append(
                f"⚡ **Alta Volatilidade:** {indicator_name} com variações significativas "
                f"({volatility:.1f}%). Monitoramento frequente e estratégias flexíveis "
                f"recomendadas para lidar com a incerteza."
            )
        elif volatility < 3:
            insights.append(
                f"🎯 **Estabilidade Excepcional:** {indicator_name} muito previsível "
                f"({volatility:.1f}%). Ambiente ideal para planejamento de longo prazo "
                f"e investimentos que dependem de estabilidade."
            )
        elif volatility < 8:
            insights.append(
                f"✅ **Volatilidade Controlada:** {indicator_name} com variações normais "
                f"({volatility:.1f}%). Comportamento dentro do esperado para este tipo "
                f"de indicador econômico."
            )
        
        # Insight sobre tendência da volatilidade
        if volatility_trend == 'Aumentando':
            insights.append(
                f"📈 **Instabilidade Crescente:** A volatilidade de {indicator_name} está "
                f"aumentando, sugerindo período de maior incerteza à frente."
            )
        elif volatility_trend == 'Diminuindo':
            insights.append(
                f"📉 **Estabilização:** A volatilidade de {indicator_name} está diminuindo, "
                f"indicando movimento em direção a maior previsibilidade."
            )
        
        return insights
    
    def _generate_indicator_specific_insights(self, indicator: str, 
                                            trend_analysis: Dict[str, any], 
                                            data: pd.DataFrame) -> List[str]:
        """Gera insights específicos para cada tipo de indicador"""
        insights = []
        
        direction = trend_analysis.get('direction', 'N/A')
        confidence = trend_analysis.get('confidence', 0)
        last_value = trend_analysis.get('last_value', 0)
        change_pct = trend_analysis.get('change_pct', 0)
        
        if indicator == 'ipca':
            insights.extend(self._ipca_specific_insights(last_value, direction, confidence, change_pct))
        elif indicator == 'selic':
            insights.extend(self._selic_specific_insights(last_value, direction, confidence, change_pct))
        elif indicator == 'pib':
            insights.extend(self._pib_specific_insights(direction, confidence, change_pct))
        elif indicator == 'cambio_dolar':
            insights.extend(self._cambio_specific_insights(last_value, direction, change_pct))
        elif indicator == 'divida_pib':
            insights.extend(self._divida_specific_insights(last_value, direction, confidence))
        
        return insights
    
    def _ipca_specific_insights(self, last_value: float, direction: str, 
                               confidence: float, change_pct: float) -> List[str]:
        """Insights específicos para IPCA"""
        insights = []
        
        if last_value > 7.5:
            insights.append(
                "🚨 **Inflação Crítica:** IPCA muito acima da meta! Risco de desancoragem "
                "das expectativas e necessidade de ação emergencial do Banco Central."
            )
        elif last_value > 6.5:
            insights.append(
                "⚠️ **Alerta Inflacionário:** IPCA acima do teto da meta (6,5%). "
                "BC provavelmente precisará apertar política monetária mais agressivamente."
            )
        elif last_value < 2.5:
            insights.append(
                "❄️ **Deflação/Desinflação:** IPCA muito baixo pode indicar recessão "
                "ou demanda fraca na economia. Risco de deflação se persistir."
            )
        elif 3.0 <= last_value <= 6.0:
            insights.append(
                "🎯 **Meta Inflacionária Atingida:** IPCA dentro do intervalo-meta (3-6%). "
                "Política monetária demonstrando eficácia no controle de preços."
            )
        
        # Insights sobre dinâmica inflacionária
        if direction == 'Crescente' and confidence > 0.6:
            insights.append(
                "📈 **Pressão Inflacionária Crescente:** Tendência consistente de alta "
                "pode exigir resposta mais agressiva da política monetária."
            )
        elif direction == 'Decrescente' and confidence > 0.6:
            insights.append(
                "📉 **Desinflação em Curso:** Queda consistente da inflação indica "
                "eficácia das medidas de controle ou desaquecimento econômico."
            )
        
        return insights
    
    def _selic_specific_insights(self, last_value: float, direction: str, 
                               confidence: float, change_pct: float) -> List[str]:
        """Insights específicos para SELIC"""
        insights = []
        
        if last_value > 13:
            insights.append(
                "📊 **Juros Muito Elevados:** SELIC em patamar restritivo pode frear "
                "crescimento econômico significativamente. Impacto no crédito e investimentos."
            )
        elif last_value > 10:
            insights.append(
                "⬆️ **Juros Altos:** SELIC em nível restritivo para combater inflação "
                "ou atrair capital estrangeiro. Pressão sobre atividade econômica."
            )
        elif last_value < 4:
            insights.append(
                "💰 **Juros Baixos:** SELIC em nível estimulativo favorece crescimento "
                "econômico e crédito, mas requer vigilância inflacionária."
            )
        elif 4 <= last_value <= 8:
            insights.append(
                "⚖️ **Juros Neutros:** SELIC em faixa que não estimula nem restringe "
                "significativamente a economia."
            )
        
        # Insights sobre ciclo de política monetária
        if direction == 'Crescente' and confidence > 0.6:
            if abs(change_pct) > 20:
                insights.append(
                    "📈 **Ciclo Agressivo de Aperto:** BC em alta intensa de juros. "
                    "Impacto negativo significativo no crescimento esperado."
                )
            else:
                insights.append(
                    "📈 **Aperto Monetário:** BC elevando juros gradualmente para "
                    "controlar inflação. Monitorar impactos na atividade."
                )
        elif direction == 'Decrescente' and confidence > 0.6:
            insights.append(
                "📉 **Ciclo de Corte:** BC reduzindo juros - sinaliza confiança "
                "no controle inflacionário e foco no crescimento."
            )
        
        return insights
    
    def _pib_specific_insights(self, direction: str, confidence: float, 
                             change_pct: float) -> List[str]:
        """Insights específicos para PIB"""
        insights = []
        
        if direction == 'Crescente' and confidence > 0.6:
            if change_pct > 10:
                insights.append(
                    "🚀 **Crescimento Acelerado:** PIB em forte expansão indica "
                    "aquecimento significativo da economia e melhora do emprego."
                )
            else:
                insights.append(
                    "📈 **Crescimento Sustentado:** PIB em expansão moderada indica "
                    "crescimento saudável da atividade econômica."
                )
        elif direction == 'Decrescente' and confidence > 0.6:
            if abs(change_pct) > 5:
                insights.append(
                    "🔴 **Recessão Iminente:** Queda acentuada do PIB pode sinalizar "
                    "recessão técnica. Monitorar indicadores de emprego e renda."
                )
            else:
                insights.append(
                    "⚠️ **Desaceleração Econômica:** PIB em tendência de queda suave "
                    "indica arrefecimento da atividade."
                )
        elif direction == 'Estável':
            insights.append(
                "📊 **Estagnação Econômica:** PIB sem crescimento pode indicar "
                "economia em transição ou falta de dinamismo."
            )
        
        return insights
    
    def _cambio_specific_insights(self, last_value: float, direction: str, 
                                change_pct: float) -> List[str]:
        """Insights específicos para Câmbio USD/BRL"""
        insights = []
        
        if last_value > 6.5:
            insights.append(
                "💱 **Real Muito Desvalorizado:** Câmbio elevado pressiona inflação "
                "via importados, mas beneficia exportadores."
            )
        elif last_value < 4.0:
            insights.append(
                "💱 **Real Muito Valorizado:** Câmbio baixo beneficia controle "
                "inflacionário, mas prejudica competitividade externa."
            )
        elif 5.0 <= last_value <= 5.5:
            insights.append(
                "💱 **Câmbio Equilibrado:** Real em faixa considerada neutra "
                "para a economia brasileira."
            )
        
        # Insights sobre dinâmica cambial
        recent_change = abs(change_pct)
        if recent_change > 25:
            if change_pct > 0:
                insights.append(
                    "💱 **Depreciação Severa:** Real em queda acentuada - risco "
                    "inflacionário alto via importados e possível necessidade "
                    "de intervenção do BC."
                )
            else:
                insights.append(
                    "💱 **Apreciação Forte:** Real valorizando rapidamente - "
                    "beneficia controle da inflação, mas pode prejudicar exportações."
                )
        elif recent_change > 15:
            insights.append(
                "💱 **Volatilidade Cambial Significativa:** Movimentos cambiais "
                "acentuados podem exigir atenção especial do Banco Central."
            )
        
        return insights
    
    def _divida_specific_insights(self, last_value: float, direction: str, 
                                confidence: float) -> List[str]:
        """Insights específicos para Dívida/PIB"""
        insights = []
        
        if last_value > 85:
            insights.append(
                "📊 **Dívida Muito Elevada:** Dívida/PIB acima de 85% representa "
                "risco fiscal significativo e limita severamente espaço para "
                "políticas anticíclicas."
            )
        elif last_value > 75:
            insights.append(
                "⚠️ **Dívida Elevada:** Dívida/PIB acima de 75% limita espaço "
                "fiscal e pode pressionar juros de longo prazo."
            )
        elif last_value < 60:
            insights.append(
                "✅ **Dívida Controlada:** Dívida/PIB em nível sustentável "
                "permite margem para políticas fiscais expansionistas."
            )
        
        # Insights sobre trajetória fiscal
        if direction == 'Crescente' and confidence > 0.6:
            insights.append(
                "📈 **Deterioração Fiscal:** Crescimento da dívida pública exige "
                "medidas urgentes de consolidação fiscal para evitar crise."
            )
        elif direction == 'Decrescente' and confidence > 0.6:
            insights.append(
                "✅ **Melhora Fiscal:** Redução da dívida pública indica disciplina "
                "fiscal e melhora da sustentabilidade das contas públicas."
            )
        
        return insights
    
    def _generate_seasonal_insights(self, indicator_name: str, 
                                  trend_analysis: Dict[str, any]) -> List[str]:
        """Gera insights sobre padrões sazonais"""
        insights = []
        
        seasonal_pattern = trend_analysis.get('seasonal_pattern', 'Não detectado')
        seasonal_strength = trend_analysis.get('seasonal_strength', 0)
        seasonal_period = trend_analysis.get('seasonal_period', None)
        
        if seasonal_pattern == 'Detectado' and seasonal_strength > 0.4:
            if seasonal_period and seasonal_period <= 12:
                insights.append(
                    f"🔄 **Padrão Sazonal Detectado:** {indicator_name} apresenta "
                    f"sazonalidade com período de {seasonal_period} meses "
                    f"(força: {seasonal_strength:.1%}). Considere este padrão "
                    f"em análises e previsões."
                )
        elif seasonal_pattern == 'Detectado' and seasonal_strength > 0.2:
            insights.append(
                f"📅 **Sazonalidade Fraca:** {indicator_name} mostra sinais de "
                f"padrão sazonal moderado. Pode influenciar comportamento "
                f"em certos períodos do ano."
            )
        
        return insights
    
    def _generate_outlier_insights(self, indicator_name: str, 
                                 data: pd.DataFrame) -> List[str]:
        """Gera insights sobre outliers nos dados"""
        insights = []
        
        if data.empty:
            return insights
        
        # Detectar outliers usando método IQR simples
        values = data['value'].dropna()
        if len(values) < 4:
            return insights
        
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)
        IQR = Q3 - Q1
        
        if IQR > 1e-10:
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = []
            for idx, row in data.iterrows():
                value = row['value']
                if pd.notna(value) and (value < lower_bound or value > upper_bound):
                    outliers.append({
                        'date': row['date'],
                        'value': value,
                        'type': 'Alto' if value > upper_bound else 'Baixo'
                    })
            
            outlier_ratio = len(outliers) / len(data)
            
            if outlier_ratio > 0.2:
                insights.append(
                    f"🔍 **Período Excepcional:** {len(outliers)} valores atípicos "
                    f"({outlier_ratio:.1%}) em {indicator_name} sugerem múltiplos "
                    f"eventos extraordinários ou mudança estrutural no indicador."
                )
            elif outlier_ratio > 0.1:
                insights.append(
                    f"⚡ **Eventos Significativos:** {len(outliers)} outliers detectados "
                    f"em {indicator_name} - possíveis choques externos ou mudanças "
                    f"de política que afetaram o comportamento normal."
                )
            elif outliers:
                recent_outlier = max(outliers, key=lambda x: x['date'])
                date_str = recent_outlier['date'].strftime('%m/%Y')
                insights.append(
                    f"📊 **Valor Atípico Recente:** {indicator_name} apresentou pico "
                    f"em {date_str} ({recent_outlier['value']:.2f}) - pode indicar "
                    f"evento pontual ou erro de medição."
                )
        
        return insights
    
    def _generate_economic_context_insights(self, indicator: str, 
                                          trend_analysis: Dict[str, any]) -> List[str]:
        """Gera insights de contexto econômico mais amplo"""
        insights = []
        
        direction = trend_analysis.get('direction', 'N/A')
        confidence = trend_analysis.get('confidence', 0)
        volatility = trend_analysis.get('volatility', 0)
        
        # Insights contextuais baseados no indicador e condições
        if indicator in ['ipca', 'selic'] and confidence > 0.6:
            if direction == 'Crescente' and indicator == 'ipca':
                insights.append(
                    "🔗 **Implicação Monetária:** Tendência inflacionária crescente "
                    "pode pressionar BC a elevar SELIC, impactando crescimento "
                    "e mercado de capitais."
                )
            elif direction == 'Crescente' and indicator == 'selic':
                insights.append(
                    "🔗 **Implicação Econômica:** Elevação da SELIC pode desacelerar "
                    "crescimento, mas é necessária para controle inflacionário."
                )
        
        if indicator == 'pib' and volatility > 20:
            insights.append(
                "🌊 **Instabilidade Macroeconômica:** Alta volatilidade do PIB "
                "pode refletir incertezas políticas, choques externos ou "
                "mudanças estruturais na economia."
            )
        
        if indicator == 'cambio_dolar' and volatility > 25:
            insights.append(
                "🌍 **Pressões Externas:** Alta volatilidade cambial pode estar "
                "relacionada a fatores globais, política doméstica ou fluxos "
                "de capital especulativo."
            )
        
        # Insight sobre qualidade dos dados para análise
        data_points = trend_analysis.get('data_points', 0)
        if data_points < 12:
            insights.append(
                f"⚠️ **Limitação Analítica:** Com apenas {data_points} pontos de dados, "
                f"a análise tem limitações. Mais dados históricos melhorariam "
                f"a precisão das conclusões."
            )
        
        return insights
    
    def _prioritize_insights(self, insights: List[str]) -> List[str]:
        """
        Prioriza insights por relevância e remove duplicatas
        
        Args:
            insights: Lista de insights não ordenados
            
        Returns:
            List[str]: Insights priorizados
        """
        if not insights:
            return []
        
        # Remover duplicatas mantendo ordem
        unique_insights = []
        seen = set()
        for insight in insights:
            # Usar primeiras 50 caracteres como chave para detectar duplicatas similares
            key = insight[:50].lower()
            if key not in seen:
                unique_insights.append(insight)
                seen.add(key)
        
        # Sistema de priorização baseado em palavras-chave
        priority_scores = []
        
        for insight in unique_insights:
            score = 0
            insight_lower = insight.lower()
            
            # Prioridade alta para alertas críticos
            if any(word in insight_lower for word in ['crítica', 'emergencial', 'severa', 'recessão']):
                score += 10
            
            # Prioridade média-alta para avisos importantes
            if any(word in insight_lower for word in ['alerta', 'atenção', 'significativo', 'agressiv']):
                score += 7
            
            # Prioridade média para insights contextuais
            if any(word in insight_lower for word in ['implicação', 'contexto', 'considera']):
                score += 5
            
            # Prioridade para insights com números específicos
            if any(char.isdigit() for char in insight):
                score += 3
            
            # Prioridade para insights sobre tendência principal
            if any(word in insight_lower for word in ['tendência', 'crescimento', 'queda']):
                score += 4
            
            # Bônus para insights informativos
            if any(word in insight_lower for word in ['meta atingida', 'controlado', 'estável']):
                score += 2
            
            priority_scores.append((score, insight))
        
        # Ordenar por score (maior primeiro) e retornar apenas os insights
        priority_scores.sort(key=lambda x: x[0], reverse=True)
        
        return [insight for score, insight in priority_scores]
    
    def generate_comparative_insights(self, indicators: List[str], 
                                    data_dict: Dict[str, pd.DataFrame],
                                    trend_analyses: Dict[str, Dict]) -> List[str]:
        """
        Gera insights comparativos entre múltiplos indicadores
        
        Args:
            indicators: Lista de indicadores para comparar
            data_dict: Dicionário com dados de cada indicador
            trend_analyses: Dicionário com análises de tendência
            
        Returns:
            List[str]: Insights comparativos
        """
        if len(indicators) < 2:
            return []
        
        insights = []
        
        # Comparações específicas entre pares importantes
        if 'ipca' in indicators and 'selic' in indicators:
            insights.extend(self._compare_ipca_selic(trend_analyses))
        
        if 'pib' in indicators and 'selic' in indicators:
            insights.extend(self._compare_pib_selic(trend_analyses))
        
        if 'cambio_dolar' in indicators and 'ipca' in indicators:
            insights.extend(self._compare_cambio_ipca(trend_analyses))
        
        # Análise de correlações gerais
        insights.extend(self._analyze_general_correlations(indicators, trend_analyses))
        
        return insights[:3]  # Máximo 3 insights comparativos
    
    def _compare_ipca_selic(self, trend_analyses: Dict[str, Dict]) -> List[str]:
        """Compara IPCA e SELIC"""
        insights = []
        
        ipca_analysis = trend_analyses.get('ipca', {})
        selic_analysis = trend_analyses.get('selic', {})
        
        ipca_direction = ipca_analysis.get('direction', 'N/A')
        selic_direction = selic_analysis.get('direction', 'N/A')
        
        if ipca_direction == 'Crescente' and selic_direction == 'Decrescente':
            insights.append(
                "🚨 **Desalinhamento Monetário:** Inflação subindo enquanto SELIC cai. "
                "Possível perda de controle inflacionário - BC pode precisar reverter política."
            )
        elif ipca_direction == 'Decrescente' and selic_direction == 'Crescente':
            insights.append(
                "✅ **Política Eficaz:** SELIC subindo com inflação controlada. "
                "Política monetária demonstrando eficácia no controle de preços."
            )
        elif ipca_direction == 'Crescente' and selic_direction == 'Crescente':
            insights.append(
                "⚔️ **Combate à Inflação:** BC elevando juros para conter pressões "
                "inflacionárias. Acompanhar eficácia das medidas nos próximos meses."
            )
        
        return insights
    
    def _compare_pib_selic(self, trend_analyses: Dict[str, Dict]) -> List[str]:
        """Compara PIB e SELIC"""
        insights = []
        
        pib_analysis = trend_analyses.get('pib', {})
        selic_analysis = trend_analyses.get('selic', {})
        
        pib_direction = pib_analysis.get('direction', 'N/A')
        selic_direction = selic_analysis.get('direction', 'N/A')
        
        if pib_direction == 'Decrescente' and selic_direction == 'Crescente':
            insights.append(
                "📉 **Dilema de Política:** PIB caindo com juros altos. "
                "Economia sob pressão de política restritiva - BC precisa "
                "balancear crescimento e inflação."
            )
        elif pib_direction == 'Crescente' and selic_direction == 'Decrescente':
            insights.append(
                "🚀 **Estímulo Efetivo:** PIB crescendo com juros baixos. "
                "Política expansionista funcionando, mas atenção à inflação."
            )
        
        return insights
    
    def _compare_cambio_ipca(self, trend_analyses: Dict[str, Dict]) -> List[str]:
        """Compara Câmbio e IPCA"""
        insights = []
        
        cambio_analysis = trend_analyses.get('cambio_dolar', {})
        ipca_analysis = trend_analyses.get('ipca', {})
        
        cambio_change = cambio_analysis.get('change_pct', 0)
        ipca_direction = ipca_analysis.get('direction', 'N/A')
        
        if cambio_change > 15 and ipca_direction == 'Crescente':
            insights.append(
                "🌊 **Pressão Cambial-Inflacionária:** Desvalorização do real "
                "amplificando pressões inflacionárias via importados. "
                "Ciclo de risco para estabilidade de preços."
            )
        elif cambio_change < -10 and ipca_direction == 'Decrescente':
            insights.append(
                "💱 **Alívio Cambial:** Apreciação do real contribuindo para "
                "controle inflacionário através de importados mais baratos."
            )
        
        return insights
    
    def _analyze_general_correlations(self, indicators: List[str], 
                                    trend_analyses: Dict[str, Dict]) -> List[str]:
        """Analisa correlações gerais entre indicadores"""
        insights = []
        
        # Contar direções predominantes
        directions = [trend_analyses.get(ind, {}).get('direction', 'N/A') for ind in indicators]
        direction_counts = {d: directions.count(d) for d in set(directions)}
        
        if direction_counts.get('Crescente', 0) >= len(indicators) * 0.7:
            insights.append(
                "📈 **Movimento Sincronizado Ascendente:** Maioria dos indicadores "
                "em tendência de alta. Possível período de aquecimento econômico geral."
            )
        elif direction_counts.get('Decrescente', 0) >= len(indicators) * 0.7:
            insights.append(
                "📉 **Movimento Sincronizado Descendente:** Maioria dos indicadores "
                "em queda. Possível período de desaceleração econômica ampla."
            )
        elif direction_counts.get('Estável', 0) >= len(indicators) * 0.6:
            insights.append(
                "📊 **Estabilidade Generalizada:** Maioria dos indicadores estável. "
                "Economia em período de consolidação ou transição."
            )
        
        return insights