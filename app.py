from flask import Flask, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
translator = Translator()

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

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.form
    text = data.get('text')
    dest_lang = data.get('dest_lang')

    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                text = f.read()

    if not text or not dest_lang:
        return jsonify({'error': 'Please provide text and destination language.'}), 400

    if dest_lang not in language:
        return jsonify({'error': 'Invalid destination language code.'}), 400

    translated = translator.translate(text, dest=dest_lang)
    translation_result = {
        'text': translated.text,
        'pronunciation': translated.pronunciation,
        'translated_from': language.get(translated.src)
    }

    # Convert translated text to speech
    tts = gTTS(translated.text, lang=dest_lang)
    tts.save("translated_audio.mp3")

    return jsonify(translation_result)

if __name__ == '__main__':
    app.run(debug=True)
