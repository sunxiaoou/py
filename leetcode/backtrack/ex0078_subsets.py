#! /usr/local/bin/python3
from typing import List


def continuousSubsets(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    res = [[]]
    for i in range(n):
        for j in range(i + 1):
            ans = []
            for k in range(j, i + 1):
                ans.append(nums[k])
            res.append(ans)
    return res


# for [1, 2, 3], start result from empty subset []
# take 1, append [] + 1 = [1]
# result = [[], [1]]
# take 2, append [] + 2 = [2], [1] + 2 = [1, 2]
# result = [[], [1], [2], [1, 2]]
# take 3, append [] + 3 = [3], [1] + 3 = [1, 3], [2] + 3 = [2, 3], [1, 2] + 3 = [1, 2, 3]
# result = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

def subsets2(nums: List[int]) -> List[List[int]]:
    res = [[]]
    for i in nums:
        ans = []
        for j in res:
            ans.append(j + [i])     # don't use j.append(i) because we need a new list here
        res += ans[:]
    return res


def subsets(nums: List[int]) -> List[List[int]]:

    def backtrack(first: int, curr: List[int]):
        # print(curr)
        if len(curr) == k:
            output.append(curr[:])
            return
        for i in range(first, n):
            # add nums[i] into the current combination
            curr.append(nums[i])
            # use next integers to complete the combination
            backtrack(i + 1, curr)
            # backtrack
            curr.pop()

    output = []
    n = len(nums)
    for k in range(n + 1):
        backtrack(0, [])
    return output


def main():
    print(subsets([1, 2, 3]))   # [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]


if __name__ == "__main__":
    main()
