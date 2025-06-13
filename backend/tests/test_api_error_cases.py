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

    def test_english_to_morse_empty_result_error(self):
        """Test English to Morse when translation returns empty result."""
        with patch('app.api.routes.MorseTranslator.english_to_morse', return_value=""):
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            
            assert response.status_code == 400
            data = response.json()
            assert "No translatable characters found" in data["detail"]

    def test_english_to_morse_exception_handling(self):
        """Test English to Morse when an unexpected exception occurs."""
        with patch('app.api.routes.MorseTranslator.english_to_morse', side_effect=Exception("Test error")):
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            
            assert response.status_code == 500
            data = response.json()
            assert "Translation failed: Test error" in data["detail"]

    def test_morse_to_english_invalid_morse_code(self):
        """Test Morse to English with invalid morse code format."""
        payload = {"morse_code": "invalid123"}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid Morse code format" in data["detail"]

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

    def test_edge_case_morse_patterns(self):
        """Test edge case morse patterns that might cause issues."""
        # Test with a pattern that might return mixed valid/invalid results
        test_cases = [
            {"morse_code": "......"},  # Invalid pattern
            {"morse_code": ".- -... X"},  # Mixed valid/invalid
            {"morse_code": ""},  # Empty (should be caught by validation)
        ]
        
        for case in test_cases:
            response = client.post("/api/v1/translate/morse-to-english", json=case)
            # Should either be 400 (validation error) or 422 (request validation error)
            assert response.status_code in [400, 422]

    def test_english_to_morse_edge_cases(self):
        """Test edge cases for English to Morse translation."""
        # Test with text that might return empty morse
        with patch('app.api.routes.MorseTranslator.english_to_morse', return_value=None):
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            
            assert response.status_code == 400
            data = response.json()
            assert "No translatable characters found" in data["detail"]

    def test_concurrent_error_handling(self):
        """Test error handling under concurrent conditions."""
        import threading
        import time
        
        results = []
        
        def make_failing_request():
            with patch('app.api.routes.MorseTranslator.english_to_morse', side_effect=Exception("Concurrent error")):
                payload = {"text": "HELLO"}
                response = client.post("/api/v1/translate/english-to-morse", json=payload)
                results.append(response.status_code)
        
        # Create multiple threads that will trigger errors
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=make_failing_request)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should return 500 (internal server error)
        assert all(status == 500 for status in results)
        assert len(results) == 3

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
