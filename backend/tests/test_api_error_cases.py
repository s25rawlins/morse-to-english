"""
Additional tests for API error cases to achieve 100% coverage.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestAPIErrorCases:
    """Test cases for API error handling to achieve 100% coverage."""


    def test_english_to_morse_exception_handling(self):
        """Test English to Morse when an unexpected exception occurs."""
        with patch('app.api.routes.MorseTranslator.english_to_morse', side_effect=Exception("Test error")):
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            
            assert response.status_code == 500
            data = response.json()
            assert "Translation failed: Test error" in data["detail"]


    def test_morse_to_english_no_valid_translations(self):
        """Test Morse to English when no valid translations are found."""
        # Use a morse pattern that returns empty results
        with patch('app.api.routes.MorseTranslator.morse_to_english', return_value=[]):
            payload = {"morse_code": ".- -..."}
            response = client.post("/api/v1/translate/morse-to-english", json=payload)
            
            assert response.status_code == 400
            data = response.json()
            assert "No valid English translations found" in data["detail"]

    def test_morse_to_english_empty_string_result(self):
        """Test Morse to English when result contains only empty strings."""
        with patch('app.api.routes.MorseTranslator.morse_to_english', return_value=[""]):
            payload = {"morse_code": ".- -..."}
            response = client.post("/api/v1/translate/morse-to-english", json=payload)
            
            assert response.status_code == 400
            data = response.json()
            assert "No valid English translations found" in data["detail"]

    def test_morse_to_english_filtered_results_empty(self):
        """Test Morse to English when filtered results are empty."""
        with patch('app.api.routes.MorseTranslator.morse_to_english', return_value=["", "", ""]):
            payload = {"morse_code": ".- -..."}
            response = client.post("/api/v1/translate/morse-to-english", json=payload)
            
            assert response.status_code == 400
            data = response.json()
            assert "No valid English translations found" in data["detail"]

    def test_morse_to_english_http_exception_reraise(self):
        """Test that HTTPExceptions are re-raised correctly."""
        from fastapi import HTTPException, status
        
        def mock_validate_morse_code(code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom validation error"
            )
        
        with patch('app.api.routes.MorseTranslator.validate_morse_code', side_effect=mock_validate_morse_code):
            payload = {"morse_code": ".- -..."}
            response = client.post("/api/v1/translate/morse-to-english", json=payload)
            
            assert response.status_code == 400
            data = response.json()
            assert "Custom validation error" in data["detail"]

    def test_morse_to_english_general_exception_handling(self):
        """Test Morse to English when an unexpected exception occurs."""
        with patch('app.api.routes.MorseTranslator.morse_to_english', side_effect=Exception("Test error")):
            payload = {"morse_code": ".- -..."}
            response = client.post("/api/v1/translate/morse-to-english", json=payload)
            
            assert response.status_code == 500
            data = response.json()
            assert "Translation failed: Test error" in data["detail"]

    def test_morse_to_english_validation_passes_but_translation_fails(self):
        """Test when validation passes but translation returns invalid results."""
        with patch('app.api.routes.MorseTranslator.validate_morse_code', return_value=True):
            with patch('app.api.routes.MorseTranslator.morse_to_english', return_value=[None, "", False]):
                payload = {"morse_code": ".- -..."}
                response = client.post("/api/v1/translate/morse-to-english", json=payload)
                
                assert response.status_code == 400
                data = response.json()
                assert "No valid English translations found" in data["detail"]




    def test_memory_stress_error_handling(self):
        """Test error handling under memory stress conditions."""
        # Simulate a memory error during translation
        with patch('app.api.routes.MorseTranslator.english_to_morse', side_effect=MemoryError("Out of memory")):
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            
            assert response.status_code == 500
            data = response.json()
            assert "Translation failed: Out of memory" in data["detail"]

    def test_unicode_error_handling(self):
        """Test error handling with unicode-related errors."""
        with patch('app.api.routes.MorseTranslator.english_to_morse', side_effect=UnicodeError("Unicode error")):
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            
            assert response.status_code == 500
            data = response.json()
            assert "Translation failed: Unicode error" in data["detail"]
