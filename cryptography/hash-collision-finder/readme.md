## Hash Collision Finder

This program takes a message and encrypts 24 bits of it using the SHA-256 algorithm provided by OpenSSL. Then, two different brute force methods are run to try and find the message with the same hash (weak) or to find the hash regardless of the message (strong). 

###Usage

    Compile the Program: Navigate to the project directory and compile the program using GCC:
```
gcc -o keyfinder keyfinder.c -lcrypto
```

Ensure that your include and library paths are correctly set if OpenSSL is installed in a custom directory.

###Run the Program: 
After compilation, run the program:
```
./keyfinder
```
    Input File: The program expects a file named words.txt in the same directory. This file should contain possible keys, one per line.

###Key Components

    - EVP Encryption: Uses the EVP interface to encrypt the plaintext.
    - File Reading: Reads potential keys from words.txt.
    - Ciphertext Comparison: Compares the generated ciphertext with the provided target.

###Example

Assuming the plaintext "Hello, World!" and the target ciphertext (from using AES-128-CBC), the words.txt might look like this:
```
key1
key2
correctkey
key4
```
The output will identify correctkey as the correct encryption key if it results in the target ciphertext.
