import sys

W = 12
NL = 144
L = 10
sys.setrecursionlimit(1000000)

def transposeRepr(initRepr, transpo):
    if transpo == 1:
        return [initRepr[0][::-1], initRepr[3], initRepr[2][::-1], initRepr[1]]

    return [initRepr[2], initRepr[1][::-1], initRepr[0], initRepr[3][::-1]]


def getRepr(initRepr, transpo, rot):
    repr = initRepr[:] if not transpo else transposeRepr(initRepr, transpo)

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


def dfs(depth, chosen, chosenRepr):
    if depth == NL:
        print(chosen[0]*chosen[-W]*chosen[-1]*chosen[W-1])  # 16937516456219
        exit()

    for tile, initRepr in allTiles.items():
        if tile not in chosen:
            for transpo in range(2):
                for rot in range(4):
                    repr = getRepr(initRepr, transpo, rot)
                    if compatible(depth,chosenRepr,repr):
                        dfs(depth+1, chosen+[tile], chosenRepr+[repr])


allTiles = {}
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

    print(tile,bords)


dfs(0, [], [])
