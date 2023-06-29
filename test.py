import re
k = {}
with open('locations.txt') as funfile:
    g = funfile.readlines()
    for s in g:
        tm = ''
        for m in s:
            if m.isdigit() or m == ' ' or m == '-':
                tm += m
        k[' '.join(tm.strip().split())] = 0

print(k)
print(len(k))