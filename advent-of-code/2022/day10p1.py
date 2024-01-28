cycles = (20, 60, 100, 140, 180, 220)
r = 1
nC = 0
totalStrength = 0
while 1:
    try:
        action = input()
        nC += 1
        if nC in cycles:
            totalStrength += nC*r
        if action != "noop":
            nC += 1
            if nC in cycles:
                totalStrength += nC * r
            r += int(action[5:])

    except Exception:
        print(totalStrength)
        break

