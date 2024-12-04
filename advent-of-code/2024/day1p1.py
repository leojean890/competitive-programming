
l1 = []
l2 = []
for i in range(1000):
    a,b = [int(j) for j in input().split()]
    l1.append(a)
    l2.append(b)
l1.sort()
l2.sort()
d=0
for i in range(1000):
    d += abs(l1[i]-l2[i])
print(d) # 2196996
