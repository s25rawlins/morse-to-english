# Morse Code Translator

A web application for translating between English text and Morse code. Includes both a standalone Python script and a full web interface with React frontend and FastAPI backend.

## Features

- Convert English text to Morse code and vice versa
- Handle ambiguous Morse code patterns with multiple interpretations
- Real-time translation as you type
- Interactive Morse code reference chart
- Responsive design for desktop and mobile
- REST API for programmatic access

## Supported Characters

Letters A-Z, numbers 0-9, and common punctuation marks. Spaces are represented as forward slashes (/) in Morse code.

## Quick Start

### Standalone Python Script

Run the interactive command-line version:

```bash
python morse_to_english.py
```

### Web Application

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The web application will open at `http://localhost:3000`.

#### Quick Start Script

Alternatively, use the startup script to run both servers:

```bash
./start_web_app.sh
```

## Usage Examples

### Python Script

```python
from morse_to_english import english_to_morse, morse_to_english

# English to Morse
morse = english_to_morse("HELLO WORLD")
print(morse)  # ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

# Morse to English
english = morse_to_english(".... . .-.. .-.. ---")
print(english)  # ["HELLO"]
```

### API Usage

```bash
# English to Morse
curl -X POST "http://localhost:8000/api/v1/translate/english-to-morse" \
     -H "Content-Type: application/json" \
     -d '{"text": "HELLO WORLD"}'

# Morse to English
curl -X POST "http://localhost:8000/api/v1/translate/morse-to-english" \
     -H "Content-Type: application/json" \
     -d '{"morse_code": ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."}'
```

## API Endpoints

- `GET /` - API information
- `GET /ping` - Health check
- `GET /api/v1/health` - Detailed health status
- `POST /api/v1/translate/english-to-morse` - Translate English to Morse
- `POST /api/v1/translate/morse-to-english` - Translate Morse to English

## Testing

Run backend tests:
```bash
cd backend
python -m pytest tests/
```

Run all tests with Nox:
```bash
nox -s test
```

## Project Structure

```
morse-to-english/
├── README.md
├── morse_to_english.py          # Standalone Python script
├── start_web_app.sh             # Quick start script
├── backend/                     # FastAPI backend
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py             # FastAPI application
│   │   ├── api/routes.py       # API endpoints
│   │   ├── core/morse_translator.py  # Translation logic
│   │   └── models/schemas.py   # Data models
│   └── tests/                  # Backend tests
├── frontend/                   # React frontend
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.jsx
│       ├── components/         # React components
│       ├── services/           # API service layer
│       └── styles/             # CSS styles
└── docs/                       # Documentation
```

## Requirements

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## License

This project is open source and available under the MIT License.
