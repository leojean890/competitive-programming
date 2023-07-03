allPos = set()

for i in range(1004):
    x, y = [int(i) for i in input().split(",")]
    allPos.add((x,y))

input()
split = int(input().split("=")[1])
print(split)
nallPos = set()

for x,y in allPos:
    if x > split:
        nallPos.add((2*split-x,y))
    else:
        nallPos.add((x, y))

print(len(nallPos)) #847
