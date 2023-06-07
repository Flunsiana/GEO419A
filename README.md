## 419A ##

# GitHub Repository #
- einer erstellt ein repository und läd den anderen ein
- per Mail EInladungslink akzeptieren

# Anaconda #

Auf einem Pc erstellt:

- mit cd Auf den Ordner navigieren

- conda create --name 419A
- conda activate 419A

Installation:
- conda install numpy
- conda install pandas
- conda install matplotlib
- conda install seaborn
- conda install scikit-learn
- conda install tensorflow
- conda install keras
- conda install jupyter
- conda install pylint

Um dem Anderen es weiterzuschicken:
- conda env export > 419A.yml

Der Andere öffnet es so:

- mit cd auf Ordner navigieren
- conda env create -f 419A.yml
- conda activate 419A

# PyCharm #

- arbeiten auf dem gleichen "main"
- wenn einer push macht wird es auf GitHub hochgeladen
- der andere muss dann sein Pycharm "updaten"
- wir arbeiten zusammen, weshalb wir uns absprechen können
- mit "commit" schreiben wir Kommentare dazu
