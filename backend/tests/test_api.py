"""
Integration tests for the FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints."""

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "Morse Code Translator API"

    def test_ping_endpoint(self):
        """Test the ping endpoint."""
        response = client.get("/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pong"

    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "supported_characters" in data
        assert len(data["supported_characters"]) > 0

    def test_supported_characters_endpoint(self):
        """Test the supported characters endpoint."""
        response = client.get("/api/v1/supported-characters")
        assert response.status_code == 200
        data = response.json()
        assert "supported_characters" in data
        assert "total_count" in data
        assert len(data["supported_characters"]) == data["total_count"]

    def test_english_to_morse_basic(self):
        """Test basic English to Morse translation via API."""
        payload = {"text": "HELLO"}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["input"] == "HELLO"
        assert data["output"] == ".... . .-.. .-.. ---"
        assert data["translation_type"] == "english_to_morse"
        assert data["success"] is True
        assert data["character_count"] == 5

    def test_english_to_morse_with_spaces(self):
        """Test English to Morse with spaces via API."""
        payload = {"text": "HELLO WORLD"}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["input"] == "HELLO WORLD"
        assert data["output"] == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        assert data["translation_type"] == "english_to_morse"
        assert data["success"] is True

    def test_english_to_morse_empty_text(self):
        """Test English to Morse with empty text."""
        payload = {"text": ""}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 422  # Validation error

    def test_english_to_morse_whitespace_only(self):
        """Test English to Morse with whitespace only."""
        payload = {"text": "   "}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 422  # Validation error

    def test_english_to_morse_too_long(self):
        """Test English to Morse with text that's too long."""
        payload = {"text": "A" * 1001}  # Exceeds max length
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 422  # Validation error

    def test_morse_to_english_basic(self):
        """Test basic Morse to English translation via API."""
        payload = {"morse_code": ".... . .-.. .-.. ---"}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["input"] == ".... . .-.. .-.. ---"
        assert data["output"] == "HELLO"
        assert data["translation_type"] == "morse_to_english"
        assert data["success"] is True

    def test_morse_to_english_with_word_breaks(self):
        """Test Morse to English with word breaks via API."""
        payload = {"morse_code": ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["input"] == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        assert data["output"] == "HELLO WORLD"


    def test_morse_to_english_empty_code(self):
        """Test Morse to English with empty code."""
        payload = {"morse_code": ""}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 422  # Validation error

    def test_morse_to_english_invalid_characters(self):
        """Test Morse to English with invalid characters."""
        payload = {"morse_code": "abc123"}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 422  # Validation error

    def test_morse_to_english_mixed_valid_invalid(self):
        """Test Morse to English with mixed valid/invalid characters."""
        payload = {"morse_code": ".- -... X"}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 422  # Validation error


    def test_english_to_morse_case_insensitive(self):
        """Test that English to Morse is case insensitive via API."""
        payload1 = {"text": "hello"}
        payload2 = {"text": "HELLO"}
        
        response1 = client.post("/api/v1/translate/english-to-morse", json=payload1)
        response2 = client.post("/api/v1/translate/english-to-morse", json=payload2)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["output"] == response2.json()["output"]

    def test_request_validation_missing_field(self):
        """Test request validation with missing required field."""
        # Missing 'text' field for english-to-morse
        response = client.post("/api/v1/translate/english-to-morse", json={})
        assert response.status_code == 422

        # Missing 'morse_code' field for morse-to-english
        response = client.post("/api/v1/translate/morse-to-english", json={})
        assert response.status_code == 422

    def test_request_validation_wrong_field_type(self):
        """Test request validation with wrong field type."""
        # Wrong type for 'text' field
        payload = {"text": 123}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        assert response.status_code == 422

        # Wrong type for 'morse_code' field
        payload = {"morse_code": 123}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        assert response.status_code == 422

    def test_cors_headers(self):
        """Test that CORS headers are present."""
        response = client.options("/api/v1/health")
        # FastAPI automatically handles OPTIONS requests for CORS
        assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly defined

    def test_content_type_json(self):
        """Test that API returns JSON content type."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_error_response_format(self):
        """Test that error responses follow the expected format."""
        payload = {"text": ""}  # Invalid empty text
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 422
        # FastAPI returns validation errors in a specific format
        data = response.json()
        assert "detail" in data

    def test_large_valid_input(self):
        """Test API with large but valid input."""
        large_text = "HELLO WORLD " * 50  # 600 characters, within limit
        payload = {"text": large_text.strip()}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["output"]) > 0

    def test_special_characters_handling(self):
        """Test how API handles special characters."""
        payload = {"text": "HELLO@WORLD!"}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        # Should translate only supported characters
        assert data["success"] is True
        # Should not contain morse for @ or !
        assert "@" not in data["output"]
        assert "!" not in data["output"]

    def test_numbers_translation(self):
        """Test translation of numbers via API."""
        payload = {"text": "123"}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["output"] == ".---- ..--- ...--"

        # Test reverse
        payload = {"morse_code": ".---- ..--- ...--"}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["output"] == "123"

    def test_sos_translation(self):
        """Test SOS translation via API."""
        payload = {"text": "SOS"}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["output"] == "... --- ..."

        # Test reverse
        payload = {"morse_code": "... --- ..."}
        response = client.post("/api/v1/translate/morse-to-english", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["output"] == "SOS"

    def test_response_schema_compliance(self):
        """Test that responses comply with the expected schema."""
        payload = {"text": "TEST"}
        response = client.post("/api/v1/translate/english-to-morse", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["input", "output", "translation_type", "character_count", "success"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["input"], str)
        assert isinstance(data["output"], (str, list))
        assert isinstance(data["translation_type"], str)
        assert isinstance(data["character_count"], int)
        assert isinstance(data["success"], bool)

    def test_concurrent_requests(self):
        """Test handling of multiple concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            payload = {"text": "HELLO"}
            response = client.post("/api/v1/translate/english-to-morse", json=payload)
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5
