import sys

iline = [(i[0], int(i[1:])) for i in input().split(",")]
iline2 = [(i[0], int(i[1:])) for i in input().split(",")]

y,x = (0,0)
crossedCoords = {(y,x)}
for direc, lgth in iline:
    dy,dx = {"R":(0,1), "L":(0,-1), "D":(1,0), "U":(-1,0)}[direc]
    for incr in range(lgth):
        y += dy
        x += dx
        if (y,x) not in crossedCoords:
            crossedCoords.add((y,x))

y,x = (0,0)
M = sys.maxsize
for direc, lgth in iline2:
    dy,dx = {"R":(0,1), "L":(0,-1), "D":(1,0), "U":(-1,0)}[direc]
    for incr in range(lgth):
        y += dy
        x += dx
        if (y,x) in crossedCoords:
            m = abs(y) + abs(x)
            if m < M:
                M = m

print(M) # 557


