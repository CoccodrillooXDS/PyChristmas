import serial
import logging
from serial.tools import list_ports
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, LCD_FONT

logging.basicConfig(
    datefmt="%H:%M:%S",
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    level=logging.DEBUG
)

def scrivi_testo(testo="Buon Natale!", matrix=None):
    if matrix is None:
        logging.warning("LED matrix not connected! LED matrix functions will not work!")
        return
    matrix.clear()
    matrix.show()
    show_message(matrix, testo, fill="white", font=proportional(LCD_FONT))
    logging.info(f"Writing {testo} on LED matrix!")
    scrivi_testo(testo, matrix)

def send_until_ok(message=None, ser=None):
    if ser is None:
        logging.warning("Arduino not connected! Arduino functions will not work!")
        return
    while True:
        try:
            logging.debug(f"Sending message \"{message}\" to Arduino...")
            ser.write(message.encode())
            logging.debug("Waiting for Arduino response...")
            response = ser.readline().decode().strip()
            logging.debug(f"Arduino response: \"{response}\"")
            if response == "OK":
                break
        except serial.SerialException:
            logging.error("Serial connection unavailable. Please check the device connection and restart program.")
            logging.warning("Arduino no longer connected! Arduino functions will not work!")
            break

def wait_for_arduino(ser=None, num=1):
    current_num = 0
    if ser is None:
        logging.warning("Arduino not connected! Arduino functions will not work!")
        return
    while True:
        try:
            logging.debug("Waiting for Arduino response...")
            response = ser.readline().decode().strip()
            logging.debug(f"Arduino response: \"{response}\"")
            current_num += 1
            if current_num >= num:
                break
        except serial.SerialException:
            logging.error("Serial connection unavailable. Please check the device connection and restart program.")
            logging.warning("Arduino no longer connected! Arduino functions will not work!")
            break