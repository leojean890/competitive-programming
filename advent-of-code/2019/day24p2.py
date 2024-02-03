from copy import deepcopy

lines = list()
for i in range(5):
    lines += [list(input())]

emptyLines = list()
for i in range(5):
    emptyLines += [['.', '.', '.', '.', '.']]

def dfs(depth, current, prev):
    if depth == 201:
        return 0,[]

    nlines = []
    counter = 0
    nxt = current[2][2]

    for i in range(5):
        line = []
        for j in range(5):
            if i != 2 or j != 2:
                neighs = 0
                if j > 0 and (i,j-1) != (2,2) and current[i][j - 1] == "#":
                    neighs += 1
                if i > 0 and (i-1,j) != (2,2) and current[i - 1][j] == "#":
                    neighs += 1
                if j < 4 and (i,j+1) != (2,2) and current[i][j + 1] == "#":
                    neighs += 1
                if i < 4 and (i+1,j) != (2,2) and current[i + 1][j] == "#":
                    neighs += 1

                if nxt:
                    if (i,j-1) == (2,2):
                        for k in range(5):
                            if nxt[k][4] == "#":
                                neighs += 1
                    if (i-1,j) == (2,2):
                        for k in range(5):
                            if nxt[4][k] == "#":
                                neighs += 1
                    if (i,j+1) == (2,2):
                        for k in range(5):
                            if nxt[k][0] == "#":
                                neighs += 1
                    if (i+1,j) == (2,2):
                        for k in range(5):
                            if nxt[0][k] == "#":
                                neighs += 1

                if prev:

                    if i == 0 and prev[1][2] == "#":
                        neighs += 1
                    if j == 0 and prev[2][1] == "#":
                        neighs += 1
                    if j == 4 and prev[2][3] == "#":
                        neighs += 1
                    if i == 4 and prev[3][2] == "#":
                        neighs += 1

                if current[i][j] == "#":
                    if neighs == 1:
                        counter += 1
                    line.append("#" if neighs == 1 else ".")
                else:
                    line.append("#" if neighs in (1, 2) else ".")
                    if neighs in (1, 2):
                        counter += 1
            else:
                c, nl = dfs(depth + 1, nxt, current)
                line.append(nl)
                counter += c

        nlines.append(line)
    return counter, nlines


current = emptyLines

for iteration in range(201):

    lines1 = list()
    for i in range(5):
        toFill = lines if iteration == 100 else emptyLines
        lines1.append(toFill[i] if i != 2 else toFill[i][:2] + [deepcopy(current)] + toFill[i][3:])

    current = lines1

wholeCurrent = current

for iteration in range(200):
    counter, wholeCurrent = dfs(0, wholeCurrent, None)
print(iteration, counter) # 1980

