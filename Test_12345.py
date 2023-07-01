# Python Standardbibliotheken
import os
import urllib.request
import zipfile

# Drittanbieter-Bibliotheken
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.crs import CRS


# Funktion zum Herunterladen der Zip-Datei der angegebenen URL und Speichern im Zielordner, falls noch nicht geschehen
def download_zip(url, destination_folder):
    """
        Funktion zum Herunterladen der Zip-Datei der angegebenen URL und Speichern im Zielordner

        Args:
            url (str): Die URL der Zip-Datei
            destination_folder (str): Der Pfad zum Zielordner, in dem die Zip-Datei gespeichert werden soll

        Returns:
            str: Der Pfad zur heruntergeladenen Zip-Datei
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    zip_filepath = os.path.join(destination_folder, os.path.basename(url))

    if os.path.exists(zip_filepath):
        print(f"{zip_filepath}\nDatei existiert bereits. Download übersprungen.")
    else:
        urllib.request.urlretrieve(url, zip_filepath)
        print(f"Heruntergeladene ZIP-Datei:\n{zip_filepath}")

    return zip_filepath


# Funktion zum Entpacken der Zip-Datei im Zielordner, falls noch nicht geschehen
def extract_zip(zip_file, destination_folder):
    """
        Funktion zum Entpacken der Zip-Datei im Zielordner

        Args:
            zip_file (str): Der Pfad zur Zip-Datei
            destination_folder (str): Der Pfad zum Zielordner, in dem die Dateien entpackt werden sollen

        Returns:
            str: Der Pfad zur extrahierten TIFF-Datei
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        for file_name in zip_contents:
            if not file_name.startswith("__MACOSX") and file_name.endswith(".tif"):
                extracted_file = os.path.join(destination_folder, file_name)
                if os.path.exists(extracted_file):
                    print(f"{extracted_file}\nDatei bereits entpackt. Entpacken übersprungen.")
                else:
                    zip_ref.extract(file_name, destination_folder)
                    print(f"Entpackte Datei:\n{extracted_file}")
            return extracted_file


# Funktion zur Verarbeitung der TIFF-Datei
def process_tiff_file(tiff_file, destination_folder):
    """
        Funktion zur Verarbeitung der TIFF-Datei, führt logarithmische Skalierung durch,
        zeigt das Bild an und speichert es als GeoTIFF und PNG

        Args:
            tiff_file (str): Der Pfad zur TIFF-Datei
            destination_folder (str): Der Pfad zum Zielordner, in dem die Ausgabedateien gespeichert werden soll

        Returns:
            None
    """
    if not os.path.exists(tiff_file):
        print("Die TIFF-Datei wurde nicht gefunden.")
        return

    with rasterio.open(tiff_file) as src:
        # TIFF-Bild als Numpy-Array einlesen
        img_array = src.read(1)

    # Logarithmus-Transformation anwenden
    log_img = 10 * np.log10(img_array)

    # Plot erstellen
    plt.figure(figsize=(8, 8))
    plt.imshow(log_img, cmap='gray', extent=[src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top])
    plt.xlabel('X-Koordinate', labelpad=10)
    plt.ylabel('Y-Koordinate', labelpad=10)
    # Titel, Fettdruck und Abstand zur Grafik einstellen
    plt.title('Logarithmisch skaliertes Satellitenbild', fontweight='bold', y=1.05)
    plt.colorbar(label='dB')

    # Als png speichern
    output_file_png = os.path.join(destination_folder, "graphik_reduced_resolution.png")
    plt.savefig(output_file_png, dpi=300)

    # Grafik anzeigen
    plt.show()


def main(destination_folder):
    """
        Hauptfunktion, die den Ablauf des Programms steuert

        Args:
            destination_folder (str): Der Pfad zum Zielordner, der als Kommandozeilenargument übergeben wurde

        Returns:
            None
        """
    # Download-URL
    download_url = "https://upload.uni-jena.de/data/649ad4879284a9.22886089/GEO419A_Testdatensatz.zip"

    # ZIP-Datei herunterladen
    zip_file_path = download_zip(download_url, destination_folder)

    # TIFF-Datei aus der ZIP-Datei extrahieren
    extracted_tiff_file = extract_zip(zip_file_path, destination_folder)

    if extracted_tiff_file:
        # TIFF-Datei verarbeiten
        process_tiff_file(extracted_tiff_file, destination_folder)
    else:
        print("Keine TIFF-Datei gefunden.")


def get_destination_folder():
    return os.getcwd()


# Den Zielordner abrufen
if __name__ == '__main__':
    destination_folder = get_destination_folder()

    # Die Hauptfunktion mit dem Zielordner aufrufen
    main(destination_folder)