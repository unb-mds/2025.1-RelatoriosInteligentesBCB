#!/usr/bin/env python3
"""
Script para executar o Dashboard Econômico

Uso:
    python run_economic_dashboard.py

Ou para executar diretamente com Streamlit:
    streamlit run ml_core/interpreter/dashboard.py
"""

import os
import sys
import subprocess

def main():
    """Função principal para executar o dashboard"""
    
    print("🚀 === DASHBOARD ECONÔMICO ===")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('ml_core/interpreter/dashboard.py'):
        print("❌ Arquivo dashboard.py não encontrado!")
        print("💡 Certifique-se de estar no diretório raiz do projeto")
        print(f"📁 Diretório atual: {os.getcwd()}")
        print("\n🔍 Arquivos disponíveis no ml_core/interpreter/:")
        if os.path.exists('ml_core/interpreter/'):
            files = os.listdir('ml_core/interpreter/')
            for file in files:
                print(f"   - {file}")
        return
    
    # Testar imports básicos
    print("🔄 Verificando dependências...")
    
    try:
        import streamlit
        print("✅ Streamlit OK")
    except ImportError:
        print("❌ Streamlit não encontrado!")
        print("💡 Instale com: pip install streamlit")
        return
    
    try:
        import plotly
        print("✅ Plotly OK")
    except ImportError:
        print("❌ Plotly não encontrado!")
        print("💡 Instale com: pip install plotly")
        return
    
    try:
        from database_manager import DatabaseManager
        print("✅ Database Manager OK")
    except ImportError:
        print("❌ Database Manager não encontrado!")
        return
    
    try:
        from ml_core.interpreter.economic_analyzer import EconomicAnalyzer
        print("✅ Economic Analyzer OK")
    except ImportError as e:
        print(f"❌ Economic Analyzer: {e}")
        return
    
    # Verificar se há dados disponíveis
    try:
        db = DatabaseManager()
        stats = db.get_stats()
        available_indicators = [k for k in stats.keys() if k != 'db_size']
        
        if available_indicators:
            print(f"✅ Dados encontrados: {len(available_indicators)} indicadores")
            print(f"📊 Indicadores: {', '.join(available_indicators[:3])}{'...' if len(available_indicators) > 3 else ''}")
        else:
            print("⚠️ Nenhum indicador encontrado no banco de dados")
            print("💡 Execute a coleta de dados primeiro:")
            print("   python -c \"from data_collector import BCBDataCollector; from database_manager import DatabaseManager; collector = BCBDataCollector(); data = collector.collect_all_data(last_n_years=3); db = DatabaseManager(); db.save_all_data(data)\"")
    except Exception as e:
        print(f"⚠️ Erro ao verificar dados: {e}")
    
    print("\n🎯 Iniciando Dashboard Econômico...")
    print("📱 O dashboard abrirá automaticamente no seu navegador")
    print("🔗 URL padrão: http://localhost:8501")
    print("\n⏹️  Para parar o dashboard, use Ctrl+C")
    print("=" * 50)
    
    # Executar o dashboard
    try:
        cmd = [sys.executable, '-m', 'streamlit', 'run', 'ml_core/interpreter/dashboard.py']
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar dashboard: {e}")
        print("\n💡 Tente executar manualmente:")
        print("   streamlit run ml_core/interpreter/dashboard.py")

if __name__ == "__main__":
    main()