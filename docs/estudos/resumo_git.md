
# Resumo de Git: Do Download aos Primeiros Passos

Git é um sistema de controle de versão distribuído essencial para gerenciar projetos de software. Ele permite rastrear alterações no código, colaborar com outros desenvolvedores e garantir a integridade do projeto ao longo do tempo.  

Trabalhar com Git em equipe envolve a criação de branches para novas funcionalidades, a integração de código via merge ou rebase e a resolução de conflitos. Plataformas como GitHub, GitLab e Bitbucket facilitam esse fluxo de trabalho ao oferecer repositórios remotos para colaboração.  

---

## 1. Instalando o Git

- **Windows:** Baixe em [git-scm.com](https://git-scm.com/) e instale.  
- **Linux:**  
  ```sh
  sudo apt update && sudo apt install git  # Debian/Ubuntu
  sudo dnf install git  # Fedora
  ```
- **MacOS:**  
  ```sh
  brew install git
  ```

Verifique se está instalado corretamente:  
```sh
git --version
```

---

## 2. Configuração Inicial

Antes de começar, configure seu nome e e-mail para identificar seus commits:  
```sh
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

Verifique as configurações:  
```sh
git config --list
```

---

## 3. Criando ou Clonando um Repositório

- **Criar um repositório novo:**  
  ```sh
  git init
  ```
- **Clonar um repositório existente:**  
  ```sh
  git clone URL_DO_REPOSITORIO
  ```

---

## 4. Principais Comandos do Git

### 4.1. Adicionar arquivos ao controle de versão  
```sh
git add nome_do_arquivo  # Adiciona um arquivo específico
git add .  # Adiciona todas as mudanças
```

### 4.2. Criar um commit (salvar as mudanças localmente)  
```sh
git commit -m "Mensagem descritiva do commit"
```

### 4.3. Verificar o status do repositório  
```sh
git status
```

### 4.4. Ver histórico de commits  
```sh
git log --oneline --graph --all  # Resumido e visual
```

### 4.5. Enviar mudanças para o repositório remoto  
```sh
git push origin branch_name
```

### 4.6. Baixar mudanças do repositório remoto  
```sh
git pull origin branch_name
```

### 4.7. Criar e trocar de branch  
```sh
git branch nome_da_branch  # Criar branch
git checkout nome_da_branch  # Trocar de branch
git switch nome_da_branch  # Alternativa moderna para checkout
git checkout -b nova_branch  # Criar e já mudar para a nova branch
```

### 4.8. Mesclar branches  
```sh
git merge nome_da_branch  # Mescla outra branch na atual
```

### 4.9. Descartar mudanças antes do commit  
```sh
git checkout -- nome_do_arquivo  # Restaura um arquivo para a última versão commitada
git reset --hard  # Restaura tudo para o último commit
```

---

## 5. Trabalhando com GitHub/GitLab/Bitbucket

Após criar um repositório remoto, vincule-o ao local:  
```sh
git remote add origin URL_DO_REPOSITORIO
git branch -M main  # Caso precise renomear para 'main'
git push -u origin main  # Enviar código pela primeira vez
```

### 📌 Fluxo de trabalho em equipe  

1. **Clone o repositório** se ainda não tiver:  
   ```sh
   git clone URL_DO_REPOSITORIO
   ```
2. **Crie uma branch para sua tarefa**:  
   ```sh
   git checkout -b minha_nova_funcionalidade
   ```
3. **Faça commits regularmente** enquanto desenvolve:  
   ```sh
   git add .
   git commit -m "Implementa nova funcionalidade"
   ```
4. **Sincronize com o repositório remoto** antes de subir suas mudanças:  
   ```sh
   git pull origin main  # Evita conflitos ao integrar o código mais recente
   ```
5. **Envie seu código para o repositório remoto**:  
   ```sh
   git push origin minha_nova_funcionalidade
   ```
6. **Crie um Pull Request (PR)** na plataforma (GitHub/GitLab/Bitbucket) e peça revisão.  

---

## 6. Resolver Conflitos de Merge

Quando há conflitos em um `merge`, edite os arquivos afetados, resolva os conflitos manualmente e faça um novo commit:  
```sh
git add .
git commit -m "Resolvendo conflitos"
```

Se necessário, rebase sua branch com a principal antes do merge:  
```sh
git checkout minha_branch
git rebase main
```

---

## 7. Boas Práticas ao Trabalhar em Equipe com Git

✅ **Crie branches para cada funcionalidade/bugfix** e mantenha a `main` sempre estável.  
✅ **Comente seus commits de forma clara** para facilitar o entendimento.  
✅ **Sincronize seu código antes de subir suas mudanças** (`git pull`) para evitar conflitos.  
✅ **Use pull requests (PRs)** para revisar código antes de mesclar com a branch principal.  
✅ **Evite commits muito grandes**—faça commits pequenos e frequentes.  
✅ **Não faça commits diretos na `main`**—sempre trabalhe em uma branch separada.  

---

## 8. Comandos Úteis Extras

- **Criar um `.gitignore` para ignorar arquivos específicos:**  
  ```sh
  echo "node_modules/" >> .gitignore
  git add .gitignore
  git commit -m "Adicionando gitignore"
  ```
- **Ver diferença entre arquivos antes de commitar:**  
  ```sh
  git diff
  ```
- **Reverter um commit:**  
  ```sh
  git revert ID_DO_COMMIT
  ```
- **Deletar uma branch local:**  
  ```sh
  git branch -d nome_da_branch
  ```
- **Deletar uma branch remota:**  
  ```sh
  git push origin --delete nome_da_branch
  ```

---

## Conclusão

Git é uma ferramenta essencial para equipes de desenvolvimento. Ao seguir boas práticas e utilizar branches, pull requests e revisões de código, é possível manter um fluxo de trabalho eficiente e evitar problemas de versionamento. 🚀  

---

### 🎥 Sugestão de vídeo rápido  
🔗 [Git para iniciantes - YouTube](https://www.youtube.com/watch?v=ts-H3W1uLMM)  

### 📚 Sugestão de playlist de Git  
📌 [Curso completo de Git - YouTube](https://www.youtube.com/watch?v=YnVnFanIAzU&list=PLucm8g_ezqNq0dOgug6paAkH0AQSJPlIe)  
