import sys

iline = [(i[0], int(i[1:])) for i in input().split(",")]
iline2 = [(i[0], int(i[1:])) for i in input().split(",")]

y,x = (0,0)
crossedCoords = {}
steps = 0
for direc, lgth in iline:
    dy,dx = {"R":(0,1), "L":(0,-1), "D":(1,0), "U":(-1,0)}[direc]
    for incr in range(lgth):
        y += dy
        x += dx
        steps += 1
        if (y,x) not in crossedCoords:
            crossedCoords[(y,x)] = steps

y,x = (0,0)
M = sys.maxsize
crossedCoords2 = {}
steps = 0
for direc, lgth in iline2:
    dy,dx = {"R":(0,1), "L":(0,-1), "D":(1,0), "U":(-1,0)}[direc]
    for incr in range(lgth):
        y += dy
        x += dx
        steps += 1
        if (y,x) not in crossedCoords2:
            crossedCoords2[(y,x)] = steps
            if (y, x) in crossedCoords:
                m = crossedCoords[(y,x)] + steps
                if m < M:
                    M = m

print(M) # 56410
# 56370 too low (si on considère que le nb de steps n'augmente pas la 2eme fois qu'on passe qqpart, statement ambigu)
