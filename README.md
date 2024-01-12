<h1 align="center">PyChristmas</h1>
<h3 align="center">Create a Christmas Tree using Arduino IoT Cloud, Raspberry PI, LED strips and Matrix</h3>
<h4 align="center"><i>Crea un albero di Natale usando Arduino IoT Cloud, Raspberry PI, strisce LED e matrici</i></h3>
<br>
<p align="center">
<a href="https://www.arduino.cc/"><img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white" alt="Arduino"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
<a href="https://cloud.arduino.cc/"><img src="https://img.shields.io/badge/Arduino_IoT_Cloud-00979D?style=for-the-badge&logo=arduino&logoColor=white" alt="Arduino IoT Cloud"></a>
</p>
<p align="center">
<a href="https://www.iiscastelli.edu.it/Pager.aspx?Page=mainpage"><img src="https://img.shields.io/badge/Made_For-ITIS_B._Castelli-blue?style=for-the-badge" alt="Made for ITIS B. Castelli"></a>

#### [Clicca qui per la versione in italiano](#italiano)
# ENGLISH:

# Overview
PyChristmas is an application that allows you to build and control remotely a Christmas tree using Arduino IoT Cloud.

The main application is written in Python and uses the Arduino IoT Cloud API to control the tree.

The tree is composed by a Raspberry PI, an Arduino MKR WiFi 1010, 3 LED strips, a LED matrix, a motor and a star.

# Features
- **Control the tree remotely** using Arduino IoT Cloud 
- **Change the tree color** anytime and anywhere 
- **Write a message** on the LED matrix
- **Turn on/off the star** from anywhere
- **Turn off/on the tree components altogether or separately**

# Requirements
## Software/Services
- **[Arduino IoT Cloud account](https://cloud.arduino.cc/)**
- **[Git](https://git-scm.com/)**
- **[Arduino IDE](https://www.arduino.cc/en/software)**
- **[Python](https://www.python.org/downloads/)** (version 3.9.0 or higher)
- **[Raspberry PI Imager](https://www.raspberrypi.org/software/)** (or any other software to flash the Raspberry PI)
- **Supported web browser** (Chrome, Firefox, Edge, Safari, etc.)

## Hardware
- **Breadboard**
- **Jumper wires**
- **Computer**
- **Power Supply** (that can provide at least 5V and 3A)
- **Arduino** (We used an **[Arduino MKR WiFi 1010](https://store.arduino.cc/arduino-mkr-wifi-1010)**)
- **USB cable** to power the Arduino
- **Raspberry PI**
- **LED strips** (We used 3 strips of 5m each with 60 LEDs/m)
- **Motor** (We used a 3V motor)
- **Star** (plastic or polystyrene)
- **LED matrix** (We used 2 MAX7219 LED dot matrix display made with 4 8x8 modules each)
- **3 resistors** (We used 330 Ohm resistors)
- **1 capacitor** (We used a 10nF capacitor)

# Circuit

![Circuit](images/Circuit.png)

# Installation

1. **Clone the repository**
    ```
    git clone https://github.com/CoccodrillooXDS/PyChristmas
    ```

## Arduino

2. Connect the Arduino to your computer using the USB cable
3. Open the **[Arduino IDE](https://www.arduino.cc/en/software)**
4. Select the Arduino board you are using from the dropdown menu or from **Tools > Board**
    * If you are using an Arduino MKR WiFi 1010, you may need to install the board first.
    * To do so, go to **Tools > Board > Boards Manager** and search for **Arduino SAMD Boards**. Click on **Install** and wait for the installation to complete.
5. Select the port your Arduino is connected to from the dropdown menu or from **Tools > Port**
6. Open the [arduino.ino](arduino/arduino.ino) file from the Arduino folder
7. Press the **Upload** button to verify and upload the code to Arduino
8. Wait for the upload to complete

## Raspberry PI and Python

9. Flash the Raspberry PI with the **[Raspberry PI OS](https://www.raspberrypi.org/software/)** (this README was written with **Raspberry PI OS**, formely known as **Raspbian**, in mind, but you can use any other OS)
10. Connect the Raspberry PI to a monitor, a keyboard and a mouse (optional if you want to use the Raspberry PI headless via SSH)
11. Connect the Raspberry PI to the internet (you can use an ethernet cable or connect to a WiFi network)
12. Open the terminal or connect to the Raspberry PI via SSH
13. Install Python 3, pip and git
    ```
    sudo apt install python3 python3-pip git
    ```
14. **Clone the repository**
    ```
    git clone https://github.com/CoccodrillooXDS/PyChristmas
    ```
15. Move to the **PyChristmas** folder
    ```
    cd /path/to/PyChristmas
    ```
16. Install the required Python packages
    ```
    pip3 install -r requirements.txt
    ```

## Arduino IoT Cloud
17. Open the **[Arduino IoT Cloud](https://cloud.arduino.cc/)**
18. Log in with your Arduino account or create one if you don't have one
19. Go to the IoT Cloud dashboard
20. Go to **Devices** and click on **ADD DEVICE**
    ![Add device](images/Arduino_IoT_Cloud/001.jpg)
21. Select "**Any Device**" under **MANUAL** and click on **CONTINUE**
    ![Manual](images/Arduino_IoT_Cloud/002.jpg)
22. Select a name for your device and click on **NEXT**
    ![Create device](images/Arduino_IoT_Cloud/003.jpg)
23. Save the **Device ID** and the **Device Secret** somewhere safe (we will need them later)
    ![Device ID and Device Secret](images/Arduino_IoT_Cloud/004.jpg)
24. Check the **I saved my device ID and Secret Key** box and press **CONTINUE**
25. Click on **GOT IT**
    ![Got it](images/Arduino_IoT_Cloud/005.jpg)
26. In the new page, click on **Create thing**
    ![Create thing](images/Arduino_IoT_Cloud/006.jpg)
27. In **Cloud Variables**, click on **ADD** and create 5 new **Read & Write** variables with **On change** Variable Update Policy:
    - **cambioIstantaneo** (bool)
    - **coloreLED** (CloudColoredLight)
    - **controlloGenerale** (bool)
    - **motoreStella** (bool)
    - **testoMatrice** (String)
    ![Add variable](images/Arduino_IoT_Cloud/007.jpg)
28. Create a new Dashboard by clicking on **CREATE DASHBOARD** under **Dashboards**
    ![Add dashboard](images/Arduino_IoT_Cloud/008.jpg)
29. Add three **Switch** widgets, one **Colored light** widget and a **Messenger** widget to the dashboard
    ![Add widgets](images/Arduino_IoT_Cloud/009.jpg)

## Embedding the Device ID and Device Secret in the Python code
30. Open the **[software.py](software.py)** file using a text editor or '*nano*' (if you are using the terminal)
    ```
    nano software.py
    ```
31. Replace the **DEVICE_ID** and **DEVICE_SECRET** variables with the ones you saved earlier (Step 23). DO NOT REMOVE THE "**b**" BEFORE THE QUOTES
    ```python
    DEVICE_ID = b"REPLACE WITH YOUR DEVICE ID"
    SECRET_KEY = b"REPLACE WITH YOUR SECRET KEY"
    ```
32. Save the file and exit (if you are using '*nano*', press **CTRL + X**, then **Y** and then **ENTER**)

## Running the application
33. Connect the Arduino to the Raspberry PI using the USB cable
34. Connect everything as shown in the **[circuit](#circuit)** section
35. Run the application
    ```
    python3 software.py
    ```

**NOTE**: You can also run the application in the background by adding a **&** at the end of the command, like this:
```
python3 software.py &
```

# Final result
![Final result](images/Tree.png)
*Unfortunately, the bottom LED strip broke during the assembly.*

## Contributing
You can contribute to the project by creating a pull request or an issue.

To contribute, you can fork the repository and after you made your changes, you can create a pull request.

## License
This project is licensed under the **MIT License**. See the **[LICENSE](LICENSE)** file for more information.

# ITALIANO:

# Panoramica
PyChristmas è un'applicazione che ti permette di costruire e controllare a distanza un albero di Natale usando Arduino IoT Cloud.

L'applicazione principale è scritta in Python e usa le API di Arduino IoT Cloud per controllare l'albero.

L'albero è composto da un Raspberry PI, un Arduino MKR WiFi 1010, 3 strisce LED, una matrice LED, un motore e una stella.

# Caratteristiche
- **Controlla l'albero a distanza** usando Arduino IoT Cloud
- **Cambia il colore dell'albero** in qualsiasi momento e ovunque
- **Scrivi un messaggio** sulla matrice LED
- **Accendi/spegni la stella** da qualsiasi luogo
- **Accendi/spegni i componenti dell'albero** tutti insieme o separatamente

# Requisiti
## Software/Servizi
- **[Account Arduino IoT Cloud](https://cloud.arduino.cc/)**
- **[Git](https://git-scm.com/)**
- **[Arduino IDE](https://www.arduino.cc/en/software)**
- **[Python](https://www.python.org/downloads/)** (versione 3.9.0 o superiore)
- **[Raspberry PI Imager](https://www.raspberrypi.org/software/)** (o qualsiasi altro software per flashare il Raspberry PI)
- **Browser web supportato** (Chrome, Firefox, Edge, Safari, etc.)

## Hardware
- **Breadboard**
- **Cavi jumper**
- **Computer**
- **Alimentatore** (che possa fornire almeno 5V e 3A)
- **Arduino** (Abbiamo usato un **[Arduino MKR WiFi 1010](https://store.arduino.cc/arduino-mkr-wifi-1010)**)
- **Cavo USB** per alimentare l'Arduino
- **Raspberry PI**
- **Strisce LED** (Abbiamo usato 3 strisce da 5m ciascuna con 60 LED/m)
- **Motore** (Abbiamo usato un motore da 3V)
- **Stella** (di plastica o polistirolo)
- **Matrice LED** (Abbiamo usato 2 matrici LED MAX7219 fatte con 4 moduli 8x8 ciascuna)
- **3 resistori** (Abbiamo usato resistori da 330 Ohm)
- **1 condensatore** (Abbiamo usato un condensatore da 10nF)

# [Circuito](#circuit)

# Installazione
1. **Clona la repository**
    ```
    git clone https://github.com/CoccodrillooXDS/PyChristmas
    ```

## Arduino

2. Collega l'Arduino al computer usando il cavo USB
3. Apri l'**[Arduino IDE](https://www.arduino.cc/en/software)**
4. Seleziona la scheda Arduino che stai usando dal menu a tendina o da **Tools > Board**
    * Se stai usando un Arduino MKR WiFi 1010, potresti dover installare la scheda prima.
    * Per farlo, vai su **Tools > Board > Boards Manager** e cerca **Arduino SAMD Boards**. Clicca su **Install** e aspetta che l'installazione sia completata.
5. Seleziona la porta a cui è collegato l'Arduino dal menu a tendina o da **Tools > Port**
6. Apri il file [arduino.ino](arduino/arduino.ino) dalla cartella Arduino
7. Premi il pulsante **Upload** per verificare e caricare il codice su Arduino
8. Aspetta che il caricamento sia completato

## Raspberry PI e Python

9. Flasha il Raspberry PI con il **[Raspberry PI OS](https://www.raspberrypi.org/software/)** (questo README è stato scritto con in mente il **Raspberry PI OS**, precedentemente noto come **Raspbian**, ma puoi usare qualsiasi altro OS)
10. Collega il Raspberry PI a un monitor, una tastiera e un mouse (opzionale se vuoi usare il Raspberry PI headless via SSH)
11. Collega il Raspberry PI ad internet (puoi usare un cavo ethernet o connetterti ad una rete WiFi)
12. Apri il terminale o connettiti al Raspberry PI via SSH
13. Installa Python 3, pip e git
    ```
    sudo apt install python3 python3-pip git
    ```
14. **Clona la repository**
    ```
    git clone https://github.com/CoccodrillooXDS/PyChristmas
    ```
15. Entra nella cartella **PyChristmas**
    ```
    cd /dove/è/presente/la/cartella/PyChristmas
    ```
16. Installa i pacchetti Python richiesti
    ```
    pip3 install -r requirements.txt
    ```

## Arduino IoT Cloud
17. Apri l'**[Arduino IoT Cloud](https://cloud.arduino.cc/)**
18. Accedi con il tuo account Arduino o creane uno se non ne hai uno
19. Vai alla dashboard di Arduino IoT Cloud
20. Vai su **Devices** e clicca su **ADD DEVICE**
    ![Add device](images/Arduino_IoT_Cloud/001.jpg)
21. Seleziona "**Any Device**" sotto **MANUAL** e clicca su **CONTINUE**
    ![Manual](images/Arduino_IoT_Cloud/002.jpg)
22. Seleziona un nome per il tuo dispositivo e clicca su **NEXT**
    ![Create device](images/Arduino_IoT_Cloud/003.jpg)
23. Salva il **Device ID** e il **Device Secret** da qualche parte (ne avrai bisogno più tardi)
    ![Device ID and Device Secret](images/Arduino_IoT_Cloud/004.jpg)
24. Seleziona la casella **I saved my device ID and Secret Key** e premi **CONTINUE**
25. Clicca su **GOT IT**
    ![Got it](images/Arduino_IoT_Cloud/005.jpg)
26. Nella nuova pagina, clicca su **Create thing**
27. In **Cloud Variables**, clicca su **ADD** e crea 5 nuove variabili **Read & Write** con **On change** Variable Update Policy:
    - **cambioIstantaneo** (bool)
    - **coloreLED** (CloudColoredLight)
    - **controlloGenerale** (bool)
    - **motoreStella** (bool)
    - **testoMatrice** (String)
    ![Add variable](images/Arduino_IoT_Cloud/007.jpg)
28. Crea una nuova Dashboard cliccando su **CREATE DASHBOARD** sotto **Dashboards**
29. Aggiungi tre widget **Switch**, un widget **Colored light** e un widget **Messenger** alla dashboard
    ![Add widgets](images/Arduino_IoT_Cloud/009.jpg)

## Incorporare il Device ID e il Device Secret nel codice Python
30. Apri il file **[software.py](software.py)** usando un editor di testo o '*nano*' (se stai usando il terminale)
    ```
    nano software.py
    ```
31. Sostituisci le variabili **DEVICE_ID** e **DEVICE_SECRET** con quelle che hai salvato prima (Step 23). NON RIMUOVERE LA "**b**" PRIMA DELLE VIRGOLETTE
    ```python
    DEVICE_ID = b"SOSTITUISCI CON IL TUO DEVICE ID"
    SECRET_KEY = b"SOSTITUISCI CON IL TUO SECRET KEY"
    ```
32. Salva il file ed esci (se stai usando '*nano*', premi **CTRL + X**, poi **Y** e poi **INVIO**)

## Eseguire l'applicazione
33. Collega l'Arduino al Raspberry PI usando il cavo USB
34. Collega tutto come mostrato nella sezione **[circuito](#circuito)**
35. Esegui l'applicazione
    ```
    python3 software.py
    ```

**NOTA**: Puoi anche eseguire l'applicazione in background aggiungendo un **&** alla fine del comando, così:
```
python3 software.py &
```

# Risultato finale
![Final result](images/Tree.png)
*Sfortunatamente, la striscia LED inferiore si è rotta durante il montaggio.*

# Contribuire
Puoi contribuire al progetto creando una pull request o un issue.

Per contribuire, puoi fare il fork della repository e dopo aver fatto le tue modifiche, puoi creare una pull request.

## Licenza
Questo progetto è sotto la **Licenza MIT**. Vedi il file **[LICENSE](LICENSE)** per maggiori informazioni.