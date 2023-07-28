# Write the implementation to solve the powerset problem discussed in the exercise
# of the exploration: Backtracking. Name your function powerset(inputSet). Name
# your file PowerSet.py

# Given a set of n distinct numbers return its power set. Write the pseudocode to return the powerset.
# Example:
#
# Input: [1,2,3]
#
# Output: [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]

# Sources: https://www.geeksforgeeks.org/power-set/
#           Exploration - Backtracking: Used the pseudocode from the exploration to write the code.

def powerset(inputSet):
    """
    Returns the powerset of the input set from Backtracking Exploration.
    """
    length = len(inputSet)
    results = []
    backtrack(0, [], inputSet, length, results)
    return results


def backtrack(index, current, inputSet, length, results):
    """
    Backtracks through the input set to find the powerset.
    """
    # add existing subset
    results.append(list(current))

    # iterate through remaining numbers
    for i in range(index, length):
        current.append(inputSet[i])
        backtrack(i + 1, current, inputSet, length, results)
        current.pop()


# examples
# print(powerset([1, 2, 3]))
# print(powerset([]))