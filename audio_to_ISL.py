import speech_recognition as sr
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Words to ignore in ISL translation
ignore_words = {"is", "are", "be", "the", "a", "an", "to", "of"}

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

def convert_to_isl(text):
    doc = nlp(text)
    subject, verb, object_, others, negation = [], [], [], [], []

    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:  # Subject
            subject.append(token.text)
        elif token.dep_ in ["dobj", "pobj"]:  # Object
            object_.append(token.text)
        elif token.dep_ in ["ROOT", "aux", "auxpass", "xcomp", "ccomp"]:  # Verb
            if token.lemma_ not in ignore_words:  # Exclude auxiliary verbs
                verb.append(token.lemma_)
        elif token.dep_ == "neg":  # Negation
            negation.append(token.text)
        else:
            others.append(token.text)

    # For questions, ensure the order is Subject-Object-Question Word
    if "?" in text:
        isl_sentence = subject + object_ + others + verb
    else:
        # Adjust for negation: move it after the verb
        if negation:
            isl_sentence = subject + verb + negation + object_ + others
        else:
            isl_sentence = subject + verb + object_ + others

    isl_sentence = [word.upper() for word in isl_sentence if word.lower() not in ignore_words]

    # If it's a question, move the question word to the end
    if "?" in text:
        isl_sentence = subject + object_ + [word for word in others if word.lower() in ['where', 'what', 'how']] + verb

    print("\nISL Translated Sentence:", " ".join(isl_sentence))
    return isl_sentence

if __name__ == "__main__":
    text = audio_to_text()
    if text:
        convert_to_isl(text)
