#! /usr/local/bin/python3


def countAndSay(n: int) -> str:
    nums = [1]
    for i in range(1, n):
        res = []
        val = nums[0]
        k = 1
        for j in range(1, len(nums)):
            if nums[j] == val:
                k += 1
            else:
                res.append(k)
                res.append(val)
                val = nums[j]
                k = 1
        res.append(k)
        res.append(val)
        nums = res
        # print(nums)
    return ''.join(str(i) for i in nums)


def main():
    print(countAndSay(5))           # "111221"


if __name__ == "__main__":
    main()
