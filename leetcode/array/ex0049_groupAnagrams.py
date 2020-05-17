#! /usr/local/bin/python3
from typing import List


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    # key is a string has sorted chars, value is a list of strings include same chars
    dictionary = {}
    for s in strs:
        key = ''.join(sorted([s[i] for i in range(len(s))]))
        if key not in dictionary:
            dictionary[key] = [s]
        else:
            dictionary[key].append(s)
    return list(dictionary.values())


def main():
    print(groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [["ate","eat","tea"], ["nat","tan"], ["bat"]]


if __name__ == "__main__":
    main()
