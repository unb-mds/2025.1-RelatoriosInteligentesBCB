import streamlit as st
from styles.custom_styles import apply_custom_styles

st.set_page_config(
    page_title="Sistema de Análise Econômica - BCB",
    page_icon="📊",
    layout="wide"
)

# === CSS customizado para modo escuro bonito ===
apply_custom_styles()

# Sidebar com título customizado
st.sidebar.markdown('<div class="sidebar-title">🧭 Navegação</div>', unsafe_allow_html=True)
pagina = st.sidebar.radio(
    "",
    [
        ":blue[Página Inicial]",
        ":blue[Coleta de Dados]",
        ":blue[Dashboard Econômico]",
        ":blue[Previsões com ML]"
    ],
    label_visibility="collapsed"
)

# Página inicial
def show_home():
    st.markdown('<div class="titulo"><h1>📊 Sistema de Análise Econômica - BCB</h1></div>', unsafe_allow_html=True)
    
    # Usando markdown nativo do Streamlit para o conteúdo
    with st.container():
        st.markdown('<div class="conteudo">', unsafe_allow_html=True)
        
        st.markdown("### 📌 Funcionalidades Disponíveis:")
        st.markdown("""
        - **Coleta de Dados**  
          Faça a coleta inicial. Utilize essa págine sempre quando é necessário atualizar seus dados.

        - **Dashboard Econômico**  
          Visualize os indicadores econômicos e suas tendências. Para acessar, use a navegação lateral.
          
        - **Previsões com ML**  
          Use machine learning para prever tendências futuras dos indicadores.
        """)
        
        st.markdown('<hr class="custom">', unsafe_allow_html=True)
        
        st.markdown('<h3 class="doc">📚 Documentação</h3>', unsafe_allow_html=True)
        st.markdown("**Como usar este sistema:**")
        st.markdown("""
        - **Coleta de dados:** Realize a coleta e atualização dos dados disponíveis.
        - **Dashboard Econômico:** Visualize os indicadores e suas relações usando a navegação lateral.
        - **Previsões com ML:** Treine modelos preditivos e visualize previsões futuras usando a navegação lateral.
        """)
        
        st.markdown("*Use o menu lateral à esquerda para alternar entre as funcionalidades.*")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="custom">', unsafe_allow_html=True)
        
        st.markdown('<h3 class="doc">📈 Informações sobre os Dados</h3>', unsafe_allow_html=True)
        st.markdown("""
        - **IPCA:** Índice que define tendências da inflação.
        - **Taxa SELIC:** Taxa básica de juros na economia.
        - **PIB:** Soma dos bens e serviços produzido por um país, estado ou cidade.
        - **Transações Correntes:** Parte do balanço de pagamentos que inclui as contas de comércio de mercadorias, balança de serviços e as transferências unilaterais.
        - **IGP-M:** Indicador que mede variação de preços em diversos setores econômicos.
        - **IPCN:** Indicador que mede variação de preços de produtos e serviços consumidos por famílias com renda mensal menor ou igual à 5 salários mínimos.
        - **Câmbio do Dólar:** Conversão de dólar para real.
        - **Resultado Primário:** Diferença entre receitas e despesas não financeiras do governo.
        """)

# Outras páginas (mantidas como antes)
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

def show_coleta():
    try:
        from app_pages.Coleta_de_Dados import coleta_page
        coleta_page(10)
    except Exception as e:
        st.error(f"Erro ao carregar a Coleta de Dados: {e}")

# Navegação entre páginas
if pagina == ":blue[Página Inicial]":
    show_home()
elif pagina == ":blue[Dashboard Econômico]":
    show_dashboard()
elif pagina == ":blue[Previsões com ML]":
    show_ml()
elif pagina == ":blue[Coleta de Dados]":
    show_coleta()
