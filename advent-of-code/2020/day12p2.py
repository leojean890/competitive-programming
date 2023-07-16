
def move(yS, xS, yWP, xWP,nb):
    return yS + nb*yWP, xS + nb*xWP

def rotate(vect, nbRot, rotationDir):
    y, x = vect
    if rotationDir == "L":
        nbRot = 4 - nbRot
    if nbRot in (0,4):
        return x, y
    elif nbRot == 1:
        return y, -x
    elif nbRot == 2:
        return -x, -y
    elif nbRot == 3:
        return -y, x


yS, xS, yWP, xWP = 0, 0, 1, 10
for i in range(755):#5
    instruction = input()
    nb = int(instruction[1:])
    if instruction[0] == "S":
        yWP = yWP-nb
    if instruction[0] == "N":
        yWP = yWP+nb
    if instruction[0] == "E":
        xWP = xWP+nb
    if instruction[0] == "W":
        xWP = xWP-nb
    if instruction[0] in ("R", "L"):
        xWP, yWP = rotate((yWP, xWP),nb//90,instruction[0])

    if instruction[0] == "F":
        yS, xS = move(yS, xS, yWP, xWP,nb)


print(abs(xS)+abs(yS))# 29895
