
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
    if not v:
        for level in range(len(l)):
            l1 = l[:level] + l[level+1:]
            signs = []
            v = True
            for j in range(len(l1) - 1):
                d = l1[j] - l1[j + 1]
                if abs(d) > 3 or d == 0 or (signs and (d > 0) != signs[0]):
                    v = False
                    break
                if not signs:
                    signs.append((d > 0))
            if v:
               break
    if v:
        n += 1
print(n) # 710
