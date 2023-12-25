

L = 604
coords = [(0,0)]
(y,x) = (0,0)
globalScore = 0
for i in range(L):
    whole = input().split("#")[1].split(")")[0]
    nb = int(whole[:5], 16)
    direc = int(whole[-1])
    if direc == 0:
        x += nb
    if direc == 2:
        x -= nb
    if direc == 1:
        y += nb
    if direc == 3:
        y -= nb
    coords.append((y,x))
    globalScore += nb # border of the polygon
    if i > 0:
        a,b = coords[i]
        u,v = coords[i-1]
        globalScore += a*v-b*u # shoelace formula

a,b = coords[0]
u,v = coords[L - 1]

globalScore += a*v-b*u

print((globalScore+2) //2) # 40343619199142
