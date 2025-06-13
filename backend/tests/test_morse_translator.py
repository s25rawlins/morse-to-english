"""
Unit tests for the MorseTranslator class.
"""

import pytest
from app.core.morse_translator import MorseTranslator


class TestMorseTranslator:
    """Test cases for MorseTranslator functionality."""

    def test_english_to_morse_basic(self):
        """Test basic English to Morse translation."""
        result = MorseTranslator.english_to_morse("HELLO")
        expected = ".... . .-.. .-.. ---"
        assert result == expected

    def test_english_to_morse_with_numbers(self):
        """Test English to Morse with numbers."""
        result = MorseTranslator.english_to_morse("ABC123")
        expected = ".- -... -.-. .---- ..--- ...--"
        assert result == expected

    def test_english_to_morse_with_spaces(self):
        """Test English to Morse with spaces."""
        result = MorseTranslator.english_to_morse("HELLO WORLD")
        expected = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        assert result == expected

    def test_english_to_morse_case_insensitive(self):
        """Test that English to Morse is case insensitive."""
        result1 = MorseTranslator.english_to_morse("hello")
        result2 = MorseTranslator.english_to_morse("HELLO")
        assert result1 == result2


    def test_english_to_morse_whitespace_only(self):
        """Test English to Morse with whitespace only."""
        result = MorseTranslator.english_to_morse("   ")
        expected = "/ / /"
        assert result == expected

    def test_english_to_morse_unsupported_characters(self):
        """Test English to Morse with unsupported characters."""
        result = MorseTranslator.english_to_morse("HELLO@WORLD!")
        expected = ".... . .-.. .-.. --- .-- --- .-. .-.. -.."
        assert result == expected

    def test_morse_to_english_basic(self):
        """Test basic Morse to English translation."""
        result = MorseTranslator.morse_to_english(".... . .-.. .-.. ---")
        assert result == ["HELLO"]

    def test_morse_to_english_with_spaces(self):
        """Test Morse to English with word spaces."""
        result = MorseTranslator.morse_to_english(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
        assert result == ["HELLO WORLD"]

    def test_morse_to_english_ambiguous(self):
        """Test Morse to English with ambiguous patterns."""
        result = MorseTranslator.morse_to_english("...-.")
        # This could be "VE" (V=...- + E=.) or other combinations
        assert len(result) >= 1
        assert "VE" in result

    def test_morse_to_english_complex_ambiguous(self):
        """Test complex ambiguous Morse code."""
        result = MorseTranslator.morse_to_english("-..-.")
        # This could be multiple interpretations
        assert len(result) >= 1
        assert isinstance(result, list)

    def test_morse_to_english_empty_string(self):
        """Test Morse to English with empty string."""
        result = MorseTranslator.morse_to_english("")
        assert result == [""]

    def test_morse_to_english_whitespace_only(self):
        """Test Morse to English with whitespace only."""
        result = MorseTranslator.morse_to_english("   ")
        assert result == [""]

    def test_morse_to_english_single_character(self):
        """Test Morse to English with single character."""
        result = MorseTranslator.morse_to_english(".-")
        # ".-" can be interpreted as "A" or "ET" (E=. + T=-)
        assert "A" in result

    def test_morse_to_english_numbers(self):
        """Test Morse to English with numbers."""
        result = MorseTranslator.morse_to_english(".---- ..--- ...--")
        assert result == ["123"]

    def test_validate_morse_code_valid(self):
        """Test validation of valid Morse code."""
        valid_codes = [
            ".- -... -.-.",
            ".... . .-.. .-.. ---",
            "... --- ...",
            ".- / -... / -.-.",
            "...-.",
            ""
        ]
        
        for code in valid_codes:
            assert MorseTranslator.validate_morse_code(code) is True

    def test_validate_morse_code_invalid(self):
        """Test validation of invalid Morse code."""
        invalid_codes = [
            "abc",
            ".- -... X",
            "hello world",
            "123",
            ".- -... #"
        ]
        
        for code in invalid_codes:
            assert MorseTranslator.validate_morse_code(code) is False

    def test_get_supported_characters(self):
        """Test getting supported characters."""
        chars = MorseTranslator.get_supported_characters()
        
        # Should include all letters
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            assert letter in chars
        
        # Should include all digits
        for digit in "0123456789":
            assert digit in chars
        
        # Should include space
        assert " " in chars

    def test_morse_code_dict_completeness(self):
        """Test that MORSE_CODE_DICT contains expected entries."""
        morse_dict = MorseTranslator.MORSE_CODE_DICT
        
        # Test some known mappings
        assert morse_dict["A"] == ".-"
        assert morse_dict["B"] == "-..."
        assert morse_dict["S"] == "..."
        assert morse_dict["O"] == "---"
        assert morse_dict["1"] == ".----"
        assert morse_dict["0"] == "-----"
        assert morse_dict[" "] == "/"

    def test_reverse_morse_dict_consistency(self):
        """Test that REVERSE_MORSE_DICT is consistent with MORSE_CODE_DICT."""
        morse_dict = MorseTranslator.MORSE_CODE_DICT
        reverse_dict = MorseTranslator.REVERSE_MORSE_DICT
        
        for char, morse in morse_dict.items():
            assert reverse_dict[morse] == char

    def test_round_trip_translation(self):
        """Test that English -> Morse -> English works correctly."""
        test_phrases = [
            "HELLO",
            "WORLD",
            "SOS",
            "ABC123",
            "TEST"
        ]
        
        for phrase in test_phrases:
            morse = MorseTranslator.english_to_morse(phrase)
            english_results = MorseTranslator.morse_to_english(morse)
            
            # The original phrase should be one of the possible translations
            assert phrase in english_results

    def test_edge_cases(self):
        """Test various edge cases."""
        # Very long input
        long_text = "A" * 100
        morse_result = MorseTranslator.english_to_morse(long_text)
        assert len(morse_result) > 0
        
        # Single space
        result = MorseTranslator.english_to_morse(" ")
        assert result == "/"
        
        # Multiple spaces
        result = MorseTranslator.english_to_morse("A  B")
        assert result == ".- / / -..."

    def test_performance_large_input(self):
        """Test performance with reasonably large input."""
        # Test with a moderately large string
        large_text = "HELLO WORLD " * 50  # 600 characters
        
        # Should complete without timeout
        morse_result = MorseTranslator.english_to_morse(large_text)
        assert len(morse_result) > 0
        
        # Test reverse translation
        english_results = MorseTranslator.morse_to_english(morse_result)
        assert len(english_results) > 0

    def test_special_morse_patterns(self):
        """Test special Morse code patterns."""
        # Test SOS
        sos_morse = "... --- ..."
        result = MorseTranslator.morse_to_english(sos_morse)
        assert "SOS" in result
        
        # Test some common abbreviations
        test_cases = [
            (".- -... -.-.", ["ABC"]),
            (".---- ..--- ...--", ["123"]),
            ("- . ... -", ["TEST"])
        ]
        
        for morse, expected in test_cases:
            result = MorseTranslator.morse_to_english(morse)
            for exp in expected:
                assert exp in result

    def test_ambiguous_patterns_comprehensive(self):
        """Test comprehensive ambiguous pattern handling."""
        # Test patterns that can be interpreted multiple ways
        ambiguous_cases = [
            "...-.",  # Could be VE or 5
            "-..-.",  # Multiple possibilities
            ".--..",  # Could be PZ or other combinations
        ]
        
        for case in ambiguous_cases:
            results = MorseTranslator.morse_to_english(case)
            # Should have multiple interpretations
            assert len(results) >= 1
            # All results should be non-empty strings
            assert all(result.strip() for result in results)

    def test_input_sanitization(self):
        """Test input sanitization and handling."""
        # Test with extra whitespace
        result1 = MorseTranslator.english_to_morse("  HELLO  ")
        expected = "/ / .... . .-.. .-.. --- / /"
        assert result1 == expected
        
        # Test Morse with extra whitespace
        result1 = MorseTranslator.morse_to_english("  .- -...  ")
        result2 = MorseTranslator.morse_to_english(".- -...")
        assert result1 == result2
