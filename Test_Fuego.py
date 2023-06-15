import urllib.request
import zipfile
import os

import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
import pandas as ps


def download_zip(url, destination_folder):
    """Download a ZIP file from the given URL and save it to the destination folder."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    zip_filename = os.path.join(destination_folder, os.path.basename(url))

    if os.path.exists(zip_filename):
        print(f"{zip_filename} file already exists. Skipping download.")
    else:
        urllib.request.urlretrieve(url, zip_filename)
        print(f"Downloaded ZIP file: {zip_filename}")

    return zip_filename


def extract_zip(zip_file, destination_folder):
    """Extract the ZIP file to the destination folder, if not already extracted."""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        for file_name in zip_contents:
            if not file_name.startswith("__MACOSX") and file_name.endswith(".tif"):
                extracted_file = os.path.join(destination_folder, file_name)
                if os.path.exists(extracted_file):
                    print(f"{extracted_file} already extracted. Skipping extraction.")
                else:
                    zip_ref.extract(file_name, destination_folder)
                    print(f"Extracted file: {extracted_file}")
            return extracted_file


# Beispielaufruf zum Herunterladen und Entpacken der ZIP-Datei
download_url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
destination_folder = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python"
zip_file = download_zip(download_url, destination_folder)


if zip_file:
    extracted_tiff_file = extract_zip(zip_file, destination_folder)

    # TIFF-Bild als Numpy-Array einlesen
    tiff_data = tiff.imread(extracted_tiff_file)

    tiff_array = np.array(tiff_data)


# Überprüfen und Ersetzen von Nullwerten
tiff_log = np.where(tiff_array > 0, tiff_array, 1e-10)

# Logarithmische Skalierung
gamma_dB0 = 10 * np.log10(tiff_log)

plt.imshow(gamma_dB0, cmap='gray')

# Neues berechnetes Bild in eine neue TIFF-Datei schreiben
output_file = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python/graphik.tif"
tiff.imsave(output_file, gamma_dB0)

plt.show()