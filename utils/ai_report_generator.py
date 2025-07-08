# Arquivo: utils/ai_report_generator.py
import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io

class AIReportGenerator:
    def __init__(self):
        """Inicializa o gerador de relatórios com IA"""
        self.report_types = {
            "technical": "📊 Relatório Técnico",
            "parables": "📖 Relatório com Parábolas",
            "simple": "👥 Relatório para Cidadãos"
        }
    
    


    def generate_report_content(self, forecast_data, stats_data, indicator_name, report_type):
        """
        Gera o conteúdo do relatório baseado no tipo selecionado usando DeepSeek API
        
        Args:
            forecast_data: DataFrame com dados de previsão
            stats_data: DataFrame com estatísticas
            indicator_name: Nome do indicador
            report_type: Tipo do relatório ('technical', 'biblical', 'simple')
        """
        
        # Extrair informações dos dados
        data_summary = self._extract_data_summary(forecast_data, stats_data, indicator_name)
        
        # Gerar relatório usando DeepSeek API
        return self.generate_report(data_summary, report_type, indicator_name)
    
    def generate_report(self, data_summary, report_type="technical", indicator_name=""):
        """
        Gera relatório personalizado baseado nos dados usando DeepSeek API
        
        Args:
            data_summary: Resumo dos dados e previsões
            indicator_name: Nome do indicador analisado
            report_type: 'technical', 'biblical', 'simple'
        """
        
        prompts = {
            "technical": self._get_technical_prompt(),
            "parables": self._get_parables_prompt(),
            "simple": self._get_simple_prompt()
        }
        
        base_prompt = prompts.get(report_type, prompts["technical"])
        
        # Construir prompt completo com dados reais
        full_prompt = f"""
        {base_prompt}
        
        DADOS PARA ANÁLISE:
        Indicador: {indicator_name}
        Média Histórica: {data_summary.get('hist_mean', 'N/A')}
        Média Projetada: {data_summary.get('pred_mean', 'N/A')}
        Tendência: {data_summary.get('trend', 'N/A')} {data_summary.get('trend_intensity', '')}
        Variação Percentual: {data_summary.get('variation', 0):+.2f}%
        Períodos de Projeção: {data_summary.get('periods', 'N/A')}
        
        INSTRUÇÕES ESPECÍFICAS:
        - Gere um relatório de EXATAMENTE 15-20 linhas
        - Use os dados fornecidos para criar análises específicas
        - Mantenha o tom adequado ao tipo de relatório escolhido
        - Seja preciso e informativo
        - Inclua implicações práticas dos dados
        
        Gere o relatório agora:
        """
        
        return self._call_ai_api(full_prompt)
    
    def _extract_data_summary(self, forecast_data, stats_data, indicator_name):
        """Extrai informações resumidas dos dados"""
        try:
            # Separar dados históricos e previstos
            historical = forecast_data[forecast_data['tipo'] == 'Histórico']
            predicted = forecast_data[forecast_data['tipo'] == 'Previsto']
            
            # Calcular tendências
            hist_mean = historical['value'].mean() if len(historical) > 0 else 0
            pred_mean = predicted['value'].mean() if len(predicted) > 0 else 0
            
            # Determinar tendência
            if pred_mean > hist_mean * 1.05:
                trend = "crescimento"
                trend_intensity = "significativo" if pred_mean > hist_mean * 1.1 else "moderado"
            elif pred_mean < hist_mean * 0.95:
                trend = "decréscimo"
                trend_intensity = "significativo" if pred_mean < hist_mean * 0.9 else "moderado"
            else:
                trend = "estabilidade"
                trend_intensity = "relativa"
            
            return {
                "indicator": indicator_name,
                "hist_mean": round(hist_mean, 2),
                "pred_mean": round(pred_mean, 2),
                "trend": trend,
                "trend_intensity": trend_intensity,
                "periods": len(predicted),
                "variation": round(((pred_mean - hist_mean) / hist_mean * 100), 2) if hist_mean != 0 else 0
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_technical_prompt(self):
        return """
        Você é um analista econômico sênior do Banco Central. Analise os dados econômicos fornecidos e 
        crie um relatório técnico profissional que:
        
        1. ESTRUTURA: Título, resumo executivo, análise técnica, implicações, perspectivas
        2. LINGUAGEM: Técnica mas acessível, use termos econômicos corretos
        3. ANÁLISE: Interprete tendências, variações percentuais e impactos macroeconômicos
        4. PERSPECTIVAS: Forneça insights sobre possíveis cenários futuros
        5. CONTEXTUALIZAÇÃO: Relacione com políticas monetárias e cenário econômico brasileiro
        
        Formato: 15-20 linhas, profissional, baseado nos dados reais fornecidos.
        """
    
    def _get_parables_prompt(self):
        return """
        Você é um contador de histórias sábio que explica economia usando parábolas e analogias simples.
        Analise os dados econômicos e crie um relatório que:
        
        1. USE PARÁBOLAS: Relacione tendências econômicas com histórias e fábulas conhecidas 
        (a cigarra e a formiga, a galinha dos ovos de ouro, etc.)
        2. SABEDORIA POPULAR: Use provérbios e ditados populares sobre administração e prudência
        3. LINGUAGEM NARRATIVA: Tom envolvente, educativo e inspirador
        4. INTERPRETAÇÃO: Traduza números em lições práticas através de histórias
        5. OTIMISMO: Mantenha perspectiva positiva e esperançosa sobre o futuro
        
        Formato: 15-20 linhas, envolvente, usando dados reais com analogias e parábolas apropriadas.
        """
    
    def _get_simple_prompt(self):
        return """
        Você é um educador popular que explica economia para pessoas comuns sem formação técnica.
        Analise os dados e crie um relatório MUITO SIMPLES que:
        
        1. LINGUAGEM COTIDIANA: Use palavras do dia a dia, evite jargões técnicos
        2. EXEMPLOS PRÁTICOS: Compare com situações familiares (supermercado, salário, casa)
        3. IMPACTO PESSOAL: Explique como afeta a vida da pessoa comum
        4. DICAS PRÁTICAS: Forneça conselhos úteis para o orçamento familiar
        5. CLAREZA TOTAL: Como se estivesse explicando para um amigo ou familiar
        
        Substitua termos técnicos:
        - IPCA = "aumento de preços no mercado"
        - SELIC = "juros básicos do país" 
        - PIB = "riqueza produzida pelo Brasil"
        - Câmbio = "preço do dólar"
        
        Formato: 15-20 linhas, linguagem popular, baseado nos dados reais fornecidos.
        """
    
    def _call_ai_api(self, prompt):
        """
        Chama a API do DeepSeek para gerar relatório real
        """
        try:
            # API DeepSeek
            api_url = "https://api.deepseek.com/v1/chat/completions"
            
            # Configuração da API Key (você precisará configurar)
            api_key = st.secrets.get("DEEPSEEK_API_KEY", "sua-api-key-aqui")
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é um especialista em análise econômica que gera relatórios claros e precisos."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # Fazer requisição para DeepSeek
            response = requests.post(api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                st.error(f"Erro na API DeepSeek: {response.status_code}")
                return self._fallback_report()
                
        except Exception as e:
            st.error(f"Erro ao conectar com DeepSeek: {e}")
            return self._fallback_report()
    
    def _fallback_report(self):
        """Relatório de fallback quando API não funciona"""
        return f"""
        RELATÓRIO GERADO LOCALMENTE
        (API DeepSeek indisponível)
        
        Com base nos dados analisados, observamos tendências importantes 
        no indicador selecionado. As projeções sugerem mudanças significativas 
        no período futuro.
        
        Para ativar relatórios com IA, configure a API Key do DeepSeek.
        
        Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
    
    def generate_pdf_report(self, report_content, report_type, indicator_name):
        """Gera PDF do relatório com formatação profissional"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import io
            from datetime import datetime
            
            # Criar buffer em memória
            buffer = io.BytesIO()
            
            # Criar documento
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
            
            # Estilos
            styles = getSampleStyleSheet()
            
            # Estilo para título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1,  # Center
                textColor='black'
            )
            
            # Estilo para subtítulos
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12,
                textColor='black'
            )
            
            # Estilo para texto normal justificado
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                alignment=4,  # Justify
                firstLineIndent=20,
                textColor='black'
            )
            
            # Estilo para informações
            info_style = ParagraphStyle(
                'CustomInfo',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6,
                textColor='grey'
            )
            
            # Conteúdo do PDF
            story = []
            
            # Título principal
            titles = {
                "technical": "Relatório Técnico de Análise Econômica",
                "parables": "Relatório com Parábolas Econômicas", 
                "simple": "Relatório Econômico para Cidadãos"
            }
            
            title = titles.get(report_type, "Relatório de Análise IA")
            story.append(Paragraph(title, title_style))
            
            # Informações do relatório
            story.append(Paragraph(f"<b>Indicador:</b> {indicator_name}", info_style))
            story.append(Paragraph(f"<b>Data de Geração:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}", info_style))
            story.append(Spacer(1, 20))
            
            # Processar conteúdo
            lines = report_content.split('\n')
            current_paragraph = ""
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    # Linha vazia - finalizar parágrafo atual
                    if current_paragraph:
                        story.append(Paragraph(current_paragraph, normal_style))
                        current_paragraph = ""
                    story.append(Spacer(1, 6))
                    continue
                
                # Verificar se é título/subtítulo
                if (line.startswith('**') and line.endswith('**')) or line.isupper() or line.endswith(':'):
                    # Finalizar parágrafo anterior
                    if current_paragraph:
                        story.append(Paragraph(current_paragraph, normal_style))
                        current_paragraph = ""
                    
                    # Adicionar título
                    clean_title = line.replace('**', '').strip()
                    story.append(Paragraph(f"<b>{clean_title}</b>", subtitle_style))
                else:
                    # Adicionar à parágrafo atual
                    if current_paragraph:
                        current_paragraph += " " + line
                    else:
                        current_paragraph = line
            
            # Adicionar último parágrafo
            if current_paragraph:
                story.append(Paragraph(current_paragraph, normal_style))
            
            # Gerar PDF
            doc.build(story)
            
            # Retornar bytes
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return pdf_data
            
        except ImportError:
            # Fallback para FPDF se reportlab não estiver disponível
            return self._generate_simple_pdf(report_content, report_type, indicator_name)
            
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
            return None

    def _generate_simple_pdf(self, report_content, report_type, indicator_name):
        """PDF simples com FPDF como fallback"""
        try:
            from fpdf import FPDF
            from datetime import datetime
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            
            # Título simples
            titles = {
                "technical": "Relatorio Tecnico",
                "parables": "Relatorio com Parabolas", 
                "simple": "Relatorio para Cidadaos"
            }
            
            title = titles.get(report_type, "Relatorio IA")
            pdf.cell(0, 10, title, ln=True, align='C')
            pdf.ln(5)
            
            # Informações
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, f"Indicador: {indicator_name.encode('ascii', 'ignore').decode()}", ln=True)
            pdf.cell(0, 6, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
            pdf.ln(5)
            
            # Conteúdo
            pdf.set_font('Arial', '', 11)
            
            # Processar linha por linha
            for line in report_content.split('\n'):
                line = line.strip()
                if line:
                    # Remover caracteres problemáticos
                    clean_line = line.encode('ascii', 'ignore').decode()
                    clean_line = clean_line.replace('**', '')
                    
                    # Quebrar linha se muito longa
                    while len(clean_line) > 80:
                        break_point = clean_line[:80].rfind(' ')
                        if break_point == -1:
                            break_point = 80
                        
                        pdf.cell(0, 5, clean_line[:break_point], ln=True)
                        clean_line = clean_line[break_point:].strip()
                    
                    if clean_line:
                        pdf.cell(0, 5, clean_line, ln=True)
                else:
                    pdf.ln(3)
            
            return bytes(pdf.output(dest='S'))
            
        except Exception as e:
            st.error(f"Erro no PDF fallback: {e}")
            return None