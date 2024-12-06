N = 130
counter = 0
walls = set()
for i in range(N):
    line = input()
    for j in range(N):
        if line[j] == "#":
            walls.add((i,j))
        if line[j] == "^":
            (iy,ix,idy,idx) = (i,j,-1,0)


def transform(dy, dx):
    return {(-1,0):(0,1),(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0)}[(dy,dx)]


(y,x,dy,dx) = (iy,ix,idy,idx)
visited = {}

while 0 <= x < N and 0 <= y < N:
    while (y+dy,x+dx) in walls:
        (dy,dx) = transform(dy,dx)
    if (y+dy,x+dx) not in visited:
        visited[(y+dy,x+dx)] = (y,x,dy,dx)
    y += dy
    x += dx


counter = 0
for a in range(N):
    for b in range(N):
        print(a,b)
        if (a,b) not in walls and (a,b) in visited and (a,b) != (iy,ix):
            nwalls = walls | {(a,b)}
            (y,x,dy,dx) = visited[(a,b)]
            path = [(y,x,dy,dx)]

            while 0 <= x < N and 0 <= y < N:
                while (y+dy,x+dx) in nwalls:
                    (dy,dx) = transform(dy,dx)
                y += dy
                x += dx

                if (y,x,dy,dx) in path:
                    counter += 1
                    break

                path.append((y,x,dy,dx))

print(counter) # 2008
