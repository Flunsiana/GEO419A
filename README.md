# Modulare Programmierung in der Fernerkundung: Dateninterpretation 419A #

Dieses Python-Skript dient dazu, eine heruntergeladene ZIP-Datei zu entpacken, eine TIFF-Datei als numpy-Array einzulesen, um diese anschließend nach der Rückstreuintensität zu logarithmisieren und das Ergebnis als Bild abzuspeichern.

## Anforderungen 

- Python 3.x
- CMD.exe Prompt 0.1.1
- Python-Pakete: `os`, `urllib.request`, `zipfile`, `matplotlib.pyplot`, `numpy`, `tifffile`, `skimage.transform`

## conda ##

- conda env create -f 419A.yml
- conda activate 419A

# Verwendung

1. Laden Sie die die Dateien `main.py` und `419.yml` aus Github herunter
2. Erstellen und aktivieren Sie die Conda-Umgebung 
3. Öffnen Sie das Python-Skript in der heruntergeladenen Conda Umgebung
4. Geben Sie die Download-URL, den Pfad zum Zielordner und den Speicherpfad der PNG_Datei in den entsprechenden Variablen `download_url`, `download_folder` und `output_file` an
5. Führen Sie das Programm aus

Das Programm lädt die ZIP-Datei herunter, entpackt sie, liest die TIFF-Datei ein und führt die erforderlichen Verarbeitungsschritte durch. Das resultierende Bild wird angezeigt und als PNG-Datei gespeichert.

