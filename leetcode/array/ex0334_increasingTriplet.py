#! /usr/local/bin/python3
from typing import List


def increasingTriplet2(nums: List[int]) -> bool:
    n = len(nums)
    m0 = -float('inf')
    m2 = float('inf')
    m1 = nums[0]
    for i in range(1, n):
        if nums[i] <= m0:
            m0 = nums[i]
        elif m0 < nums[i] <= m1:
            if m0 != -float('inf'):
                m1, m2 = m0, nums[i]
                m0 = -float('inf')
            else:
                m0 = nums[i]
        elif m1 < nums[i] <= m2:
            m2 = nums[i]
        elif m2 != float('inf'):
            print(m1, m2, nums[i])
            return True
    return False


# Just keep and update minimum number and second minimum number,
# meanwhile wait for third number bigger than second minimum
# We don't need to care sequence of their indexes,
# because if second minimum existed, a origin minimum must exist before it,
# regardless it has been replaced or not.
def increasingTriplet(nums: List[int]) -> bool:
    mini = sec_min = float('inf')
    for i in nums:
        mini = min(mini, i)
        if i > mini:                # mini doesn't change in last sentence
            sec_min = min(sec_min, i)
        if i > sec_min:             # sec_min doesn't change in last sentence
            return True
    return False


def main():
    print(increasingTriplet([1, 2, 1, 2, 1, 2]))            # False
    print(increasingTriplet([1, 0, -1, 1, 2]))              # True
    print(increasingTriplet([1, 0, 0, 1]))                  # False
    print(increasingTriplet([1, 2, 2, 1]))                  # False
    print(increasingTriplet([0, 4, 2, 1, 0, -3, -1]))       # False
    print(increasingTriplet([1, 2, 3, 4, 5]))               # True
    print(increasingTriplet([5, 4, 3, 2, 1]))               # False


if __name__ == "__main__":
    main()
