counter = 0
for nb in range(245318,765747+1):
    s = [int(i) for i in str(nb)]
    v = False
    c = 1
    for i in range(5):
        if s[i+1] < s[i]:
            v = False
            break
        if s[i + 1] == s[i]:
            c += 1
        else:
            if c == 2:
                v = True
            c = 1
    else:
        if c == 2:
            v = True

    if v:
        counter += 1
print(counter) # 699
