# styles/custom_styles.py

import streamlit as st

def apply_custom_styles():
    custom_css = """
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
    """
    st.markdown(custom_css, unsafe_allow_html=True)