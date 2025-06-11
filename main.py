import streamlit as st

st.set_page_config(
    page_title="Sistema de Análise Econômica - BCB",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Escolha a funcionalidade:",
    [
        "Página Inicial",
        "Coleta de Dados",
        "Dashboard Econômico",
        "Previsões com ML"
    ]
)

def show_home():
    st.title("Sistema de Análise Econômica - Dados do Banco Central do Brasil")
    st.markdown("""
**Funcionalidades Disponíveis:**

- **Coleta de Dados**  
  Atualiza a base de dados com os últimos dados disponíveis nas APIs do BCB.

- **Dashboard Econômico**  
  Visualize os indicadores econômicos e suas tendências. Para acessar, use a navegação lateral.

- **Previsões com ML**  
  Use machine learning para prever tendências futuras dos indicadores. Para acessar, use a navegação lateral.

---

### Documentação

**Como usar este sistema:**

- **Coleta de Dados:** Primeiro, colete os dados mais recentes das APIs do Banco Central do Brasil.
- **Dashboard Econômico:** Visualize os indicadores e suas relações usando a navegação lateral.
- **Previsões com ML:** Treine modelos preditivos e visualize previsões futuras usando a navegação lateral.

> Use o menu de navegação à esquerda para alternar entre as diferentes funcionalidades.
    """)

def show_coleta():
    try:
        from app_pages.Coleta_de_Dados import coleta_page
        coleta_page(10)  # Coleta dados dos últimos 10 anos como padrão
    except Exception as e:
        st.error(f"Erro ao carregar a Coleta de Dados: {e}")

def show_dashboard():
    try:
        from app_pages.Dashboard_Economico import dashboard_page
        dashboard_page()
    except Exception as e:
        st.error(f"Erro ao carregar o Dashboard Econômico: {e}")

def show_ml():
    try:
        from app_pages.Previsoes_ML import ml_page
        ml_page()
    except Exception as e:
        st.error(f"Erro ao carregar as Previsões com ML: {e}")

if pagina == "Página Inicial":
    show_home()
elif pagina == "Coleta de Dados":
    show_coleta()
elif pagina == "Dashboard Econômico":
    show_dashboard()
elif pagina == "Previsões com ML":
    show_ml()