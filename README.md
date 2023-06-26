# Modulare Programmierung in der Fernerkundung: Dateninterpretation 419A #

Dieses Python-Skript dient dazu, eine heruntergeladene ZIP-Datei zu entpacken, eine TIFF-Datei als numpy-Array einzulesen, um diese anschließend nach der Rückstreuintensität zu logarithmisieren und das Ergebnis als Bild abzuspeichern.

## Anforderungen ##

- Python 3.9.13 
- CMD.exe Prompt 0.1.1
- Python-Pakete: `os`, `urllib.request`, `zipfile`, `matplotlib.pyplot`, `numpy`, `tifffile`, `skimage.transform`

## conda ##

- conda env create -f 419A.yml
- conda activate 419A

## Formel ##

𝛾𝑑𝐵₀ = 10 * log₁₀(𝛾ₗ𝑖𝑛₀)

# Verwendung

1. Laden Sie die die Dateien `main.py` und `419.yml` aus Github herunter
2. Erstellen und aktivieren Sie die Conda-Umgebung 
3. Öffnen Sie das Python-Skript in der erstellten Conda-Umgebung
4. Geben Sie die Download-URL, den Pfad zum Zielordner und den Speicherpfad der PNG_Datei in den entsprechenden Variablen `download_url`, `download_folder` und `output_file` an
5. Führen Sie das Programm aus

