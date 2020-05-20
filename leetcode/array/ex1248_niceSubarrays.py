#! /usr/local/bin/python3
from typing import List


def numberOfSubarrays(nums: List[int], k: int) -> int:
    s, ps = 0, [0]              # ps is prefix_sums, it needs an extra 0 at head
    for i in nums:
        if i % 2:
            s += 1
        ps.append(s)
    print(ps)

    count = 0                   # the case can convert a two_sum problem
    two_sum = {}
    # sum: ps[i] = ps[j] + k (0 <= j <= i), count number of ps[j]
    for i in range(len(ps)):
        d = ps[i] - k
        if d in two_sum:
            count += two_sum[d]
        if ps[i] in two_sum:
            two_sum[ps[i]] += 1
        else:
            two_sum[ps[i]] = 1
    print(two_sum)
    return count


def main():
    print(numberOfSubarrays([1, 1, 2, 1, 1], 3))                  # 2
    print(numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2))   # 16


if __name__ == "__main__":
    main()
