
def dfs(depth, choices):
    if depth == L:
        nLine = line

        for i in range(L):
            choice = choices[i]
            toChange = possibilities[i]
            nLine = nLine[:toChange] + choice + nLine[toChange+1:]

        counter = 0
        index = 0
        current = nbs[index]
        for i in range(l):
            if nLine[i] == "#":
                counter += 1
            elif counter > 0:
                if counter != current:
                    return 0
                counter = 0
                index += 1
                current = 0 if index == len(nbs) else nbs[index]

        if counter > 0:
            if counter != current:
                return 0
            index += 1

        return 1 if index == len(nbs) else 0

    return dfs(depth+1, choices+["."]) + dfs(depth+1, choices+["#"])


N = 1000
s = 0
for ind in range(N):
    line, nbs = input().split()
    nbs = [int(i) for i in nbs.split(",")]
    l = len(line)
    possibilities = []

    for i in range(len(line)):
        if line[i] == "?":
            possibilities.append(i)
    L = len(possibilities)
    v = dfs(0, [])
    s += v

print(s) # 6981
