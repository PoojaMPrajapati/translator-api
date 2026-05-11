from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import uuid   #  IMPORTANT FIX

app = Flask(__name__)
CORS(app)

# static folder
if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/")
def home():
    return "Translator API Running ✔"


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    text = data.get("text", "")
    direction = data.get("direction", "en-hi")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    translated = ""
    lang = "en"

    #  TRANSLATION LOGIC
    if direction == "en-hi":
        translated = GoogleTranslator(source="auto", target="hi").translate(text)
        lang = "hi"

    elif direction == "hi-en":
        translated = GoogleTranslator(source="auto", target="en").translate(text)
        lang = "en"

    else:
        return jsonify({"error": "Invalid direction"}), 400

    #  FIX 1: UNIQUE FILE NAME (NO REUSE)
    filename = f"reply_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join("static", filename)

    try:
        tts = gTTS(text=translated, lang=lang, slow=False)
        tts.save(audio_path)
    except:
        tts = gTTS(text=translated, lang="en", slow=False)
        tts.save(audio_path)

    return jsonify({
        "input": text,
        "output": translated,
        "audio": "/static/" + filename
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)