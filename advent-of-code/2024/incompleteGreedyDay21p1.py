from collections import deque
from time import process_time

start_time = process_time()
N = 5
counter = 0
posPerCaseNum = {"A":(3,2),"0":(3,1),"1":(2,0),"2":(2,1),"3":(2,2),"4":(1,0),"5":(1,1),"6":(1,2),"7":(0,0),"8":(0,1),"9":(0,2)}
posPerCaseDir = {"v":(1,1),">":(1,2),"<":(1,0),"^":(0,1),"A":(0,2)}
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
#arrows =
counter = 0
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
        """dy = y-a
        dx = x-b
        # attention avec ma méthode je peux sortir du pad, vaut mieux bfs ?
        if dy > 0:
            for k in range(dy):
                actions.append(arrows[DOWN])"""
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
                nactions.extend(path+["A"])
                break
            for (u,v,d) in ((r+1,c,"v"),(r-1,c,"^"),(r,c+1,">"),(r,c-1,"<")):
                if (u,v) in posPerCaseNum.values():
                    q.appendleft((u,v,path+[d]))
    print(nactions)
    actions = ["A"]+nactions
    for repeat in range(2):
        nactions = []
        for j in range(len(actions)-1):  # 3
            elt = actions[j + 1]
            elt2 = actions[j]
            (y, x) = posPerCaseDir[elt]
            (a, b) = posPerCaseDir[elt2]
            """dy = y-a
            dx = x-b
            # attention avec ma méthode je peux sortir du pad, vaut mieux bfs ?
            if dy > 0:
                for k in range(dy):
                    actions.append(arrows[DOWN])"""
            q = deque()
            q.appendleft((a, b, []))
            while q:
                (r, c, path) = q.pop()
                if (r, c) == (y, x):
                    nactions.extend(path+["A"])
                    break
                for (u, v, d) in ((r + 1, c, "v"), (r - 1, c, "^"), (r, c + 1, ">"), (r, c - 1, "<")):
                    if (u, v) in posPerCaseNum.values():
                        q.appendleft((u, v, path + [d]))

        print(nactions)
        actions = ["A"] + nactions
    print(len(actions),start,len(actions)*start)
    counter += len(actions)*start
print(process_time() - start_time, counter) # 1.5625 841533074412361
