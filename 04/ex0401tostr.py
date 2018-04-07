#! /usr/bin/python3

def toStr(list):
    str = ''
    for i in range(len(list)):
        if i < len(list) - 1:
            str += list[i] + ', '
        else:
            str += 'and ' + list[i]
    return str

spam = ['apples', 'bananas', 'tofu', 'cats']
print(toStr(spam))
