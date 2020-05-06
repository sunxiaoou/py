#! /usr/local/bin/python3
from typing import List


"""
dp[i] represents min cost of ith day, proximately 
dp[i] = min(dp[i - periods[0]] + costs[0], dp[i - periods[1] + costs[1], dp[i - period[2] + costs[2])
"""

def mincostTickets(days: List[int], costs: List[int]) -> int:
    periods = [1, 7, 30]
    n = days[-1] + 1
    dp = [0] * n
    for i in range(1, n):
        if i in days:
            dp[i] = dp[i - periods[0]] + min(j for j in costs)
            if i < periods[1]:
                dp[i] = min(dp[i], costs[1])
            else:
                dp[i] = min(dp[i], dp[i - periods[1]] + costs[1])
            if i < periods[2]:
                dp[i] = min(dp[i], costs[2])
            else:
                dp[i] = min(dp[i], dp[i - periods[2]] + costs[2])
        else:
            dp[i] = dp[i - 1]

    print([i for i in range(n)])
    print(dp)
    return dp[-1]


def main():
    print(mincostTickets([1, 4, 6, 7, 8, 15], [2, 7, 15]))                          # 11
    print(mincostTickets([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15]))      # 17
    print(mincostTickets([1, 4, 6, 7, 8, 20], [7, 2, 15]))                          # 6
    print(mincostTickets([1,2,3,4,6,8,9,10,13,14,16,17,19,21,24,26,27,28,29], [3,14,50]))   # 50



if __name__ == "__main__":
    main()
