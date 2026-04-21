# Streamlit Live Temperatur

Diese App zeigt eine **sehr einfache Live-Messung** der internen Temperatur des Raspberry Pi Pico (RP2040) mit Streamlit.

## Starten

```powershell
uv sync
uv run streamlit run streamlit_live_temp/app.py
```

## Was die App macht

- baut ueber `mpremote` eine Verbindung zum Pico auf
- fuehrt pro Messpunkt einen kurzen MicroPython-Code auf dem Pico aus
- liest `raw` (ADC-Rohwert) und berechnete Temperatur (`temp_c`)
- aktualisiert zwei Live-Diagramme in Streamlit

## Verwendete Pakete und warum

- `streamlit`
  - fuer die Web-Oberflaeche (Buttons, Sidebar, Live-Plot, Status)
  - schnellster Weg fuer eine einfache Live-Ansicht ohne Frontend-Setup

- `mpremote`
  - offizielles MicroPython-Tool, um Code ueber USB auf dem Pico auszufuehren
  - wird hier genutzt, um Messcode direkt auf dem Board laufen zu lassen

- `subprocess` (Python-Standardbibliothek)
  - startet den `mpremote`-Befehl aus der App heraus
  - sammelt stdout/stderr fuer Fehlerbehandlung

- `sys` (Python-Standardbibliothek)
  - liefert mit `sys.executable` den aktiven Python-Interpreter
  - wichtig, damit `mpremote` aus der richtigen virtuellen Umgebung gestartet wird

- `time` (Python-Standardbibliothek)
  - steuert das Messintervall ueber `sleep`

## Hinweise

- Pico muss per USB verbunden sein und MicroPython installiert haben.
- Beim ersten Streamlit-Start kann eine E-Mail-Abfrage erscheinen; einfach leer lassen und mit Enter bestaetigen.
- `Port = auto` funktioniert meist direkt.
- Falls noetig, einen festen Port setzen (z. B. `COM4`).
- Die Formel fuer `temp_c` ist die uebliche RP2040-Naehungsformel und dient als schneller Start.
