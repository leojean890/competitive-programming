


from shapely.geometry import Point, Polygon



L = 604
coords = [(0,0)]
visited = {(0,0)}
(y,x) = (0,0)
Mx = my = mx = My = 0
for i in range(L):
    a = input()
    #print(a.split("("))
    direc, nb = a.split(" (")[0].split()
    nb = int(nb)
    if direc == "R":
        for a in range(x, x+nb+1):
            visited.add((y,a))
        x += nb
    if direc == "L":
        for a in range(x-nb, x+1):
            visited.add((y,a))
        x -= nb
    if direc == "D":
        for a in range(y, y+nb+1):
            visited.add((a,x))
        y += nb
    if direc == "U":
        for a in range(y-nb, y+1):
            visited.add((a,x))
        y -= nb
    coords.append((y,x))
    visited.add((y,x))
    Mx = max(Mx, x)
    My = max(My, y)
    mx = min(mx, x)
    my = min(my, y)


poly = Polygon(coords)
print(len(visited)) # 4306 too low mais attente du résultat final

counter = 0
for y in range(my, My):
    for x in range(mx, Mx+1):
        if (y,x) not in visited:
            p1 = Point(y, x)

            if p1.within(poly):
                visited.add((y,x))

print(len(visited)) # too low mais attente du résultat final => 2 min pour 61865
