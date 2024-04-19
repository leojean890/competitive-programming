
import sys

W = 12
NL = 144
L = 10
L1 = 8
sys.setrecursionlimit(1000000)


def transposeRepr(initRepr):
    return [initRepr[0][::-1], initRepr[3], initRepr[2][::-1], initRepr[1]]


def getRepr(initRepr, transpo, rot):
    repr = initRepr[:] if not transpo else transposeRepr(initRepr)

    if rot == 0:
        return repr
    if rot == 1:
        return [repr[-1][::-1], repr[0], repr[1][::-1], repr[2]]
    if rot == 3:
        return [repr[1], repr[2][::-1], repr[-1], repr[0][::-1]]
    return [repr[2][::-1], repr[-1][::-1], repr[0][::-1], repr[1][::-1]]


def compatible(depth,chosenRepr,repr):#HDBG
    if depth >= W and chosenRepr[depth-W][2] != repr[0]:
        return False
    if depth%W and chosenRepr[depth-1][1] != repr[3]:
        return False

    return True


def dfs(depth, chosen, chosenRepr, transpsEtRots):
    if depth == NL:
        print(chosen[0]*chosen[-W]*chosen[-1]*chosen[W-1]) # 16937516456219
        return (chosen, chosenRepr, transpsEtRots)

    for tile, initRepr in allTiles.items():
        if tile not in chosen:
            for transpo in range(2):
                for rot in range(4):
                    repr = getRepr(initRepr, transpo, rot)
                    if compatible(depth,chosenRepr,repr):
                        res = dfs(depth + 1, chosen + [tile], chosenRepr + [repr], transpsEtRots + [(transpo, rot)])
                        if res:return res


allTiles = {}
allLines = {}
for i in range(NL):
    tile = int(input().split()[1][:-1])

    lines = []
    for j in range(L):
        lines.append(input())
    if i < NL-1:
        input()

    transposed = list(zip(*lines))
    bords = [lines[0],"".join(transposed[-1]),lines[-1],"".join(transposed[0])]
    allTiles[tile] = bords
    nlines = []
    for j in range(1,L-1):
        nlines.append(lines[j][1:-1])
    allLines[tile] = nlines


chosen, chosenRepr, transpsEtRots = dfs(0, [], [], [])


def transposeLines(lines):
    nlines = []
    for line in lines:
        nlines.append(line[::-1])
    return nlines


def rotateLines(lines, transpo, rot):
    if transpo:
        lines = transposeLines(lines)

    if rot == 0:
        return lines
    if rot == 3:
        return list(zip(*lines))[::-1]
    if rot == 1:
        nlines = []
        for line in list(zip(*lines)):
            nlines.append(line[::-1])
        return nlines

    # rot 2 fois : on inverse l'ordre des lignes + chaque ligne est [::-1]
    nlines = []
    for line in lines[::-1]:
        nlines.append(line[::-1])
    return nlines


nLines = []
for i in range(L1*W):
    line = []
    for j in range(L1 * W):
        line.append(".")
    nLines.append(line)

counterD = 0
for i in range(NL):
    tile = chosen[i]
    lines = allLines[tile]
    transpo, rot = transpsEtRots[i]
    nlines = rotateLines(lines, transpo, rot)

    c = i%W
    r = i//W

    for i in range(L1):
        for j in range(L1):
            nLines[r*L1+i][c*L1+j] = nlines[i][j]
            if nlines[i][j] == "#":
                counterD += 1


dieses = ((0,18),(1,0),(1,5),(1,6),(1,11),(1,12),(1,17),(1,18),(1,19),(2,1),(2,4),(2,7),(2,10),(2,13),(2,16))

for transpo in range(2):
    for rot in range(4):
        nLs = []
        for i in range(L1 * W):
            nLs.append(nLines[i].copy())
        nLs = rotateLines(nLs, transpo, rot)
        # on pourrait transposer le motif du sea monster au lieu de l'image mais whatever...

        nbSeaMonsters = 0
        for i in range(L1 * W - 3):
            for j in range(L1 * W - 20):
                v = False
                for y in range(3):
                    for x in range(20):
                        elt = nLs[i+y][j+x]
                        if elt == ".":
                            if (y,x) in dieses:
                                v = True
                                break
                    if v:break
                else:
                    nbSeaMonsters += 1


        if nbSeaMonsters:
            print(counterD - 15*nbSeaMonsters) #1858
            exit()
