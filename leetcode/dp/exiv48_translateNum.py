#! /usr/local/bin/python3


# if nums[i] and nums[i - 1] combine to a number > 25, dp[i] = dp[i - 1]
# otherwise, we need to add extra permutations of the number with
# nums(0 ... i - 2), then it turns out a Fibonacci numbers
def translateNum(num: int) -> int:
    nums = [int(i) for i in list(str(num))]
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        if nums[i - 1] and nums[i - 1] * 10 + nums[i] < 26:
            dp[i] = dp[i - 2] + dp[i - 1]
        else:
            dp[i] = dp[i - 1]
    return dp[-1]


def main():
    print(translateNum(102))            # 2
    print(translateNum(12222))          # 5


if __name__ == "__main__":
    main()
