import streamlit as st

st.set_page_config(
    page_title="Sistema de Análise Econômica - BCB",
    page_icon="📊",
    layout="wide"
)

# === CSS customizado para modo escuro bonito ===
st.markdown("""
<style>
    /* Fonte e cores globais */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        color: #e0e0e0;
        background-color: #0e1117;
    }

    /* Cabeçalho centralizado e com fundo */
    .titulo {
        background-color: #1e1e1e;
        padding: 30px;
        border-radius: 12px;
        border-left: 6px solid #5aaaff;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    .titulo h1 {
        color: #5aaaff;
        font-size: 2.2rem;
        margin: 0;
    }

    .conteudo {
        background-color: #1c1f26;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 0 8px rgba(0,0,0,0.3);
        color: #d0d0d0;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    .sidebar-title {
        font-size: 18px;
        font-weight: bold;
        color: #5aaaff;
        padding-top: 10px;
        margin-bottom: 10px;
    }

    hr.custom {
        border: none;
        border-top: 1px solid #444;
        margin: 25px 0;
    }
    
    h3.doc {
        color: #5aaaff !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar com título customizado
st.sidebar.markdown('<div class="sidebar-title">🧭 Navegação</div>', unsafe_allow_html=True)
pagina = st.sidebar.radio(
    "",
    [
        "Página Inicial",
        "Coleta de Dados",
        "Dashboard Econômico",
        "Previsões com ML"
    ],
    label_visibility="collapsed"
)

# Página inicial
def show_home():
    st.markdown('<div class="titulo"><h1>📊 Sistema de Análise Econômica - BCB</h1></div>', unsafe_allow_html=True)
    
    # Usando markdown nativo do Streamlit para o conteúdo
    with st.container():
        st.markdown('<div class="conteudo">', unsafe_allow_html=True)
        
        st.markdown("### Funcionalidades Disponíveis:")
        st.markdown("""
        - **Coleta de Dados**  
          Atualiza a base de dados com os últimos dados disponíveis nas APIs do BCB.
          
        - **Dashboard Econômico**  
          Visualize os indicadores econômicos e suas tendências. Para acessar, use a navegação lateral.
          
        - **Previsões com ML**  
          Use machine learning para prever tendências futuras dos indicadores.
        """)
        
        st.markdown('<hr class="custom">', unsafe_allow_html=True)
        
        st.markdown('<h3 class="doc">📚 Documentação</h3>', unsafe_allow_html=True)
        st.markdown("**Como usar este sistema:**")
        st.markdown("""
        - **Coleta de Dados:** Primeiro, colete os dados mais recentes das APIs do Banco Central do Brasil.
        - **Dashboard Econômico:** Visualize os indicadores e suas relações usando a navegação lateral.
        - **Previsões com ML:** Treine modelos preditivos e visualize previsões futuras usando a navegação lateral.
        """)
        
        st.markdown("*Use o menu lateral à esquerda para alternar entre as funcionalidades.*")
        st.markdown('</div>', unsafe_allow_html=True)

# Outras páginas (mantidas como antes)
def show_coleta():
    try:
        from app_pages.Coleta_de_Dados import coleta_page
        coleta_page(10)
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

# Navegação entre páginas
if pagina == "Página Inicial":
    show_home()
elif pagina == "Coleta de Dados":
    show_coleta()
elif pagina == "Dashboard Econômico":
    show_dashboard()
elif pagina == "Previsões com ML":
    show_ml()