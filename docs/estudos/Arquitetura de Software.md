# Arquitetura de Software

## O que é arquitetura de software e qual é a sua importancia?

Arquitetura de software pode ser entendida como a estrutura fundamental que forma um software, compreendendo seus elementos e suas relações e propriedades.
Na prática, arquitetura de software ajuda os desenvolvedores de um projeto a ter um entendimento simultânio do funcionamento do sistema a ser projetado.
Uma arquitetura eficiente é importante para a manutenção de um sistema em longo prazo, reduzindo custos e tempo gasto para adicionar novos recursos.
Além disso, ela também ajuda os desenvolvidores a ter uma visão de como queira modelar projeto durante as fases iniciais de desenvolvimento.

## Escolhendo a arquitetura

Antes de pular em algum tipo de arquitetura, é bom estudar e analisar o problema no qual seu programa está tentando solucionar.
Também é importante levar em consideração as vantagens e limitações de cada padrão em relação ao seu projeto. As vantagens de usar um padrão arquitetural são:
- Maior flexibilidade e escalabilidade de software
- Facilidade de manutenção e evolução
- Segurança
- Melhor desempenho das aplicações
- Redução de custos e riscos

## Exemplos de Arquiteturas de Software

- Layers (Camadas):
    O sistema é separado por camadas com funcionalidades especificas do sistema, o que gera mais flexibilidade à aplicação.
    Apesar da facilidade no desenvolvimento e realização de testes, muitas camadas podem prejudicar a estabilidade do sistema e diminuir sua eficiência.
- MVC (Module-View-Control):
    O sistema é separdo em três elementos: model (armazenamento e manipulação de dados), view (interface do usuário) e control (fluxo da aplicação, ligação entre o model e view).
    Esse sistema facilita a manutenção e pode ser transferido de um projeto para o outro, mas pode apresentar pior desempenho para projetos complexos.
- Microservices (micros serviços):
    Baseado em multiplos serviços, esse tipo de arquitetura possui uma independência e escabilidade em cada modulo.
    Um único projeto de Microservices pode ter multiplas linguagens de programação em seus diferentes modulos.
    Esse tipo de sistema tem vantagem de acesso a multiplas tecnologias diferentes, no custo de cosistência e distribuição de custos.
-  Pipes-and-filters (PF):
    O sistema é linear, composto de componentes independentes chamados de filtros.
    Os filtros recebem dados, realizam uma transformação desses dados e os enviam ao canal de saída.
- Client-server (cliente servidor):
    O sistema é separado entre processos e modulos distintos do servidor e do cliente, unindo seus dados de alguma forma.
    O modulo do cliente é responsável pela interface e aplicação dos dados e o modulo do servidor é responsável pela obtenção dos dados.
    Esse sistema é mais utilizado para sistemas de visualização dados mais simples com pouca atualizações.
- Orientada a serviços (SOA)
    O sistema é separado em serviços com especialidades específicas.
    Em comparação à arquitetura de microserviços, os modulos são mais complexos e ainda são construidos na mesma linguagem.
    Essa arquitetura é normalmente utilizado para propor serviços de grandes empresas, como NuBank e Amazon.

## Artigos e Vídeos sobre o Tópico

[Artigo sobre o Assunto com exemplos]: https://www.alura.com.br/artigos/padroes-arquiteturais-arquitetura-software-descomplicada?srsltid=AfmBOorbc8L6ZpN_twuHfYYO63eou0ROYvpHBAbL6JsJGJoUA-8E1LrK
[Artigo enviado em sala de aula] https://martinfowler.com/architecture/

[Vídeo Sobre Arquitetura de Softwares]: https://www.youtube.com/watch?v=kYx1QC1XZSo
