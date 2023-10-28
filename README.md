# Flask URL Shortener

This is a simple URL shortener built with Flask.

## Features

- Shorten URLs
- Redirect to original URL using the shortened URL
- Get metadata for a shortened URL
- Search for URLs

## Installation

1. Clone this repository: `git clone https://github.com/yourusername/flask-url-shortener.git`
2. Navigate to the project directory: `cd flask-url-shortener`
3. Install the required packages: `pip install -r requirements.txt`

## Usage

1. Run the application: `python app.py`
2. Open your web browser and navigate to `http://127.0.0.1:5000`

## Endpoints

- `POST /create`: Create a new shortened URL
- `GET /<short_url>`: Redirect to the original URL using the shortened URL
- `GET /api/<short_url>`: Get metadata for a shortened URL
- `GET /search`: Search for URLs

