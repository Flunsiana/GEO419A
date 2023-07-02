# Python Standardbibliotheken
import os
import urllib.request
import zipfile
import sys

# Drittanbieter-Bibliotheken
import matplotlib.pyplot as plt
import numpy as np
import rasterio


# Funktion zum Herunterladen der Zip-Datei der angegebenen URL und Speichern im Zielordner, falls noch nicht geschehen
def download_zip(url, destination_folder_download):
    """
        Funktion zum Herunterladen der Zip-Datei der angegebenen URL und Speichern im Zielordner

        Args:
            url (str): Die URL der Zip-Datei
            destination_folder_download (str): Der Pfad zum Zielordner, in dem die Zip-Datei gespeichert werden soll

        Returns:
            str: Der Pfad zur heruntergeladenen Zip-Datei
    """
    if not os.path.exists(destination_folder_download):
        os.makedirs(destination_folder_download)

    zip_filepath = os.path.join(destination_folder_download, os.path.basename(url))

    if os.path.exists(zip_filepath):
        print(f"{zip_filepath}\nDatei existiert bereits. Download übersprungen.")
    else:
        urllib.request.urlretrieve(url, zip_filepath)
        print(f"Heruntergeladene ZIP-Datei:\n{zip_filepath}")

    return zip_filepath


# Funktion zum Entpacken der Zip-Datei im Zielordner, falls noch nicht geschehen
def extract_zip(zip_file, destination_folder_extract):
    """
        Funktion zum Entpacken der Zip-Datei im Zielordner

        Args:
            zip_file (str): Der Pfad zur Zip-Datei
            destination_folder_extract (str): Der Pfad zum Zielordner, in dem die Dateien entpackt werden sollen

        Returns:
            str: Der Pfad zur extrahierten TIFF-Datei
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        for file_name in zip_contents:
            if not file_name.startswith("__MACOSX") and file_name.endswith(".tif"):
                extracted_file = os.path.join(destination_folder_extract, file_name)
                if os.path.exists(extracted_file):
                    print(f"{extracted_file}\nDatei bereits entpackt. Entpacken übersprungen.")
                else:
                    zip_ref.extract(file_name, destination_folder_extract)
                    print(f"Entpackte Datei:\n{extracted_file}")
            return extracted_file


# Funktion zur Verarbeitung der TIFF-Datei
def process_tiff_file(tiff_file, destination_folder_tiff):
    """
        Funktion zur Verarbeitung der TIFF-Datei

        Args:
            tiff_file (str): Der Pfad zur TIFF-Datei
            destination_folder_tiff (str): Der Pfad zum Zielordner, in dem die Ausgabedateien gespeichert werden soll

        Returns:
            None
    """
    if not os.path.exists(tiff_file):
        print("Die TIFF-Datei wurde nicht gefunden.")
        return

    with rasterio.open(tiff_file) as src:
        # TIFF-Bild als Numpy-Array einlesen
        img_array = src.read(1)

    # Überprüfen und Ersetzen von Nullwerten mit np.nan
    null_img = np.where(img_array != 0, img_array, np.nan)

    # Logarithmus-Transformation anwenden
    log_img = 10 * np.log10(null_img)

    # Plot erstellen, Farbskala setzen und Ausdehnung definieren
    plt.imshow(log_img, cmap='gray', extent=[src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top])

    # Achsenbeschriftung und Abstand zwischen Achsenbeschriftungen erhöhen
    plt.xlabel('X-Koordinate', labelpad=10)
    plt.ylabel('Y-Koordinate', labelpad=10)

    # Titel, Fettdruck und Abstand zur Grafik einstellen
    plt.title('Logarithmisch skaliertes Satellitenbild', fontweight='bold', y=1.05)
    plt.colorbar(label='VH-Backscatter [dB]')

    # Rahmen um die Grafik einstellen
    ax = plt.gca()
    ax.spines['top'].set_visible(0.5)
    ax.spines['right'].set_visible(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)

    # Als png speichern
    output_file_png = os.path.join(destination_folder_tiff, "Satellitenbild_log.png")
    plt.savefig(output_file_png, dpi=300)

    # Grafik anzeigen
    plt.show()


def main(destination_folder_main):
    """
        Hauptfunktion, die den Ablauf des Programms steuert

        Args:
            destination_folder_main (str): Der Pfad zum Zielordner

        Returns:
            None
    """
    # Download-URL
    download_url = "https://upload.uni-jena.de/data/649ad4879284a9.22886089/GEO419A_Testdatensatz.zip"

    # ZIP-Datei herunterladen
    zip_file_path = download_zip(download_url, destination_folder_main)

    # TIFF-Datei aus der ZIP-Datei extrahieren
    extracted_tiff_file = extract_zip(zip_file_path, destination_folder_main)

    if extracted_tiff_file:
        # TIFF-Datei verarbeiten
        process_tiff_file(extracted_tiff_file, destination_folder_main)
    else:
        print("Keine TIFF-Datei gefunden.")


# Den Zielordner abrufen
if __name__ == '__main__':
    # Überprüfen, ob ein Befehlszeilenargument für den Zielordner angegeben wird
    if len(sys.argv) > 1:
        destination_folder = sys.argv[1]
    else:
        # Falls kein Zielordner angegeben wird, das aktuelle Arbeitsverzeichnis verwenden
        destination_folder = os.getcwd()

    # Die main-Funktion wird aufgerufen und dem Zielordner übergeben
    main(destination_folder)
