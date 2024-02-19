allRes = {}
allResS = {}
allResL = {}
lll = []
N = 134
N2 = 633
for i in range(N2):
    if i < N:
        index, resultat = input().split(":")
        if "|" in resultat:
            resultat = resultat.split("|")
            allRes[index] = (tuple(resultat[0].split()), tuple(resultat[1].split(),))
        elif "\"" in resultat:
            allResS[index] = [resultat.replace(" ","").replace("\"","")]
        else:
            allResL[index] = resultat.split()
    else:
        s = input()
        if s:
            lll.append(s)


def dfs(s, depth):
    res = []
    if depth == len(v):
        return [s]

    if type(v[depth]) == list:
        for u in v[depth]:
            for l in allResS[u]:
                for ss in dfs(s + l, depth + 1):
                    res.append(ss)
    else:
        for l in allResS[v[depth]]:
            for ss in dfs(s + l, depth + 1):
                res.append(ss)

    return res


while allRes or allResL:
    for k, v in allResL.copy().items():
        if all(u in allResS for u in v):
            allResS[k] = dfs("",0)
            del allResL[k]

    for k, l in allRes.copy().items():
        if all(u in allResS for v in l for u in v):
            ll = []
            for v in l:
                for elt in dfs("",0):
                    ll.append(elt)
            allResS[k] = ll
            del allRes[k]


print(sum(1 for elt in lll if elt in allResS["0"])) # 224
