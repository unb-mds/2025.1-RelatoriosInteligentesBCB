# Arquivo: setup.py
import subprocess
import sys

def install_requirements():
    print("Instalando pacotes necessários...")
    packages = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "requests",
        "streamlit",
        "sqlalchemy",
        "scikit-learn",
        "plotly",
        "prophet",
        "fpdf2",
        "cmdstanpy",
        "reportlab",
        "requests",
        "kaleido"
    ]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Pacotes instalados com sucesso!")

if __name__ == "__main__":
    install_requirements()
