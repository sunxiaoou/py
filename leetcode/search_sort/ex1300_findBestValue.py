#! /usr/local/bin/python3
from typing import List


def findBestValue(arr: List[int], target: int) -> int:
    n = len(arr)
    arr.sort()
    # print(arr)

    le, ri = 0, n - 1
    while le <= ri:             # bin search in numbers
        mid = (le + ri) // 2
        su = sum(arr[: mid]) + arr[mid] * (n - mid)
        if su == target:
            return arr[mid]
        if su < target:
            le = mid + 1
        else:
            ri = mid - 1

    if ri < 0:                  # res is less than all numbers
        av = target // n        # return average or average + 1
        return av if abs(av * n - target) < abs((av + 1) * n - target) else av + 1
    if le > n - 1:              # res is bigger than all numbers
        return max(arr)         # return maximum in numbers

    a2 = list(range(arr[ri], arr[le] + 1))      # bin search in missing numbers
    # print(a2)
    le, ri = 0, len(a2) - 1
    while le <= ri:
        m2 = (le + ri) // 2
        if arr[mid] < a2[m2]:           # if origin mid < current mid, keep it
            su = sum(arr[: mid + 1]) + a2[m2] * (n - 1 - mid)
        else:                           # otherwise, use current mid instead
            su = sum(arr[: mid]) + a2[m2] * (n - mid)
        if su == target:
            return a2[m2]
        if su < target:
            le = m2 + 1
        else:
            ri = m2 - 1
        # print(le, ri, m2, su - target)
    sl = abs(sum(arr[: mid + 1]) + a2[le] * (n - 1 - mid) - target)
    sr = abs(sum(arr[: mid + 1]) + a2[ri] * (n - 1 - mid) - target)
    return a2[le] if sl < sr else a2[ri]    # if differences are same, return the less one


def main():
    print(findBestValue([1, 2, 23, 24, 34, 36], 110))                   # 30
    print(findBestValue([1547, 83230, 57084, 93444, 70879], 71237))     # 17422
    print(findBestValue([60864, 25176, 27249, 21296, 20204], 56803))    # 11361
    print(findBestValue([3, 5, 9], 10))     # 3
    print(findBestValue([4, 9, 3], 10))     # 3
    print(findBestValue([2, 3, 5], 10))     # 5


if __name__ == "__main__":
    main()
