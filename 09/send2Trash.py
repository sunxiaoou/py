#! /usr/bin/python3

import random, send2trash

chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
fn = 'bacon.' + ''.join(random.sample(chars, 3))

baconFile = open(fn, 'a')   # creates the file
baconFile.write('Bacon is not a vegetable.')
baconFile.close()

print('Send ' + fn + ' to Trash')
send2trash.send2trash(fn)
