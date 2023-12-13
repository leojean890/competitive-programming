
def getSums(sumCols, sumRws):
    L = len(allLines)
    transposed = [list(a) for a in zip(*allLines)]
    LL = len(transposed)

    blacklisted = -1
    found = set()

    for j in range(L - 1):
        if all(allLines[j - k] == allLines[j + k + 1] for k in range(min(j + 1, L - j - 1))):
            blacklisted = j

    for y in range(L):
        for x in range(LL):
            allLines[y][x] = "." if allLines[y][x] == "#" else "#"

            for j in range(L - 1):
                if j != blacklisted and all(allLines[j - k] == allLines[j + k + 1] for k in range(min(j + 1, L - j - 1))):
                    found.add(j + 1)

            allLines[y][x] = "." if allLines[y][x] == "#" else "#"

    for elt in found:
        sumRws += elt

    found = set()
    blacklisted = -1

    for j in range(LL - 1):
        if all(transposed[j - k] == transposed[j + k + 1] for k in range(min(j + 1, LL - j - 1))):
            blacklisted = j

    for y in range(LL):
        for x in range(L):
            transposed[y][x] = "." if transposed[y][x] == "#" else "#"

            for j in range(LL - 1):
                if j != blacklisted and all(transposed[j - k] == transposed[j + k + 1] for k in range(min(j + 1, LL - j - 1))):
                    found.add(j + 1)

            transposed[y][x] = "." if transposed[y][x] == "#" else "#"

    for elt in found:
        sumCols += elt

    return sumCols, sumRws


allLines = []
sumCols = 0
sumRws = 0

for i in range(1343):
    line = input()
    if line:
        allLines.append(list(line))
    else:
        sumCols, sumRws = getSums(sumCols, sumRws)
        allLines = []

if allLines:
    sumCols, sumRws = getSums(sumCols, sumRws)

print(sumCols+100*sumRws) # 37478

