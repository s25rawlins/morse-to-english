"""
Morse Code Translation Module

This module provides functionality to translate between English text and Morse code,
including handling of ambiguous Morse code patterns that can have multiple interpretations.
"""

from typing import List, Dict


class MorseTranslator:
    """A class for translating between English and Morse code."""
    
    # Morse code dictionary mapping letters/numbers to morse patterns
    MORSE_CODE_DICT: Dict[str, str] = {
        'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',
        'F': '..-.',   'G': '--.',    'H': '....',   'I': '..',     'J': '.---',
        'K': '-.-',    'L': '.-..',   'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',    'S': '...',    'T': '-',
        'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',   'Y': '-.--',
        'Z': '--..',   '1': '.----',  '2': '..---',  '3': '...--',  '4': '....-',
        '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',  '9': '----.',
        '0': '-----',  ' ': '/'
    }
    
    # Reverse dictionary for morse to english translation
    REVERSE_MORSE_DICT: Dict[str, str] = {
        morse: letter for letter, morse in MORSE_CODE_DICT.items()
    }
    
    @classmethod
    def english_to_morse(cls, english_text: str) -> str:
        """
        Convert English text to Morse code.
        
        Args:
            english_text: The English text to convert
            
        Returns:
            The Morse code representation with spaces between characters
        """
        if not english_text:
            return ""
        
        # Don't strip whitespace - preserve it for proper translation
        english_text = english_text.upper()
        morse_result = []
        
        for char in english_text:
            if char in cls.MORSE_CODE_DICT:
                morse_result.append(cls.MORSE_CODE_DICT[char])
            else:
                # Skip unsupported characters silently
                continue
        
        return ' '.join(morse_result)
    
    @classmethod
    def morse_to_english(cls, morse_text: str) -> List[str]:
        """
        Convert Morse code to English text.
        
        This method handles both standard spaced Morse code and ambiguous
        patterns without spaces that may have multiple interpretations.
        
        Args:
            morse_text: The Morse code to convert
            
        Returns:
            A list of possible English translations
        """
        if not morse_text:
            return ['']
            
        morse_text = morse_text.strip()
        
        if not morse_text:
            return ['']
        
        # Check if morse code contains spaces (standard format)
        if ' ' in morse_text:
            morse_units = morse_text.split(' ')
            morse_units = [unit for unit in morse_units if unit]
            return cls._find_all_translations(morse_units, 0, '')
        else:
            # Handle ambiguous morse code without spaces
            morse_chars = list(morse_text)
            return cls._find_ambiguous_translations(morse_chars, 0, '')
    
    @classmethod
    def _find_all_translations(cls, morse_units: List[str], index: int, 
                             current_translation: str) -> List[str]:
        """
        Recursively find all possible translations for spaced Morse code.
        
        Args:
            morse_units: List of morse code units separated by spaces
            index: Current position in the morse_units list
            current_translation: Translation built so far
            
        Returns:
            List of all possible complete translations
        """
        if index >= len(morse_units):
            return [current_translation]
        
        all_translations = []
        
        # First try single morse unit
        current_unit = morse_units[index]
        if current_unit in cls.REVERSE_MORSE_DICT:
            letter = cls.REVERSE_MORSE_DICT[current_unit]
            
            if letter == ' ':
                new_translation = current_translation + ' '
            else:
                new_translation = current_translation + letter
            
            remaining_translations = cls._find_all_translations(
                morse_units, index + 1, new_translation
            )
            
            all_translations.extend(remaining_translations)
        
        # Then try combinations of morse units for ambiguous patterns
        for end_index in range(index + 2, len(morse_units) + 1):
            potential_pattern = ' '.join(morse_units[index:end_index])
            
            if potential_pattern in cls.REVERSE_MORSE_DICT:
                letter = cls.REVERSE_MORSE_DICT[potential_pattern]
                
                if letter == ' ':
                    new_translation = current_translation + ' '
                else:
                    new_translation = current_translation + letter
                
                remaining_translations = cls._find_all_translations(
                    morse_units, end_index, new_translation
                )
                
                all_translations.extend(remaining_translations)
        
        return all_translations
    
    @classmethod
    def _find_ambiguous_translations(cls, morse_chars: List[str], index: int,
                                   current_translation: str) -> List[str]:
        """
        Recursively find all possible translations for ambiguous Morse code.
        
        Args:
            morse_chars: List of individual morse characters (dots and dashes)
            index: Current position in the morse_chars list
            current_translation: Translation built so far
            
        Returns:
            List of all possible complete translations
        """
        if index >= len(morse_chars):
            return [current_translation]
        
        all_translations = []
        
        # Try different pattern lengths (up to 5 characters for longest morse pattern)
        max_pattern_length = min(6, len(morse_chars) - index + 1)
        
        for pattern_length in range(1, max_pattern_length):
            potential_pattern = ''.join(morse_chars[index:index + pattern_length])
            
            if potential_pattern in cls.REVERSE_MORSE_DICT:
                letter = cls.REVERSE_MORSE_DICT[potential_pattern]
                
                # Skip space character in ambiguous mode
                if letter != ' ':
                    new_translation = current_translation + letter
                    
                    remaining_translations = cls._find_ambiguous_translations(
                        morse_chars, index + pattern_length, new_translation
                    )
                    
                    all_translations.extend(remaining_translations)
        
        return all_translations
    
    @classmethod
    def validate_morse_code(cls, morse_text: str) -> bool:
        """
        Validate that a string contains only valid Morse code characters.
        
        Args:
            morse_text: The text to validate
            
        Returns:
            True if the text contains only valid Morse characters
        """
        if not morse_text:
            return True
            
        valid_chars = set('.- /')
        return all(char in valid_chars for char in morse_text)
    
    @classmethod
    def get_supported_characters(cls) -> List[str]:
        """
        Get a list of all characters supported for English to Morse translation.
        
        Returns:
            List of supported characters
        """
        return list(cls.MORSE_CODE_DICT.keys())
