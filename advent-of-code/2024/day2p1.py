
n = 0
for i in range(1000):
    l = [int(j) for j in input().split()]
    signs = []
    v = True
    for j in range(len(l)-1):
        d = l[j] - l[j+1]
        if abs(d) > 3 or d == 0 or (signs and (d>0) != signs[0]):
            v = False
            break
        if not signs:
            signs.append((d>0))
    if v:
        n += 1
    #print(v)
print(n) #
