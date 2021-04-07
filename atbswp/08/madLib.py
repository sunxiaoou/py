#! /usr/bin/python3

import re

words = ['ADJECTIVE', 'NOUN', 'ADVERB', 'VERB']
text = 'The ADJECTIVE panda walked to the NOUN and then VERB. A nearby NOUN was unaffected by these events.'

for word in words:
    print('Enter an ' + word + ':')
    new = input()
    regex = re.compile(word)
    text = regex.sub(new, text)

print(text)
