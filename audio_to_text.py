import speech_recognition as sr


recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak now...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        print("Converting speech to text...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google API.")

