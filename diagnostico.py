# Crie um novo arquivo chamado diagnostico.py
import pandas as pd
from database_manager import DatabaseManager

def verificar_banco():
    db = DatabaseManager()
    stats = db.get_stats()
    
    print("\n=== DIAGNÓSTICO DO BANCO DE DADOS ===")
    for table, info in stats.items():
        if table != 'db_size':
            print(f"\nTabela: {table}")
            print(f"Registros: {info['count']}")
            print(f"Período: {info['period']}")
            
            # Verificar primeiros registros
            dados = db.load_data(table)
            if dados is not None and not dados.empty:
                print("\nPrimeiros registros:")
                print(dados.head(3))
                
                # Verificar valores únicos por mês (para ver se há duplicatas)
                dados['mes'] = dados['date'].dt.to_period('M')
                contagem_por_mes = dados.groupby('mes').size()
                print(f"\nNúmero de registros por mês (primeiros 5 meses):")
                print(contagem_por_mes.head())
            else:
                print("Não foi possível carregar dados desta tabela.")
    
    print(f"\nTamanho do banco: {stats.get('db_size', 'N/A')}")
    print("\n======================================")

if __name__ == "__main__":
    verificar_banco()