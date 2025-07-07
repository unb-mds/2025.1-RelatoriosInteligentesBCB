import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io
import plotly.io as pio
import os

def generate_downloadable_report(interpretative_text: str, forecast_df: pd.DataFrame, metrics_df: pd.DataFrame, fig_plot):
    
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Título do Relatório
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatório de Previsão Econômica", 0, 1, 'C')
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, 'C')
    pdf.ln(10)

    # 2. Texto Interpretativo
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, interpretative_text)
    pdf.ln(10)

    # 3. Gráfico da Previsão
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Gráfico da Previsão", 0, 1)
    
    temp_image_path = "temp_chart.png"
    pio.write_image(fig_plot, temp_image_path)
    pdf.image(temp_image_path, x=10, w=pdf.w - 20)
    os.remove(temp_image_path) # Reativando a remoção do arquivo
    pdf.ln(20)

    # 4. Tabela de Métricas
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Métricas de Avaliação", 0, 1)
    
    pdf.set_font("Arial", 'B', 10)
    col_width = pdf.w / 3 
    
    for header in metrics_df.columns:
        pdf.cell(col_width, 10, header, 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for index, row in metrics_df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, str(round(item, 4)), 1, 0, 'C')
        pdf.ln()

    return bytes(pdf.output())
