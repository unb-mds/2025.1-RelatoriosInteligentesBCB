# 🧭 Guia da Estrutura do Projeto: Squad07

Este documento serve como o mapa geral do nosso projeto, explicando o propósito de cada pasta e arquivo principal.

---

## 🗺️ Mapa Geral do Projeto

A estrutura de pastas e arquivos do nosso projeto está organizada assim:

2025-1-Squad07/
│
├── .gitignore
├── README.md
├── main.py
├── setup.py
├── config.py
│
├── data_collector.py
├── database_manager.py
│
├── app_pages/
│ ├── Coleta_de_Dados.py
│ ├── Dashboard_Economico.py
│ └── Previsoes_ML.py
│
├── components/
│ └── indicadores.py
│
├── ml_core/
│ ├── forecaster.py
│ └── interpreter.py
│
├── utils/
│ └── report_generator.py
│
├── tests/
│ └── ...
│
└── guias_de_desenvolvimento/
├── guia_estrutura_projeto.md
├── guia_execucao_task_git.md
├── guia_padrao_commits.md
└── guia_estrutura_PR.md

---

## ⚙️ Os Pilares do Sistema

### `README.md` 📄 – O Ponto de Partida  
Instruções essenciais para configurar o ambiente, instalar dependências e rodar o projeto.

### `.gitignore` 🗑️ – O Filtro do Projeto  
Lista arquivos e pastas a serem ignorados pelo Git, como `venv/`, arquivos temporários e segredos.

### `main.py` 🖥️ – O Maestro da Orquestra  
Inicia o aplicativo Streamlit e organiza a navegação entre as páginas.

### `config.py` ⚙️ – O Caderno de Configurações  
Centraliza configurações estáticas como URLs de APIs, nome do banco e indicadores usados.

### `data_collector.py` 📡 – O Coletor de Dados  
Responsável por buscar dados nas APIs do Banco Central e prepará-los para uso.

### `database_manager.py` 🗄️ – O Bibliotecário dos Dados  
Gerencia o banco de dados SQLite: cria, salva e recupera dados.

---

## 🎨 As Telas e Ferramentas do Aplicativo

### `app_pages/` 📱 – Telas Interativas
Contém as páginas do aplicativo:

- `Coleta_de_Dados.py`: coleta e salva novos dados.
- `Dashboard_Economico.py`: visualiza gráficos e análises.
- `Previsoes_ML.py`: mostra previsões e interpretação.

### `components/` 🛠️ – O Cinto de Utilidades  
Contém funções reutilizáveis, como `indicadores.py`, responsável por exibir os cartões de indicadores.

---

## 🧠 O Cérebro da Inteligência e Qualidade

### `ml_core/` 🧠 – Central de Machine Learning
- `forecaster.py`: lógica de previsão e métricas.
- `interpreter.py`: transforma resultados em textos interpretativos.

### `utils/` 🧩 – Ferramentas Auxiliares  
- `report_generator.py`: gera relatórios combinando texto, gráficos e métricas.

### `tests/` 🛡️ – Guardiões de Qualidade  
Contém testes automatizados para garantir o bom funcionamento de cada módulo.

---

## 📚 Guias e Documentação

### `guias_de_desenvolvimento/` – Central de Documentação

- `guia_estrutura_projeto.md`: este guia que você está lendo.
- `guia_execucao_task_git.md`: como executar uma task do Git ao PR.
- `guia_padrao_commits.md`: padrão de mensagens de commit.
- `guia_estrutura_PR.md`: boas práticas para Pull Requests.

---

Mantenha este guia por perto para garantir que seu desenvolvimento siga alinhado com a estrutura do projeto! 🚀