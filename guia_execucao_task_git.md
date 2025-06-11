
# Guia Git para Membros do Grupo: Do Repositório ao Código Final

Este guia cobre o fluxo de trabalho básico com Git e GitHub (ou GitLab/Bitbucket) para cada tarefa da sprint, utilizando **dev** como a branch principal de desenvolvimento.

---

## 1. Preparação Inicial (Apenas na Primeira Vez)

Se você nunca trabalhou com o repositório antes:

### 1.1. Clone o Repositório:

```bash
git clone <URL_DO_REPOSITÓRIO>
```

### 1.2. Acesse a Pasta do Projeto:

```bash
cd 2025-1-Squad07
```

### 1.3. Crie e Ative o Ambiente Virtual:

```bash
python -m venv venv
```

No Windows (PowerShell):

```powershell
.env\Scriptsctivate
```

No macOS/Linux (bash):

```bash
source venv/bin/activate
```

### 1.4. Instale as Dependências:

```bash
pip install -r requirements.txt
```

---

## 2. Iniciando uma Nova Tarefa (Para Cada Nova Task)

### 2.1. Garanta que está na branch de desenvolvimento (dev) e atualizado:

```bash
git checkout dev
git pull origin dev
```

### 2.2. Crie um Novo Ramo (Branch) para a sua Tarefa:

O nome do ramo deve ser descritivo, partindo da **dev**.

```bash
git checkout -b feature/nome-da-sua-tarefa-ou-issue
```

---

## 3. Desenvolvendo a Tarefa (Codificando)

### 3.1. Faça suas Alterações no Código

Implemente a funcionalidade ou correção necessária.

### 3.2. Teste suas Alterações Localmente:

```bash
streamlit run main.py
pytest
```

### 3.3. Adicione e Faça Commits das Suas Alterações:

Adicione todos os arquivos modificados e crie um commit com uma mensagem clara.

```bash
git add .
git commit -m "feat: [Mensagem Clara de Commit]"
```

---

## 4. Finalizando a Tarefa e Subindo para Revisão (Pull Request)

Este é um momento crucial para garantir uma integração suave do seu código.

### 4.1. Sincronize com a dev para Resolver Conflitos Localmente:

Antes de enviar seu código, puxe as últimas alterações da **dev**. Isso permite que você resolva quaisquer conflitos na sua máquina, que é o local mais fácil e seguro para fazer isso.

```bash
git pull origin dev
```

Se houverem conflitos, resolva-os em seu editor de código. Após resolver, adicione os arquivos (`git add .`) e faça um novo commit.

Teste tudo novamente para garantir que a integração com as novas atualizações da **dev** não quebrou sua funcionalidade.

### 4.2. Suba (Push) o seu Ramo Atualizado:

Agora que sua branch contém suas alterações e está sincronizada com a **dev**, envie-a para o repositório remoto.

```bash
git push origin feature/nome-da-sua-tarefa-ou-issue
```

### 4.3. Crie um Pull Request (PR):

Acesse o GitHub (ou GitLab/Bitbucket) para abrir um Pull Request com o alvo na branch **dev**. Seu PR estará limpo, sem conflitos, e pronto para a revisão da equipe. Vincule à issue correspondente (ex: `#NumeroDaIssue`), preencha o modelo de PR e designe os revisores.

---

## 5. Revisão de Código e Mesclagem

### 5.1. Responda aos Comentários:

Se houverem sugestões de melhoria, faça as alterações necessárias, faça o commit e suba novamente para o mesmo ramo (`git push`). O Pull Request será atualizado automaticamente.

### 5.2. Mesclagem:

Uma vez que o PR for aprovado pelos revisores, ele será mesclado à branch **dev**.

### 5.3. Deletar seu Ramo Local e Remoto:

Após a mesclagem, você pode apagar o ramo para manter o repositório limpo.

```bash
git checkout dev
git pull origin dev
git branch -d feature/nome-da-sua-tarefa-ou-issue
git push origin --delete feature/nome-da-sua-tarefa-ou-issue
```
