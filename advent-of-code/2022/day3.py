score = 0

while 1:
    try:
        a = input()
        b = a[:len(a)//2]
        c = a[len(a)//2:]
        d = set()
        for elt in b:
            d.add(elt)
        for elt in c:
            if elt in d:
                if elt.islower():
                    score += ord(elt) - 96
                else:
                    score += ord(elt) - 38
                break

    except Exception:
        break

print(score)
