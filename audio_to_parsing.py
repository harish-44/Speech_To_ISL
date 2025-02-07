import speech_recognition as sr
import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Converting speech to text...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google API.")

def dependency_parsing(text):
    doc = nlp(text)
    print("\nDependency Parsing Results:")
    for token in doc:
        print(f"{token.text} -> {token.dep_} ({token.pos_})")

if __name__ == "__main__":
    text = audio_to_text()
    if text:
        dependency_parsing(text)