# Modulare Programmierung in der Fernerkundung: Dateninterpretation 419A #

Dieses Python-Skript dient dazu, eine heruntergeladene ZIP-Datei zu entpacken, eine TIFF-Datei als numpy-Array einzulesen, um diese anschließend nach der Rückstreuintensität zu logarithmisieren und das Ergebnis als Bild abzuspeichern.

## conda ##

conda env create -f 419A.yml
\n conda activate 419A

# PyCharm #

1. Importieren von folgenden Python-Standardbibliotheken und Drittanbieterbibliotheken:

- os: Zur Interaktion mit dem Betriebssystem (Interaktion mit Datei- und Ordnerpfaden , Verzeichnisse erstellen, Dateistatus prüfen und Pfadmanipulationen, hier um sicherzustellen, dass die benötigten Ordner vorhanden sind und um den Dateistatus zu überprüfen, bevor der Download und die Extraktion erfolgen)
- urllib.request: Zum Herunterladen von Dateien von einer URL
- zipfile: Zum Entpacken von ZIP-Dateien
- matplotlib.pyplot: Zur Erstellung von Plots
- numpy: Zur Arbeit mit Arrays
- tifffile: Zum Lesen von TIFF-Bilddateien
- skimage.transform.resize: Zur Änderung der Auflösung eines Bildes

2. Funktion download_zip(url, destination_folder) definieren, um eine ZIP-Datei von der gegebenen URL herunterzuladen und in den angegebenen Zielordner zu speichern:

- Überprüfung, ob der Zielordner bereits vorhanden ist. Wenn nicht, wird ein neuer Ordner erstellt
- Überprüfung, ob die ZIP-Datei bereits im Zielordner vorhanden ist. Wenn ja, wird die Meldung zurückgegeben, dass der Download übersprungen werden soll
- Andernfalls wird die ZIP-Datei von der URL heruntergeladen und speichert diese im Zielordner ab

3. Funktion extract_zip(zip_file, destination_folder) definieren, um die ZIP-Datei in den angegebenen Zielordner zu entpacken:

- Öffnen der ZIP-Datei
- Überprüfung des Inhalts der ZIP-Datei
- Filterung nach Dateiendung und dem Ausschluss von "__MACOSX"-Dateien, um sicherzustellen, dass nur die relevanten TIFF-Dateien extrahiert werden
- Datei "__MACOSX" wird von macOS-Betriebssystemen erstellt und ist in ZIP-Archiven oft sichtbar. Diese enthält Metadaten, die für das macOS Betriebssystem relevant sind, aber für die Verarbeitung der TIFF-Bilddateien nicht benötigt werden und daher ausgelassen werden
- Für jede Datei im ZIP-Inhalt, die nicht mit "__MACOSX" beginnt und die Endung ".tif" hat:
  - Überprüfung, ob die extrahierte Datei bereits im Zielordner vorhanden ist. Wenn ja, wird eine Meldung ausgegeben und die Extraktion überspungen
  - Andernfalls wird die Datei im Zielordner extrahiert

4. Definition der Download-URL der ZIP-Datei und des Zielordners, in dem die Datei gespeichert werden soll

5. Funktion download_zip(download_url, download_folder) wird aufgerufen, um die ZIP-Datei herunterzuladen und im Zielordner abzuspeichern

6. Funktion extract_zip(zip_file_path, download_folder) wird aufgerufen, um die ZIP-Datei im Zielordner zu entpacken und die extrahierte TIFF-Datei auszuwählen

7. Das TIFF-Bild wird als Numpy-Array mit tiff.imread(extracted_tiff_file) ausgelesen

8. Das Numpy-Array wird in einen neuen Array "tiff_array" konvertiert

9. Das Numpy-Array "tiff_array" wird auf Nullwerte geprüft und ersetzt diese durch np.nan 

10. Logarithmische Skalierung des Arrays mit 10 * np.log10(tiff_log) wird in einem neuen Array "gamma_dB0" gespeichert

11. Die Auflösung des Bildes wird mit der Funktion resize(gamma_dB0, reduced_resolution) auf eine festgelegte Größe mit "reduced_resolution" reduziert und das Ergebnis im Array "gamma_dB0_resized" gespeichert

12. Die minimalen und maximalen Werte im reduzierten Array "gamma_dB0_resized" werden mit np.nanmin(gamma_dB0_resized) und np.nanmax(gamma_dB0_resized) ausgegeben, um den Wertebereich zu kennen

13. Das reduzierte Bild wird mit plt.imshow(gamma_dB0_resized, cmap='gray') in einem Plot angezeigt

14. Eine Farbskala für den Plot wird mit plt.colorbar(label='dB') hinzugefügt

15. Die Farbskala wird an den minimalen und maximalen Wertebereich des Bildes (vmin=0 und vmax=1) mit plt.clim(min_value, max_value) angepasst

16. Dem Plot wird Titel, Achsenbeschriftungen und Rahmen hinzugefügt

17. Die "no data"-Bereiche im Bild werden mit plt.imshow(np.isnan(gamma_dB0_resized), cmap='gray', alpha=0.2, vmin=0, vmax=1) eingestellt
  - alpha=0.2 bestimmt die Transparenz der "no data"-Bereiche im Bild
  - np.isnan(gamma_dB0_resized) erzeugt ein boolsches Array mit denselben Dimensionen wie "gamma_dB0_resized", sodass die "no data"-Bereiche im Bild durch True-Werte im boolschen Array dargestellt werden

19. Plot wird als PNG-Datei mit plt.savefig(output_file, dpi=300) gespeichert

20. Mit plt.show() wird er erstellte Plot angezeigt

