#! /usr/local/bin/python3

for i in range(1, 101):
    txt = '{:4d}: '.format(i)
    k = 0
    for j in range(1, i + 1):
        if i % j == 0:
            k += 1
            txt += '{}, '.format(j)
    txt = txt[:-2]
    txt += ' - ({})'.format(k) 
    print(txt)
