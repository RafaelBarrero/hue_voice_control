import os
import threading
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

import speech_recognition as sr

from src.speech.voice_thread import Voice

load_dotenv()

WIT_AI_KEY = os.getenv('WIT_AI_KEY')
HEROKU_CHANGE = os.getenv('HEROKU_CHANGE')

r = sr.Recognizer()
source = sr.Microphone()

wit = False
salir = False

voice = Voice()


def callback(recognizer, audio):
    global salir

    try:
        if wit:
            recognized: str = recognizer.recognize_wit(audio, key=WIT_AI_KEY)
        else:
            recognized: str = recognizer.recognize_google(audio, language="es-ES")
        print(f"He reconocido {recognized.strip()} en callback")

        if recognized.strip() != "" and "jarvis" in recognized.lower() or "darvish" in recognized.lower():
            voice.say("¿Me llamabas?")
            jarvis()
        elif recognized.strip() != "" and "salir" in recognized.lower():
            print("salir")
            voice.say("Cerrando script")
            salir = True

    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"No se ha podido reconocer la voz; {e}")


def change_heroku_accounts():
    exit_status = subprocess.call(HEROKU_CHANGE)
    if exit_status == 0:
        voice.say("Cuentas cambiadas")
    else:
        voice.say("Ha habido un problema al cambiar las cuentas")


def voice_recognition(recognition_str: str = None):
    global wit

    if recognition_str == "wit":
        wit = True
    with source as mic:
        r.adjust_for_ambient_noise(mic)
        r.pause_threshold = 0.5

    stop = r.listen_in_background(source, callback)
    print("Di algo")

    while not salir:
        time.sleep(0.1)

    stop()
    voice.terminate()


def jarvis():
    global wit
    print("jarvis")

    audio = r.listen(source)

    try:
        if wit:
            recognized: str = r.recognize_wit(audio, key=WIT_AI_KEY)
        else:
            recognized: str = r.recognize_google(audio, language="es-ES")
        print(f"He reconocido {recognized.strip()} en jarvis")

        if recognized.strip() != "" and "morado" in recognized.lower():
            voice.say("Cambiando las luces a morado")

        elif recognized.strip() != "" and "cuenta" in recognized.lower():
            voice.say("Cambiando las cuentas de Heroku")
            thread = threading.Thread(target=change_heroku_accounts)
            thread.start()

        elif recognized.strip() != "" and "salir" in recognized.lower():
            voice.say("Adiós, Rafa")
            return

        # Calls the same function to start a loop if not "apagar"
        jarvis()
    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"No se ha podido reconocer la voz; {e}")
        jarvis()
