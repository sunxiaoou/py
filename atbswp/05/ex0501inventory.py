#! /usr/bin/python3

def display(name, dic):
    print(name + ':')
    sum = 0
    for k, v in dic.items():
        sum += v
        print(str(v) + ' ' + k)
    print('Total number of items: ' + str(sum))    

inventory = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
display('Inventory', inventory)
