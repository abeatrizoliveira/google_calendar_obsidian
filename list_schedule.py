from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# 1. Carrega as credenciais do token.json
creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# 2. Criar o serviço: nome da API "calendar", versão "v3"
service = build("calendar", "v3", credentials=creds)

# 3. Pedir a lista de agendas
response = service.calendarList().list().execute()

for schedule in response["items"]:
    print(schedule["summary"])
    print(schedule)
