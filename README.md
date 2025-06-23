# 📊 Relatórios do IPEA

O foco deste projeto é a **geração automática de relatórios inteligentes** para análise dos **dados financeiros do IPEA**, por meio de uma **interface intuitiva em Streamlit**. A aplicação é voltada para **gestores públicos do IPEA**, **pesquisadores** e **universitários**, oferecendo uma experiência acessível e analítica.

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

---
=======
# 📊 Projeto de Relatórios Inteligentes — IPEADATA

## 💡 Sobre o Projeto

Este projeto tem como objetivo automatizar a geração de **relatórios inteligentes** a partir da análise de dados financeiros do IPEA. A proposta é facilitar o acesso à informação para **gestores públicos**, utilizando visualizações interativas e textos explicativos gerados automaticamente.

A solução é desenvolvida com **Streamlit**, utilizando **modelos de NLP open source** e **visualização de dados em tempo real**.

🔗 Acesse a versão provisória: [https://relatorioipea-mds.streamlit.app](https://relatorioipea-mds.streamlit.app)  
🌿 Branch ativa: `dev` (atualize os arquivos nela para refletir no app).

📓 Documentação das etapas de densenvolvimento do projeto: [https://miro.com/app/board/uXjVIJxt3qo=/]

---

## 🚀 Funcionalidades

- Visualização interativa de dados financeiros.
- Geração automática de relatórios em linguagem natural (NLP).
- Resumos automatizados de tendências e alertas para gestores.
- Interface simples e acessível com foco na experiência do usuário.
- Uso exclusivo de tecnologias **open source**.

---

## 🧰 Tecnologias Utilizadas

- **Python**
- **Streamlit**
- **Pandas / NumPy**
- **Plotly / Matplotlib**
- **Modelos NLP (BERTTopic, spaCy, etc.)**

---

## 🖥️ Como Rodar Localmente

Para executar o projeto localmente, siga esta sequência de comandos no terminal:

```bash
# 1. Instale as dependências do projeto
python setup.py install

# 2. Realize a coleta de dados iniciais
python data_collector.py

# 3. Execute a aplicação no navegador com Streamlit
streamlit run main.py