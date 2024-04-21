# KeyFinder Project

## Overview

The KeyFinder project is designed to demonstrate the usage of OpenSSL's cryptographic functions in a C programming environment. It explores how a given plaintext encrypted with AES-128-CBC encryption under different keys can be used to identify the correct encryption key from a provided list. The project emphasizes understanding and implementing OpenSSL's EVP encryption to find which key from a given list correctly encrypts a specified plaintext to match a predefined ciphertext.

## Requirements

- **openssl
- **gcc

### Usage

Compile the Program: Navigate to the project directory and compile the program using gcc:

```
gcc -o keyfinder keyfinder.c -lcrypto
```

Ensure that your include and library paths are correctly set if OpenSSL is installed in a custom directory.

Run the Program: After compilation, run the program:

```
    ./keyfinder
```

Input File: The program expects a file named words.txt in the same directory. This file should contain possible keys, one per line.

### Program Structure

    keyfinder.c: The main program file containing C code to perform the encryption and match the ciphertext with the provided ciphertext.

### Key Components

    EVP Encryption: Uses the EVP interface to encrypt the plaintext.
    File Reading: Reads potential keys from words.txt.
    Ciphertext Comparison: Compares the generated ciphertext with the provided target.

### Example

Assuming the plaintext "Hello, World!" and the target ciphertext (from using AES-128-CBC), the words.txt might look like this:

```
key1
key2
correctkey
key4
```

The output will identify correctkey as the correct encryption key if it results in the target ciphertext.
Sources for the project are included in the C file!
