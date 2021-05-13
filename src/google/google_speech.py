import speech_recognition as sr


def google_voice_recognition():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        while True:
            audio = r.listen(source)
            # recognize speech using Google Speech Recognition
            try:
                recognized = r.recognize_google(audio, language="es-ES")
                print(f"Google Speech Recognition thinks you said {recognized}")
            except (sr.UnknownValueError, sr.RequestError) as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                break

            if recognized in ["google", "Google"]:
                while True:
                    audio = r.listen(source)
                    try:
                        recognized = r.recognize_google(audio, language="es-ES")
                    except (sr.UnknownValueError, sr.RequestError) as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
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
