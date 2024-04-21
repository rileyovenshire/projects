#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* ----------------------------------------------------------------------------
 * HASH COLLISION DETECTION
 *
 * - this program works to push the resistance properties of weak and strong collision
 *   	in regard to hash functions via brute force collision
 * - program in detail:
 *	 1.) 24 bit hash calculation using sha-256, using only the first 24 bits
 *	 2.) weak collision - generate random messages until we get the same hash output
 *	 	that demonstrates a weak collision
 *	 3.) strong collision - generates random messages and logs hashes until a repeat is found,
 *	 	demonstrating a strong collision (regardless of message content)
 *	 4.) runs both the weak and strong tests, then reports the number of iterations
 *	 	until the weak and strong collisions were found
 *
 * USAGE:
 * - compile with : gcc -o main collision.c -lcrypto
 * - run ./main
 * - results will take < 10 seconds
 *
 * SOURCE(S):
 * - extensive use of man pages: https://www.openssl.org/docs/man1.1.1/man3/EVP_DigestInit.html
 * - referenced the wiki page for the same concept 
 *----------------------------------------------------------------------------*/

// 24-bit hashing using the sha-256 algo
unsigned long do_24bit_hash(const unsigned char *msg, size_t msg_len) {
	// create a hash buffer with max size, from docs
	unsigned char hash[EVP_MAX_MD_SIZE];
	unsigned int hash_len;

	// context
	EVP_MD_CTX *mdctx;
	if ((mdctx = EVP_MD_CTX_new()) == NULL) {
	       fprintf(stderr, "Hash context creation failure.\n");
       		return 0;
	}

	// use sha256 hashing
	// referenced the docs for the application of DigestInit and the EVP_sha256 functions
	if (1 != EVP_DigestInit_ex(mdctx, EVP_sha256(), NULL)) {
		fprintf(stderr, "Hash init failure.\n");
		EVP_MD_CTX_free(mdctx);	
		return 0;
	}

	// read in message (msg) using DigestUpdate, hashing msg_len bytes of data
	if (1 != EVP_DigestUpdate(mdctx, msg, msg_len)) {
		fprintf(stderr, "Message read failure.\n");
		EVP_MD_CTX_free(mdctx);
		return 0;
	}

	// finish by finalizing the hash, moving right along in the manual page with DigestFinal
	if (1 != EVP_DigestFinal_ex(mdctx, hash, &hash_len)) {
		fprintf(stderr, "Hash finalization failure.\n");
		EVP_MD_CTX_free(mdctx);
		return 0;
	}

	// clean up, like before
	EVP_MD_CTX_free(mdctx);

	// converting the first 3 bytes into a single int (3bytes * 8bit per byte = 24bits)
	// take the bytes at [0, 1, 2] which are cast to unsigned longs for bit shifting
	// shifting 0 << 16 to shift it left by 16
	// shiting 1 << 8 to shift it left by 8
	// 2 stays where it is, at the start of the bits
	// bitwise | OR, convert the 3 values into one 32 bit int
	return ((unsigned long)hash[0] << 16) | ((unsigned long)hash[1] << 8) | hash[2];
}

/* --------------------------------------------------------------------------------------------------------
 * WEAK COLLISION
 *
 * - generate random messages to find one that has the same hash as enc msg
 *-----------------------------------------------------------------------------------------------*/
unsigned int weak_coll(const unsigned char *msg, size_t msg_len) {
	// hash given msg
	unsigned long target_hash = do_24bit_hash(msg, msg_len);

	// bitwise NOT to guarantee there is a difference
	// see https://www.geeksforgeeks.org/bitwise-operators-in-c-cpp/ for guidance on use
	unsigned long coll_hash = ~target_hash;
	unsigned int counter = 0;

	// store the messages generated
	unsigned char new_msg[1024];

	// seed rand()
	srand(time(NULL));

	// begin generating new_msg until we collide
	while (coll_hash != target_hash) {
		sprintf(new_msg, "Random message: %d", rand());

		// hash new_msg with previously written function
		coll_hash = do_24bit_hash(new_msg, strlen(new_msg));
		counter++;
	}

	return counter;
}

/* ---------------------------------------------------------------------------
 * STRONG COLLLISION
 *
 * - brute force to find two different messages that end up with the same hash
 * - there are 2^24 possible hash values == 16777215
 * - source: https://kevingal.com/apps/collision.html
 * --------------------------------------------------------------------------*/

unsigned int strong_coll() {
	// init potential hash values with zeroes -- see source above for info
	// 2**24	
	// DEBUG: stack overflow segfault caused by this array, dynamic allocation of 
	// memory applied
	// C: A Modern Approach by King used as a reference to handle large array
	// 	memory allocation with calloc
	
	unsigned long *hashes = calloc(16777216, sizeof(unsigned long));

	if (hashes == NULL) {
		fprintf(stderr, "Couldn't allocate memory.\n");
		exit(1);
	}

	unsigned long current_hash;
	unsigned int counter = 0;

	// messages buffer
	unsigned char msg[1024];

	// seed rand
	srand(time(NULL));

	while(1) {
		sprintf(msg, "Random message: %d", rand());
		current_hash = do_24bit_hash(msg, strlen(msg));

		// condition to check if this hash already exists in our bank,
		// if so we have found the collision
		if (current_hash < 16777216 && hashes[current_hash]) {
			break;
		}

		// flip 0 to 1, making it known that we have seen this hash before
		hashes[current_hash] = 1;
		counter++;
		}

	// clean and free to avoid so
	free(hashes);

	return counter;
}

/* -------------------------------------------------------------------------------------------------
 * MAIN
 *
 * - takes a messaage and calls both functions
 *-------------------------------------------------------------------------------------------------*/
int main() {
	const char *msg = "This is a top secret.";

	// function calls, strong takes no args
	unsigned int weaktrials = weak_coll((unsigned char *)msg, strlen(msg));
	unsigned int strongtrials = strong_coll();

	// report results
	printf("Weak collision average trial count to find message: %u\n", weaktrials);
	printf("Strong collision average trial count to find hash: %u\n", strongtrials);

	return 0;
}
