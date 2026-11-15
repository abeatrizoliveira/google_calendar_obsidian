
# Observações 

## Segurança e privacidade

- O app pede apenas o escopo **`calendar.readonly`**: ele nunca consegue criar, editar ou apagar eventos.
- **Nunca** envie o `credentials.json` nem o `token.json` para o GitHub. Eles já estão no `.gitignore`.
- Seus eventos são lidos direto do Google para o seu computador; nada passa por servidor de terceiros.

<br>

## Solução de problemas

| Sintoma | Provável causa |
|---|---|
| `Error 403: org_internal` ao fazer login | O app foi criado como *Interno* (conta de organização). Use Gmail pessoal ou mude para *Externo*. |
| `getaddrinfo failed` / `TransportError` ao ligar o notebook | A rede ainda não subiu. O script já tenta 5 vezes; adicione um atraso na tarefa. |
| A nota para de atualizar depois de uns 7 dias | App em modo *Testing*. Rode `python login.py` de novo ou publique o app. |
| `O sistema não pode encontrar o caminho especificado` no `.bat` | Caminho da pasta ou do Python errado no `rodar.bat`. |
| `FileNotFoundError: token.json` no Agendador | Falta o `cd /d` no `.bat`: o script está rodando de outra pasta. |
| `ModuleNotFoundError: google...` | O Python usado não é o mesmo onde você instalou as dependências. |
| A nota fica vazia | Confira se está logada na conta certa e se há eventos no período (o script já percorre todas as agendas). |
| As cores não aparecem | Clique em outra linha ou use o Modo de leitura. A linha em edição mostra o código-fonte. |
