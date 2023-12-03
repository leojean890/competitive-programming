
nbsPerCoords = {}
symbols = set()
N = 140
currentNumber = ""
currentNumberCoords = tuple()
for i in range(N):
    line = input()

    for j in range(N):
        if line[j].isdigit():
            currentNumberCoords += ((i,j),)
            currentNumber += line[j]
        else:
            if currentNumberCoords:
                nbsPerCoords[currentNumberCoords] = int(currentNumber)
                currentNumber = ""
                currentNumberCoords = tuple()
            if line[j] != ".":
                symbols.add((i,j))

    if currentNumberCoords:
        nbsPerCoords[currentNumberCoords] = int(currentNumber)
        currentNumber = ""
        currentNumberCoords = tuple()

total = 0

for allCoords, nb in nbsPerCoords.items():
    if any([abs(i-y) < 2 and abs(j-x) < 2 for (i,j) in symbols for (y,x) in allCoords]):
        total += nb

print(total) # 520135

