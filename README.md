# 📊 Relatórios do IPEA

O foco deste projeto é a **geração automática de relatórios inteligentes** para análise dos **dados financeiros do IPEA**, por meio de uma **interface intuitiva em Streamlit**. A aplicação é voltada para **gestores públicos do IPEA**, **pesquisadores** e **universitários**, oferecendo uma experiência acessível e analítica.

🔗 Acesse a versão provisória: [https://relatorioipea-mds.streamlit.app](https://relatorioipea-mds.streamlit.app)  
🌿 Branch ativa: `dev` (atualize os arquivos nela para refletir no app).

📓 Documentação das etapas de densenvolvimento do projeto: [https://miro.com/app/board/uXjVIJxt3qo=/]

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Streamlit
- SQLite
- Pandas, Scikit-learn, Plotly
- Docker (opcional)

---

## 🛠️ Pré-requisitos

- Python 3.10 ou superior
- Git
- pip (gerenciador de pacotes Python)
- (Opcional) Docker

---

## 📥 Como Rodar Localmente

1. Clone o repositório:

    git clone https://github.com/seu-usuario/relatorios-ipea.git
    cd relatorios-ipea

2. Crie e ative um ambiente virtual (recomendado):

    python -m venv venv
    source venv/bin/activate      # Linux/macOS
    venv\Scripts\activate         # Windows

3. Instale as dependências:

    python setup.py install

4. Rode o aplicativo:

    streamlit run main.py

---

## 🧪 Como Testar / Reproduzir

- Puxe o ramo desejado:

    git pull origin <nome-da-sua-branch>

- Instale as dependências (caso ainda não tenha feito):

    python setup.py install

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


