#! /usr/local/bin/python3


def decodeString(s: str) -> str:
    stack = []
    for ch in s:
        if ch == ']':
            sub = ''
            while stack[-1] != '[':
                sub = stack.pop() + sub
            stack.pop()
            n = ''
            while stack and stack[-1].isdigit():
                n = stack.pop() + n
            stack.append(sub * int(n))
        else:
            stack.append(ch)
    return ''.join(stack)


def main():
    print(decodeString("3[z]2[2[y]pq4[2[jk]e1[f]]]ef"))
    # "zzzyypqjkjkefjkjkefjkjkefjkjkefyypqjkjkefjkjkefjkjkefjkjkefef"
    print(decodeString("3[a]2[b4[F]c]"))    # "aaabFFFFcbFFFFc"
    print(decodeString("2[abc]3[cd]ef"))    # "abcabccdcdcdef"
    print(decodeString("3[a2[c]]"))         # "accaccacc"
    print(decodeString("3[a]2[bc]"))        # "aaabcbc"


if __name__ == "__main__":
    main()
