# RaspyPico Minimal Setup

Dieses Projekt ist absichtlich minimal:

- USB-Verbindung zum Raspberry Pi Pico (MicroPython)
- Code aus einem Notebook auf dem Pico ausfuehren
- LED-Blink-Test

## 1) Voraussetzungen

- Raspberry Pi Pico ist per USB angeschlossen.
- Auf dem Pico laeuft **MicroPython**.

### MicroPython auf den Pico flashen (Windows)

1. Passende Download-Seite waehlen:
   - Raspberry Pi Pico: https://micropython.org/download/RPI_PICO/
2. Auf der Seite unter **Releases** die neueste `.uf2` Datei herunterladen.
3. Pico vom USB trennen.
4. **BOOTSEL-Taste** auf dem Board gedrueckt halten.
   - Die Taste ist auf dem Board mit `BOOTSEL` beschriftet (nahe USB-Anschluss).
5. Waehrend die Taste gedrueckt ist, Pico per USB wieder anschliessen.
6. Taste loslassen, sobald in Windows ein neues Laufwerk (meist `RPI-RP2`) erscheint.
7. Die heruntergeladene `.uf2` Datei auf dieses Laufwerk kopieren.
8. Nach dem Kopieren startet der Pico automatisch neu und das `RPI-RP2` Laufwerk verschwindet wieder.

Danach sollte der Pico als serieller Port (COMx) auftauchen.

## 2) Umgebung installieren

```powershell
uv sync
.\.venv\Scripts\Activate.ps1
python -m ipykernel install --user --name raspypico --display-name "Python (raspypico)"
```

`uv sync` installiert auch `mpremote` (wird im Notebook genutzt, um Code auf dem Pico auszufuehren).

## Was ist `mpremote`?

`mpremote` ist das offizielle MicroPython-CLI-Tool, um ein Board (z. B. Pico) ueber USB/Serial fernzusteuern.
Damit kann man unter anderem:

- Geraete finden: `mpremote connect list`
- Ein Geraet verbinden (automatisch): `mpremote connect auto ...`
- Python-Code direkt auf dem Pico ausfuehren: `mpremote exec "print('hello')"`
- Dateien auf das Board kopieren und verwalten

Offizielle Doku:
- https://docs.micropython.org/en/latest/reference/mpremote.html

## 3) Notebook starten

- `test_pico.ipynb` oeffnen
- Kernel: **Python (raspypico)** waehlen
- Zellen von oben nach unten ausfuehren

## Hinweise

- Wenn keine Verbindung gefunden wird, zeigt die erste Notebook-Zelle die Ausgabe von `mpremote connect list`.
- Der LED-Test nutzt `Pin("LED")` und faellt auf `Pin(25)` zurueck.

## Was bei `run_on_pico(...)` passiert

Im Notebook wird ein Python-String gebaut, zum Beispiel:

```python
code = f'''
...
print(f"{{t:.3f}},{{raw}},{{temp_c:.2f}}")
...
'''
out, err = run_on_pico(code, port=port, exec_timeout_s=20)
```

Wichtig:

- Dieser `code`-String wird auf dem **Pico** ausgefuehrt, nicht im Notebook-Kernel.
- `run_on_pico(...)` ruft intern `python -m mpremote connect auto exec <code>` auf.
- `out` ist die Text-Ausgabe vom Pico (stdout), `err` sind Fehlermeldungen (stderr).
- Zum schnellen Verstehen reicht oft:

```python
print(out)
```

Warum `{{...}}` im inneren `print(f"...")`?

- Der aeussere String ist schon ein `f'''...'''` im Notebook.
- Mit doppelten Klammern bleiben die Platzhalter fuer den Pico erhalten.
- Ohne doppelte Klammern versucht das Notebook, z. B. `{t}`, selbst auszuwerten (`NameError` moeglich).

