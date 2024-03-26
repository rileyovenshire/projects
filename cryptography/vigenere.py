# Vigenere Cipher implementation
# - encryption of alphabetic text by way of polyalphabetic substitution
# - use: uses a keyword where each letter of the keyword refers to a shift used to encrpyt the message. Essentially, we use multiple Caesar ciphers in sequence with different shift values, all determined by the keyword. Goal is to minimize frequency analysis.

def gen_key(msg, key):
    '''
    Expand key/word to match msg length.
    '''
    if len(msg) == len(key):
        return key
    else: 
        # repeat key until is matches msg len
        for i in range(len(msg) - len(key)):
            keyword += keyword[i % len(key)]
    return key

def encrypt(msg, key):
    '''
    encrypt the message using the vigenere ciper
    '''
    cipher = ''
    for i in range(len(msg)):
        if msg[i].isalpha()
        # if character is a letter, shift the letters according to key
        # convert alphanumerically w/ zero index A, add shift, convert back
        shift = ord(key[i].upper()) - ord('A')
        if msg[i].isupper():
            cipher += chr((ord(msg[i]) + shift - ord('A')) % 26 + ord('A'))
        else:
            cipher += chr((ord(msg[i] + shift - ord('a')) % 26 + ord('a'))

    else:
        # if char is a special character, leave it
        cipher += message[i]

    return cipher


def decrypt(cipher, key):
    '''
    Decrypt the message using vigenere
    '''
    decrypted = ''
    
