def move(y,x,d,nb):
    if d == (-1, 0):
        return y-nb,x
    if d == (1, 0):
        return y+nb,x
    if d == (0, -1):
        return y,x-nb
    if d == (0, 1):
        return y,x+nb


def rotate(vect, nbRot, rotationDir):
    dy,dx = vect
    allD = ((-1, 0), (0, -1), (1, 0), (0, 1))
    if rotationDir == "R":
        allD = ((0,1),(1,0),(0,-1),(-1,0)) 

    return allD[(allD.index((dy,dx)) + nbRot)%4]


y, x, d, = 0, 0, (0,1)
for i in range(755):#5
    print(y,x,d)
    instruction = input()
    nb = int(instruction[1:])
    if instruction[0] == "S":
        y = y+nb
    if instruction[0] == "N":
        y = y-nb
    if instruction[0] == "E":
        x = x+nb
    if instruction[0] == "W":
        x = x-nb
    if instruction[0] in ("R", "L"):
        d = rotate(d,nb//90,instruction[0])
    if instruction[0] == "F":
        y,x = move(y,x,d,nb)

print(abs(x)+abs(y))#362
