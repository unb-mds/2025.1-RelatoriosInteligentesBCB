# 📊 Projeto de Relatórios Inteligentes — IPEADATA

## 💡 Sobre o Projeto

Este projeto tem como objetivo automatizar a geração de **relatórios inteligentes** a partir da análise de dados financeiros do IPEA. A proposta é facilitar o acesso à informação para **gestores públicos**, utilizando visualizações interativas e textos explicativos gerados automaticamente.

A solução é desenvolvida com **Streamlit**, utilizando **modelos de NLP open source** e **visualização de dados em tempo real**.

🔗 Acesse a versão provisória: [https://relatorioipea-mds.streamlit.app](https://relatorioipea-mds.streamlit.app)  
🌿 Branch ativa: `dev` (atualize os arquivos nela para refletir no app).

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
