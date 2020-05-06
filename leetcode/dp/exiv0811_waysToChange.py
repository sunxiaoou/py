#! /usr/local/bin/python3
COIN = [25, 10, 5, 1]
INF = MOD = 1000000007


def waysToChange_slow(n: int) -> int:
    nums = [0] * 4

    for i in range(len(COIN)):
        nums[i] = n // COIN[i]
        n = n % COIN[i]
    # print(nums)
    count = 1
    while True:
        while True:
            while nums[2] > 0:
                nums[2] -= 1
                nums[3] += 5
                # print(nums)
                count += 1
            if nums[1] == 0:
                break
            nums[1] -= 1
            nums[2], nums[3] = divmod(10 + nums[3], 5)
            # print(nums)
            count += 1
        if nums[0] == 0:
            break
        nums[0] -= 1
        nums[1], re = divmod(25 + nums[3], 10)
        nums[2], nums[3] = divmod(re, 5)
        # print(nums)
        count += 1
    return count % MOD


def waysToChange(n: int) -> int:
    count = [0] * (n + 1)
    count[0] = 1
    dp = [-INF] * (n + 1)
    dp[0] = 0
    for i in range(len(COIN)):
        for j in range(COIN[i], n + 1):
            tmp = max(dp[j], COIN[i] + dp[j - COIN[i]])
            cnt = 0
            if tmp == dp[j]:
                cnt += count[j]
            if tmp == COIN[i] + dp[j - COIN[i]]:
                cnt += count[j - COIN[i]]
            if cnt >= MOD:
                cnt -= MOD
            dp[j], count[j] = tmp, cnt
    # print(dp, count)

    res = 0
    for i in range(n + 1):
        if dp[i] == n:
            res += count[i]
            if res >= MOD:
                res -= MOD

    return res


def main():
    print(waysToChange_slow(10))
    print(waysToChange(10))
    print(waysToChange_slow(26))
    print(waysToChange(26))
    print(waysToChange(900750))


if __name__ == "__main__":
    main()
