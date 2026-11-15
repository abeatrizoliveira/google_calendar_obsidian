import time
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow  
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError, TransportError

# Permissões que pede ao usuário | readonly -> ler a agenda sem alterar
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def save_token(creds):
    # Guarda as credenciais (incluindo o token de renovação) para o próximo uso
    with open("token.json", "w")as file:
        file.write(creds.to_json())


def get_credentials():
    creds = None

    # 1. Carrega o token salvo, se existir
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 2. Caso mais comum: o token ainda vale. Devolve e acaba aqui.
    if creds and creds.valid:
        return creds

    # 3. Token vencido, mas com token de renovação: tenta renovar sem navegador.
    # Se a rede ainda não subiu, espera e tenta de novo.
    if creds and creds.expired and creds.refresh_token:
        for attempt in range(5):
            try:
                creds.refresh(Request())
                save_token(creds)
                return creds
            except TransportError:
                print(f"Tentativa {attempt + 1} falhou (sem rede). Esperando...")
                time.sleep(10)
            except RefreshError:
                # O login venceu de vez: repetir não adianta, vai para o passo 4
                print("Login vencido. Será preciso entrar de novo.")
                break

        else:
            # O for terminou sem break: as 5 tentativas falharam por falta de rede
            raise SystemExit("Sem conexão com o Google. Tente novamente mais tarde.")

    # 4. Primeiro login, ou login vencido: abre o navegador
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    save_token(creds)
    return creds


if __name__ == "__main__":
    get_credentials()