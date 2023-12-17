
def dfs(depth, chainesRestantes, tailleChaineCourante):
    global d
    if depth == l:
        if len(chainesRestantes) == 1 and tailleChaineCourante == chainesRestantes[0]:
            return 1
        return 1 if tailleChaineCourante == len(chainesRestantes) == 0 else 0

    if (depth, chainesRestantes, tailleChaineCourante) in d:
        return d[(depth, chainesRestantes, tailleChaineCourante)]

    M = 0
    if line[depth] == "#":
         M = dfs(depth + 1, chainesRestantes, tailleChaineCourante+1) if chainesRestantes and tailleChaineCourante <= chainesRestantes[0] else 0
    elif line[depth] == ".":
        if chainesRestantes and tailleChaineCourante == chainesRestantes[0]:
            M = dfs(depth + 1, chainesRestantes[1:], 0)
        if tailleChaineCourante == 0:
            M = dfs(depth + 1, chainesRestantes, 0)
    else: #if line[depth] == "?":
        if chainesRestantes and tailleChaineCourante <= chainesRestantes[0]:
            M += dfs(depth + 1, chainesRestantes, tailleChaineCourante + 1)
        if chainesRestantes and tailleChaineCourante == chainesRestantes[0]:
            M += dfs(depth + 1, chainesRestantes[1:], 0)
        if tailleChaineCourante == 0:
            M += dfs(depth + 1, chainesRestantes, 0)
    d[(depth, chainesRestantes, tailleChaineCourante)] = M
    return M


N = 1000
s = 0
for ind in range(N):
    print(ind)
    d = {}
    line, nbs = input().split()
    nbs = ",".join([nbs,nbs,nbs,nbs,nbs])
    line = "?".join([line,line,line,line,line])
    nbs = tuple([int(i) for i in nbs.split(",")])
    l = len(line)
    v = dfs(0, nbs, 0)
    s += v

print(s) # 4546215031609

