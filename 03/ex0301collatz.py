#! /usr/bin/python3

def collatz(number):
    if number == 1:
        return
    if number % 2 == 0:
        number = number // 2
    else:
        number = number * 3 + 1
    print('number = ' + str(number))
    collatz(number)

print('Enter number:')
try:
    collatz(int(input()))
except ValueError:
    print('Error: Invalid input')
