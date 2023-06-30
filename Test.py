# Python Standardbibliotheken
import os
import urllib.request
import zipfile

# Drittanbieter-Bibliotheken
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import tifffile as tiff
#from skimage.transform import resize
from PIL import Image


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
        Funktion zur Verarbeitung der TIFF-Datei

        Args:
            tiff_file (str): Der Pfad zur TIFF-Datei
            destination_folder (str): Der Pfad zum Zielordner, in dem die Ergebnisgrafik gespeichert werden soll

        Returns:
            None
        """
    if not os.path.exists(tiff_file):
        print("Die TIFF-Datei wurde nicht gefunden.")
        return

    # TIFF-Bild als Numpy-Array einlesen
    tiff_data = rasterio.open(tiff_file).read(1)

    # Numpy-Array erstellen
    tiff_array = np.array(tiff_data)

    # Überprüfen und Ersetzen von Nullwerten mit np.nan
    tiff_log = np.where(tiff_array != 0, tiff_array, np.nan)

    # Logarithmische Skalierung
    gamma_dB0 = 10 * np.log10(tiff_log)

    # Wertebereich überprüfen
    min_value = np.nanmin(gamma_dB0)
    max_value = np.nanmax(gamma_dB0)
    print("Min-Wert:", min_value)
    print("Max-Wert:", max_value)

    # Farbskala erstellen
    plt.imshow(gamma_dB0, cmap='gray')

    # Begrenzung der Farbskala auf den Wertebereich
    plt.clim(min_value, max_value)

    # Titel, Fettdruck und Abstand zur Grafik einstellen
    plt.title('Logarithmisch skaliertes Satellitenbild', fontweight='bold', y=1.05)

    # Achsenbeschriftung und Abstand zwischen Achsenbeschriftungen und Farbskala erhöhen
    plt.xlabel('X-Koordinate', labelpad=10)
    plt.ylabel('Y-Koordinate', labelpad=10)

    # Rahmen um die Grafik einstellen
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)

    # Farbkodierung der "no data"-Bereiche
    plt.imshow(np.isnan(gamma_dB0), cmap='gray', alpha=0.2, vmin=0, vmax=1)

    # Farbskala erstellen
    scale = plt.colorbar(label='dB')

    # Begrenzung der Farbskala auf den Wertebereich
    plt.clim(min_value, max_value)

    # Als GeoTIFF speichern
    output_file = os.path.join(destination_folder, "graphik.tif")
    with rasterio.open(output_file, 'w', driver='GTiff', width=gamma_dB0.shape[1], height=gamma_dB0.shape[0],
                       count=1, dtype=gamma_dB0.dtype) as dst:
        dst.write(gamma_dB0, 1)

    # Grafik anzeigen

    plt.show()

    # Als png speichern
    output_file = os.path.join(destination_folder, "graphik_reduced_resolution_v2.png")
    plt.savefig(output_file, dpi=300)


def main(destination_folder):
    """
        Hauptfunktion, die den Ablauf des Programms steuert

        Args:
            destination_folder (str): Der Pfad zum Zielordner, der als Kommandozeilenargument übergeben wurde

        Returns:
            None
        """
    # Download-URL
    download_url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"

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
