def getSums(sumCols, sumRws):
    L = len(allLines)
    for j in range(L - 1):
        if all(allLines[j - k] == allLines[j + k + 1] for k in range(min(j + 1, L - j - 1))):
            sumRws += j + 1

    transposed = list(zip(*allLines))
    L = len(transposed)
    for j in range(L - 1):
        if all(transposed[j - k] == transposed[j + k + 1] for k in range(min(j + 1, L - j - 1))):
            sumCols += j + 1

    return sumCols, sumRws


allLines = []
sumCols = 0
sumRws = 0

for i in range(1343):
    line = input()
    if line:
        allLines.append(line)
    else:
        sumCols, sumRws = getSums(sumCols, sumRws)
        allLines = []

if allLines:
    sumCols, sumRws = getSums(sumCols, sumRws)

print(sumCols+100*sumRws) # 30575
