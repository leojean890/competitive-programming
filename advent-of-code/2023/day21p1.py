N = 131
lines = []

for i in range(N):
    lines.append(input())
    if "S" in lines[-1]:
        entrance = (i, lines[-1].index("S"))
        lines[-1] = lines[-1].replace("S",".")

currentSpots = {entrance}
for maxDepth in range(64):
    newCurrentSpots = set()
    for (y,x) in currentSpots:
        for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if lines[a][b] == "." and (a,b) not in newCurrentSpots:
                newCurrentSpots.add((a,b))
        currentSpots = newCurrentSpots
print(len(currentSpots)) # 3748
