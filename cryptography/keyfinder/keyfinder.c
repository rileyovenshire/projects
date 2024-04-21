#include <openssl/evp.h>
#include <openssl/aes.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* --------------------------------------------------------------------------------
 * ENCRYPTION
 *
 * - performs aes-128 cbc encryption
 * - takes in plaintext, key, iv. 
 * - allocates buffer for ciphertext
 * - standard returns, 0 for success and 1 for failure
 * - SOURCE(S):
 *   	- OpenSSL wiki - https://wiki.openssl.org/index.php/EVP_Symmetric_Encryption_and_Decryption#Encrypting_the_message
 * ------------------------------------------------------------------------------*/
int encrypt(const unsigned char *plaintext, int plaintext_len, unsigned char *key, unsigned char *iv, unsigned char *ciphertext) {
	// set up context
	EVP_CIPHER_CTX *ctx;
	int len;
	int ciphertext_len;

	// error handling - return 1
	if (!(ctx = EVP_CIPHER_CTX_new()))
		return 1;
	if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv))
		return 1;

	// get message to be encrypted
	if (1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
		return 1;
	ciphertext_len = len;

	// finalizing the encryption
	if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len))
		return 1;
	ciphertext_len += len;

	// cleaning up and finalizing
	EVP_CIPHER_CTX_free(ctx);

	return 0;
}

/* --------------------------------------------------------------------------------
 * CHECK PLAINTEXT LENGTH
 *
 * - helper function to ensure that the plaintext has a length of 21
 * -------------------------------------------------------------------------------*/
int check_length(const char *filename) {
	FILE *file = fopen(filename, "rb");
	if (!file) {
		perror("File read failure.");
		return -1;
	}

	// go to the end of the file
	fseek(file, 0, SEEK_END);
	int file_length = ftell(file);
	fclose(file);

	return file_length;
}

/* --------------------------------------------------------------------------------
 * MAIN
 *
 * - read file words.txt, padding along the way to form 16 byte keys
 * - perform encryption with given key
 * - if we find the correct key after calling encrypt and memcmp-ing, we print it
 * - tries all words and exits if it cannot find the key
 * - SOURCE(S):
 *   	- OpenSSL docs: same URL as above, but in the "Setting It Up" section
 *   	- Project notes, used the plaintext and ciphertext provided 
 * ------------------------------------------------------------------------------*/

int main(void) {
	// known plaintext - from the project page
	// "This is a top secret." > plaintext.txt
	const char *plaintext_filename = "plaintext.txt";
	int plaintext_length = check_length(plaintext_filename);
	if (plaintext_length != 22) {
		fprintf(stderr, "Plaintext file length is incorrect. Must be 21 char.\n");
		return 1;
	}

	// read the plaintext from the file into a buffer of 22 char for null term
	FILE *plaintext_file = fopen(plaintext_filename, "rb");
	unsigned char plaintext[22];
	if (fread(plaintext, 1, 21, plaintext_file) != 21) {
		perror("Plaintext read error.");
		return 1;
	}

	// actual saving of the text
	// close that mah and move on
	plaintext[21] = '\0';
	fclose(plaintext_file);

	// example in source gives 256 bit key, but we only need 128 bits, so this is our expected result in hex
	// from the project page - just to be completely clear I also had chatGPT format this into a dict for me after giving it the ciphertext in hex
	unsigned char expected_ciphertext[] = {
		0x8d, 0x20, 0xe5, 0x05, 0x6a, 0x8d, 0x24, 0xd0,
		0x46, 0x2c, 0xe7, 0x4e, 0x49, 0x04, 0xc1, 0xb5,
		0x13, 0xe1, 0x0d, 0x1d, 0xf4, 0xa2, 0xef, 0x2a,
		0xd4, 0x54, 0x0f, 0xae, 0x1c, 0xa0, 0xaa, 0xf9
	};

	// ciphertext needs a buffer  of 128 bits
	unsigned char ciphertext[128];

	// init vector is filled with zeros to begin
	unsigned char iv[16] = {0};

	// open words.txt
	FILE *file = fopen("words.txt", "r");
	if (!file) {
		perror("Couldn't open file.");
		return 1;
	}

	// potential key words, pulled from dict and put into buffer
	// 16 bit max with an additional spot for the null terminator
	char word[17];

	while (fgets(word, sizeof(word), file)) {
		// remove the new line character at the end
		size_t len = strlen(word);
		if (word[len-1] == '\n') {
		       // null it and negate len
		       word[len-1]='\0';
	      		--len;
		}

		// padding the word with spaces to make it 16 chars
		memset(word + len, ' ', 16 - len);

		// encrypt the plaintext with the key using function from before
		if (encrypt(plaintext, strlen(plaintext), (unsigned char*)word, iv, ciphertext) == 0) {
		
		// make the comparison (mentioned above)
		if (memcmp(ciphertext, expected_ciphertext, sizeof(expected_ciphertext)) == 0) {
			printf("Key found! Key is: '%s'\n", word);
			fclose(file);
			return 0;
		}
	}
}

// no key found :(
printf("No key found.\n");
fclose(file);
return 1;
}


