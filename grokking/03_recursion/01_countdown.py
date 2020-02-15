#! /usr/local/bin/python3

def countdown(i):
  # base case
  if i <= 0:
    return 0
  # recursive case
  else:
    print(i)
    return countdown(i-1)

countdown(5)
