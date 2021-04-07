#! /usr/bin/python3

def addDict(dic, items):
    for i in range(len(items)):
        if items[i] not in dic.keys():
            dic.setdefault(items[i], 1)
        else:
            dic[items[i]] += 1
    return dic

def display(name, dic):
    print(name + ':')
    sum = 0
    for k, v in dic.items():
        sum += v
        print(str(v) + ' ' + k)
    print('Total number of items: ' + str(sum))    

inv = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']

inv = addDict(inv, dragonLoot)
display('Inventory', inv)
