
import sys


def move(x, y, d):
    if d == U:
        return (x,y-1)
    if d == D:
        return (x,y+1)
    if d == L:
        return (x-1,y)

    return(x+1,y)


U=0
L=1
D=2
R=3
inv = {U:D,D:U,L:R,R:L}
rot = {U:L,L:D,D:R,R:U}
points = []
xx = []
yy = []
for line in sys.stdin:
    (x,y,d) = (0,0,U)
    for elt in line:
        if elt == "H":
            (x, y) = move(x,y,d)
        elif elt == "B":
            (x, y) = move(x,y,inv[d])
        elif elt == "G":
            d = rot[d]
        elif elt == "D":
            d = rot[inv[d]]

    points.append((y,x))
    xx.append(x)
    yy.append(y)

mx = min(xx)
my = min(yy)
Mx = max(xx)
My = max(yy)


for i in range(my, My+1):
    line = ""
    for j in range(mx, Mx+1):
        line += ("." if (i,j) not in points else "X")
    print(line)
