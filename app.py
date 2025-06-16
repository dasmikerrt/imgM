from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

TEXT_API_URL = "https://text.pollinations.ai/openai"
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"

SYSTEM_PROMPT = "You are a collaborative fantasy storyteller."

# Helper to call the text generation endpoint

def generate_story(prompt):
    payload = {
        "model": "openai",
        "prompt": prompt,
        "system_prompt": SYSTEM_PROMPT,
    }
    response = requests.post(TEXT_API_URL, json=payload)
    response.raise_for_status()
    return response.json().get("text", "")


def generate_image(prompt, model="flux", width=1024, height=1024):
    params = {
        "model": model,
        "width": width,
        "height": height,
    }
    url = IMAGE_API_URL + requests.utils.quote(prompt)
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.url


def text_to_speech(text, voice="nova"):
    payload = {
        "model": "openai-audio",
        "input": text,
        "voice": voice,
    }
    response = requests.post(TEXT_API_URL, json=payload)
    response.raise_for_status()
    audio_b64 = response.json().get("audio")
    if not audio_b64:
        return None
    audio_bytes = base64.b64decode(audio_b64)
    return audio_bytes


def vision_story(image_data):
    img_b64 = base64.b64encode(image_data).decode("utf-8")
    payload = {
        "model": "openai",
        "prompt": "Tell a story inspired by this image.",
        "image": img_b64,
    }
    response = requests.post(TEXT_API_URL, json=payload)
    response.raise_for_status()
    return response.json().get("text", "")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.json.get("text", "")
    story = generate_story(user_input)
    return jsonify({"story": story})


@app.route("/image", methods=["POST"])
def image():
    prompt = request.json.get("prompt", "")
    image_url = generate_image(prompt)
    return jsonify({"url": image_url})


@app.route("/speech", methods=["POST"])
def speech():
    text = request.json.get("text", "")
    voice = request.json.get("voice", "nova")
    audio_bytes = text_to_speech(text, voice)
    if audio_bytes is None:
        return jsonify({"error": "No audio"}), 500
    filename = "static/output.mp3"
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    return jsonify({"url": "/" + filename})


@app.route("/vision", methods=["POST"])
def vision():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400
    file = request.files['image']
    data = file.read()
    story = vision_story(data)
    return jsonify({"story": story})


if __name__ == "__main__":
    app.run(debug=True)
