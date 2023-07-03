
W = 139#10
H = 137#9

goingDown = set()
goingRight = set()

for i in range(H):
    line = input()
    for j in range(W):
        if line[j] == ">":
            goingRight.add((i,j))
        if line[j] == "v":
            goingDown.add((i,j))

turn = 0
moved = True
while moved:
    turn += 1
    print(turn)
    newGoingRight = set()
    moved = False

    for (i,j) in goingRight:
        newCoord = (i,(j+1)%W)
        if newCoord not in goingRight and newCoord not in goingDown:
            newGoingRight.add(newCoord)
            moved = True
        else:
            newGoingRight.add((i,j))

    goingRight = newGoingRight
    newGoingDown = set()

    for (i,j) in goingDown:
        newCoord = ((i+1)%H, j)
        if newCoord not in goingRight and newCoord not in goingDown:
            newGoingDown.add(newCoord)
            moved = True
        else:
            newGoingDown.add((i,j))

    goingDown = newGoingDown

print(turn) # 530
