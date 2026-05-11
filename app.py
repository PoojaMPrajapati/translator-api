from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
from googletrans import Translator
import os

app = Flask(__name__)
CORS(app)

translator = Translator()

if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/")
def home():
    return "Translator API Running ✔"


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    text = data["text"]
    direction = data["direction"]

    if direction == "en-hi":
        translated = translator.translate(text, dest="hi").text
        lang = "hi"
    else:
        translated = translator.translate(text, dest="en").text
        lang = "en"

    audio_path = "static/reply.mp3"
    tts = gTTS(translated, lang=lang)
    tts.save(audio_path)

    return jsonify({
        "input": text,
        "output": translated,
        "audio": "/static/reply.mp3"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)