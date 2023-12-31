import sys
from collections import defaultdict

lines = []
i = 0
elves = set()
while 1:
    try:
        a = input()
        lines.append(a)
        for j in range(len(a)):
            if a[j] == "#":
                elves.add((i,j))
        i += 1
    except Exception:
        break

orders = [(0,1,2,3),(1,2,3,0),(2,3,0,1),(3,0,1,2)]
for turn in range(1000):#10
    actions = {}
    counters = defaultdict(int)
    for (i,j) in elves:
        possibilities = [((i - 1, j), (i - 1, j + 1), (i - 1, j - 1)), ((i + 1, j), (i + 1, j + 1), (i + 1, j - 1)),
                         ((i, j - 1), (i + 1, j - 1), (i - 1, j - 1)), ((i, j + 1), (i + 1, j + 1), (i - 1, j + 1))]
        if any(pos in elves for pos in [(i+1,j),(i+1,j+1),(i+1,j-1),(i,j+1),(i,j-1),(i-1,j),(i-1,j+1),(i-1,j-1)]):
            for order in orders[turn%4]:
                currentToCheck = possibilities[order]
                if all([pos not in elves for pos in currentToCheck]):
                    actions[(i,j)] = currentToCheck[0]
                    counters[currentToCheck[0]] += 1
                    break

    newElves = set()

    for elve in elves:
        if elve in actions:
            #for elve, action in actions.items():
            action = actions[elve]
            if counters[action] == 1:
                newElves.add(action)
            else:
                newElves.add(elve)
        else:
            newElves.add(elve)
    if elves == newElves:
        print(turn+1)
        exit()

    elves = newElves


mX = sys.maxsize
mY = sys.maxsize
MX = -sys.maxsize
MY = -sys.maxsize

for (y,x) in elves:
    if y < mY:
        mY = y
    if x < mX:
        mX = x
    if y > MY:
        MY = y
    if x > MX:
        MX = x

counter = 0
for i in range(mY, MY+1):
    for j in range(mX, MX+1):
        if (i,j) not in elves:
            counter += 1

print(counter) 
print(MX, MY, mX, mY)

print((MY-mY+1) * (MX-mX+1) - len(elves))
