# Modulare Programmierung in der Fernerkundung: Dateninterpretation 419A #

Dieses Python-Skript dient dazu, eine heruntergeladene ZIP-Datei zu entpacken, eine TIFF-Datei als numpy-Array einzulesen, um diese anschließend nach der Rückstreuintensität zu logarithmisieren und das Ergebnis als Bild abzuspeichern.

## Anforderungen

- Python 3.x
- Python-Pakete: `os`, `urllib.request`, `zipfile`, `matplotlib.pyplot`, `numpy`, `tifffile`, `skimage.transform`

## conda ##

- conda env create -f 419A.yml
- conda activate 419A

# Verwendung

1. Laden Sie die 'main.py' und die '419.yml" herunter
3. Geben Sie die Download-URL,den Pfad zum Zielordner und den Speicherpfad der PNG_Datei in den entsprechenden Variablen `download_url`, `download_folder` und `output_file` an
4. Führen Sie das Programm aus

Das Programm lädt die ZIP-Datei herunter, entpackt sie, liest die TIFF-Datei ein und führt die erforderlichen Verarbeitungsschritte durch. Das resultierende Bild wird angezeigt und als PNG-Datei gespeichert.

