# DNA sequence is made of characters A, C, G and T, which represent nucleotides. A sample
# DNA string can be given as ‘ACCGTTTAAAG’. Finding similarities between two DNA
# sequences is a critical computation problem that is solved in bioinformatics.
# Given two DNA strings find the length of the longest common string alignment between
# them (it need not be continuous). Assume empty string does not match with anything.


# consulted sources: https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
# Exploration   -   Dynamic Programming, Longest Common Subsequence


def dna_match_topdown(DNA1, DNA2):
    """DP implementation from a top-down approach to find the length of the LCS between 2 DNA strand strings."""
    # base case
    if len(DNA1) == 0 or len(DNA2) == 0:
        return 0

    # recursive case - check if first characters match
    if DNA1[0] == DNA2[0]:
        # if they match, return 1 + the rest of the string (hence the slice)
        return 1 + dna_match_topdown(DNA1[1:], DNA2[1:])
    else:
        # if they don't match, return the max of the rest of the string
        return max(dna_match_topdown(DNA1[1:], DNA2), dna_match_topdown(DNA1, DNA2[1:]))


def dna_match_bottomup(DNA1, DNA2):
    """DP implementation from a bottom-up approach to find the length of the LCS between 2 DNA strand strings."""
    m = len(DNA1)
    n = len(DNA2)

    # create a table to store the results of subproblems - with extra space for base cases
    # took this code from the Exploration
    cache = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # fill the table in bottom-up fashion
    # code used from the Exploration
    for i in range(m + 1):
        for j in range(n + 1):
            # base case
            if i == 0 or j == 0:
                cache[i][j] = 0
            # recursive case - check if first characters match
            elif DNA1[i - 1] == DNA2[j - 1]:
                cache[i][j] = cache[i - 1][j - 1] + 1
            else:
                cache[i][j] = max(cache[i - 1][j], cache[i][j - 1])

    # return the last value in the table (bottom right corner)
    return cache[m][n]


# test cases
DNA_1 = 'ATAGTTCCGTCAAA'
DNA_2 = 'GTGTTCCCGTCAAA'


# shared subsequence: TGTCCGTCAAA
# length: 12
print(dna_match_topdown(DNA_1, DNA_2))
print(dna_match_bottomup(DNA_1, DNA_2))
