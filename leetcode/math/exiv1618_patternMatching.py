#! /usr/local/bin/python3


def patternMatching(pattern: str, value: str) -> bool:
    if not pattern:
        return not value                # v "" matches p ""
    if not value:
        return len(pattern) == 1        # v "" matches p "a" or "b"
    m, n = len(pattern), len(value)
    ca = pattern.count("a")             # count of a
    cb = m - ca                         # count of b
    if not ca or not cb:
        return value[: n // m] * m == value     # summary of parts equal entirety

    for i in range((n + 1) // ca):              # try different length of a
        j, r = divmod(n - i * ca, cb)
        if r:                                   # not integer, illegal length of b
            continue                            # skip
        sa, sb = set(), set()
        k = 0
        for ch in pattern:                      # split value to a and b
            if ch == 'a':
                sa.add(value[k: k + i])
                k += i
            else:
                sb.add(value[k: k + j])
                k += j
        if len(sa) == len(sb) == 1:             # all a are same, all b are same
            return True
    return False


def main():
    print(patternMatching("bbab", "bbaa"))              # True, as b is empty
    print(patternMatching("b", ""))                     # True
    print(patternMatching("", "x"))                     # False
    print(patternMatching("aabab", "catcatgocatgo"))    # True
    print(patternMatching("aaaa", "dogdogdogdog"))      # False
    print(patternMatching("abba", "dogcatcatdog"))      # True
    print(patternMatching("abba", "dogcatcatfish"))     # False
    print(patternMatching("abba", "dogdogdogdog"))      # True


if __name__ == "__main__":
    main()
