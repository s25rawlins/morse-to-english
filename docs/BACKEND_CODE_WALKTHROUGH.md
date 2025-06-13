# Backend Code Overview

This document provides an overview of the FastAPI backend for the Morse Code Translator.

## Architecture

The backend is built with FastAPI using a layered architecture pattern:

- **Presentation Layer** - HTTP handling, routing, and middleware (`main.py`, `routes.py`)
- **Business Logic Layer** - Core translation algorithms (`core/morse_translator.py`)
- **Data Layer** - Request/response models and validation (`models/schemas.py`)

## Key Components

### FastAPI Application (`app/main.py`)

The main application file configures:
- FastAPI app instance with metadata
- CORS middleware for frontend communication
- Global exception handlers
- Route inclusion with API versioning

### API Routes (`app/api/routes.py`)

Defines the REST endpoints:
- `GET /api/v1/health` - Health check with supported characters
- `POST /api/v1/translate/english-to-morse` - English to Morse translation
- `POST /api/v1/translate/morse-to-english` - Morse to English translation

Each endpoint includes:
- Request validation using Pydantic models
- Business logic calls to MorseTranslator
- Consistent error handling
- Structured response format

### Translation Logic (`app/core/morse_translator.py`)

Contains the core business logic:
- Static morse code dictionary mappings
- English to Morse conversion
- Morse to English conversion with ambiguity handling
- Input validation methods

Key algorithms:
- **Standard Translation** - Handles spaced morse code
- **Ambiguous Translation** - Recursive algorithm for unspaced morse code
- **Pattern Matching** - Finds all possible interpretations

### Data Models (`app/models/schemas.py`)

Pydantic models for request/response validation:
- `EnglishToMorseRequest` - English text input validation
- `MorseToEnglishRequest` - Morse code input validation
- `TranslationResponse` - Standardized response format
- `HealthResponse` - Health check response
- `ErrorResponse` - Error response format

## API Design

### RESTful Principles

- Resource-based URLs (`/translate/english-to-morse`)
- Appropriate HTTP methods (POST for translations, GET for health)
- Consistent status codes (200, 400, 422, 500)
- JSON request/response format

### Error Handling

Multi-layer error handling approach:
1. **Pydantic Validation** - Automatic input validation (422 errors)
2. **Business Logic Validation** - Domain-specific checks (400 errors)
3. **Exception Handling** - Unexpected errors (500 errors)
4. **Global Handlers** - Consistent error response format

### Response Format

All successful responses follow a consistent structure:
```json
{
  "input": "original input",
  "output": "translation result",
  "translation_type": "english_to_morse",
  "character_count": 5,
  "success": true
}
```

## Testing

The backend includes comprehensive tests:

### Unit Tests (`tests/test_morse_translator.py`)
- Test core translation algorithms
- Edge cases and error conditions
- Input validation

### Integration Tests (`tests/test_api.py`)
- End-to-end API testing
- Request/response validation
- Error scenario testing

### Test Patterns
- Arrange-Act-Assert structure
- Parametrized tests for multiple inputs
- FastAPI TestClient for HTTP testing

## Development Setup

1. Create virtual environment: `python -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python -m app.main`
5. Run tests: `python -m pytest tests/`

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── morse_translator.py # Business logic
│   └── models/
│       ├── __init__.py
│       └── schemas.py         # Pydantic models
├── tests/                     # Test files
├── requirements.txt           # Dependencies
└── README.md
```

## Key Features

- **Automatic Documentation** - OpenAPI/Swagger at `/docs`
- **Type Safety** - Python type hints throughout
- **Input Validation** - Pydantic model validation
- **CORS Support** - Frontend integration
- **Error Handling** - Comprehensive error management
- **Testing** - Unit and integration tests
- **Performance** - ASGI-based async handling

The backend provides a robust, well-documented API that handles both simple and complex morse code translation scenarios while maintaining good performance and reliability.
