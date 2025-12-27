
counter = 0
N = 496
coords = []
for i in range(N):
    x,y = map(int, input().split(","))
    coords.append((x,y))

m = 0
for i in range(N-1):
    (x,y) = coords[i]
    for j in range(i+1,N):
        (a, b) = coords[j]
        d = abs(1+x-a)*abs(1+y-b)
        if d > m:
            m = d
            print(m) # 4752484112
