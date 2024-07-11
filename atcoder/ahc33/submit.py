import random
import sys
from collections import deque
from functools import lru_cache
from time import process_time

bestM = 25

@lru_cache(None)
def dfs(depth, currentToTake, sortedCarried, remaining, maxNbCarried):
    global bestM
    if depth == 25:
        bestM = min(bestM, maxNbCarried)
        return maxNbCarried, []

    M = 25
    best = []

    for i in range(5):
        if remaining[i] < 5:
            ncurrentToTake = currentToTake
            v = False
            if objs[i][remaining[i]] == ncurrentToTake:
                v = True

                ncurrentToTake += 1
                counter = 0
                while counter < len(sortedCarried) and ncurrentToTake == sortedCarried[counter]:
                    counter += 1
                    ncurrentToTake += 1
                if counter > 0:
                    nsortedCarried = sortedCarried[counter:]

            else:
                nsortedCarried = tuple(sorted(sortedCarried+(objs[i][remaining[i]],)))
            nremaining = remaining[:i] + (remaining[i]+1,) + remaining[i+1:]
            v2 = not v or counter > 0
            if v2:
                nmaxNbCarried = max(maxNbCarried, len(nsortedCarried))
            else:
                nmaxNbCarried = maxNbCarried
            if nmaxNbCarried < bestM:
                if v2:
                    (m, acts) = dfs(depth+1, ncurrentToTake, nsortedCarried, nremaining, nmaxNbCarried)
                else:
                    (m, acts) = dfs(depth+1, ncurrentToTake, sortedCarried, nremaining, maxNbCarried)

                if m < M:
                    M = m
                    best = [i] + acts

    return M, best


repl = {"R": "L", "L": "R", "U": "D", "D": "U"}
N = int(input())
start_time = process_time()
objs = []

for i in range(N):
    objs.append([int(j) for j in input().split()])

delta = 0
M, bestCombi = dfs(0, 0, tuple(), (0, 0, 0, 0, 0), 0)
end_time = process_time()
best = None


while end_time - start_time + delta < 0.2:

    locs = {}
    invLocs = {}
    deplaced = {}
    actions = ["" for i in range(N)]
    (cy, cx) = (0, 0)
    currentInd = 0

    for i in range(N):
        if i > 0:
            actions[i] = "B"
        deplaced[i] = 0

    it = 0
    vvv = True
    for r in bestCombi:

        vvv = True

        q = deque()
        q.appendleft((cy, cx, ""))
        visited = {(cy, cx)}

        while q:
            (y, x, d) = q.pop()
            if (y, x) == (r, 0):
                break

            for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                if 0 <= b < N and 0 <= a < N and (a, b) not in visited:  
                    q.appendleft((a, b, d + dd))
                    visited.add((a, b))
        (cy, cx) = (r, 0)
        actions[0] += d
        if objs[r][deplaced[r]] > it:
            lll = [(i, j) for j in range(1, 4) for i in range(N) if (i, j) not in invLocs]
            if not lll:
                vvv = False
                break
            (i, j) = random.choice(lll)
            q = deque()
            q.appendleft((r, 0, ""))
            visited = {(r, 0)}
            while q:
                (y, x, d) = q.pop()
                if (y, x) == (i, j):
                    break

                for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                    if 0 <= b < N and 0 <= a < N and (a, b) not in visited: 
                        q.appendleft((a, b, d + dd))
                        visited.add((a, b))
            if (y, x) != (i, j):
                vvv = False
                break
            nnn = ""
            for elt in d[::-1]:
                nnn += repl[elt]

            actions[0] += "P" + d + "Q" + nnn
            locs[objs[r][deplaced[r]]] = (i, j)
            invLocs[(i, j)] = objs[r][deplaced[r]]
            deplaced[r] += 1

        else:
            # move c to target
            q = deque()
            q.appendleft((r, 0, ""))
            visited = {(r, 0)}
            while q:
                (y, x, d) = q.pop()
                if (y, x) == (it // N, N - 1): 
                    break
                for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                    if 0 <= b < N and 0 <= a < N and (a, b) not in visited: 
                        q.appendleft((a, b, d + dd))
                        visited.add((a, b))
            if (y, x) != (it // N, N - 1):
                vvv = False
                break

            actions[0] += "P" + d + "Q"  
            deplaced[r] += 1
            it += 1

            (cy, cx) = (y, x)

        while it in locs:
            (i, j) = locs[it]

            for r1 in range(1):
                q = deque()
                q.appendleft((cy, cx, ""))
                visited = {(cy, cx)}
                while q:
                    (y, x, d) = q.pop()

                    if (y, x) == (i, j):
                        found = d + "P"
                        break
                    for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                        if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                            q.appendleft((a, b, d + dd))
                            visited.add((a, b))
                if (y, x) == (i, j):  
                    q = deque()
                    q.appendleft((y, x, ""))
                    visited = {(y, x)}
                    while q:
                        (y, x, d) = q.pop()
                        if (y, x) == (it // N, N - 1): 
                            found += d + "Q"
                            break
                        for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                            if 0 <= b < N and 0 <= a < N and (
                            a, b) not in visited:
                                q.appendleft((a, b, d + dd))
                                visited.add((a, b))
                    if (y, x) == (it // N, N - 1): 
                        cy, cx = y, x
                        actions[0] += found

                        del locs[it]
                        del invLocs[(i, j)]
                        it += 1
                        break

        if not vvv:
            nok = True
            break

    else:
        if not best or len(best[0]) > len(actions[0]):
            best = actions
    curr = process_time()
    delta = max(delta, curr - end_time)
    end_time = curr

while end_time - start_time +delta < 0.4:

    locs = {}
    invLocs = {}
    deplaced = {}
    actions = ["" for i in range(N)]
    (cy,cx) = (0,0)

    for i in range(N):
        if i > 0:
            actions[i] = "B"
        deplaced[i] = 0

    for it in range(25):
        if it in locs:
            (i, j) = locs[it]

            for r in range(1):
                q = deque()
                q.appendleft((cy,cx, ""))
                visited = {(cy,cx)}
                while q:
                    (y, x, d) = q.pop()

                    if (y, x) == (i, j):
                        found = d+"P"
                        break
                    for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                        if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                            q.appendleft((a,b, d + dd))
                            visited.add((a, b))
                if (y, x) == (i, j):
                    q = deque()
                    q.appendleft((y, x, ""))
                    visited = {(y, x)}
                    while q:
                        (y, x, d) = q.pop()
                        if (y, x) == (it//N,N-1):
                            found += d+"Q"
                            break
                        for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                            if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                                q.appendleft((a,b, d + dd))
                                visited.add((a, b))
                    if (y, x) == (it//N,N-1):
                        cy, cx = y,x
                        actions[0] += found


                        del locs[it]
                        del invLocs[(i, j)]
                        break
            else:
                nok = True
                break
        else:
            for r in range(N):
                if any(objs[r][c] == it for c in range(N)):
                    vvv = True
                    q = deque()
                    q.appendleft((cy,cx,""))
                    visited = {(cy,cx)}

                    while q:
                        (y, x, d) = q.pop()
                        if (y, x) == (r, 0):
                            break

                        for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                            if 0 <= b < N and 0 <= a < N and (a, b) not in visited: 
                                q.appendleft((a, b, d + dd))
                                visited.add((a, b))
                    (cy, cx) = (r, 0)
                    actions[0] += d
                    for c in range(deplaced[r],N):
                        if objs[r][c] > it:
                            lll = [(i, j) for j in range(1,4) for i in range(N) if (i, j) not in invLocs]
                            if not lll:
                                vvv = False
                                break
                            (i,j) = random.choice(lll)
                            q = deque()
                            q.appendleft((r,0,""))
                            visited = {(r,0)}
                            while q:
                                (y,x,d) = q.pop()
                                if (y,x) == (i,j):
                                    break

                                for (a,b,dd) in ((y+1,x,"D"),(y-1,x,"U"),(y,x+1,"R"),(y,x-1,"L")):
                                    if 0 <= b < N and 0 <= a < N and (a,b) not in visited:
                                        q.appendleft((a,b, d+dd))
                                        visited.add((a,b))
                            if (y,x) != (i,j):
                                vvv = False
                                break
                            nnn = ""
                            for elt in d[::-1]:
                                nnn += repl[elt]

                            actions[0] += "P"+d+"Q"+nnn
                            locs[objs[r][c]] = (i,j)
                            invLocs[(i,j)] = objs[r][c]
                            deplaced[r] = c

                        else:
                            # move c to target
                            q = deque()
                            q.appendleft((r, 0, ""))
                            visited = {(r, 0)}
                            while q:
                                (y, x, d) = q.pop()
                                if (y, x) == (it // N, N - 1): 
                                    break
                                for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                                    if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                                        q.appendleft((a,b, d + dd))
                                        visited.add((a, b))
                            if (y,x) != (it // N, N - 1):
                                vvv = False
                                break


                            actions[0] += "P"+d+"Q"
                            deplaced[r] = c+1

                            q = deque()
                            q.appendleft((y, x, ""))
                            visited = {(y, x)}
                            (cy, cx) = (y, x)
                            break
                    if vvv:
                        break
            else:
                nok = True
                break
    else:
        if not best or len(best[0]) > len(actions[0]):
            best = actions

    curr = process_time()
    delta = max(delta, curr - end_time)
    end_time = curr


locs = {}
invLocs = {}
deplaced = {}
actions = ["PRRRQLLLPRRQLLPRQ" for i in range(N)]
(cy,cx) = (0,1)

for i in range(N):
    if i > 0:
        actions[i] += "B"
    deplaced[i] = 3
    for j in range(N-1):
        locs[objs[i][j]] = (i,3-j)
        invLocs[(i,3-j)] = objs[i][j]

for it in range(25):
    if it in locs:
        (i, j) = locs[it]

        for r in range(1):
            q = deque()
            q.appendleft((cy,cx, ""))
            visited = {(cy,cx)}
            while q:
                (y, x, d) = q.pop()

                if (y, x) == (i, j):
                    found = d+"P"
                    break
                for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                    if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                        q.appendleft((a,b, d + dd))
                        visited.add((a, b))
            if (y, x) == (i, j):
                q = deque()
                q.appendleft((y, x, ""))
                visited = {(y, x)}
                while q:
                    (y, x, d) = q.pop()
                    if (y, x) == (it//N,N-1):
                        found += d+"Q"
                        break
                    for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                        if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                            q.appendleft((a,b, d + dd))
                            visited.add((a, b))
                if (y, x) == (it//N,N-1):
                    cy, cx = y,x
                    actions[0] += found

                    del locs[it]
                    del invLocs[(i, j)]
                    break
        else:
            nok = True
            break
    else:
        for r in range(N):
            if any(objs[r][c] == it for c in range(N)):
                vvv = True

                q = deque()
                q.appendleft((cy,cx,""))
                visited = {(cy,cx)}

                while q:
                    (y, x, d) = q.pop()
                    if (y, x) == (r, 0):
                        break

                    for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                        if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                            q.appendleft((a, b, d + dd))
                            visited.add((a, b))
                (cy, cx) = (r, 0)
                actions[0] += d
                for c in range(deplaced[r],N):
                    if objs[r][c] > it:
                        lll = [(i, j) for j in range(1,4) for i in range(N) if (i, j) not in invLocs]
                        if not lll:
                            vvv = False
                            break
                        (i,j) = random.choice(lll)
                        q = deque()
                        q.appendleft((r,0,""))
                        visited = {(r,0)}
                        while q:
                            (y,x,d) = q.pop()
                            if (y,x) == (i,j):
                                break

                            for (a,b,dd) in ((y+1,x,"D"),(y-1,x,"U"),(y,x+1,"R"),(y,x-1,"L")):
                                if 0 <= b < N and 0 <= a < N and (a,b) not in visited:
                                    q.appendleft((a,b, d+dd))
                                    visited.add((a,b))
                        if (y,x) != (i,j):
                            vvv = False
                            break
                        nnn = ""
                        for elt in d[::-1]:
                            nnn += repl[elt]

                        actions[0] += "P"+d+"Q"+nnn
                        locs[objs[r][c]] = (i,j)
                        invLocs[(i,j)] = objs[r][c]
                        deplaced[r] = c

                    else:
                        # move c to target
                        q = deque()
                        q.appendleft((r, 0, ""))
                        visited = {(r, 0)}
                        while q:
                            (y, x, d) = q.pop()
                            if (y, x) == (it // N, N - 1): 
                                break
                            for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                                if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                                    q.appendleft((a,b, d + dd))
                                    visited.add((a, b))
                        if (y,x) != (it // N, N - 1):
                            vvv = False
                            break

                        actions[0] += "P"+d+"Q"
                        deplaced[r] = c+1

                        q = deque()
                        q.appendleft((y, x, ""))
                        visited = {(y, x)}
                        (cy, cx) = (y, x)
                        
                        break
                if vvv:
                    break
        else:
            nok = True
            break

else:
    if not best or len(best[0]) > len(actions[0]):
        best = actions

curr = process_time()
delta = max(delta, curr - end_time)
end_time = curr

possibilities = ["PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQ", "PRRRQLLLPRRQ", "PRRQLLPRQ", "PRQ", "PRRQ", "PRRRQ"]
possibilitiesNbs = ["321","31","32","21","1","2","3"]

possibilities0 = {}
possibilitiesNbs0 = {}

possibilities0[17] = ["PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[17] = ["321","312","132","123","213","231"]

possibilities0[12] = ["PRRRQLLLPRRQ", "PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[12] = ["32","321","312","132","123","213","231"]

possibilities0[11] = ["PRRRQLLLPRQ", "PRRRQLLLPRRQ", "PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[11] = ["31","32","321","312","132","123","213","231"]

possibilities0[9] = ["PRRQLLPRQ", "PRRRQLLLPRQ", "PRRRQLLLPRRQ", "PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[9] = ["21","31","32","321","312","132","123","213","231"]

possibilities0[5] = ["PRRRQ", "PRRQLLPRQ", "PRRRQLLLPRQ", "PRRRQLLLPRRQ", "PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[5] = ["3","21","31","32","321","312","132","123","213","231"]

possibilities0[4] = ["PRRQ", "PRRRQ", "PRRQLLPRQ", "PRRRQLLLPRQ", "PRRRQLLLPRRQ", "PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[4] = ["2","3","21","31","32","321","312","132","123","213","231"]

possibilities0[3] = ["PRQ", "PRRQ", "PRRRQ", "PRRQLLPRQ", "PRRRQLLLPRQ", "PRRRQLLLPRRQ", "PRRRQLLLPRRQLLPRQ", "PRRRQLLLPRQLPRRQ", "PRQLPRRRQLLLPRRQ", "PRQLPRRQLLPRRRQ", "PRRQLLPRQLPRRRQ", "PRRQLLPRRRQLLLPRQ"]
possibilitiesNbs0[3] = ["1","2","3","21","31","32","321","312","132","123","213","231"]

while end_time - start_time + delta < 2.9:

    M = 3
    locs = {}
    invLocs = {}
    deplaced = {}
    actions = [""]

    for i in range(1, N):

        choice = random.randint(0,6)
        actions.append(possibilities[choice]+"B")
        M = max(M, len(possibilities[choice]))
        L = len(possibilitiesNbs[choice])
        deplaced[i] = L

        for j in range(L): #CHG
            locs[objs[i][j]] = (i, int(possibilitiesNbs[choice][j])) 
            invLocs[(i, int(possibilitiesNbs[choice][j]))] = objs[i][j] 

    choice = random.randint(0, len(possibilities0[M])-1)
    actions[0] += possibilities0[M][choice]
    L = len(possibilitiesNbs0[M][choice])
    deplaced[0] = L

    for j in range(L):  # CHG
        locs[objs[0][j]] = (0, int(possibilitiesNbs0[M][choice][j]))  # CHG
        invLocs[(0, int(possibilitiesNbs0[M][choice][j]))] = objs[0][j]  # CHG

    (cy, cx) = (0, int(possibilitiesNbs0[M][choice][-1]))

    for it in range(25):
        if it in locs:
            (i, j) = locs[it]

            for r in range(1):
                q = deque()
                q.appendleft((cy, cx, ""))
                visited = {(cy, cx)}
                while q:
                    (y, x, d) = q.pop()

                    if (y, x) == (i, j):
                        found = d + "P"
                        break
                    for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                        if 0 <= b < N and 0 <= a < N and (a, b) not in visited:
                            q.appendleft((a, b, d + dd))
                            visited.add((a, b))
                if (y, x) == (i, j):  # found:
                    q = deque()
                    q.appendleft((y, x, ""))
                    visited = {(y, x)}
                    while q:
                        (y, x, d) = q.pop()
                        if (y, x) == (it // N, N - 1):  # TESTER
                            found += d + "Q"
                            break
                        for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                            if 0 <= b < N and 0 <= a < N and (
                            a, b) not in visited:  # and (r==0 or (a, b) not in invLocs):
                                q.appendleft((a, b, d + dd))
                                visited.add((a, b))
                    if (y, x) == (it // N, N - 1):  # found[-1] == "Q":
                        cy, cx = y, x
                        actions[0] += found


                        del locs[it]
                        del invLocs[(i, j)]
                        break
            else:
                nok = True
                break
        else:
            for r in range(N):
                if any(objs[r][c] == it for c in range(N)):
                    vvv = True

                    q = deque()
                    q.appendleft((cy, cx, ""))
                    visited = {(cy, cx)}

                    while q:
                        (y, x, d) = q.pop()
                        if (y, x) == (r, 0):
                            break

                        for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                            if 0 <= b < N and 0 <= a < N and (
                            a, b) not in visited:  # and (r==0 or (a, b) not in invLocs):
                                q.appendleft((a, b, d + dd))
                                visited.add((a, b))
                    (cy, cx) = (r, 0)
                    actions[0] += d
                    for c in range(deplaced[r], N):
                        if objs[r][c] > it:
                            lll = [(i, j) for j in range(1, 4) for i in range(N) if (i, j) not in invLocs]
                            if not lll:
                                vvv = False
                                break
                            (i, j) = random.choice(lll)
                            q = deque()
                            q.appendleft((r, 0, ""))
                            visited = {(r, 0)}
                            while q:
                                (y, x, d) = q.pop()
                                if (y, x) == (i, j):
                                    break

                                for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                                    if 0 <= b < N and 0 <= a < N and (
                                    a, b) not in visited: 
                                        q.appendleft((a, b, d + dd))
                                        visited.add((a, b))
                            if (y, x) != (i, j):
                                vvv = False
                                break
                            nnn = ""
                            for elt in d[::-1]:
                                nnn += repl[elt]

                            actions[0] += "P" + d + "Q" + nnn
                            locs[objs[r][c]] = (i, j)
                            invLocs[(i, j)] = objs[r][c]
                            deplaced[r] = c

                        else:
                            # move c to target
                            q = deque()
                            q.appendleft((r, 0, ""))
                            visited = {(r, 0)}
                            while q:
                                (y, x, d) = q.pop()
                                if (y, x) == (it // N, N - 1):
                                    break
                                for (a, b, dd) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                                    if 0 <= b < N and 0 <= a < N and (
                                    a, b) not in visited:  
                                        q.appendleft((a, b, d + dd))
                                        visited.add((a, b))
                            if (y, x) != (it // N, N - 1):
                                vvv = False
                                break


                            actions[0] += "P" + d + "Q"  # +nnn
                            deplaced[r] = c + 1

                            q = deque()
                            q.appendleft((y, x, ""))
                            visited = {(y, x)}
                            (cy, cx) = (y, x)

                            break
                    if vvv:
                        break
            else:
                nok = True
                break

    else:
        if not best or len(best[0]) > len(actions[0]):
            best = actions

    curr = process_time()
    delta = max(delta, curr - end_time)
    end_time = curr


if not best:
    best = ["" for i in range(N)]

    for r in range(N):
        for c in range(N):
            for dest_r in range(N):
                if dest_r*N <= objs[r][c] < (dest_r+1)*N:
                    #print("dest_r", dest_r, file=sys.stderr)
                    best[r] += "P"+4*"R"
                    d = abs(dest_r - r)
                    if dest_r < r:
                        best[r] += d * "U" + "Q" + d*"D"
                    elif dest_r > r:
                        best[r] += d * "D" + "Q" + d*"U"
                    else:
                        best[r] += "Q"
                    best[r] += 4*"L"
                    for r1 in range(N):
                        if r1 != r:
                            best[r1] += (len(best[r]) - len(best[r1])) * "."
                    break

for i in range(N):
    print(best[i])

