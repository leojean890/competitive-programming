from collections import defaultdict

indexes = defaultdict(list)
tab = [int(i) for i in input().split(",")]
for i in range(len(tab)):
    indexes[tab[i]].append(i)
L = len(tab)
for i in range(L, 30000000): # O(n), 1min30 only ...
    elt = tab[-1]
    if len(indexes[elt]) == 1:
        tab.append(0)
        indexes[tab[i]].append(i)
    else:
        tab.append(indexes[elt][-1] - indexes[elt][-2])
        indexes[tab[i]].append(i)

print(tab[-1]) # 352
