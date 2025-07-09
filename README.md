# 📊 Relatórios Inteligentes do BCB

O foco deste projeto é a **geração automática de relatórios inteligentes** para análise dos **dados financeiros do BCB**, por meio de uma **interface intuitiva em Streamlit**. A aplicação é voltada para **gestores públicos do IPEA**, **pesquisadores** e **universitários**, oferecendo uma experiência acessível e analítica.

🔗 Acesse a versão provisória: [https://apresentacaomdsgrupo7.streamlit.app/]  
🌿 Branch ativa: 'main'.  
  
📓 Documentação das etapas de densenvolvimento do projeto: [https://miro.com/app/board/uXjVIJxt3qo=/]

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Streamlit
- SQLite
- Pandas, Scikit-learn, Plotly, Prophet
- DeepSeek AI
- Docker (Opcional)

---

## 🛠️ Pré-requisitos

- Python 3.10 ou superior
- Git
- pip (gerenciador de pacotes Python)
- (Opcional) Docker
- (Opcional) Chave da API DeepSeek

---

## 📥 Como Rodar Localmente

1. Clone o repositório:

   git clone https://github.com/unb-mds/2025.1-RelatoriosInteligentesBCB.git  
   cd 2025.1-RelatoriosInteligentesBCB

3. Crie e ative um ambiente virtual (recomendado):

    python -m venv venv
    - source venv/bin/activate      **# Linux/macOS**
    - venv\Scripts\activate         **# Windows**

4. Instale as dependências:

    python setup.py

5. Rode o aplicativo:

    streamlit run main.py

---
## 🐳 Relatórios com IA DeepSeek

Caso deseja gerar relatórios personalizados com IA da DeepSeek, é necessário ter uma chave particular de sua API. Com ela em mãos, siga os seguintes passos:

- Crie uma pasta chamada ".streamlit" na pasta principal do repositório;
- Crie um arquivo chamado "secrets.toml" dentro da pasta criada;
- Escreva o seguinte comando com sua chave dentro do arquivo criado:

        DEEPSEEK_API_KEY = "INSIRA SUA CHAVE AQUI"

*Observação: Ainda há um relatório de gráfico mais simples para download caso não tenha uma chave da API DeepSeek.*

---
       
# ⚙️ Notas para os Desenvolvedores do Projeto

## 🧪 Como Testar / Reproduzir

- Puxe o ramo desejado:

    git pull origin <nome-da-sua-branch>

- Instale as dependências (caso ainda não tenha feito):

    python setup.py

- Execute o Streamlit:

    streamlit run main.py

- Navegue por todas as páginas da aplicação:
  - Página Inicial
  - Coleta de Dados
  - Dashboard Econômico
  - Previsões com ML

- Verifique se:
  - Todas as páginas carregam sem erros;
  - As funcionalidades principais estão operando corretamente:
    - Coleta de dados;
    - Visualização no dashboard;
    - Previsões com modelos de machine learning.

---

## 🌱 Política de Branches

### 🧪 dev – Ambiente de Integração

- Cada membro deve trabalhar em sua **branch temática** (por exemplo, `feature/dashboard`).
- Ao finalizar uma funcionalidade (ou parte dela), deve ser feito um **pull request para a branch `dev`**.
- A `dev` será o nosso ambiente de integração, onde testamos a aplicação como um todo, com as partes se conectando progressivamente.

### 🔒 main – Versão Final

- A `main` ficará reservada para a **entrega final do projeto**.
- O merge da `dev` para a `main` só será feito quando todas as frentes estiverem prontas e testadas.


