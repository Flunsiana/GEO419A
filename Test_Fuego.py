# python standard libraries
import os
import urllib.request
import zipfile

# third-party libraries
import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff
from skimage.transform import resize


def download_zip(url, destination_folder):
    """Download a ZIP file from the given URL and save it to the destination folder."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    zip_filename = os.path.join(destination_folder, os.path.basename(url))

    if os.path.exists(zip_filename):
        print(f"{zip_filename}\nfile already exists. Skipping download.")
    else:
        urllib.request.urlretrieve(url, zip_filename)
        print(f"Downloaded ZIP file:\n{zip_filename}")

    return zip_filename


def extract_zip(zip_file, destination_folder):
    """Extract the ZIP file to the destination folder, if not already extracted."""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        for file_name in zip_contents:
            if not file_name.startswith("__MACOSX") and file_name.endswith(".tif"):
                extracted_file = os.path.join(destination_folder, file_name)
                if os.path.exists(extracted_file):
                    print(f"{extracted_file}\nalready extracted. Skipping extraction.")
                else:
                    zip_ref.extract(file_name, destination_folder)
                    print(f"Extracted file:\n{extracted_file}")
            return extracted_file


# Beispielaufruf zum Herunterladen und Entpacken der ZIP-Datei
download_url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
download_folder = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python"
zip_file_path = download_zip(download_url, download_folder)

extracted_tiff_file = extract_zip(zip_file_path, download_folder)

# TIFF-Bild als Numpy-Array einlesen
tiff_data = tiff.imread(extracted_tiff_file)

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

plt.imshow(gamma_dB0_resized, cmap='gray')

# Farbskala erstellen
scale = plt.colorbar(label='dB')
# Abstand zwischen Farbskalen-Beschriftung und Farbskala erhöhen
scale.ax.yaxis.set_label_coords(4, 0.5)

# Begrenzung der Farbskala auf den Wertebereich
plt.clim(min_value, max_value)

# Titel und dicke Schrift und Abstand zur Grafik
plt.title('Logarithmisch skaliertes Satellitenbild', fontweight='bold', y=1.05)

# Achsenbeschriftung und Abstand zwischen Achsenbeschriftungen und Farbskala erhöhen
plt.xlabel('X-Koordinate', labelpad=10)
plt.ylabel('Y-Koordinate', labelpad=10)

# Rahmens um die Grafik einstellen
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# Farbkodierung der "no data"-Bereiche
plt.imshow(np.isnan(gamma_dB0_resized), cmap='gray', alpha=0.2, vmin=0, vmax=1)

# als png abspeichern
output_file = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python/graphik_reduced_resolution.png"
plt.savefig(output_file, dpi=300)

plt.show()
