import os
import time

from dotenv import load_dotenv

import speech_recognition as sr

load_dotenv()

WIT_AI_KEY = os.getenv('WIT_AI_KEY')

r = sr.Recognizer()
source = sr.Microphone()
wit = False
salir = False


def callback(recognizer, audio):
    global salir
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        if wit:
            recognized: str = recognizer.recognize_wit(audio, key=WIT_AI_KEY)
        else:
            recognized: str = recognizer.recognize_google(audio, language="es-ES")
        print(f"He reconocido {recognized} en callback")
        if recognized and "jarvis" in recognized.lower() or "darvish" in recognized.lower():
            jarvis()
        elif recognized and "salir" in recognized.lower():
            print("salir")
            salir = True
    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"No se ha podido reconocer la voz; {e}")


def voice_recognition(recognition_str: str = None):
    global wit
    if recognition_str == "wit":
        wit = True
    with source as mic:
        r.adjust_for_ambient_noise(mic)
    stop = r.listen_in_background(source, callback)
    print("Di algo")
    while not salir:
        time.sleep(0.1)
    stop()


def jarvis():
    global wit
    print("Jarvis")
    audio = r.listen(source)
    try:
        if wit:
            recognized: str = r.recognize_wit(audio, key=WIT_AI_KEY)
        else:
            recognized: str = r.recognize_google(audio, language="es-ES")
        print(f"He reconocido {recognized} en jarvis")
        if recognized and "morado" in recognized.lower():
            print("morado")
        elif recognized and "apagar" in recognized.lower():
            print("apagar")
            return
        jarvis()
    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"No se ha podido reconocer la voz; {e}")
        jarvis()
