# Morse Code Translator

A full-stack web application for translating between English text and Morse code, featuring both a standalone Python script and a modern web interface with React frontend and FastAPI backend.

## Features

- **Bidirectional Translation**: Convert English text to Morse code and vice versa
- **Ambiguous Pattern Handling**: Intelligently handles Morse code without spaces, providing multiple possible interpretations
- **Real-time Translation**: Auto-translates as you type with debounced input
- **Interactive Reference**: Built-in Morse code reference chart with letters, numbers, and punctuation
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **REST API**: Full-featured API for programmatic access
- **Comprehensive Testing**: Unit tests for core functionality

## Supported Characters

- **Letters**: A-Z (case insensitive)
- **Numbers**: 0-9
- **Punctuation**: Period, comma, question mark, apostrophe, exclamation, slash, parentheses, ampersand, colon, semicolon, equals, plus, minus, underscore, quotation marks, dollar sign, at symbol
- **Spaces**: Represented as forward slashes (/) in Morse code

## Project Structure

```
morse-to-english/
├── README.md
├── morse_to_english.py          # Standalone Python script
├── backend/                     # FastAPI backend
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── api/
│   │   │   └── routes.py       # API endpoints
│   │   ├── core/
│   │   │   └── morse_translator.py  # Core translation logic
│   │   └── models/
│   │       └── schemas.py      # Pydantic models
│   └── tests/                  # Backend tests
├── frontend/                   # React frontend
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.jsx
│       ├── components/         # React components
│       ├── services/           # API service layer
│       └── styles/             # CSS styles
└── noxfile.py                  # Test automation
```

## Quick Start

### Option 1: Standalone Python Script

The simplest way to use the translator is with the standalone Python script:

```bash
python morse_to_english.py
```

This provides an interactive command-line interface with:
- English to Morse translation
- Morse to English translation
- Demo mode with examples
- Menu-driven interface

### Option 2: Full Web Application

For the complete web experience with GUI:

#### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

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

The web application will open at `http://localhost:3000`

## Usage Examples

### Standalone Script

```python
# Import the module
from morse_to_english import english_to_morse, morse_to_english

# English to Morse
morse = english_to_morse("HELLO WORLD")
print(morse)  # ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

# Morse to English
english = morse_to_english(".... . .-.. .-.. ---")
print(english)  # ["HELLO"]

# Ambiguous Morse (without spaces)
ambiguous = morse_to_english("...-.")
print(ambiguous)  # ["VE", "UF"]
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

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Choose translation mode (English → Morse or Morse → English)
3. Type in the input field - translation happens automatically
4. Use the reference guide to look up specific characters
5. Copy results or swap input/output as needed

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /ping` - Health check
- `GET /api/v1/health` - Detailed health status
- `POST /api/v1/translate/english-to-morse` - Translate English to Morse
- `POST /api/v1/translate/morse-to-english` - Translate Morse to English
- `GET /api/v1/supported-characters` - Get list of supported characters

## Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Using Nox (recommended)

```bash
nox -s test
```

This runs tests across multiple Python versions if available.

## Development

### Code Style

The project follows Python PEP 8 standards and uses:
- Type hints for better code documentation
- Comprehensive docstrings
- Error handling and validation
- Modular, reusable components

### Adding Features

1. **Backend**: Add new endpoints in `backend/app/api/routes.py`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **Core Logic**: Extend `backend/app/core/morse_translator.py`

## Technical Details

### Morse Code Handling

- **Standard Format**: Uses spaces between letters and `/` for word breaks
- **Ambiguous Format**: Handles continuous strings without spaces
- **Multiple Interpretations**: Returns all possible translations for ambiguous patterns
- **Validation**: Ensures only valid Morse characters (`.`, `-`, ` `, `/`) are processed

### Performance Features

- **Debounced Input**: Prevents excessive API calls during typing
- **Caching**: Efficient lookup using reverse dictionaries
- **Recursive Algorithm**: Handles complex ambiguous patterns
- **Error Handling**: Graceful degradation with informative error messages

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in `backend/app/main.py` or `frontend/package.json`
2. **CORS errors**: Ensure backend is running before starting frontend
3. **Module not found**: Activate virtual environment and install dependencies
4. **Build failures**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### Getting Help

- Check the API documentation at `http://localhost:8000/docs`
- Review the test files for usage examples
- Ensure all dependencies are properly installed
