"""
Tests for schemas.py to achieve 100% coverage.
"""

import pytest
from pydantic import ValidationError
from app.models.schemas import (
    EnglishToMorseRequest,
    MorseToEnglishRequest,
    TranslationResponse,
    ErrorResponse,
    HealthResponse
)


class TestSchemasCoverage:
    """Test cases for schemas.py to achieve 100% coverage."""

    def test_english_to_morse_request_valid(self):
        """Test valid EnglishToMorseRequest creation."""
        request = EnglishToMorseRequest(text="HELLO WORLD")
        assert request.text == "HELLO WORLD"

    def test_english_to_morse_request_strip_whitespace(self):
        """Test that EnglishToMorseRequest strips whitespace."""
        request = EnglishToMorseRequest(text="  HELLO WORLD  ")
        assert request.text == "HELLO WORLD"


    def test_english_to_morse_request_whitespace_only(self):
        """Test EnglishToMorseRequest with whitespace only."""
        with pytest.raises(ValidationError) as exc_info:
            EnglishToMorseRequest(text="   ")
        
        assert "Text cannot be empty or only whitespace" in str(exc_info.value)


    def test_morse_to_english_request_valid(self):
        """Test valid MorseToEnglishRequest creation."""
        request = MorseToEnglishRequest(morse_code=".- -... -.-.")
        assert request.morse_code == ".- -... -.-."

    def test_morse_to_english_request_strip_whitespace(self):
        """Test that MorseToEnglishRequest strips whitespace."""
        request = MorseToEnglishRequest(morse_code="  .- -... -.-.  ")
        assert request.morse_code == ".- -... -.-."


    def test_morse_to_english_request_whitespace_only(self):
        """Test MorseToEnglishRequest with whitespace only morse code."""
        with pytest.raises(ValidationError) as exc_info:
            MorseToEnglishRequest(morse_code="   ")
        
        assert "Morse code cannot be empty or only whitespace" in str(exc_info.value)

    def test_morse_to_english_request_invalid_characters(self):
        """Test MorseToEnglishRequest with invalid characters."""
        with pytest.raises(ValidationError) as exc_info:
            MorseToEnglishRequest(morse_code=".- -... X")
        
        assert "Invalid characters in Morse code" in str(exc_info.value)


    def test_morse_to_english_request_valid_characters_only(self):
        """Test MorseToEnglishRequest with all valid characters."""
        valid_morse_codes = [
            ".- -... -.-.",
            "... --- ...",
            ".- / -... / -.-.",
            "...-.",
            "-----",
            ".----"
        ]
        
        for morse_code in valid_morse_codes:
            request = MorseToEnglishRequest(morse_code=morse_code)
            assert request.morse_code == morse_code

    def test_translation_response_string_output(self):
        """Test TranslationResponse with string output."""
        response = TranslationResponse(
            input="HELLO",
            output=".... . .-.. .-.. ---",
            translation_type="english_to_morse",
            character_count=5
        )
        
        assert response.input == "HELLO"
        assert response.output == ".... . .-.. .-.. ---"
        assert response.translation_type == "english_to_morse"
        assert response.character_count == 5
        assert response.success is True  # Default value

    def test_translation_response_list_output(self):
        """Test TranslationResponse with list output."""
        response = TranslationResponse(
            input="...-.",
            output=["VE", "5"],
            translation_type="morse_to_english",
            character_count=5
        )
        
        assert response.input == "...-."
        assert response.output == ["VE", "5"]
        assert response.translation_type == "morse_to_english"
        assert response.character_count == 5
        assert response.success is True

    def test_translation_response_explicit_success_false(self):
        """Test TranslationResponse with explicit success=False."""
        response = TranslationResponse(
            input="HELLO",
            output="",
            translation_type="english_to_morse",
            character_count=5,
            success=False
        )
        
        assert response.success is False

    def test_error_response_with_detail(self):
        """Test ErrorResponse with detail."""
        response = ErrorResponse(
            error="Validation failed",
            detail="Invalid input provided"
        )
        
        assert response.error == "Validation failed"
        assert response.detail == "Invalid input provided"
        assert response.success is False  # Default value

    def test_error_response_without_detail(self):
        """Test ErrorResponse without detail."""
        response = ErrorResponse(error="Something went wrong")
        
        assert response.error == "Something went wrong"
        assert response.detail is None  # Default value
        assert response.success is False

    def test_health_response_defaults(self):
        """Test HealthResponse with default values."""
        response = HealthResponse(supported_characters=["A", "B", "C"])
        
        assert response.status == "healthy"  # Default value
        assert response.version == "1.0.0"  # Default value
        assert response.supported_characters == ["A", "B", "C"]

    def test_health_response_custom_values(self):
        """Test HealthResponse with custom values."""
        response = HealthResponse(
            status="operational",
            version="2.0.0",
            supported_characters=["A", "B", "C", "1", "2", "3"]
        )
        
        assert response.status == "operational"
        assert response.version == "2.0.0"
        assert response.supported_characters == ["A", "B", "C", "1", "2", "3"]

    def test_schema_serialization(self):
        """Test that schemas can be serialized to dict."""
        # Test EnglishToMorseRequest
        request = EnglishToMorseRequest(text="HELLO")
        assert request.dict() == {"text": "HELLO"}
        
        # Test MorseToEnglishRequest
        request = MorseToEnglishRequest(morse_code=".- -...")
        assert request.dict() == {"morse_code": ".- -..."}
        
        # Test TranslationResponse
        response = TranslationResponse(
            input="HELLO",
            output=".... . .-.. .-.. ---",
            translation_type="english_to_morse",
            character_count=5
        )
        expected = {
            "input": "HELLO",
            "output": ".... . .-.. .-.. ---",
            "translation_type": "english_to_morse",
            "character_count": 5,
            "success": True
        }
        assert response.dict() == expected

    def test_schema_json_serialization(self):
        """Test that schemas can be serialized to JSON."""
        response = TranslationResponse(
            input="HELLO",
            output=".... . .-.. .-.. ---",
            translation_type="english_to_morse",
            character_count=5
        )
        
        json_str = response.json()
        assert "HELLO" in json_str
        assert ".... . .-.. .-.. ---" in json_str
        assert "english_to_morse" in json_str


    def test_field_constraints(self):
        """Test field constraints."""
        # Test min_length constraint
        with pytest.raises(ValidationError):
            EnglishToMorseRequest(text="")
        
        with pytest.raises(ValidationError):
            MorseToEnglishRequest(morse_code="")

    def test_complex_morse_patterns(self):
        """Test complex morse patterns validation."""
        complex_patterns = [
            ".- -... -.-. / -.. . ..-.",  # ABC / DEF
            "... --- ... / ... --- ...",  # SOS / SOS
            ".---- ..--- ...-- / ....- ..... -----",  # 123 / 450
        ]
        
        for pattern in complex_patterns:
            request = MorseToEnglishRequest(morse_code=pattern)
            assert request.morse_code == pattern


    def test_unicode_handling(self):
        """Test unicode character handling in validation."""
        # Test with unicode characters that should fail
        with pytest.raises(ValidationError):
            MorseToEnglishRequest(morse_code=".- ñ -...")
        
        with pytest.raises(ValidationError):
            MorseToEnglishRequest(morse_code=".- 中 -...")
