allPos = set()
#bczrceab BCZRCEAB
for i in range(1004):
    x, y = [int(i) for i in input().split(",")]
    allPos.add((x,y))

input()
for i in range(12):
    split = input().split(" ")[-1]
    coord = int(split.split("=")[1])
    coordType = split.split("=")[0]
    print(coord, coordType)
    nallPos = set()

    if coordType == "x":
        for x,y in allPos:
            if x > coord:
                nallPos.add((2*coord-x,y))
            else:
                nallPos.add((x, y))
    else:
        for x,y in allPos:
            if y > coord:
                nallPos.add((x, 2*coord-y))
            else:
                nallPos.add((x, y))
    allPos = nallPos

print(len(nallPos)) #847


lines = []
for i in range(200):
    line = []
    for j in range(200):
        if (j,i) in nallPos:
            line.append("x")
        else:
            line.append(".")
    lines.append(line)
    print(line)
