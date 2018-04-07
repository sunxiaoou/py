#! /usr/bin/python3

def printTable(table):
    colWidths = [0] * len(table)
    for j in range(len(table)):
        for i in range(len(table[j])):
            if colWidths[j] < len(table[j][i]):
                colWidths[j] = len(table[j][i])                
    for i in range(len(table[0])):
        for j in range(len(table)):
            print(table[j][i].rjust(colWidths[j]) + ' ', end = '')
        print()


tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]

printTable(tableData)

