def caesar(s, shift, direction='encrypt'):
    '''
    Caesar cipher function for double encryption and decryption

    Parameters: 
    s (str): input string
    shift (int): number of positions to shift
    direction (str): 'encrypt' or 'decrypt'
    '''

    result = ''
    for char in s: 
        # encrpt uppercase
        if char.isupper():
            base = ord('A')
        elif char.islower():
            base = ord('a')
        else:
            # digits, punctuation, spaces remain the same
            result += char
            continue

        if direction == 'encrypt':
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += chr((ord(char) - base - shift) % 26 + base)
    
    return result

def double_caesar(s, shift1, shift2, direction='encrypt'):
    '''
    Double Caesar cipher function for double encryption and decryption

    Parameters: 
    s (str): input string
    shift1 (int): number of positions to shift for the first pass
    shift2 (int): number of positions to shift for the second pass
    direction (str): 'encrypt' or 'decrypt'
    '''
    if direction == 'encrypt':
        first_go = caesar(s, shift1, direction)
        second_go = caesar(first_go, shift2, direction)
        return second_go
    else: 
        first_go = caesar(s, shift2, direction)
        second_go = caesar(first_go, shift1, direction)
        return second_go

# user input for operation type
operation = input('Encrypt (e) or decrypt (d): ').lower()
if operation not in ['e', 'd']:
    print('Invalid input, please enter e or d.')
else: 
    # user input for string and shift
    s = input('Enter a string: ')
    shift = int(input('Enter first shift value: '))
    shift2 = int(input('Enter second shift value: '))

    result = double_caesar(s, shift, shift2, direction='encrypt' if operation == 'e' else 'decrypt')
    print(f'Result: {result}')        
