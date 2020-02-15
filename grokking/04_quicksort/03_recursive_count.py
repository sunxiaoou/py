#! /usr/local/bin/python3

def count(list):
  if list == []:
    return 0
  return 1 + count(list[1:])
