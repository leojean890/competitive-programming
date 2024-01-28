counter = 0
while 1:
    try:
        a, b = input().split(",")
        c, d = [int(i) for i in a.split("-")]
        e, f = [int(i) for i in b.split("-")]
        if (c <= e and d >= f) or (c >= e and d <= f):
            counter += 1

    except Exception:
        break

print(counter)

