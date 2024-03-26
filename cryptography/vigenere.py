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
        key = list(key)
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt(msg, key):
    '''
    encrypt the message using the vigenere ciper
    '''
    cipher = ''
    k_index = 0
    for i in msg:
        if i.isalpha():
            shift = ord(key[k_index].upper()) - ord('A')
            k_index = (k_index + 1) % len(key)
            if i.isupper():
                cipher += chr((ord(i) + shift - ord('A')) % 26 + ord('A'))
            else:
                cipher += chr((ord(i) + shift - ord('a')) % 26 + ord('a'))
        else:
            cipher += i
    return cipher


def decrypt(cipher, key):
    '''
    Decrypt the message using vigenere
    '''
    decrypted = ''
    k_index = 0
    for i in cipher:
        if i.isalpha():
            shift = ord(key[k_index].upper()) - ord('A')
            k_index = (k_index + 1) % len(key)
            if i.isupper():
                decrypted += chr((ord(i) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted += chr((ord(i) - shift - ord('a')) % 26 + ord('a'))
        else:
            decrypted += i
    return decrypted

# ----------------------------
if __name__ == '__main__':
    msg = input('Enter message: ')
    key = input('Enter key: ')

    key = gen_key(msg, key)

    encrypted = encrypt(msg, key)
    print("Encrypted: ", encrypted)


    decrypted = decrypt(encrypted, key)
    print("Decrypted: ", decrypted)

