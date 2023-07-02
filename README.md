# GEO419A - Modulare Programmierung in der Fernerkundung: Dateninterpretation #

Dieses Python-Skript dient dazu, eine heruntergeladene ZIP-Datei zu entpacken, eine TIFF-Datei als numpy-Array einzulesen, um diese anschließend nach der Rückstreuintensität zu logarithmisieren und das Ergebnis zu ploten, um es als Bild abzuspeichern.

## Anforderungen ##

- Python 3.9.13 
- CMD.exe Prompt 0.1.1
- Python-Pakete: `os`, `urllib.request`, `zipfile`, `sys`, `matplotlib.pyplot`, `numpy`, `rasterio`

## Vorbereitung ##

1. Laden Sie die die Dateien `GEO419A.py`, `Input.py` und `GEO419A.yml` aus Github herunter
2. Erstellen und aktivieren Sie die Conda-Umgebung

## Conda ##

```
conda env create -f GEO419A.yml
conda activate GEO419A
```

# Ausführung #

## integrierte Entwicklungsumgebung ##

- Laden Sie beide Python-Skripte `GEO419A.py` und `Input.py` in den gleichen Arbeitsordner 
- Achten Sie darauf, dass Sie in der Conda-Umgebung GEO419A sind
- Führen Sie `Input.py` aus und geben Sie nach Aufforderung ihr Nutzerverzeichnis ein


## Kommandozeile ##

- Laden Sie das Python-Skript `GEO419A.py` in Ihren Arbeitsordner
```
cd \Pfad\Arbeitsordner\
conda activate GEO419A
python GEO419A.py
```

