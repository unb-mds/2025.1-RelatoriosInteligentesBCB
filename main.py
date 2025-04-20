# Arquivo: main.py
import streamlit as st
import subprocess
import sys
import os

def check_requirements():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import pandas, numpy, matplotlib, seaborn, requests, streamlit, sqlalchemy
        import sklearn, plotly
        return True
    except ImportError:
        return False

def run_setup():
    """Executa o script de configuração"""
    subprocess.check_call([sys.executable, "setup.py"])
    st.success("Ambiente configurado com sucesso!")

def collect_data():
    """Executa o script de coleta de dados"""
    subprocess.check_call([sys.executable, "data_collector.py"])
    st.success("Dados coletados com sucesso!")

def run_dashboard():
    """Executa o dashboard principal"""
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])

def run_ml_dashboard():
    """Executa o dashboard de machine learning"""
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "ml_app.py"])

# Interface principal
st.set_page_config(
# Arquivo: main.py (continuação)
    page_title="Sistema de Análise Econômica - BCB",
    page_icon="📊",
    layout="wide"
)

st.title("Sistema de Análise Econômica com Dados do Banco Central do Brasil")
st.markdown("""
Este sistema permite coletar, visualizar e analisar dados econômicos do Banco Central do Brasil,
além de criar modelos de machine learning para previsão de indicadores.
""")

# Verificar dependências
if not check_requirements():
    st.warning("Algumas dependências não estão instaladas.")
    if st.button("Instalar Dependências"):
        run_setup()

# Menu principal
st.header("Escolha uma opção:")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Coleta de Dados")
    st.markdown("Atualiza a base de dados com os últimos dados disponíveis nas APIs do BCB.")
    if st.button("Coletar Dados"):
        with st.spinner("Coletando dados..."):
            collect_data()

with col2:
    st.subheader("Dashboard Econômico")
    st.markdown("Visualize os indicadores econômicos e suas tendências.")
    if st.button("Abrir Dashboard"):
        run_dashboard()
        st.success("Dashboard aberto em uma nova aba!")

with col3:
    st.subheader("Previsões com ML")
    st.markdown("Use machine learning para prever tendências futuras dos indicadores.")
    if st.button("Abrir Previsões"):
        run_ml_dashboard()
        st.success("Dashboard de ML aberto em uma nova aba!")

# Informações adicionais
st.header("Documentação")
st.markdown("""
### Como usar este sistema

1. **Coleta de Dados**: Primeiro, colete os dados mais recentes das APIs do Banco Central do Brasil.
2. **Dashboard Econômico**: Visualize os indicadores e suas relações.
3. **Previsões com ML**: Treine modelos preditivos e visualize previsões futuras.

### Sobre os Dados

Os dados são obtidos diretamente das APIs do Banco Central do Brasil e incluem:
- **Inflação (IPCA)**: Índice de Preços ao Consumidor Amplo, medida oficial da inflação no Brasil.
- **PIB Real**: Produto Interno Bruto ajustado pela inflação.
- **Dívida/PIB**: Relação entre a dívida pública e o PIB.
- **Taxa SELIC**: Taxa básica de juros da economia brasileira.
- **Meta da SELIC**: Meta estabelecida pelo Copom.
- **Saldo em Transações Correntes**: Medida do balanço de pagamentos.
- **Resultado Primário**: Indicador fiscal do governo.

### Sobre os Modelos de ML

Os modelos disponíveis para previsão incluem:
- **Regressão Linear**: Modelo linear simples para identificar tendências.
- **Ridge e Lasso**: Variantes regularizadas da regressão linear.
- **Random Forest**: Modelo baseado em árvores de decisão para capturar relações não lineares.

### Compartilhando o Projeto

Para compartilhar este projeto com colegas, você pode:
1. **Usar controle de versão**: Hospede o código no GitHub e compartilhe o repositório.
2. **Compartilhar localmente**: Execute em seu computador e compartilhe o acesso via rede local.
3. **Implantar online**: Use serviços como Streamlit Cloud para disponibilizar na web.
""")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com Python, Streamlit e scikit-learn")