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

## 📂 Estrutura das Branches

A estrutura de branches foi organizada para facilitar o desenvolvimento das diferentes etapas do projeto. Cada branch está direcionada para uma área específica de trabalho:

- **`dev`**: A branch principal que contém o código de produção. Qualquer alteração que deva ser implementada no Streamlit e gerada no app deve ser feita aqui. Essa é a branch que faz o deploy com o Streamlit.

- **`coleta_dados`**: Focada na **coleta de dados econômicos** através de APIs. Nessa branch, são implementadas funcionalidades relacionadas ao tratamento e armazenamento dos dados financeiros para posterior análise.

- **`dashboard_economico`**: Direcionada para a **geração de dashboards** interativos. Nessa branch, são desenvolvidas as funcionalidades e layouts para a visualização de dados, com foco na experiência de visualização para os usuários do IPEA.

- **`previsao_ml`**: Focada no **filtro de previsão dos dados**. Essa branch é responsável pela aplicação de modelos de Machine Learning para fazer previsões e gerar insights sobre os dados econômicos analisados.

Essas branches são de trabalho e garantem que cada equipe se concentre em uma parte específica do projeto, garantindo um fluxo de desenvolvimento mais organizado.

---

## Integrantes do Projeto:

* Bruno Henryque Grangeiro [Product Owner]
* Rafael Silva Wasconselos [Scrum Master]
* Anna Julia Primo
* Gabriel Guedes Fernandes
* Henrique Fontenelle Galvão
* Jhulia Cristina Gomes
* Lorena Ribeiro Martins
* Luis Gustavo Lopes

### Nossa organização pelo Miro
[https://miro.com/app/board/uXjVIJxt3qo=/](https://miro.com/app/board/uXjVIJxt3qo=/)
