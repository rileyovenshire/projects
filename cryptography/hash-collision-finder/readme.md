# Hash Collision Project

## Overview

The Hash Collision project is designed to explore the weak and strong collision resistance properties of cryptographic hash functions through a brute-force approach. This project uses a modified version of SHA-256 where only the first 24 bits of the hash output are considered, making the task computationally feasible for educational purposes.

## Features

- **Brute-Force Collision Testing**: Implements brute-force methods to find collisions in a weakened cryptographic hash function.
- **Modified SHA-256 Hashing**: Uses a custom 24-bit output of the SHA-256 hash function to speed up collision finding.
- **Weak vs. Strong Collision Resistance**: Differentiates and tests both weak and strong collision resistance properties.

## Usage

The project includes two main executable components designed to test each type of collision resistance:

1. **Weak Collision Testing**: Finds how many attempts it takes to produce a hash collision with a given initial input and hash.
2. **Strong Collision Testing**: Determines how many attempts are required to find any two distinct inputs that produce the same hash output.

## Running the Hash Collision Testing Program

### Overview

This document explains how to run the Hash Collision Testing Program, which explores the weak and strong collision resistance properties of cryptographic hash functions. The program simulates a brute-force attack to discover how many attempts are required to find collisions when only the first 24 bits of SHA-256 hash outputs are considered.

### How to Run the Program

1. **Compilation**: First, compile the program using GCC or any compatible C compiler. Ensure that the OpenSSL library is correctly linked. Here is the command to compile the program:

    ```bash
    gcc -o collision_test collision.c -lcrypto
    ```

    This command compiles the `collision.c` file into an executable named `collision_test`, linking against the OpenSSL cryptographic library (`-lcrypto`).

2. **Execution**: Run the compiled program directly from the command line:

    ```bash
    ./collision_test
    ```

    This command executes the `collision_test` binary. When run, the program will perform multiple tests to find weak and strong collisions, repeating each test to gather statistically significant data.

### Expected Output

Upon execution, the program outputs the average number of attempts (trials) required to find a weak collision and a strong collision. Here's an example of what the output might look like:
```
Weak collision average trial count to find message: 7937634
Strong collision average trial count to find hash: 12116
```
Each line provides the average number of trials over multiple repetitions to find a collision. The weak collision line reports on the challenge of finding another input that hashes to the same output as a predetermined input. In contrast, the strong collision line reflects the effort to find any two distinct inputs that result in the same hash output.

## Understanding the Output

### Weak Collision Resistance

- **What it Shows**: The average number of trials needed to find a second input that matches the hash of a given input.
- **Interpretation**: A higher number of trials indicates a strong weak collision resistance, as it suggests that it is difficult to find another message that hashes to the same value as any given message.

### Strong Collision Resistance

- **What it Shows**: The average number of trials needed to find any two distinct inputs that hash to the same output.
- **Interpretation**: Fewer trials needed to find a strong collision, as compared to a weak collision, highlight the impact of the Birthday Paradox. This paradox suggests that it is statistically easier to find any collision among a set of random inputs than to match a specific input's hash.

### Analyzing Trends

The consistent finding of fewer trials for strong collisions than for weak collisions supports the theoretical understanding of hash functions and collision resistance. This real-world experiment underlines why cryptographic applications must carefully consider the hash function and output size they employ to ensure security against both types of collisions.

In summary, these results validate the cryptographic principles that guide the design of hash functions, especially concerning their use in environments where security against brute-force attacks is a critical concern.

