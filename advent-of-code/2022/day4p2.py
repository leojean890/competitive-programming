
counter = 0
while 1:
    try:
        a, b = input().split(",")
        c, d = [int(i) for i in a.split("-")]
        e, f = [int(i) for i in b.split("-")]
        if e <= c <= f or e <= d <= f or c <= e <= d or c <= f <= d:
            counter += 1

    except Exception:
        break

print(counter)
