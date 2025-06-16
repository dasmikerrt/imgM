# Creative Storytelling Assistant

This project demonstrates a simple Flask application that works with the [Pollinations](https://pollinations.ai) API to help users create stories with text, images and audio. It provides a web interface where you can write or upload content and receive suggestions from the AI.

## Features

- **Text generation** using the Pollinations text endpoint with a fantasy storyteller system prompt.
- **Text-to-image** generation on text selection or paragraph click.
- **Text-to-speech** playback for generated stories or image captions.
- **Vision mode** where you can upload an image and receive a story inspired by it.

## Requirements

- Python 3.11
- `flask`
- `requests`

Install dependencies with:

```bash
pip install flask requests
```

## Usage

Run the application locally:

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`. Open this address in your browser and start creating stories. Generated images and audio are saved under the `static/` directory.

## Repository Layout

- `app.py` – Flask backend with routes for text, image, speech and vision endpoints.
- `templates/index.html` – Frontend interface for story editing and media display.
- `static/style.css` – Simple styles for the web UI.

Feel free to modify or extend the UI and backend to suit your creative projects
