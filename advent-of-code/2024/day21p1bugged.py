import itertools
import sys
from collections import deque
from copy import deepcopy
from time import process_time

start_time = process_time()
N = 5
posPerCaseNum = {"A":(3,2),"0":(3,1),"1":(2,0),"2":(2,1),"3":(2,2),"4":(1,0),"5":(1,1),"6":(1,2),"7":(0,0),"8":(0,1),"9":(0,2)}
posPerCaseDir = {"v":(1,1),">":(1,2),"<":(1,0),"^":(0,1),"A":(0,2)}
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
#arrows =
counter = 0


def dfs2(nActions, moves, depth):
    if depth == len(nActions):
        nnactions = []
        for j in range(len(moves)-1):  # 3
            elt = moves[j + 1]
            elt2 = moves[j]
            (y, x) = posPerCaseDir[elt]
            (a, b) = posPerCaseDir[elt2]
            q = deque()
            q.appendleft((a, b, []))
            while q:
                (r, c, path) = q.pop()
                if (r, c) == (y, x):
                    nnactions.append(path+["A"])
                    break
                for (u, v, d) in ((r + 1, c, "v"), (r - 1, c, "^"), (r, c + 1, ">"), (r, c - 1, "<")):
                    if (u, v) in posPerCaseDir.values():
                        q.appendleft((u, v, path + [d]))

        #print(nnactions)
        #nnactions = ["A"] + nnactions

        return sum(len(ff) for ff in nnactions)+1

    m = sys.maxsize

    for action in nActions[depth]:
        nMoves = deepcopy(moves)
        for a in action:
            nMoves.append(a)
        m = min(dfs2(nActions, nMoves, depth+1),m)

    return m


def dfs(moves, depth):
    if depth == len(actions):
        #print(moves)
        nactions = []
        for j in range(len(moves)-1):  # 3
            elt = moves[j + 1]
            elt2 = moves[j]
            (y, x) = posPerCaseDir[elt]
            (a, b) = posPerCaseDir[elt2]
            q = deque()
            q.appendleft((a, b, []))
            while q:
                (r, c, path) = q.pop()
                if (r, c) == (y, x):
                    nactions.append(list(itertools.permutations(path)))
                    nactions.append([["A"]])
                    break
                for (u, v, d) in ((r + 1, c, "v"), (r - 1, c, "^"), (r, c + 1, ">"), (r, c - 1, "<")):
                    if (u, v) in posPerCaseNum.values():
                        q.appendleft((u, v, path + [d]))

        #print(nactions)
        nactions = [["A"]] + nactions

        return dfs2(nactions, [], 0)

    m = sys.maxsize
    for action in actions[depth]:
        if depth == 0:
            print(m, len(actions[depth]))

        nMoves = deepcopy(moves)
        for a in action:
            nMoves.append(a)
        m = min(dfs(nMoves,depth+1),m)

    return m


for t in range(N):
    actions = ["A"]+list(input())
    print(actions)
    start = ""
    for elt in actions:
        if elt.isdigit() and not (elt == "0" and start == ""):
            start += elt
    start = int(start)
    nactions = []
    for j in range(len(actions)-1):#3
        elt = actions[j+1]
        elt2 = actions[j]
        (y,x) = posPerCaseNum[elt]
        (a,b) = posPerCaseNum[elt2]

        q = deque()
        q.appendleft((a,b,[]))
        while q:
            (r,c,path) = q.pop()
            if (r,c) == (y,x):
                # pour chaque shuffle (itertools.combinations) du path, on dfs
                # (ce qui compte c'est de tester ttes les combs du premier et du dernier ?)
                # pour trouver les enchainements optimaux avec la suite
                # du coup dfs depth 4 (divers chemins pour atteindre chacun des chiffres/lettres depuis la pos précédente)
                # et ensuite rebelotte sur la combinatoire du pad des flêches
                nactions.append(list(itertools.permutations(path,len(path))))
                nactions.append([["A"]])
                break
            for (u,v,d) in ((r+1,c,"v"),(r-1,c,"^"),(r,c+1,">"),(r,c-1,"<")):
                if (u,v) in posPerCaseNum.values():
                    q.appendleft((u,v,path+[d]))
    #print(nactions)
    actions = [["A"]]+nactions
    nMoves = dfs([], 0)


    print(nMoves,start,nMoves*start)
    counter += nMoves*start
print(process_time() - start_time, counter) #

"""
['A', '0', '2', '9', 'A']
9223372036854775807 1
69 29 2001
['A', '9', '8', '0', 'A']
9223372036854775807 1
61 980 59780
['A', '1', '7', '9', 'A']
9223372036854775807 1
65 179 11635
['A', '4', '5', '6', 'A']
9223372036854775807 1
61 456 27816
['A', '3', '7', '9', 'A']
9223372036854775807 1
65 379 24635
68.296875 125867


au lieu de 68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding these together produces 126384.
"""
