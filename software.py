# ------------------------------
#     Import Python modules
# ------------------------------

from arduino_iot_cloud import ArduinoCloudClient, ColoredLight
import logging, sys, time, colorsys, threading, multiprocessing, serial
import digitalio, board
from serial.tools import list_ports
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.led_matrix.device import max7219

# utils.py
from utils import scrivi_testo, send_until_ok, wait_for_arduino

# ------------------------------
#  Arduino Cloud configuration
# ------------------------------

sys.path.append("lib")

DEVICE_ID = b"<REPLACE WITH YOUR DEVICE ID>"
SECRET_KEY = b"<REPLACE WITH YOUR SECRET KEY>"

# Launch the Arduino Cloud client in a separate thread
def start_client():
    client.start()

testo = "Buon Natale!"

booting = True

# ------------------------------
#      Logging configuration
# ------------------------------

logging.basicConfig(
    datefmt="%H:%M:%S",
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    level=logging.DEBUG
)

# ------------------------------
#    Raspberry Pi GPIO setup
# ------------------------------

## Motore stella
motore_stella = digitalio.DigitalInOut(board.D27)
motore_stella.direction = digitalio.Direction.OUTPUT

## LED strip configuration
prev_hue = prev_sat = None
colore = [0, 0, 0]

## LED matrix configuration
try:
    matrix_serial = spi(port=0, device=0, gpio=noop())
    matrix = max7219(matrix_serial, cascaded=8, block_orientation=-90)
except:
    logging.warning("LED matrix not connected! LED matrix functions will not work!")
    matrix_serial = None
    matrix = None

# ------------------------------
#     Arduino Serial config
# ------------------------------

def find_arduino():
    ports = list_ports.comports()
    for p in ports:
        logging.debug(f"Serial port device detected: {p}, Manufacturer: {p.manufacturer}")
        if p.manufacturer is not None and ("Arduino" in p.manufacturer or "Arduino" in p.description):
            return p.device
    return None

arduino_port = find_arduino()

if arduino_port is not None:
    ser = serial.Serial(arduino_port, 9600)
    logging.info(f"Arduino connected on port {arduino_port}!")
else:
    ser = None
    logging.warning("Arduino not connected! Arduino related functions will not work!")

# How data will be structured:
# [0/1, 0/1, 0-255, 0-255, 0-255, 0-100]
# [ON/OFF, Instant Change, R, G, B, Brightness]

# ------------------------------
#      Callback functions
# ------------------------------

def on_coloreled_changed(client, value):
    global prev_hue, prev_sat, colore, ser, booting
    if not booting:
        logging.info(f"LED Changed! Status is: SWI: {value.swi}, HUE: {value.hue}, SAT: {value.sat}, BRI: {value.bri} --> {hsl_to_rgb(value.hue, value.sat)}")

        colore = hsl_to_rgb(value.hue, value.sat)

        # If the HUE or SAT values haven't changed, don't start a new thread
        if prev_hue == value.hue and prev_sat == value.sat:
            return

        # Log the new color and the previous HUE and SAT values
        logging.debug(f"New color: {colore}, Previous HUE: {prev_hue}, Previous SAT: {prev_sat}")

        prev_hue, prev_sat = value.hue, value.sat

        if client["cambioIstantaneo"] and client["controlloGenerale"]:
            send_until_ok(f"1, 1, {int(colore[0])}, {int(colore[1])}, {int(colore[2])}, {int(value.bri)}", ser)
        elif client["controlloGenerale"]:
            send_until_ok(f"1, 0, {int(colore[0])}, {int(colore[1])}, {int(colore[2])}, {int(value.bri)}", ser)

def on_cambioistantaneo_changed(client, value):
    global booting
    if not booting:
        logging.info(f"cambioIstantaneo Changed! Status is: {value}")

def on_controllogenerale_changed(client, value):
    global booting
    if not booting:
        logging.info(f"controlloGenerale Changed! Status is: {value}")
        if value:
            attiva_tutto()
        else:
            disattiva_tutto()

def on_motorestella_changed(client, value):
    global booting
    if not booting:
        logging.info(f"motoreStella Changed! Status is: {value}")
        if value and client["controlloGenerale"]:
            attiva_motore()
        else:
            disattiva_motore()

def on_testomatrice_changed(client, value):
    global matrice, testo, booting, matrix
    if not booting:
        logging.info(f"testoMatrice Changed! Status is: {value}")
        old_testo = testo
        testo = str(value)
        if testo.strip() == "":
            testo = "Buon Natale!"
        if testo == "rainbow":
            testo = old_testo
            if client["controlloGenerale"]:
                send_until_ok(f"1, 2, 0, 0, 0, 0", ser)
            client["testoMatrice"] = testo
            return
        if matrice.is_alive():
            matrice.terminate()
        if client["controlloGenerale"]:
            matrice = multiprocessing.Process(target=scrivi_testo, args=(testo,matrix,))
            matrice.start()

# ------------------------------
#   Color conversion functions
# ------------------------------

def rgb_to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return hue, saturation, 50

def hsl_to_rgb(hue, saturation, lightness=50):
    hue, saturation, lightness = hue / 360.0, saturation / 100.0, lightness / 100.0  # normalize hue to range [0, 1]
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return int(r * 255), int(g * 255), int(b * 255)

# ------------------------------
#        Multi-threading
# ------------------------------

def termina_thread_matrix():
    global matrice
    if matrice is not None and matrice.is_alive():
        matrice.terminate()
        matrice = None
    regen_thread_matrix()
    
def regen_thread_matrix():
    global matrice, testo, matrix
    matrice = multiprocessing.Process(target=scrivi_testo, args=(testo,matrix))

# ------------------------------
#      Controllo generale
# ------------------------------

def disattiva_tutto():
    global matrice, colore, ser
    termina_thread_matrix()
    if ser is None:
        logging.warning("Arduino not connected! Arduino functions will not work!")
    else:
        send_until_ok(f"0, 1, {int(colore[0])}, {int(colore[1])}, {int(colore[2])}, {int(client['coloreLED'].bri)}", ser)
    spegni_matrice()
    disattiva_motore()
    logging.info("Motore stella disattivato!")

def attiva_tutto():
    global matrice, colore, ser
    if ser is None:
        logging.warning("Arduino not connected! Arduino functions will not work!")
    else:
        send_until_ok(f"1, 1, {int(colore[0])}, {int(colore[1])}, {int(colore[2])}, {int(client['coloreLED'].bri)}", ser)
    termina_thread_matrix()
    matrice.start()
    attiva_motore()
    logging.info("Motore stella attivato!")

# ------------------------------
#     Motore stella (GPIO17)
# ------------------------------

def attiva_motore():
    global motore_stella
    if motore_stella is None:
        logging.warning("Motore stella not connected! Motore stella functions will not work!")
        return
    motore_stella.value = True
    logging.info("Motore stella attivato!")

def disattiva_motore():
    global motore_stella
    if motore_stella is None:
        logging.warning("Motore stella not connected! Motore stella functions will not work!")
        return
    motore_stella.value = False
    logging.info("Motore stella disattivato!")

# ------------------------------
#     LED matrix functions
# ------------------------------

# scrivi_testo is in utils.py

def spegni_matrice():
    global matrix
    if matrix is None:
        logging.warning("LED matrix not connected! LED matrix functions will not work!")
        return
    termina_thread_matrix()
    matrix.clear()
    matrix.hide()
    logging.info("LED matrix turned off!")


# ------------------------------
#             Main
# ------------------------------

if __name__ == "__main__":
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    regen_thread_matrix()

    client.register(ColoredLight("coloreLED", on_write=on_coloreled_changed))
    client.register("cambioIstantaneo", value=None, on_write=on_cambioistantaneo_changed)
    client.register("controlloGenerale", value=None, on_write=on_controllogenerale_changed)
    client.register("motoreStella", value=None, on_write=on_motorestella_changed)
    client.register("testoMatrice", value=None, on_write=on_testomatrice_changed)

    thread = threading.Thread(target=start_client)
    thread.start()

    time.sleep(7)
    booting = False
    time.sleep(0.5)
    logging.info("Updating default values...")
    client["cambioIstantaneo"] = False
    client["controlloGenerale"] = True
    client["motoreStella"] = True
    testo = "Buon Natale!"
    client["testoMatrice"] = testo
    client["coloreLED"].hue = 108.0
    client["coloreLED"].sat = 92.0
    client["coloreLED"].bri = 50.0
    logging.info("Default values updated!")
    time.sleep(1)
    attiva_tutto()
