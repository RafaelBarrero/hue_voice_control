import os

from dotenv import load_dotenv

import speech_recognition as sr

load_dotenv()

WIT_AI_KEY = os.getenv('WIT_AI_KEY')


def wit_voice_recognition():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Say something!")
            audio = r.listen(source)
            try:
                recognized = r.recognize_wit(audio, key=WIT_AI_KEY)
                print(f"Wit.ai thinks you said {recognized}")
            except (sr.UnknownValueError, sr.RequestError) as e:
                print("Could not request results from Wit.ai service; {0}".format(e))
                break

            if recognized in ["google", "Google"]:
                while True:
                    audio = r.listen(source)
                    try:
                        recognized = r.recognize_wit(audio, key=WIT_AI_KEY)
                        print(f"Wit.ai thinks you said {recognized}")
                    except (sr.UnknownValueError, sr.RequestError) as e:
                        print("Could not request results from Wit.ai service; {0}".format(e))
                        break

                    if recognized in "morado":
                        print("morado")
                    elif recognized in "salir":
                        print("salir")
                        break
            elif recognized in "salir":
                print("salir")
                break
            else:
                print("no es google")
