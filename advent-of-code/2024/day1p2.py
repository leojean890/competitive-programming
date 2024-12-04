from collections import defaultdict

l1 = []
l2 = defaultdict(int)
for i in range(1000):
    a,b = [int(j) for j in input().split()]
    l1.append(a)
    l2[b] += 1
d=0
for i in range(1000):
    d += l1[i]*l2[l1[i]]
print(d) #23655822
