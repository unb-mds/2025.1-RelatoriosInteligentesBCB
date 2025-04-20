# Arquivo: database_manager.py
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='economic_data.db'):
        """Inicializa o gerenciador de banco de dados SQLite"""
        self.db_path = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        
        # Criar o banco de dados se não existir
        if not os.path.exists(db_name):
            self._create_tables()
            self._optimize_sqlite()
    
    def _create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Indicadores do BCB
        indicators = [
            'ipca',             # Inflação: IPCA
            'pib',              # Atividade Econômica: PIB Real
            'divida_pib',       # Dívida Pública: Relação Dívida/PIB
            'selic',            # Taxa SELIC diária
            'selic_meta',       # Meta da taxa SELIC
            'transacoes',       # Balanço de Pagamentos: Saldo em Transações Correntes
            'resultado_primario' # Indicadores Fiscais: Resultado Primário
        ]
        
        for indicator in indicators:
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {indicator} (
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                value FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Criar índice para a coluna de data
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_{indicator}_date ON {indicator} (date)')
        
        conn.commit()
        conn.close()
    
    def _optimize_sqlite(self):
        """Configura otimizações para o SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Ativar modo WAL (Write-Ahead Logging) para melhorar concorrência
        cursor.execute('PRAGMA journal_mode=WAL')
        
        # Garantir integridade dos dados
        cursor.execute('PRAGMA foreign_keys=ON')
        
        # Otimizar operações para velocidade
        cursor.execute('PRAGMA synchronous=NORMAL')
        
        conn.commit()
        conn.close()
    
    def save_data(self, table_name, df):
        """Salva um DataFrame no banco de dados"""
        if df is None or df.empty:
            print(f"Nenhum dado para salvar na tabela {table_name}")
            return False
        
        # Selecionar apenas as colunas necessárias
        if 'date' in df.columns and 'value' in df.columns:
            df_copy = df[['date', 'value']].copy()
            
            # Verificar por valores duplicados na data (para atualização)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                # Para cada linha, inserir ou atualizar (upsert)
                for _, row in df_copy.iterrows():
                    date_str = row['date'].strftime('%Y-%m-%d') if isinstance(row['date'], datetime) else row['date']
                    value = row['value']
                    
                    # Verificar se já existe um registro para esta data
                    cursor.execute(f"SELECT id FROM {table_name} WHERE date = ?", (date_str,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Atualizar registro existente
                        cursor.execute(f"UPDATE {table_name} SET value = ?, created_at = CURRENT_TIMESTAMP WHERE date = ?", 
                                      (value, date_str))
                    else:
                        # Inserir novo registro
                        cursor.execute(f"INSERT INTO {table_name} (date, value) VALUES (?, ?)", 
                                      (date_str, value))
                
                conn.commit()
                print(f"Dados salvos com sucesso na tabela {table_name}")
                return True
            
            except Exception as e:
                conn.rollback()
                print(f"Erro ao salvar dados na tabela {table_name}: {e}")
                return False
            finally:
                conn.close()
        else:
            print(f"Colunas necessárias não encontradas no DataFrame para a tabela {table_name}")
            return False
    
    def save_all_data(self, data_dict):
        """Salva todos os DataFrames do dicionário em suas respectivas tabelas"""
        results = {}
        
        for table_name, df in data_dict.items():
            success = self.save_data(table_name, df)
            results[table_name] = success
        
        return results
    
    def load_data(self, table_name, start_date=None, end_date=None):
        """
        Carrega dados de uma tabela do banco de dados, com opção de filtrar por período
        
        Args:
            table_name: Nome da tabela
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            DataFrame com os dados
        """
        try:
            query = f"SELECT * FROM {table_name}"
            
            # Adicionar filtros de data se fornecidos
            if start_date and end_date:
                query += f" WHERE date BETWEEN '{start_date}' AND '{end_date}'"
            elif start_date:
                query += f" WHERE date >= '{start_date}'"
            elif end_date:
                query += f" WHERE date <= '{end_date}'"
                
            query += " ORDER BY date"
            
            df = pd.read_sql(query, self.engine)
            
            # Converter a coluna de data para datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                
            return df
        except Exception as e:
            print(f"Erro ao carregar dados da tabela {table_name}: {e}")
            return None
    
    def get_stats(self):
        """Obtém estatísticas sobre o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Obter lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
        
        # Obter contagem de registros por tabela
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            # Obter período de dados
            cursor.execute(f"SELECT MIN(date), MAX(date) FROM {table}")
            min_date, max_date = cursor.fetchone()
            
            stats[table] = {
                'count': count,
                'period': f"{min_date} a {max_date}" if min_date and max_date else "Sem dados"
            }
        
        # Obter tamanho do banco de dados
        if os.path.exists(self.db_path):
            stats['db_size'] = f"{os.path.getsize(self.db_path) / (1024 * 1024):.2f} MB"
        
        conn.close()
        return stats

if __name__ == "__main__":
    # Teste da classe DatabaseManager
    from data_collector import BCBDataCollector
    
    # Coletar dados
    collector = BCBDataCollector()
    data = collector.collect_all_data(last_n_years=5)
    
    # Salvar dados no banco de dados
    db_manager = DatabaseManager()
    results = db_manager.save_all_data(data)
    
    # Verificar estatísticas
    stats = db_manager.get_stats()
    print("\nEstatísticas do banco de dados:")
    for table, table_stats in stats.items():
        if table != 'db_size':
            print(f"  {table.upper()}: {table_stats['count']} registros ({table_stats['period']})")
    print(f"Tamanho do banco de dados: {stats.get('db_size', 'N/A')}")