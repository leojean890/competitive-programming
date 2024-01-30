
import sys
from collections import defaultdict

astrs = []

astrs.append({"p":[-5,6,-11],"v":[0,0,0]})
astrs.append({"p":[-8,-4,-2],"v":[0,0,0]})
astrs.append({"p":[1,16,4],"v":[0,0,0]})
astrs.append({"p":[11,11,-4],"v":[0,0,0]})

coordPerTurn = [defaultdict(int),defaultdict(int),defaultdict(int)]
coordPrinted = defaultdict(bool)
cycleLengths = []
for iter in range(sys.maxsize):
    for coord in range(3):
        if not coordPrinted[coord]:
            state = (astrs[0]["p"][coord], astrs[1]["p"][coord], astrs[2]["p"][coord], astrs[3]["p"][coord], astrs[0]["v"][coord], astrs[1]["v"][coord], astrs[2]["v"][coord], astrs[3]["v"][coord])
            if state in coordPerTurn[coord]:
                coordPrinted[coord] = True
                cycleLengths.append(iter)
            coordPerTurn[coord][state] = iter
    if len(cycleLengths) == 3:
        break

    nastrs = []
    for astr in range(4):
        np = astrs[astr]["p"]
        for concurrent in range(4):
            cp = astrs[concurrent]["p"]
            for coord in range(3):
                if cp[coord] > np[coord]:
                    astrs[astr]["v"][coord] += 1
                if cp[coord] < np[coord]:
                    astrs[astr]["v"][coord] -= 1

    for astr in range(4):
        for coord in range(3):
            astrs[astr]["p"][coord] += astrs[astr]["v"][coord]


def ppcm(a,b):
    p=a*b
    while(a!=b):
        if (a<b): b-=a
        else: a-=b
    return p/a

res = 1
for l in cycleLengths:
    res = ppcm(res, l)
print(res) # 312992287193064
