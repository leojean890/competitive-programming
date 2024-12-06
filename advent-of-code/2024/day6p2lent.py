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
visited = {(y,x)}

while 0 <= x < N and 0 <= y < N:
    while (y+dy,x+dx) in walls:
        (dy,dx) = transform(dy,dx)
    y += dy
    x += dx
    visited.add((y,x))


counter = 0
for a in range(N):
    for b in range(N):
        print(a,b)
        if (a,b) not in walls and (a,b) in visited:
            nwalls = walls | {(a,b)}
            path = []
            (y,x,dy,dx) =(iy,ix,idy,idx)

            while 0 <= x < N and 0 <= y < N:
                while (y+dy,x+dx) in nwalls:
                    (dy,dx) = transform(dy,dx)
                y += dy
                x += dx

                if (y,x,dy,dx) in path:
                    counter += 1
                    break

                path.append((y,x,dy,dx))

print(counter) # 2008 (erreur de considérer la position de départ en tant que bloc possible)
