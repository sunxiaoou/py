#! /usr/bin/python3

import re

def marchSentence(sentences):
    regex = re.compile(r'((Alice|Bob|Carol) (eats|pets|throws) (apples|cats|baseballs)\.)', re.I) 

    for i in range(len(sentences)):
        mo = regex.search(sentences[i])
        if (mo != None):
            print(mo.group())

sentences = ['Alice eats apples.', 'Bob pets cats.', 'Carol throws baseballs.',
        'Alice throws Apples.', 'BOB EATS CATS.', 'Robocop eats apples.',
        'ALICE THROWS FOOTBALLS.' 'Carol eats 7 cats.']
marchSentence(sentences)
