
from collections import deque

lines = []
q = deque()

for i in range(41):
    line = input()
    W = len(line)
    lines.append(line)
    if "E" in line:
        start = (i, line.index('E'), 0, ["E"])
        q.appendleft(start)
        visited = {(i, line.index('E'))}
        lines[-1] = line.replace("E", "z")
H = len(lines)

while q:
    y, x, depth, path = q.pop()

    M = chr(ord(lines[y][x])+1)
    m = chr(ord(lines[y][x])-1)
    if lines[y][x] == "E":
        M = "z"
        m = "y"

    for a,b in ( (y+1, x), (y-1, x), (y, x+1), (y, x-1) ):
        if 0 <= b < 81 and 0 <= a < 41 and m <= "a" and lines[a][b] in ("S", "a"):
            print(depth+1)
            exit()
        if 0 <= b < 81 and 0 <= a < 41 and (a,b) not in visited and m <= lines[a][b] <= "z":
            q.appendleft((a,b, depth+1, path+[lines[a][b]]))
            visited.add((a,b))
