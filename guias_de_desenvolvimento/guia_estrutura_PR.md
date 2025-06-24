**Título do PR:** `feat: Implementou lógica de interpretação do relatório via NLP (#<Número_da_Issue>)`

---

### Resumo das Alterações:
* **Criou** o novo módulo `ml_core/interpreter.py`.
* **Implementou** a função `generate_nlp_report` que analisa as tendências históricas e de previsão e gera um texto descritivo.
* **Integrou** as métricas calculadas na Task 1 ao texto interpretativo.

### Propósito da Alteração:
Esta PR adiciona a inteligência de **Processamento de Linguagem Natural (NLP)** para transformar os dados numéricos de previsão em um relatório textual compreensível. Isso é um dos **desafios chave do projeto** e a base para a exibição e exportação do relatório na interface.

### Como Testar / Reproduzir:
1.  Puxe este ramo: `git pull origin feature/gerar-relatorio-texto-nlp`
2.  Inicie a aplicação: `streamlit run main.py`
3.  Navegue para a página "Previsões com ML".
4.  Selecione um indicador (ex: IPCA) e um período de previsão (ex: 6 meses).
5.  Clique em "Simular Previsão".
6.  **Observe** se o texto interpretativo (a ser exibido na Task 4) está sendo gerado corretamente no console (ou em algum `st.write` temporário) e se a lógica de tendência e métricas está refletida no texto.

### Pontos de Atenção para o Revisor:
* Revise a lógica de análise de tendência dentro de `ml_core/interpreter.py` para garantir que as condições (`if/else`) capturam bem os cenários.
* Verifique a clareza e gramática do texto gerado pela função `generate_nlp_report`.

### Checklist do Desenvolvedor:
- [x] O código foi testado localmente e está funcionando conforme o esperado?
- [ ] Todos os comentários e código legado desnecessário foram removidos?
- [ ] O README (ou outra documentação) foi atualizado, se necessário?
- [ ] Todas as dependências externas foram listadas no `setup.py` (se houver novas)?



