#! /usr/local/bin/python3


def minWindow(s: str, t: str) -> str:

    def found_all(dic: dict, d2: dict) -> bool:
        return all(dic[k] <= d2[k] for k in dic.keys())

    dic, d2 = {}, {}
    for ch in t:
        if ch not in dic:
            dic[ch] = 1
        else:
            dic[ch] += 1
        d2[ch] = 0

    mini = ""
    le, ri = -1, 0
    while True:
        while ri < len(s) and not found_all(dic, d2):
            if s[ri] in t:
                d2[s[ri]] += 1
                if le == -1:
                    le = ri
            ri += 1
        if not found_all(dic, d2):
            break
        print(d2, s[le: ri])
        if not mini or len(s[le: ri]) < len(mini):
            mini = s[le: ri]
        d2[s[le]] -= 1
        le += 1
        while le < ri and s[le] not in t:
            le += 1
    return mini


def main():
    print(minWindow("bba", "ab"))                   # "ba"
    print(minWindow("ADOBECODEBANC", "ABC"))        # "BANC"
    print(minWindow("a", "aa"))                     # ""


if __name__ == "__main__":
    main()
