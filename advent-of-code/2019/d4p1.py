
counter = 0
for nb in range(245318,765747+1):
    s = [int(i) for i in str(nb)]
    v = False
    for i in range(5):
        if s[i+1] < s[i]:
            v = False
            break
        if s[i + 1] == s[i]:
            v = True
    if v:
        counter += 1
print(counter) # 1079
