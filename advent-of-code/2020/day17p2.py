from copy import deepcopy
W = 8
lines = list()
for i in range(W):
    lines += [list(input())]

emptyLines = list()
for i in range(21):
    emptyLines += [['.', '.', '.', '.', '.','.', '.', '.', '.', '.','.', '.', '.', '.','.', '.','.', '.', '.', '.','.']]

allLines = []

for w in range(21):
    zLines = []
    for z in range(21):
        clines = deepcopy(emptyLines)
        if w == z == 10:
            for i in range(W):
                clines[i+10-W//2][10-W//2:10+W//2] = lines[i]
                #clines[i+10-W//2][10-W//2:10+W//2-1] = lines[i] w pair ?

        zLines.append(clines)
    allLines.append(zLines)


for iteration in range(6):
    newAllLines = []
    counter = 0
    for w in range(21):
        newZLines = []
        for z in range(21):
            newLines = []
            for y in range(21):
                newLine = []
                for x in range(21):
                    nActive = 0
                    for a in (-1,0,1):
                        nx = x+a
                        for b in (-1,0,1):
                            ny = y+b
                            for c in (-1,0,1):
                                nz = z+c
                                for d in (-1, 0, 1):
                                    nw = w + d
                                    if not a == b == c == d == 0 and all(n in range(21) for n in (nx,ny,nz,nw)):
                                        if allLines[nw][nz][ny][nx] == "#":
                                            nActive += 1
                    if allLines[w][z][y][x] == "#":
                        newLine.append("#" if nActive in (2,3) else ".")
                        if nActive in (2,3):
                            counter += 1
                    else:
                        newLine.append("#" if nActive == 3 else ".")
                        if nActive == 3:
                            counter += 1

                newLines.append(newLine)
            newZLines.append(newLines)
        newAllLines.append(newZLines)

    allLines = newAllLines
print(iteration, counter) # 295
