import streamlit as st
import speech_recognition as sr
import spacy
import os
import time
from PIL import Image, ImageEnhance

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Words to ignore in ISL translation
ignore_words = {"is", "are", "be", "the", "a", "an", "to", "of"}

# Define question words to detect
question_words = {"who", "what", "when", "how", "where"}

# Path to folder containing letter images
IMAGE_FOLDER = r"D:\Speech_to_SignLang\Images"  # Ensure images are high-quality & named as A.jpg, B.jpg, ..., Z.jpg

def audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            st.write("⏳ Converting speech to text...")
            text = recognizer.recognize_google(audio)
            st.write(f"🗣 **You said:** {text}")
            return text
        except sr.UnknownValueError:
            st.write("⚠️ Could not understand the audio.")
        except sr.RequestError:
            st.write("⚠️ Could not request results from Google API.")

def convert_to_isl(text):
    """Convert English text to ISL-friendly structure using spaCy."""
    doc = nlp(text)
    subject, verb, obj, others, question, greeting = [], [], [], [], [], []

    for token in doc:
        if token.text.lower() in {"hello", "hi"}:  # Greetings
            greeting.append(token.text)
        elif token.dep_ in ["nsubj", "nsubjpass"]:  # Subject
            subject.append(token.text)
        elif token.dep_ in ["dobj", "pobj"]:  # Object
            obj.append(token.text)
        elif token.dep_ in ["ROOT", "aux", "auxpass", "xcomp", "ccomp"]:  # Verb
            if token.lemma_ not in ignore_words:
                verb.append(token.lemma_)
        elif token.text.lower() in question_words:  # Question words
            question.append(token.text)
        else:
            others.append(token.text)

    # Form ISL sentence structure: Greeting + Subject + Question + Object + Verb
    isl_sentence = greeting + subject + question + obj + verb

    # Convert to uppercase and filter ignored words
    isl_sentence = [word.upper() for word in isl_sentence if word.lower() not in ignore_words]

    st.write(f"✅ **ISL Translated Sentence:** {' '.join(isl_sentence)}")
    return isl_sentence

def display_images(isl_sentence):
    """Display letter images in a sequence like a video effect with pauses between words."""
    placeholder = st.empty()
    
    for word in isl_sentence:
        word_images = []
        
        # Collect images for each letter in the word
        for letter in word:
            letter_image = os.path.join(IMAGE_FOLDER, f"{letter}.jpg")
            if os.path.exists(letter_image):
                word_images.append(letter_image)
            else:
                st.write(f"⚠️ No image found for '{letter}'")

        # Display each letter of the word sequentially
        for img_path in word_images:
            img = Image.open(img_path)
            
            # **Enhance Image Quality**
            img = img.resize((600, 600), Image.LANCZOS)  # Resize for clarity
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)  # Increase sharpness
            
            placeholder.image(img, caption="ISL Translation", use_container_width=True)
            time.sleep(0.5)  # Pause between letters (0.5 sec)
        time.sleep(1)  # **Pause between words (1 sec) for clarity**

# Streamlit App UI
st.title("🖐 ISL Translator - Speech to Sign Language")

if st.button("🎤 Start Speech Recognition"):
    text = audio_to_text()
    if text:
        isl_sentence = convert_to_isl(text)
        display_images(isl_sentence)
