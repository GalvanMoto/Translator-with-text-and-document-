import requests
import streamlit as st
from playsound import playsound
from io import BytesIO
import os

language = {
    "bn": "Bangla",
    "en": "English",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "he": "Hebrew",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    'la': "Latin",
    "ms": "Malay",
    "ne": "Nepali",
    "ru": "Russian",
    "ar": "Arabic",
    "zh": "Chinese",
    "es": "Spanish"
}

def translate_text(text, dest_lang):
    url = "http://127.0.0.1:5000/translate"  # Update with your server address
    data = {'text': text, 'dest_lang': dest_lang}
    response = requests.post(url, data=data)
    return response.json()

st.title("Text Translator")

text_input = st.text_area("Enter text to translate:")

file = st.file_uploader("Upload Document (.txt, .pdf, .docx)")

dest_lang = st.selectbox("Select destination language:", options=list(language.values()))

if st.button("Translate"):
    if text_input or file is not None:
        if file is not None:
            file_content = file.read()
            text_input = file_content.decode('utf-8')
        translation_result = translate_text(text_input, [key for key, value in language.items() if value == dest_lang][0])
        st.write(f"Translation: {translation_result['text']}")
        st.write(f"Pronunciation: {translation_result['pronunciation']}")
        st.write(f"Translated from: {translation_result['translated_from']}")

        # Play translated audio
        st.audio("translated_audio.mp3", format="audio/mp3")
    else:
        st.warning("Please enter text or upload a document to translate.")
