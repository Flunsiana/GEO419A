# Python Standardbibliotheken
import os
import urllib.request
import zipfile

# Drittanbieter-Bibliotheken
import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff
from skimage.transform import resize


# Funktion zum Herunterladen der Zip-Datei der angegebenen URL und Speichern im Zielordner, falls noch nicht geschehen
def download_zip(url, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    zip_filename = os.path.join(destination_folder, os.path.basename(url))

    if os.path.exists(zip_filename):
        print(f"{zip_filename}\nFile already exists. Skipping download.")
    else:
        urllib.request.urlretrieve(url, zip_filename)
        print(f"Downloaded ZIP file:\n{zip_filename}")

    return zip_filename


# Funktion zum Entpacken der Zip-Datei im Zielordner, falls noch nicht geschehen
def extract_zip(zip_file, destination_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        for file_name in zip_contents:
            if not file_name.startswith("__MACOSX") and file_name.endswith(".tif"):
                extracted_file = os.path.join(destination_folder, file_name)
                if os.path.exists(extracted_file):
                    print(f"{extracted_file}\nFile already extracted. Skipping extraction.")
                else:
                    zip_ref.extract(file_name, destination_folder)
                    print(f"Extracted file:\n{extracted_file}")
            return extracted_file


# Download-URL
download_url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
# Ordnerpfad
download_folder = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python"
# ZIP-Datei herunterladen
zip_file_path = download_zip(download_url, download_folder)

# TIFF-Datei aus der ZIP-Datei extrahieren
extracted_tiff_file = extract_zip(zip_file_path, download_folder)

# TIFF-Bild als Numpy-Array einlesen
tiff_data = tiff.imread(extracted_tiff_file)

# Numpy-Array erstellen
tiff_array = np.array(tiff_data)

# Überprüfen und Ersetzen von Nullwerten mit np.nan
tiff_log = np.where(tiff_array != 0, tiff_array, np.nan)

# Logarithmische Skalierung
gamma_dB0 = 10 * np.log10(tiff_log)

# Auflösung reduzieren
reduced_resolution = (20000, 20000)
gamma_dB0_resized = resize(gamma_dB0, reduced_resolution)

# Wertebereich überprüfen
min_value = np.nanmin(gamma_dB0_resized)
max_value = np.nanmax(gamma_dB0_resized)
print("Min Value:", min_value)
print("Max Value:", max_value)

# Bild anzeigen
plt.imshow(gamma_dB0_resized, cmap='gray')

# Farbskala erstellen
scale = plt.colorbar(label='dB')

# Abstand zwischen Farbskalen-Beschriftung und Farbskala erhöhen
scale.ax.yaxis.set_label_coords(4, 0.5)

# Begrenzung der Farbskala auf den Wertebereich
plt.clim(min_value, max_value)

# Titel, fette Schrift und Abstand zur Grafik
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
plt.imshow(np.isnan(gamma_dB0_resized), cmap='gray', alpha=0.2, vmin=0, vmax=1)

# Als png speichern
output_file = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python/graphik_reduced_resolution.png"
plt.savefig(output_file, dpi=300)

# Grafik anzeigen
plt.show()
