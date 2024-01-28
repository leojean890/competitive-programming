cycles = (20, 60, 100, 140, 180, 220)
r = 1
nC = 0
lines = [[]]
while 1:
    try:
        action = input()
        lines[-1].append("#" if nC in range(r-1,r+2) else ".")
        nC += 1
        if nC == 40:
            nC = 0
            lines.append([])
        if action != "noop":
            lines[-1].append("#" if nC in range(r - 1, r + 2) else ".")
            nC += 1
            if nC == 40:
                nC = 0
                lines.append([])
            r += int(action[5:])

    except Exception:
        for line in lines:
            print("".join(line))
        break

