# Resumo dos Arquivos do Projeto IPEA

Este documento resume as funções e responsabilidades dos principais arquivos do sistema de análise e previsão de indicadores econômicos do IPEA.
### 📄 `data_collector.py`
**Responsável pela coleta de dados econômicos via API do Banco Central.**
- Contém a classe `BCBDataCollector`, que encapsula a lógica de conexão com as APIs do BCB.
- Possui métodos específicos para coletar séries temporais como IPCA, PIB, Selic, etc.
- Realiza tratamento de erros HTTP e formata os dados para uso padronizado.
- Utiliza `requests` para requisições e `pandas` para manipulação de dados.

### 📄 `database_manager.py`
**Gerencia o armazenamento dos dados coletados em um banco SQLite.**
- Contém a classe `DatabaseManager`, que abstrai operações com banco de dados.
- Cria automaticamente tabelas para cada indicador, com suporte a índices.
- Salva, atualiza e consulta dados de forma eficiente usando `SQLAlchemy`.
- Implementa melhorias como modo WAL e tratamento de tipos.

### 📄 `ml_models.py`
**Centraliza a lógica de Machine Learning aplicada às séries temporais.**
- Define a classe `EconomicPredictor`, com métodos para:
  - Preparação dos dados (`prepare_data`)
  - Treinamento dos modelos (`train_model`)
  - Avaliação com métricas específicas (MAE, RMSE, R²)
- Implementa algoritmos como Regressão Linear, Random Forest, Ridge e Lasso.
- Suporta validação temporal com `TimeSeriesSplit`.
- Permite salvar e carregar modelos com `joblib`.

### 📄 `app.py`
**Interface principal para visualização dos dados econômicos no Streamlit.**
- Implementa navegação por abas e filtros interativos.
- Utiliza `Plotly` para gerar gráficos de linha, barra e área com interatividade.
- Permite seleção de séries e períodos.
- Usa `st.cache_data` e `st.sidebar` para otimizar e organizar a interface.

### 📄 `ml_app.py`
**Interface específica para visualização de previsões com modelos de ML.**
- Permite selecionar um modelo e indicador econômico para prever.
- Gera gráficos com intervalos de confiança das previsões.
- Exibe métricas de desempenho e importância das variáveis (features).
- Facilita análises comparativas entre valores reais e previstos.

### 📄 `main.py`
**Integra os módulos do sistema em uma aplicação única com navegação completa.**
- Serve como ponto de entrada da aplicação Streamlit.
- Junta as funcionalidades de `app.py` e `ml_app.py`.
- Gerencia a navegação entre páginas com uso de sessões (`st.session_state`).
- Inclui explicações, documentação embutida e layout geral.

### 📄 `Dockerfile` e `docker-compose.yml`
**Automatizam a execução do projeto em ambiente isolado via Docker.**
- `Dockerfile` define o ambiente necessário (Python, dependências).
- `docker-compose.yml` facilita a execução do sistema com banco e interface juntos.
- Permite o deploy local e em nuvem com um único comando.

### 📄 `README.md`
**Arquivo de documentação principal do projeto.**
- Explica como instalar, rodar e contribuir para o sistema.
- Descreve as funcionalidades disponíveis e estrutura dos arquivos.
- Contém instruções para deployment, testes e uso em produção.

### 🧪 Arquivos de teste (`test_*.py`)
**Garantem que os principais módulos do sistema funcionam corretamente.**
- Testam a coleta, armazenamento, modelagem e visualização de dados.
- Utilizam `pytest` para organizar e executar os testes de forma automatizada.
- Auxiliam na detecção de bugs e na manutenção do sistema.
