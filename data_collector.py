# Arquivo: data_collector.py
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

class BCBDataCollector:
    def __init__(self):
        self.base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
        
        # Mapeamento de indicadores e suas séries
        self.indicators = {
            'ipca': 433,          # Inflação: IPCA
            'pib': 4380,          # Atividade Econômica: PIB Real
            'divida_pib': 13761,  # Dívida Pública: Relação Dívida/PIB
            'selic': 11,          # Taxa SELIC diária
            'selic_meta': 4189,   # Meta da taxa SELIC
            'transacoes': 22707,  # Balanço de Pagamentos: Saldo em Transações Correntes
            'resultado_primario': 7547  # Indicadores Fiscais: Resultado Primário
        }
    
    def get_data(self, indicator, start_date=None, end_date=None):
        """
        Obter dados de um indicador específico
        
        Args:
            indicator: Nome do indicador (chave do dicionário self.indicators)
            start_date: Data inicial (formato 'DD/MM/AAAA', opcional)
            end_date: Data final (formato 'DD/MM/AAAA', opcional)
        
        Returns:
            DataFrame com os dados do indicador
        """
        if indicator not in self.indicators:
            print(f"Indicador '{indicator}' não reconhecido")
            return None
        
        # Construir URL
        serie_id = self.indicators[indicator]
        url = f"{self.base_url}.{serie_id}/dados?formato=json"
        
        # Adicionar parâmetros de data, se fornecidos
        if start_date:
            url += f"&dataInicial={start_date}"
        if end_date:
            url += f"&dataFinal={end_date}"
        
        try:
            # Fazer requisição à API
            response = requests.get(url)
            response.raise_for_status()
            
            # Converter resposta para JSON
            data = response.json()
            
            if data:
                # Converter para DataFrame
                df = pd.DataFrame(data)
                
                # Renomear colunas para padrão
                df.rename(columns={
                    'data': 'date',
                    'valor': 'value'
                }, inplace=True)
                
                # Converter data para datetime
                df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
                
                # Adicionar coluna com nome do indicador
                df['indicator'] = indicator
                
                return df
            else:
                print(f"Nenhum dado retornado para o indicador '{indicator}'")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API para o indicador '{indicator}': {e}")
            return None
    
    def collect_all_data(self, last_n_years=5):
        """
        Coletar dados de todos os indicadores
        
        Args:
            last_n_years: Número de anos retroativos para coletar dados
        
        Returns:
            Dict com DataFrames para cada indicador
        """
        # Calcular datas
        end_date = datetime.now().strftime('%d/%m/%Y')
        start_date = (datetime.now() - timedelta(days=365 * last_n_years)).strftime('%d/%m/%Y')
        
        results = {}
        
        # Coletar dados para cada indicador
        for indicator in self.indicators.keys():
            print(f"Coletando dados para {indicator}...")
            try:
                df = self.get_data(indicator, start_date, end_date)
                
                if df is not None and not df.empty:
                    print(f"Coletados {len(df)} registros para {indicator}")
                    results[indicator] = df
                else:
                    print(f"Nenhum dado retornado para {indicator}")
            except Exception as e:
                print(f"Erro ao coletar dados para {indicator}: {e}")
        
        return results




if __name__ == "__main__":
    # Teste da classe
    collector = BCBDataCollector()
    
    # Coletar dados dos últimos 5 anos
    data = collector.collect_all_data(last_n_years=5)
    
    # Verificar dados coletados
    for indicator, df in data.items():
        if df is not None:
            print(f"\nDados de {indicator}:")
            print(f"Período: {df['date'].min().strftime('%d/%m/%Y')} a {df['date'].max().strftime('%d/%m/%Y')}")
            print(f"Registros: {len(df)}")
            print(f"Primeiros registros:")
            print(df.head(3))