# Importação de bibliotecas
import datetime as dt
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from login import get_credentials

# * Definição de variáveis importantes: caminho, datas... Variáveis que não precisam entrar na função.
VAULT = Path(r"C:\CAMINHO_DA_PASTA_DO_PROJETO")

weekdays = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
present_day = dt.date.today()
weekday = weekdays[present_day.weekday()]


def get_events(service, schedules, start, end):
    # Busca os eventos de todas as agendas entre start e end e devolve a lista ordenada.
    events = []
    
    for schedule in schedules:
        response = service.events().list(
            calendarId=schedule["id"],
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        color = schedule["backgroundColor"]

        # dentro do loop das agendas: roda uma vez para cada agenda
        for event in response["items"]:
            title = event.get("summary", "(sem título)")
            event_start = event["start"]

            if "dateTime" in event_start:
                when = dt.datetime.fromisoformat(event_start["dateTime"])
                hour_text = when.strftime("%d/%m %H:%M")
            else:
                day = dt.date.fromisoformat(event_start["date"])
                hour_text = dt.datetime.strftime(day, "%d/%m")

            key = event_start.get("dateTime", event_start.get("date"))
            line = "<span style='color: #2b2b2b; border-radius:2px; padding: 0 6px; background-color:" + color + "'>" + schedule["summary"] + "</span> " + "─ **" + hour_text + "**  <span style='color:" + color + "'>─</span> " + title
            events.append((key, line))
        
    events.sort()
    return events


def build_section(title,events):
    # Monta as linhas de uma seção da nota (título + eventos).
    lines = [title, "---"]
    
    if not events:
        lines.append('Nenhum evento!')
    else:
        for _key, line in events:
            lines.append(f'- {line}')

    return lines


def main():
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)
        schedules = service.calendarList().list().execute()["items"]

        now = dt.datetime.now().astimezone()

        start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        end_today = start_today + dt.timedelta(days=1)

        end_week = end_today + dt.timedelta(days=7)

        all_events = get_events(service, schedules, start_today, end_week)

        today_str = present_day.strftime("%Y-%m-%d")

        today = [e for e in all_events if e[0][:10] <= today_str]
        week = [e for e in all_events if e[0][:10] > today_str]

        lines = ["#### " + weekday + " • " + present_day.strftime("%d/%m")]
        lines += build_section("## Eventos de hoje ☀️", today)
        lines += [""] + build_section("## Eventos da semana 🪴", week)

        (VAULT / "agenda.md").write_text("\n".join(lines), encoding="utf-8")
    
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()