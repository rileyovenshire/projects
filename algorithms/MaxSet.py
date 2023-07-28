# Given a list of numbers, return a subsequence of non-consecutive numbers in the form of a
# list that would have the maximum sum. When the numbers are all negatives your code
# should return []

# sources: https://www.geeksforgeeks.org/maximum-sum-such-that-no-two-elements-are-adjacent/
# https://www.youtube.com/watch?v=UtGtF6nc35g
# Group discussion, group 4



def max_independent_set(nums):
    """
    Finds the maximum sum of non-consecutive numbers in a list that would have the maximum sum.
    """
    # check length
    length = len(nums)
    if length == 0:
        return []
    if length == 1:
        return nums
    # check if all nums are negative
    if max(nums) < 0:
        return []
    if max(nums) == 0:
        return [0]

    # start building dynamic programming table
    table = [0] * length
    table[0] = nums[0]
    table[1] = max(nums[0], nums[1])

    # iterate through remaining numbers
    for i in range(2, length):
        table[i] = max(nums[i] + table[i - 2], table[i - 1])
    if table[-1] <= 0:
        return []
    else:
        # create a list of the numbers that make up the max sum
        result = []
        i = length - 1

        while i >= 0:
            # if current num is in max sum, add it to the result list
            if nums[i] == table[i] or nums[i] + table[i - 2] == table[i]:
                result.append(nums[i])
                i -= 2
            else:
                # or move on to next num
                i -= 1
    result.reverse()
    return result