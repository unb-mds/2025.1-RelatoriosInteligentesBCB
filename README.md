# Projeto de Análise de Dados Econômicos

Sistema para coleta, visualização e análise de indicadores econômicos do Banco Central do Brasil, com previsões usando Machine Learning.

## Executando com Docker

```bash
# Construir a imagem
docker build -t projeto-dados-economicos .

# Executar o container
docker run -p 8501:8501 projeto-dados-economicos