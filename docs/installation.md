# Instalação

## Pré-requisitos

- Python **3.11 ou superior**
- Uma conta Google com agendas
- Um cofre (*vault*) do Obsidian
- Windows (para a parte de automação; o script em si é Python puro)

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/calendar-obsidian.git
cd calendar-obsidian
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Se preferir isolar o projeto, crie um ambiente virtual antes:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Crie as credenciais no Google Cloud

> A interface do Google muda de vez em quando, então os nomes dos menus podem variar um pouco.

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/) e **crie um projeto**.
2. Em **APIs e serviços → Biblioteca**, procure **Google Calendar API** e clique em **Ativar**.
3. Configure a **tela de consentimento OAuth**:
   - Tipo de usuário: **Externo**
   - Em **Usuários de teste**, adicione o seu próprio e-mail
   - Escopo: `.../auth/calendar.readonly` (somente leitura)
4. Em **Credenciais → Criar credenciais → ID do cliente OAuth**, escolha **Aplicativo para computador** (*Desktop app*).
5. Baixe o JSON, renomeie para **`credentials.json`** e coloque na pasta do projeto.

> [!WARNING]
> **Conta da faculdade ou do trabalho:** se você criar o projeto com uma conta de organização, pode aparecer o erro `403: org_internal`. Use uma conta Gmail pessoal ou mude o tipo de usuário para **Externo**.

> [!WARNING]
> **Modo Testing:** enquanto o app estiver em modo de teste, o Google pode expirar o login a cada ~7 dias. Para evitar, publique o app (Publicar app na tela de consentimento). Para uso pessoal, não é preciso passar pela verificação do Google.

### 4. Configure o caminho do seu cofre

Abra o `events.py` e ajuste a constante `VAULT`:

```python
VAULT = Path(r"C:\Users\SEU_USUARIO\Documents\Meu Cofre")
```

### 5. Faça o primeiro login

```bash
python login.py
```

O navegador abre pedindo autorização. Como o app é seu e não foi verificado pelo Google, aparece o aviso de **"app não verificado"**: clique em **Avançado → Acessar (nome do app)**. Isso cria o `token.json`.

### 6. Rode

```bash
python events.py
```

A nota `agenda.md` aparece no seu cofre!

<br>

# Automatizando no Windows

### 1. Crie o `rodar.bat`

Copie o `rodar.example.bat` para `rodar.bat` e ajuste os caminhos:

```bat
@echo off
cd /d "C:\caminho\do\projeto"
python events.py >> log.txt 2>&1
```

- O `cd /d` garante que o script ache o `token.json` mesmo rodando pelo Agendador.
- O `>> log.txt 2>&1` guarda tudo o que o script imprimir, inclusive erros. Como a tarefa roda escondida, o `log.txt` é a forma de descobrir o que deu errado.
- Se você usa ambiente virtual ou um Python específico, troque `python` pelo caminho completo do executável.

Teste com um duplo clique antes de agendar.

### 2. Crie a tarefa

1. Abra o **Agendador de Tarefas** → **Criar Tarefa Básica**.
2. **Disparador:** *Quando eu fizer logon* (e, se quiser, um diário também).
3. **Ação:** *Iniciar um programa* → escolha o `rodar.bat`.

### 3. Ajustes recomendados

| Onde | Configuração |
|---|---|
| Condições | Marcar *Iniciar somente se a seguinte conexão de rede estiver disponível* |
| Condições | Desmarcar *Iniciar somente se o computador estiver ligado na energia CA* |
| Configurações | *Executar assim que possível após uma inicialização agendada ser perdida* |
| Configurações | *Se ocorrer falha na tarefa, reiniciar a cada 1 minuto, até 3 vezes* |
| Configurações | *Interromper a tarefa se executada por mais de 1 hora* |
| Disparadores | Atrasar a tarefa em 1 ou 2 minutos após o logon (dá tempo de o Wi-Fi conectar) |
