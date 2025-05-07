# Arquivo: ml_models.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from database_manager import DatabaseManager
import joblib
import os

class EconomicPredictor:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.models = {}
        self.scalers = {}
        self.model_dir = 'models'
        
        # Criar diretório para salvar modelos
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    
    
    def prepare_data(self, target_indicator, window_size=3):
        """
        Prepara os dados para previsão de séries temporais
        
        Args:
            target_indicator: Nome do indicador alvo para prever ('ipca', 'selic', etc.)
            window_size: Tamanho da janela para features de lag
            
        Returns:
            X: Features
            y: Target values
            dates: Datas correspondentes
        """
        # Carregar dados do alvo
        target_data = self.db_manager.load_data(target_indicator)
        
        if target_data is None or target_data.empty:
            print(f"Dados insuficientes para o indicador {target_indicator}")
            return None, None, None
        
        print(f"Carregados {len(target_data)} registros para {target_indicator}")
        
        # Garantir que as datas estão em ordem cronológica
        target_data = target_data.sort_values('date')
        
        # Criar features de lag para o próprio indicador
        df = target_data.copy()
        for i in range(1, window_size + 1):
            df[f'{target_indicator}_lag_{i}'] = df['value'].shift(i)
        
        # Lista de indicadores com dados
        available_indicators = []
        
        # Verifique quais indicadores têm dados disponíveis
        for indicator in ['ipca', 'pib', 'divida_pib', 'selic_meta', 'transacoes']:
            if indicator != target_indicator:
                ind_data = self.db_manager.load_data(indicator)
                if ind_data is not None and len(ind_data) > 0:
                    available_indicators.append(indicator)
        
        print(f"Indicadores disponíveis: {available_indicators}")
        
        # Adicionar outros indicadores disponíveis
        for indicator in available_indicators:
            # Carregar dados
            ind_data = self.db_manager.load_data(indicator)
            
            # Sincronizar por data
            ind_data = ind_data.sort_values('date')
            ind_data = ind_data.set_index('date')
            
            # Juntar com o dataframe principal
            df = df.set_index('date')
            df[indicator] = ind_data['value']
            df = df.reset_index()
            
            # Criar lag para este indicador
            df[f'{indicator}_lag_1'] = df[indicator].shift(1)
        
        # Preencher valores NaN
        print(f"Antes de preencher NaN: {df.shape[0]} registros, {df.isna().sum().sum()} valores NaN")
        df = df.fillna(method='ffill').fillna(method='bfill')
        print(f"Após preencher NaN: {df.shape[0]} registros, {df.isna().sum().sum()} valores NaN")
        
        # Remover linhas iniciais (devido aos lags)
        df = df.iloc[window_size:].reset_index(drop=True)
        
        # Remover quaisquer linhas restantes com NaN
        df = df.dropna()
        
        if df.empty:
            print("Após remover valores NaN, não restaram dados suficientes")
            return None, None, None
        
        print(f"Dados finais: {df.shape[0]} registros")
        
        # Separar features e target
        y = df['value']
        dates = df['date']
        
        # Remover colunas que não são features
        X = df.drop(['value', 'date', 'id', 'created_at'], axis=1, errors='ignore')
        
        return X, y, dates





    
    def train_model(self, target_indicator, model_type='random_forest', test_size=0.2):
        """
        Treina um modelo para prever o indicador alvo
        
        Args:
            target_indicator: Nome do indicador alvo ('ipca', 'selic', etc.)
            model_type: Tipo de modelo ('linear', 'ridge', 'lasso', 'random_forest')
            test_size: Proporção dos dados para teste
            
        Returns:
            Dict com métricas de avaliação
        """
        # Preparar dados
        X, y, dates = self.prepare_data(target_indicator)


    def train_model(self, target_indicator, model_type='random_forest', test_size=0.2):
        """
        Treina um modelo para prever o indicador alvo
        
        Args:
            target_indicator: Nome do indicador alvo ('ipca', 'selic', etc.)
            model_type: Tipo de modelo ('linear', 'ridge', 'lasso', 'random_forest')
            test_size: Proporção dos dados para teste
            
        Returns:
            Dict com métricas de avaliação
        """
        # Preparar dados
        print(f"Tentando preparar dados para {target_indicator}...")
        X, y, dates = self.prepare_data(target_indicator)
        
        # Adicione estas linhas para debug:
        if X is None:
            print("X é None - falha ao preparar dados")
            return None
        
        print(f"Dados preparados com sucesso: {X.shape[0]} registros com {X.shape[1]} features")
        print(f"Primeiras features: {list(X.columns)[:5]}")
        print(f"Intervalo de datas: {dates.min()} a {dates.max()}")
    
    # Continue com o restante da função...

        





        
        if X is None:
            print("Falha ao preparar os dados")
            return None
        
        # Dividir em treino e teste (respeitando a ordem temporal)
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        dates_test = dates.iloc[split_idx:]
        
        # Escalar os dados
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Salvar o scaler
        self.scalers[target_indicator] = scaler
        
        # Selecionar e treinar o modelo
        if model_type == 'linear':
            model = LinearRegression()
        elif model_type == 'ridge':
            model = Ridge(alpha=1.0)
        elif model_type == 'lasso':
            model = Lasso(alpha=0.1)
        else:  # default: random_forest
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Treinar o modelo
        model.fit(X_train_scaled, y_train)
        
        # Salvar o modelo treinado
        self.models[target_indicator] = model
        
        # Fazer previsões
        y_pred = model.predict(X_test_scaled)
        
        # Calcular métricas
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        
        # Criar gráfico de comparação
        plt.figure(figsize=(12, 6))
        plt.plot(dates_test, y_test, label='Valor Real')
        plt.plot(dates_test, y_pred, label='Previsão', linestyle='--')
        plt.title(f'Previsão vs Real - {target_indicator.upper()}')
        plt.xlabel('Data')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True)
        
        # Salvar o gráfico
        plt.savefig(f"{self.model_dir}/{target_indicator}_prediction.png")
        
        # Salvar o modelo em disco
        joblib.dump(model, f"{self.model_dir}/{target_indicator}_{model_type}_model.pkl")
        joblib.dump(scaler, f"{self.model_dir}/{target_indicator}_scaler.pkl")
        
        return metrics
    
    def predict_future(self, target_indicator, steps=6):
        """
        Faz previsões para períodos futuros
        
        Args:
            target_indicator: Nome do indicador alvo ('ipca', 'selic', etc.)
            steps: Número de períodos futuros para prever
            
        Returns:
            DataFrame com as previsões
        """
        if target_indicator not in self.models:
            # Tentar carregar o modelo do disco
            model_path = f"{self.model_dir}/{target_indicator}_random_forest_model.pkl"
            scaler_path = f"{self.model_dir}/{target_indicator}_scaler.pkl"
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.models[target_indicator] = joblib.load(model_path)
                self.scalers[target_indicator] = joblib.load(scaler_path)
            else:
                print(f"Modelo para {target_indicator} não encontrado. Treine o modelo primeiro.")
                return None
        
        # Carregar os dados mais recentes
        X, y, dates = self.prepare_data(target_indicator)
        
        if X is None:
            return None
        
        # Obter o modelo e scaler
        model = self.models[target_indicator]
        scaler = self.scalers[target_indicator]
        
        # Usar os dados mais recentes para previsão
        latest_data = X.iloc[-1:].copy()
        
        predictions = []
        last_date = dates.iloc[-1]
        prediction_dates = pd.date_range(start=last_date, periods=steps+1, freq='M')[1:]
        
        for i in range(steps):
            # Escalar os dados
            input_data = scaler.transform(latest_data)
            
            # Fazer previsão
            pred = model.predict(input_data)[0]
            predictions.append(pred)
            
            # Atualizar os dados para a próxima previsão
            # Isso é uma simplificação, um modelo real precisaria de uma lógica mais sofisticada
            for col in latest_data.columns:
                if '_lag_' in col:
                    indicator_name = col.split('_lag_')[0]
                    lag_num = int(col.split('_lag_')[1])
                    
                    if lag_num > 1:
                        prev_lag_col = f"{indicator_name}_lag_{lag_num-1}"
                        if prev_lag_col in latest_data.columns:
                            latest_data[col] = latest_data[prev_lag_col].values
                    else:
                        if indicator_name == target_indicator:
                            latest_data[col] = pred
            
        # Criar DataFrame de resultados
        future_df = pd.DataFrame({
            'date': prediction_dates,
            'value': predictions
        })
        
        return future_df
    
    def get_feature_importance(self, target_indicator):
        """
        Obtém a importância das features para modelos que suportam
        
        Args:
            target_indicator: Nome do indicador
            
        Returns:
            DataFrame com importância das features
        """
        if target_indicator not in self.models:
            print(f"Modelo para {target_indicator} não encontrado")
            return None
        
        model = self.models[target_indicator]
        
        # Verificar se o modelo suporta feature importance
        if hasattr(model, 'feature_importances_'):
            # Preparar dados para obter nomes das features
            X, _, _ = self.prepare_data(target_indicator)
            
            if X is None:
                return None
            
            # Criar DataFrame
            importance = pd.DataFrame({
                'feature': X.columns,
                'importance': model.feature_importances_
            })
            
            # Ordenar
            importance = importance.sort_values('importance', ascending=False)
            
            return importance
        elif hasattr(model, 'coef_'):
            # Para modelos lineares
            X, _, _ = self.prepare_data(target_indicator)
            
            if X is None:
                return None
            
            # Criar DataFrame
            importance = pd.DataFrame({
                'feature': X.columns,
                'coefficient': model.coef_
            })
            
            # Ordenar por valor absoluto
            importance['abs_coefficient'] = np.abs(importance['coefficient'])
            importance = importance.sort_values('abs_coefficient', ascending=False)
            
            return importance
        else:
            print(f"O modelo não suporta feature importance")
            return None

if __name__ == "__main__":
    # Testar a classe
    predictor = EconomicPredictor()
    
    # Treinar modelos para alguns indicadores
    indicators = ['ipca', 'selic']
    model_types = ['random_forest']
    
    for indicator in indicators:
        for model_type in model_types:
            print(f"Treinando modelo {model_type} para {indicator}...")
            metrics = predictor.train_model(indicator, model_type)
            
            if metrics:
                print(f"Métricas para {indicator} com modelo {model_type}:")
                for metric_name, metric_value in metrics.items():
                    print(f"  {metric_name}: {metric_value:.4f}")
                
                # Fazer previsão
                print(f"\nPrevisão para os próximos 6 meses:")
                future = predictor.predict_future(indicator, steps=6)
                
                if future is not None:
                    print(future)
                
                # Importância das features (para Random Forest)
                if model_type == 'random_forest':
                    importance = predictor.get_feature_importance(indicator)
                    
                    if importance is not None:
                        print("\nImportância das features:")
                        print(importance.head(10))    