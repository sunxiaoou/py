#! /usr/local/bin/python3
from typing import List


def evil(b: str, a: str, op: str) -> int:
    res = eval(a + op + b)
    if op == "/":
        res = int(res)
    # print(a + " " + op + " " + b + " = " + str(res))
    return res


def evalRPN(tokens: List[str]) -> int:
    if len(tokens) == 1:
        return int(tokens[0])
    stack = []
    res = 0
    for i in tokens:
        if i in ["+", "-", "*", "/"]:
            res = evil(stack.pop(), stack.pop(), i)
            stack.append(str(res))
        else:
            stack.append(i)
    return res


def main():
    tokens = ["-78","-33","196","+","-19","-","115","+","-","-99","/","-18","8","*","-86","-","-","16","/","26","-14","-","-","47","-","101","-","163","*","143","-","0","-","171","+","120","*","-60","+","156","/","173","/","-24","11","+","21","/","*","44","*","180","70","-40","-","*","86","132","-84","+","*","-","38","/","/","21","28","/","+","83","/","-31","156","-","+","28","/","95","-","120","+","8","*","90","-","-94","*","-73","/","-62","/","93","*","196","-","-59","+","187","-","143","/","-79","-89","+","-"]
    print(evalRPN(tokens))                                  # 165
    print(evalRPN(["4", "-2", "/", "2", "-3", "-", "-"]))   # -7
    print(evalRPN(["18"]))                                  # 18
    print(evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))
    # 22
    print(evalRPN(["4", "13", "5", "/", "+"]))              # 6
    print(evalRPN(["2", "1", "+", "3", "*"]))               # 9


if __name__ == "__main__":
    main()




