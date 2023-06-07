import urllib.request
import zipfile
import os


def download_zip(url, destination_folder):
    """Download a ZIP file from the given URL and save it to the destination folder."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    zip_filename = os.path.join(destination_folder, os.path.basename(url))
    urllib.request.urlretrieve(url, zip_filename)
    print(f"Downloaded ZIP file: {zip_filename}")

    return zip_filename


def extract_zip(zip_file, destination_folder):
    """Extract the ZIP file to the destination folder."""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    print(f"Extracted ZIP file to: {destination_folder}")


# Beispielaufruf zum Herunterladen der ZIP-Datei
download_url = "https://upload.uni-jena.de/data/641c17ff33dd02.60763151/GEO419A_Testdatensatz.zip"
destination_directory = "C:/Users/natas/OneDrive/Dokumente/Master_Geoinformatik/1. Semester/Python"
zip_file = download_zip(download_url, destination_directory)
extract_zip(zip_file, destination_directory)
