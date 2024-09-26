from collections import defaultdict
braille_dict = {'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..', 'f': 'OOO...', 'g': 'OOOO..', 
                'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..', 'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.',
                'o': 'O..OO.', 'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.', 'u': 'O...OO',
                'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO', 'y': 'OO.OOO', 'z': 'O..OOO', '1': 'O.....', '2': 'O.O...',
                '3': 'OO....', '4': 'OO.O..', '5': 'O..O..', '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...', 
                '0': '.OOO..', '.': '..OO.O', ',': '..O...', '?': '..O.OO', '!': '..OOO.', ':': '..OO..', ';': '..O.O.',
                '-': '..O...O', '/': '..O.O.O', '(': 'O.O..O', ')': '.OO.OO', '<': '.O..O.', '>': 'O..OO.', 
                'space': '......', 'capital follows': '.....O', 'number follows': '.O.OOO', 'decimal follows': '.O...O'}


reverse_braille_dict = defaultdict(list)

for key, value in braille_dict.items():
    reverse_braille_dict[value].append(key.lower())


def identify_input_type(input_str):
    # Check if the input is a Braille pattern
    def is_braille(s):
        return  all(c in 'O.' for c in s)#len(s) == 6 and
    
    # Check if the input is an English word (letters or punctuation)
    def is_english_word(s):
        return all(c.isalpha() or c in '.,?!:;-/<>()1234567890 ' for c in s)

    # Determine the input type
    if is_braille(input_str):
        return "Braille"
    elif is_english_word(input_str):
        return "English word"
    else:
        return "Unknown or invalid input"



def translate_braille_with_ambiguities(braille_sequence):
    '''braille_patterns = braille_sequence.split()'''
    braille_patterns = [braille_sequence[i:i+6] for i in range(0, len(braille_sequence), 6)]
    # Variables to track current state
    english_output = []
    capital_next = False
    number_mode = False

    for pattern in braille_patterns:
        if pattern == '......':  # Space
            english_output.append(' ')
            number_mode = False
        elif pattern == '.....O':  # Capital follows
            capital_next = True
        elif pattern == '.O.OOO':  # Number follows
            number_mode = True
        else:
            possible_values = reverse_braille_dict[pattern]
            
            if number_mode:
                # In number mode, prioritize numbers if available
                numbers = [val for val in possible_values if val.isdigit()]
                if numbers:
                    english_output.append(numbers[0])  # Select first number
            else:
                # Not in number mode, prioritize letters and handle capitals
                letters = [val for val in possible_values if val.isalpha()]
                if letters:
                    letter = letters[0]  # Select first letter
                    if capital_next:
                        letter = letter.upper()
                        capital_next = False  # Reset capital mode
                    english_output.append(letter)

    return ''.join(english_output)

'''# Example braille input with ambiguities
braille_input = ".....O O..... .....O .O...O O.O... O....."
# "a 2 1 a"
print(translate_braille_with_ambiguities(braille_input))  # Output: "a 2 1 a"'''
def translate_english_to_braille(english_input):
    braille_output = []
    number_mode = False

    for char in english_input:
        if char.isupper():  # Handle capital letters
            braille_output.append(braille_dict['capital follows'])  # Capital indicator
            braille_output.append(braille_dict[char.lower()])  # Braille for lowercase letter
        elif char.isdigit():  # Handle numbers
            if not number_mode:
                braille_output.append(braille_dict['number follows'])  # Number indicator
                number_mode = True  # Enter number mode
            braille_output.append(braille_dict[char])  # Braille for the number
        elif char == ' ':  # Handle spaces
            braille_output.append(braille_dict['space'])  # Braille for space
            number_mode = False  # Exit number mode on space
        elif char in braille_dict:  # Handle lowercase letters and punctuation
            braille_output.append(braille_dict[char])

    return ''.join(braille_output)  # Return space-separated Braille patterns

def translator(input_str):
    if identify_input_type(input_str) == 'Braille':
        return translate_braille_with_ambiguities(input_str)
    elif identify_input_type(input_str) == 'English word':
        return translate_english_to_braille(input_str)
def main():
    print(translator("42"))
    print(translator('.....OO.....O.O...OO...........O.OOOO.....O.O...OO....'))


main()
