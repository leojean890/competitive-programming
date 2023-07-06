
m = 0

for i in range(789):
    placement = input()
    l, r = 0, 127
    current = 0
    while placement[current] in "FB":
        mid = (r + l)
        if placement[current] == "F":
            r = mid//2 if mid%2 else mid//2 - 1
            row = r
        else:
            l = mid//2 + 1 if mid%2 else mid//2
            row = l
        current += 1

    l, r = 0, 8
    while current < len(placement):
        mid = (r + l)
        if placement[current] == "L":
            r = mid//2 if mid%2 else mid//2 - 1
            col = r
        else:
            l = mid//2 + 1 if mid%2 else mid//2
            col = l
        current += 1

    ind = row * 8 + col
    if ind > m:
        m = ind
print(m) # 864
