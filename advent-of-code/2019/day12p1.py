
astrs = []

astrs.append({"p":[-5,6,-11],"v":[0,0,0]})
astrs.append({"p":[-8,-4,-2],"v":[0,0,0]})
astrs.append({"p":[1,16,4],"v":[0,0,0]})
astrs.append({"p":[11,11,-4],"v":[0,0,0]})

for iter in range(1000):

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

total = 0
for astr in range(4):
    pt = 0
    for coord in range(3):
        pt += abs(astrs[astr]["v"][coord])

    ct = 0
    for coord in range(3):
        ct += abs(astrs[astr]["p"][coord])

    total += pt*ct
print(total)#13399
