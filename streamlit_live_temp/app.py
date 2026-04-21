import subprocess
import sys
import time

import streamlit as st


# Diese Funktion fuehrt einen Python-Code-String auf dem Pico aus.
# Technisch passiert das ueber: python -m mpremote connect <port> exec <code>
# Rueckgabe:
# - stdout (Textausgabe vom Pico)
# - stderr (Fehlermeldungen vom Pico/mpremote)
# - returncode (0 = erfolgreich)
def run_on_pico(code: str, port: str = "auto", exec_timeout_s: float = 20.0):
    # sys.executable sorgt dafuer, dass exakt der Python-Interpreter
    # der aktiven Umgebung verwendet wird (z. B. .venv).
    cmd = [sys.executable, "-m", "mpremote", "connect", port, "exec", code]

    # capture_output=True sammelt stdout/stderr ein, statt direkt ins Terminal zu schreiben.
    # text=True liefert Strings statt Bytes.
    # timeout verhindert, dass die App ewig haengen bleibt.
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=exec_timeout_s)

    # strip() entfernt fuehrende/nachfolgende Zeilenumbrueche.
    return proc.stdout.strip(), proc.stderr.strip(), proc.returncode


# Diese Funktion liest den internen Temperatursensor des RP2040 aus.
# Der eigentliche Sensor-Code laeuft auf dem Pico (nicht auf dem PC).
def read_raw_and_temp(port: str = "auto"):
    # Mehrzeiliger MicroPython-Code, der direkt auf dem Pico ausgefuehrt wird.
    code = '''
from machine import ADC

sensor = ADC(4)
raw = sensor.read_u16()
voltage = raw * 3.3 / 65535
temp_c = 27 - (voltage - 0.706) / 0.001721
print(f"{raw},{temp_c:.2f}")
'''

    out, err, rc = run_on_pico(code=code, port=port)

    # Wenn mpremote fehlschlaegt oder stderr etwas enthaelt,
    # geben wir einen klaren Fehler nach oben.
    if rc != 0 or err:
        raise RuntimeError(err or "Unbekannter mpremote-Fehler")

    # Erwartetes Format: "<raw>,<temp>"
    raw_str, temp_str = out.split(",")
    return int(float(raw_str)), float(temp_str)


# Seiteneinstellungen: Titel im Browser-Tab + breites Layout.
st.set_page_config(page_title="Pico Live Temperature", layout="wide")

# Sichtbare Ueberschriften in der App.
st.title("Raspberry Pi Pico - Live Temperatur")
st.caption("Minimales Live-Plot-Beispiel mit Streamlit und mpremote")

# Sidebar-Parameter:
# - Port: "auto" versucht automatisch das richtige USB-Geraet zu finden.
# - Samples: Anzahl Messpunkte insgesamt.
# - Intervall: Wartezeit zwischen zwei Messungen.
port = st.sidebar.text_input("Port", value="auto")
num_samples = st.sidebar.slider("Anzahl Messpunkte", min_value=10, max_value=600, value=60, step=10)
interval_s = st.sidebar.slider("Intervall (Sekunden)", min_value=0.2, max_value=5.0, value=1.0, step=0.1)

# Start-Button: erst nach Klick laeuft die Messschleife los.
start = st.button("Messung starten")

if start:
    # st.empty() erzeugt Platzhalter, die wir bei jedem Schleifendurchlauf neu befuellen.
    temp_chart = st.empty()
    raw_chart = st.empty()
    status = st.empty()
    progress = st.progress(0)

    # Hier sammeln wir die Daten fuer die Diagramme.
    temp_values = []
    raw_values = []

    # Haupt-Messschleife
    for i in range(num_samples):
        try:
            raw, temp_c = read_raw_and_temp(port=port)
        except Exception as exc:
            # Bei Fehler sauber abbrechen und Meldung anzeigen.
            st.error(f"Messung fehlgeschlagen bei Punkt {i + 1}: {exc}")
            break

        # Neuen Messwert an Datenlisten anhaengen.
        raw_values.append(raw)
        temp_values.append(temp_c)

        # Live-Plot aktualisieren.
        temp_chart.line_chart({"temp_c": temp_values})
        raw_chart.line_chart({"raw": raw_values})

        # Laufende Statusanzeige fuer schnelle Rueckmeldung.
        status.write(f"Punkt {i + 1}/{num_samples}: raw={raw} temp={temp_c:.2f} degC")

        # Fortschrittsbalken aktualisieren.
        progress.progress(int(((i + 1) / num_samples) * 100))

        # Pause bis zur naechsten Messung.
        time.sleep(interval_s)
else:
    # Hinweis, solange noch keine Messung gestartet wurde.
    st.info("Pico per USB verbinden und dann auf 'Messung starten' klicken.")
