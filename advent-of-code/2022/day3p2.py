score = 0
l = []
while 1:
    try:
        l.append(input())
        if len(l) == 3:
            for elt in l[0]:
                if elt in l[1] and elt in l[2]:
                    if elt.islower():
                        score += ord(elt) - 96
                    else:
                        score += ord(elt) - 38
                    break
            l = []
    except Exception:
        break

print(score)
