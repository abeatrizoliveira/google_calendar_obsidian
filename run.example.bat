@echo off
REM Copie este arquivo para rodar.bat e ajuste os caminhos.
REM O rodar.bat fica fora do Git (está no .gitignore) porque tem caminhos pessoais.

REM Entra na pasta do projeto (necessário para o script achar o token.json)
cd /d "C:\caminho\do\projeto\calendar-obsidian"

REM Roda o script e guarda tudo (inclusive erros) no log.txt
python events.py >> log.txt 2>&1