#! /usr/local/bin/python3


def isValid(s: str) -> bool:
    stack = []
    for ch in s:
        if ch == '(' or ch == '[' or ch == '{':
            stack.append(ch)
        elif not stack:
            break
        elif ch == ')' and stack.pop() != '(':
            break
        elif ch == ']' and stack.pop() != '[':
            break
        elif ch == '}' and stack.pop() != '{':
            break
    else:
        if not stack:
            return True
    return False


def main():
    print(isValid("["))             # False
    print(isValid("()"))            # True
    print(isValid("()[]{}"))        # True
    print(isValid("(]"))            # False
    print(isValid("([)]"))          # False
    print(isValid("{[]}"))          # True


if __name__ == "__main__":
    main()
