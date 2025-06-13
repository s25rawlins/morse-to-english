MORSE_CODE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',
    'F': '..-.',   'G': '--.',    'H': '....',   'I': '..',     'J': '.---',
    'K': '-.-',    'L': '.-..',   'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',    'S': '...',    'T': '-',
    'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',   'Y': '-.--',
    'Z': '--..',   '1': '.----',  '2': '..---',  '3': '...--',  '4': '....-',
    '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',  '9': '----.',
    '0': '-----',  ' ': '/'
}

REVERSE_MORSE_DICT = {morse: letter for letter, morse in MORSE_CODE_DICT.items()}


def english_to_morse(english_text):
    english_text = english_text.upper()
    morse_result = []
    
    for char in english_text:
        if char in MORSE_CODE_DICT:
            morse_result.append(MORSE_CODE_DICT[char])
        else:
            morse_result.append('?')
    
    return ' '.join(morse_result)


def morse_to_english(morse_text):
    morse_text = morse_text.strip()
    
    if not morse_text:
        return ['']
    
    if ' ' in morse_text:
        morse_units = morse_text.split(' ')
        morse_units = [unit for unit in morse_units if unit]
        return _find_all_translations(morse_units, 0, '')
    else:
        morse_chars = list(morse_text)
        return _find_ambiguous_translations(morse_chars, 0, '')


def _find_all_translations(morse_units, index, current_translation):
    if index >= len(morse_units):
        return [current_translation]
    
    all_translations = []
    
    for end_index in range(index + 1, len(morse_units) + 1):
        potential_pattern = ' '.join(morse_units[index:end_index])
        
        if potential_pattern in REVERSE_MORSE_DICT:
            letter = REVERSE_MORSE_DICT[potential_pattern]
            
            if letter == ' ':
                new_translation = current_translation + ' '
            else:
                new_translation = current_translation + letter
            
            remaining_translations = _find_all_translations(
                morse_units, end_index, new_translation
            )
            
            all_translations.extend(remaining_translations)
    
    return all_translations


def _find_ambiguous_translations(morse_chars, index, current_translation):
    if index >= len(morse_chars):
        return [current_translation]
    
    all_translations = []
    
    for pattern_length in range(1, min(6, len(morse_chars) - index + 1)):
        potential_pattern = ''.join(morse_chars[index:index + pattern_length])
        
        if potential_pattern in REVERSE_MORSE_DICT:
            letter = REVERSE_MORSE_DICT[potential_pattern]
            
            if letter != ' ':
                new_translation = current_translation + letter
                
                remaining_translations = _find_ambiguous_translations(
                    morse_chars, index + pattern_length, new_translation
                )
                
                all_translations.extend(remaining_translations)
    
    return all_translations


def run_demo():
    print("=== Morse Code Translation Demo ===\n")
    
    print("1. English to Morse Translation:")
    test_phrases = ["HELLO WORLD", "SOS", "PUPPY", "A B C"]
    
    for phrase in test_phrases:
        morse = english_to_morse(phrase)
        print(f"   '{phrase}' -> '{morse}'")
    
    print("\n2. Morse to English Translation:")
    test_morse = [
        ".... . .-.. .-.. --- / .-- --- .-. .-.. -..",
        "... --- ...",
        ".- / -... / -.-."
    ]
    
    for morse in test_morse:
        english_options = morse_to_english(morse)
        print(f"   '{morse}' -> {english_options}")
    
    print("\n3. Ambiguous Morse Code:")
    ambiguous_cases = ["...-.", "-..-."]
    
    for morse in ambiguous_cases:
        english_options = morse_to_english(morse)
        print(f"   '{morse}' -> {english_options}")
        print(f"      (Found {len(english_options)} possible interpretation(s))")


def interactive_english_to_morse():
    print("\n=== English to Morse Code Translation ===")
    print("Enter English text to convert to Morse code.")
    print("(Supports letters A-Z, digits 0-9, and spaces)")
    
    while True:
        english_input = input("\nEnter English text (or 'back' to return to menu): ").strip()
        
        if english_input.lower() == 'back':
            break
        
        if not english_input:
            print("Please enter some text to translate.")
            continue
        
        morse_result = english_to_morse(english_input)
        
        print(f"\nInput:  '{english_input}'")
        print(f"Morse:  '{morse_result}'")
        print(f"Characters: {len(english_input)} -> Morse units: {len(morse_result.split())}")


def interactive_morse_to_english():
    print("\n=== Morse Code to English Translation ===")
    print("Enter Morse code to convert to English.")
    print("Format options:")
    print("  - Standard: Use spaces between letters (e.g., '.- -... -.-.')")
    print("  - Ambiguous: No spaces for multiple interpretations (e.g., '.-...-.')")
    print("  - Word breaks: Use '/' for spaces between words")
    
    while True:
        morse_input = input("\nEnter Morse code (or 'back' to return to menu): ").strip()
        
        if morse_input.lower() == 'back':
            break
        
        if not morse_input:
            print("Please enter some Morse code to translate.")
            continue
        
        valid_chars = set('.- /')
        if not all(char in valid_chars for char in morse_input):
            print("Invalid characters in Morse code. Use only dots (.), dashes (-), spaces, and slashes (/).")
            continue
        
        english_results = morse_to_english(morse_input)
        
        print(f"\nMorse input: '{morse_input}'")
        
        if not english_results:
            print("No valid English translations found.")
            print("Check that your Morse code uses valid patterns.")
        elif len(english_results) == 1:
            print(f"English:     '{english_results[0]}'")
        else:
            print(f"Found {len(english_results)} possible interpretations:")
            for i, result in enumerate(english_results, 1):
                print(f"  {i}. '{result}'")


def display_menu():
    print("\n" + "="*50)
    print("    MORSE CODE TRANSLATOR")
    print("="*50)
    print("1. English to Morse Code")
    print("2. Morse Code to English") 
    print("3. Run Demo (show test cases)")
    print("4. Exit")
    print("-"*50)


def get_menu_choice():
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= 4:
                return choice_num
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("Morse Code Translator")
    
    while True:
        display_menu()
        choice = get_menu_choice()
        
        if choice == 1:
            interactive_english_to_morse()
        elif choice == 2:
            interactive_morse_to_english()
        elif choice == 3:
            run_demo()
        elif choice == 4:
            print("\nGoodbye World")
            break


if __name__ == "__main__":
    main()
