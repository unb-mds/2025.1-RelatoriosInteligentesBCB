# ml_core/interpreter/__init__.py

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='streamlit')

# Variáveis de status dos componentes
STREAMLIT_AVAILABLE = False
ECONOMIC_ANALYZER_AVAILABLE = False
DATA_HANDLER_AVAILABLE = False
PREDICTION_ENGINE_AVAILABLE = False
TREND_ANALYZER_AVAILABLE = False
VISUALIZATION_AVAILABLE = False

# Variável global para o interpreter
interpreter = None

try:
    # 1. Importar configurações principais
    print("🔄 Carregando configurações...")
    from .config import INTERPRETER_CONFIG
    print("✅ Configurações carregadas")
    
    # 2. Verificar Streamlit
    try:
        import streamlit as st
        STREAMLIT_AVAILABLE = True
        print("✅ Streamlit disponível")
    except ImportError:
        STREAMLIT_AVAILABLE = False
        print("⚠️ Streamlit não disponível")
    
    # 3. Importar componentes individuais com tratamento de erro
    try:
        from .economic_analyzer import EconomicAnalyzer, quick_economic_analysis
        ECONOMIC_ANALYZER_AVAILABLE = True
        print("✅ Economic Analyzer disponível")
    except Exception as e:
        ECONOMIC_ANALYZER_AVAILABLE = False
        print(f"⚠️ Economic Analyzer não disponível: {e}")
    
    try:
        from .data_handler import DataHandler
        DATA_HANDLER_AVAILABLE = True
        print("✅ Data Handler disponível")
    except Exception as e:
        DATA_HANDLER_AVAILABLE = False
        print(f"⚠️ Data Handler não disponível: {e}")
    
    try:
        from .prediction_engine import PredictionEngine
        PREDICTION_ENGINE_AVAILABLE = True
        print("✅ Prediction Engine disponível")
    except Exception as e:
        PREDICTION_ENGINE_AVAILABLE = False
        print(f"⚠️ Prediction Engine não disponível: {e}")
    
    try:
        from .trend_analysis import TrendAnalyzer
        TREND_ANALYZER_AVAILABLE = True
        print("✅ Trend Analyzer disponível")
    except Exception as e:
        TREND_ANALYZER_AVAILABLE = False
        print(f"⚠️ Trend Analyzer não disponível: {e}")
    
    try:
        from .visualization import VisualizationEngine
        VISUALIZATION_AVAILABLE = True
        print("✅ Visualization Engine disponível")
    except Exception as e:
        VISUALIZATION_AVAILABLE = False
        print(f"⚠️ Visualization Engine não disponível: {e}")
    
    # 4. Criar classe MLInterpreter
    class MLInterpreter:
        """
        Classe principal do ML Interpreter com funcionalidades econômicas avançadas
        """
        
        def __init__(self):
            # Configuração principal
            self.config = INTERPRETER_CONFIG if INTERPRETER_CONFIG else {}
            
            # Inicializar componentes
            self.economic_analyzer = None
            self.data_handler = None
            self.prediction_engine = None
            self.trend_analyzer = None
            self.visualization_engine = None
            
            # Inicializar componentes disponíveis
            self._initialize_components()
        
        def _initialize_components(self):
            """Inicializa os componentes disponíveis com tratamento de erro"""
            
            if ECONOMIC_ANALYZER_AVAILABLE:
                try:
                    self.economic_analyzer = EconomicAnalyzer()
                except Exception as e:
                    print(f"⚠️ Erro ao inicializar Economic Analyzer: {e}")
            
            if DATA_HANDLER_AVAILABLE:
                try:
                    self.data_handler = DataHandler()
                except Exception as e:
                    print(f"⚠️ Erro ao inicializar Data Handler: {e}")
            
            if PREDICTION_ENGINE_AVAILABLE:
                try:
                    self.prediction_engine = PredictionEngine()
                except Exception as e:
                    print(f"⚠️ Erro ao inicializar Prediction Engine: {e}")
            
            if TREND_ANALYZER_AVAILABLE:
                try:
                    self.trend_analyzer = TrendAnalyzer()
                except Exception as e:
                    print(f"⚠️ Erro ao inicializar Trend Analyzer: {e}")
            
            if VISUALIZATION_AVAILABLE:
                try:
                    self.visualization_engine = VisualizationEngine()
                except Exception as e:
                    print(f"⚠️ Erro ao inicializar Visualization Engine: {e}")
        
        def analyze_indicators(self, indicators, period_months=12):
            """
            Análise completa de indicadores econômicos
            """
            if not self.economic_analyzer:
                print("❌ Economic Analyzer não disponível")
                return None
            
            try:
                return quick_economic_analysis(indicators, period_months)
            except Exception as e:
                print(f"❌ Erro na análise de indicadores: {e}")
                return None
        
        def generate_correlation_matrix(self, indicators, period_months=12):
            """Gera matriz de correlação entre indicadores"""
            if not self.economic_analyzer:
                print("❌ Economic Analyzer não disponível")
                return None
            
            try:
                self.economic_analyzer.load_indicators(indicators)
                return self.economic_analyzer.calculate_correlation_matrix(period_months)
            except Exception as e:
                print(f"❌ Erro na matriz de correlação: {e}")
                return None
        
        def generate_forecast(self, indicator, periods=6):
            """Gera previsão para um indicador específico"""
            if not self.economic_analyzer:
                print("❌ Economic Analyzer não disponível")
                return None
            
            try:
                forecasts = self.economic_analyzer.generate_forecast_comparison([indicator], periods)
                return forecasts.get(indicator)
            except Exception as e:
                print(f"❌ Erro na previsão: {e}")
                return None
        
        def generate_ai_report(self, indicators):
            """Gera relatório de análise com IA"""
            if not self.economic_analyzer:
                print("❌ Economic Analyzer não disponível")
                return None
            
            try:
                self.economic_analyzer.load_indicators(indicators)
                return self.economic_analyzer.generate_ai_analysis_report(indicators)
            except Exception as e:
                print(f"❌ Erro no relatório IA: {e}")
                return None
        
        def run_dashboard(self):
            """Executa o dashboard web (se Streamlit disponível)"""
            if not STREAMLIT_AVAILABLE:
                print("❌ Streamlit não disponível. Instale com: pip install streamlit")
                return False
            
            try:
                print("🚀 Para iniciar o dashboard execute:")
                print("   streamlit run ml_core/interpreter/dashboard.py")
                return True
            except Exception as e:
                print(f"❌ Erro ao preparar dashboard: {e}")
                return False
        
        def get_status(self):
            """Retorna status dos componentes"""
            return {
                'economic_analyzer': ECONOMIC_ANALYZER_AVAILABLE,
                'data_handler': DATA_HANDLER_AVAILABLE,
                'prediction_engine': PREDICTION_ENGINE_AVAILABLE,
                'trend_analyzer': TREND_ANALYZER_AVAILABLE,
                'visualization': VISUALIZATION_AVAILABLE,
                'streamlit': STREAMLIT_AVAILABLE,
                'interpreter_initialized': True
            }
    
    # 5. Criar instância do interpreter
    print("🔄 Inicializando ML Interpreter...")
    interpreter = MLInterpreter()
    print("✅ ML Interpreter inicializado com sucesso")
    
    # 6. Função de conveniência para análise rápida
    def analyze_economic_scenario(indicators, period_months=12):
        """
        Função de conveniência para análise rápida de cenário econômico
        """
        if ECONOMIC_ANALYZER_AVAILABLE:
            try:
                return quick_economic_analysis(indicators, period_months)
            except Exception as e:
                print(f"❌ Erro na análise econômica: {e}")
                return None
        else:
            print("❌ Economic Analyzer não disponível")
            return None
    
    # 7. Exportar componentes principais
    __all__ = [
        'MLInterpreter',
        'interpreter', 
        'analyze_economic_scenario'
    ]
    
    # Adicionar componentes opcionais se disponíveis
    if ECONOMIC_ANALYZER_AVAILABLE:
        __all__.extend(['EconomicAnalyzer', 'quick_economic_analysis'])
    
    if DATA_HANDLER_AVAILABLE:
        __all__.append('DataHandler')
    
    if PREDICTION_ENGINE_AVAILABLE:
        __all__.append('PredictionEngine')
    
    print("✅ ML Interpreter - Versão Modular carregada com sucesso")

except Exception as e:
    print(f"❌ Erro crítico no ML Interpreter: {e}")
    
    # Importar traceback para debug
    import traceback
    print("🔍 Stack trace completo:")
    traceback.print_exc()
    
    # Versão fallback simples
    try:
        from .config import INTERPRETER_CONFIG
        
        class SimpleFallbackInterpreter:
            """Versão simplificada como fallback"""
            
            def __init__(self):
                self.config = INTERPRETER_CONFIG if INTERPRETER_CONFIG else {}
            
            def analyze_indicators(self, indicators, period_months=12):
                print("⚠️ Funcionalidade limitada - versão fallback")
                return None
            
            def get_status(self):
                return {
                    'fallback_mode': True,
                    'error': 'Versão fallback ativa'
                }
        
        interpreter = SimpleFallbackInterpreter()
        print("⚠️ ML Interpreter - Usando versão de fallback")
        
        __all__ = ['interpreter']
        
    except Exception as fallback_error:
        print(f"❌ Erro crítico também no fallback: {fallback_error}")
        interpreter = None
        __all__ = []

# Garantir que interpreter nunca seja None
if interpreter is None:
    class EmptyInterpreter:
        def get_status(self):
            return {'error': 'Interpreter não inicializado'}
        
        def analyze_indicators(self, *args, **kwargs):
            return None
    
    interpreter = EmptyInterpreter()
    print("🛡️ Interpreter de emergência ativado")