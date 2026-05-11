from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import time

app = Flask(__name__)
CORS(app)

# ensure static folder exists
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

    # Translation logic
    if direction == "en-hi":
        translated = GoogleTranslator(source='auto', target='hi').translate(text)
        lang = "hi"
    else:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        lang = "en"

    # unique audio filename (prevents overwrite issues)
    filename = f"reply_{int(time.time())}.mp3"
    audio_path = os.path.join("static", filename)

    # text to speech
    tts = gTTS(translated, lang=lang)
    tts.save(audio_path)

    return jsonify({
        "input": text,
        "output": translated,
        "audio": f"/static/{filename}"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)