scoresPerResult = {"X":1, "Y":2, "Z":3}#13 12 2 vict
score = 0

while 1:
    try:
        a, b = [i for i in input().split()]
        c = "Z"
        if a=="B" and b=="X" or a=="C" and b=="Z" or a=="A" and b=="Y":
            c = "X"
        elif a=="C" and b=="X" or a=="A" and b=="Z" or a=="B" and b=="Y":
            c = "Y"

        score += scoresPerResult[c]
        if b=="Z":
            score += 6
        elif b=="Y":
            score += 3
    except Exception:
        break

print(score)

