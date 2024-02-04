from copy import deepcopy
W = 8
lines = list()
for i in range(W):
    lines += [list(input())]

emptyLines = list()
for i in range(21):
    emptyLines += [['.', '.', '.', '.', '.','.', '.', '.', '.', '.','.', '.', '.', '.','.', '.','.', '.', '.', '.','.']]

allLines = []

for z in range(21):
    clines = deepcopy(emptyLines)
    if z == 10:
        for i in range(W):
            clines[i+10-W//2][10-W//2:10+W//2] = lines[i]
    allLines.append(clines)


for iteration in range(6):
    newAllLines = []
    counter = 0
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
                            if not a == b == c == 0 and all(n in range(21) for n in (nx,ny,nz)):
                                if allLines[nz][ny][nx] == "#":
                                    nActive += 1
                if allLines[z][y][x] == "#":
                    newLine.append("#" if nActive in (2,3) else ".")
                    if nActive in (2,3):
                        counter += 1
                else:
                    newLine.append("#" if nActive == 3 else ".")
                    if nActive == 3:
                        counter += 1

            newLines.append(newLine)
        newAllLines.append(newLines)

    allLines = newAllLines
print(iteration, counter) # 295
