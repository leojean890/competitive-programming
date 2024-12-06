from collections import defaultdict

N = 130
counter = 0
walls = set()
for i in range(N):
    line = input()
    for j in range(N):
        if line[j] == "#":
            walls.add((i,j))
        if line[j] == "^":
            (y,x,dy,dx) = (i,j,-1,0)


def transform(dy, dx):
    return {(-1,0):(0,1),(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0)}[(dy,dx)]

visited = {(y,x)}

while 0 <= x < N and 0 <= y < N:
    counter += 1
    while (y+dy,x+dx) in walls:
        (dy,dx) = transform(dy,dx)
    y += dy
    x += dx
    visited.add((y,x))


print(len(visited)-1) # 5516
