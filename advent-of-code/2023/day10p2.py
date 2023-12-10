
from shapely.geometry import Point, Polygon
from collections import deque


def validate(y,x,a,b):
    if lines[y][x] == "J":
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True

    if lines[y][x] == "L":
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True

    if lines[y][x] == "7":
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True

    if lines[y][x] == "F":
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True

    if lines[y][x] == "|":
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True

    if lines[y][x] == "-":
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True

    if lines[y][x] == "S":
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True


W = 140
H = 140
lines = []
for i in range(H):
    line = input()
    lines.append(line)
    for j in range(W):
        if line[j] == "S":
            entrance = (i,j)

q = deque()
q.appendleft((entrance[0], entrance[1]))
visited = {entrance}
coords = []
while q:
    (y,x) = q.popleft()
    coords.append((y,x))
    for (a,b) in ((y+1,x), (y-1,x),(y,x+1),(y,x-1)):
        if 0 <= a < H and 0 <= b < W and (a,b) not in visited and validate(y,x,a,b):
            q.appendleft((a,b))
            visited.add((a,b))

poly = Polygon(coords)

counter = 0
for y in range(H):
    for x in range(W):
        if (y,x) not in visited:
            p1 = Point(y, x)

            if p1.within(poly):
                counter += 1

print(counter) # 281

