
# Personalização

Tudo o que dá para ajustar está no `events.py`.

**Quantos dias mostrar na semana** (em `main`):

```python
end_week = end_today + dt.timedelta(days=7)   # troque o 7
```

**Nome e local da nota** (em `main`):

```python
(VAULT / "agenda.md").write_text(...)
# ex.: (VAULT / "Agenda" / "agenda.md")  → a pasta precisa existir
```

**Títulos, textos e emojis das seções** (em `main`):

```python
lines += build_section("## Eventos de hoje ☀️", today)
lines += [""] + build_section("## Eventos da semana 🪴", week)
```

**Visual do rótulo colorido** (em `get_events`): a cor de fundo vem da cor da agenda no Google Calendar, então basta mudar a cor lá. Já o resto do estilo está no `style='...'` da variável `line`: cor do texto (`#2b2b2b`), `padding` e `border-radius`. Se quiser usar a cor de texto que o próprio Google escolheu para combinar com cada agenda, use `agenda["foregroundColor"]`.

**Formato de data e hora:**

```python
hour_text = when.strftime("%d/%m %H:%M")   # ex.: 16/11 07:00
```

**Ignorar uma agenda** (por exemplo, os feriados), no início do `for agenda in agendas` em `get_events`:

```python
IGNORAR = {"Holidays in Brazil"}

for agenda in agendas:
    if agenda["summary"] in IGNORAR:
        continue
    ...
```