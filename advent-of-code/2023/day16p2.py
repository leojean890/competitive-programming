

from collections import deque

N = 110
M = 0
lines = []
for i in range(N):
    lines.append(input())

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

direc = {RIGHT:(0,1), LEFT:(0,-1),DOWN:(1,0),UP:(-1,0)}
turn = {"/":{RIGHT:UP, LEFT:DOWN, DOWN:LEFT, UP:RIGHT}, "\\":{RIGHT:DOWN, LEFT:UP, UP:LEFT, DOWN:RIGHT}}
spl = {"|":{RIGHT:(UP, DOWN), LEFT:(UP, DOWN), DOWN:(DOWN,), UP:(UP,)}, "-":{RIGHT:(RIGHT,), LEFT:(LEFT,), DOWN:(LEFT, RIGHT), UP:(LEFT, RIGHT)}}

for yx in range(N):
  for iny, inx, ind in ((yx, 0, RIGHT),(yx, N-1, LEFT),(0, yx, DOWN),(N-1, yx, UP)):

    q = deque()
    q.appendleft((iny, inx, ind))
    visited = {(iny, inx, ind)}
    energized = {(iny, inx)}

    while q:
        (y,x,d) = q.pop()
        currSpot = lines[y][x]
        if currSpot in spl:
            for d in spl[currSpot][d]:
                (dy,dx) = direc[d]
                a = y+dy
                b = x+dx
                if 0 <= a < N and 0 <= b < N and (a, b, d) not in visited:
                    visited.add((a, b, d))
                    energized.add((a, b))
                    q.appendleft((a, b, d))
        else:
            if currSpot in turn:
                d = turn[currSpot][d]
            (dy,dx) = direc[d]
            y += dy
            x += dx
            if 0 <= y < N and 0 <= x < N and (y,x,d) not in visited:
                q.appendleft((y,x,d))
                visited.add((y, x, d))
                energized.add((y, x))
    if M < len(energized):
        M = len(energized)

print(M) # 8026


